import pandas as pd
import requests

def get_ea_nhl_ratings(url):
    """
    Scrapes the EA Sports NHL player ratings page and returns a DataFrame.

    Args:
        url: The URL of the EA Sports NHL ratings page.

    Returns:
        A pandas DataFrame containing player ratings, or None if an error occurs.
    """
    try:
        # Use a user-agent to avoid potential issues with default requests header
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Check for bad response

        # pandas.read_html reads tables from the HTML and returns a list of DataFrames
        # The EA site has one main table with the ratings
        dfs = pd.read_html(response.text)

        if dfs:
            # The first table in the list should be the player ratings
            ratings_df = dfs[0]
            return ratings_df
        else:
            print("No tables found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# The current EA Sports NHL 26 ratings URL (adjust for future game versions)
ratings_url = "https://www.ea.com/games/nhl/ratings"


# Fetch the data
player_ratings = get_ea_nhl_ratings(ratings_url)

if player_ratings is not None:
    # Print the first few rows of the DataFrame
    print(player_ratings.head())
    # You can save the data to a CSV file if needed
    # player_ratings.to_csv('nhl_player_ratings.csv', index=False)