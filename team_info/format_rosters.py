



# this code creates rosters with players 


from nhlpy import NHLClient
import pandas as pd


# testing
"""
# Basic usage
client = NHLClient()

# Get all teams
teams = client.teams.teams()

# Get current standings
standings = client.standings.league_standings()

# Get today's games
games = client.schedule.daily_schedule()

# Get current season roster
roster = client.teams.team_roster(team_abbr="SJS", season="20252026")

print(roster["goalies"][0]["firstName"])
"""

client = NHLClient()
teams = client.teams.teams()


### get players basic info in a df
def clean_name(ntype, name):
    """
    Clean the name of the player or team
    """
    return name[ntype]['default']

df_player_names = pd.DataFrame()

for team in teams:
    players = client.teams.team_roster(team_abbr=team['abbr'], season="20242025")
    for p in players['forwards'] + players['defensemen'] + players['goalies']:
        p['team'] = team['abbr']
        p['firstName'] = clean_name('firstName', p)
        p['lastName'] = clean_name('lastName', p)
    forwards, defense, goalies = players['forwards'], players['defensemen'], players['goalies']

    df_player_names = pd.concat(
        [df_player_names, 
         pd.DataFrame(forwards), 
         pd.DataFrame(defense), 
         #pd.DataFrame(goalies)
         ], ignore_index=True)

df_player_names = df_player_names.drop(columns=["headshot", "birthCity", "birthCountry", "birthStateProvince", "heightInCentimeters", "weightInKilograms"])

df_player_names["skaterFullName"] = df_player_names["firstName"] + " " + df_player_names["lastName"]


#### get stats
from nhlpy.api.query.builder import QueryBuilder, QueryContext
from nhlpy.api.query.filters.franchise import FranchiseQuery
from nhlpy.api.query.filters.season import SeasonQuery
import time


sq = SeasonQuery(season_start="20252026", season_end="20252026")
query_builder = QueryBuilder()

test = None
df_player_stats = pd.DataFrame()

for team in teams: 
    #pause for 1 second
    #time.sleep(1). # < --- I sometimes get rate limited, this is just to slow down a bit.
    fq = FranchiseQuery(franchise_id=team['franchise_id'])
    context = query_builder.build(filters=[fq, sq])

    data = client.stats.skater_stats_with_query_context(
        report_type='summary',
        query_context=context,
        aggregate=True
    )
    data_df = pd.DataFrame(data['data'])

    df_player_stats = pd.concat([df_player_stats, data_df], ignore_index=True)

df_player_stats = df_player_stats.rename(columns={"playerId": "id"})

df_players = pd.merge(df_player_names, df_player_stats, on="id", how="left")



### ways to check that everything worked
'''
for i in range(len(df_players.columns)):
    print(df_players.columns[i])

# check that the merge was done correctly
for i in range(len(df_players)):
    if df_players["skaterFullName_x"].values[i] != df_players["skaterFullName_y"].values[i]:
        print(df_players["skaterFullName_x"].values[i], df_players["skaterFullName_y"].values[i])
# all players that fail this test either their name is spelled differentlt (e.g., Matt vs. Matthew),
# or they do not have stats this year (i.e., they have not played in a game).
'''

df_players_sj_skaters = df_players[df_players["team"] == "SJS"]


### get goalie stats
# Get basic goalie stats
goalie_stats_basic = client.stats.goalie_stats_summary(
    start_season="20252026", 
    end_season="20252026",
    limit=10000
)
df_goalie_stats_basic = pd.DataFrame(goalie_stats_basic)

# Get advanced goalie stats
goalie_stats_advanced = client.stats.goalie_stats_summary(
    start_season="20252026",
    end_season="20252026",
    stats_type="advanced",
    limit=10000
)
df_goalie_stats_advanced = pd.DataFrame(goalie_stats_advanced)


for i in range(len(df_goalie_stats_basic.columns)):
    print(df_goalie_stats_basic.columns[i])

for i in range(len(df_goalie_stats_advanced.columns)):
    print(df_goalie_stats_advanced.columns[i])

df_goalies = pd.merge(df_goalie_stats_basic, df_goalie_stats_advanced, on="playerId", how="left")



# TODO: make the above code functions for better practice (prioirty 1)
# TODO: split the data frame up into 32 dfs (1 for each team), make these into a library (maybe) (priority 1)
# TODO: grab dfs for goalies, merge them into df_players. There should be different functions for grabbing skater and goalie stats (priority 1)
# TODO: add more advanced stats for more complex model (priority 2)
# TODO: consider changing NaNs in player stats to 0's if that makes training the models fail (priority 3)


####### random notes
# summary stats are for testing model
# for training, will need to get stats for each day games are played (i.e., summary stats for each day as the season progresses)


### using the modules notes
# help(client.stats.goalie_stats_summary) gives the options for getting goalie stats
