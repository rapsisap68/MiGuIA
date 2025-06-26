import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    """Fetches content from a URL and returns a BeautifulSoup object."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def extract_game_names(soup):
    """Extracts game names from the BeautifulSoup object."""
    game_names = []
    if not soup:
        return game_names

    # Refined approach:
    # Find all <h4> or <h3> tags. If such a tag's parent is an <a> tag,
    # and that <a> tag also contains an image (<picture> or <img> directly or as descendant),
    # then consider the text of the <h4>/<h3> to be a game name.
    potential_titles = soup.find_all(['h4', 'h3']) # Look for h4 or h3 tags

    for title_tag in potential_titles:
        # Check if the title tag itself is within an <a> tag that might be a game link
        parent_a_of_title = title_tag.find_parent('a')

        if parent_a_of_title:
            # Now check if this specific <a> tag (parent_a_of_title) also contains an image.
            # This ensures the <h4>/<h3> and <img> are related under the same main link.
            if parent_a_of_title.find('img') or parent_a_of_title.find('picture'):
                game_name = title_tag.text.strip()
                if game_name:
                    # Avoid adding generic titles or section headers if any slip through
                    if len(game_name) > 2 and len(game_name) < 50: # Reasonable length for a game title
                        game_names.append(game_name)

    # Remove duplicates while preserving order
    if game_names:
        seen = set()
        game_names = [x for x in game_names if not (x in seen or seen.add(x))]

    return game_names

if __name__ == "__main__":
    target_url = "https://www.cognifit.com/es/juegos-mentales"
    print(f"Fetching and parsing {target_url}...")
    soup = fetch_page_content(target_url)

    if soup:
        print("Extracting game names with refined logic...")
        names = extract_game_names(soup)
        if names:
            print("\\nFound game names:")
            for name in names:
                print(f"- {name}")
        else:
            print("No game names found with refined logic.")
            print("This could be due to:")
            print("1. The HTML structure is different from expected (e.g., game names are not in h3/h4 tags within image-containing links).")
            print("2. The game content is loaded dynamically by JavaScript after the initial page load, and is not present in the HTML fetched by the 'requests' library.")
            print("   (The view_text_website tool might have different capabilities for handling JavaScript-rendered content).")
            print("3. The specific selectors used are still not accurately matching the page's structure for game titles.")
    else:
        print("Could not fetch or parse the page.")

    print("\\nScript finished.")
