import os
from scraping.reddit_scraper import scrape_user, save_user_data
from processing.persona_generator import persona_from_reddit

def process_user(username):
    # Step 1: Scrape and save Reddit data
    print(f"Scraping data for: {username}")
    data = scrape_user(username)
    save_user_data(username, data)

    # Step 2: Generate persona
    input_path = f"data/{username}_raw.json"
    output_path = f"output/{username}_persona.txt"
    print(f"Generating persona for: {username}")
    persona_from_reddit(input_path, output_path)
    print(f"Done. Persona saved to: {output_path}\n")

if __name__ == "__main__":
    usernames = ["replace_with_username1", "replace_with_username2"]  # Add more usernames as needed
    for user in usernames:
        process_user(user)
