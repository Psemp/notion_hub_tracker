# GitHub Repositories to Notion

This program fetches public repositories from a GitHub account and inserts them into a Notion database. It excludes repositories listed in the `.repo_ignore` file. The program retrieves repository details such as name, description, license, and languages used, and inserts this information into the corresponding columns of the Notion database.

## Usage

1. Set up the environment variables for the GitHub access token, Notion API key, and Notion database ID.
2. Create a `.repo_ignore` file to list any repositories that you want to exclude from the Notion database.
3. Run the `insert_script.py` file.

The program will fetch the public repositories from the specified GitHub account, create a `Gh_repo` object for each repository (defined in `models/gh_repo.py`), and insert their details into the Notion database using functions in the `scripts/notion_db.py` module.

## Dependencies

- requirements.txt


## Future Improvements :
- Checking if repo already in DB
- Adding datetime as json in requests
- Updater (description/date/progress)
