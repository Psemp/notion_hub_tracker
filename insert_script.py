import os

from github import Github
from dotenv import load_dotenv

from models.gh_repo import Gh_repo
from scripts.notion_db import get_database_schema, insert_repo

load_dotenv()

with open(".repo_ignore", "r") as file:
    repo_ignore = [line.strip() for line in file]

GH_ACCESS_TOKEN = os.getenv("GH_TOKEN")
NOTION_API_KEY = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")

g = Github(GH_ACCESS_TOKEN)

# github account
github_login = "psemp"

user = g.get_user(login=github_login)

repos = user.get_repos()

public_repos = []

for repo in repos:
    if not repo.private and repo.name not in repo_ignore:
        repo_object = Gh_repo(repo=repo)
        public_repos.append(repo_object)


database_schema = get_database_schema(database_id=NOTION_DB_ID, api_key=NOTION_API_KEY)

for repo in public_repos:
    insert_repo(repo=repo, database_id=NOTION_DB_ID, api_key=NOTION_API_KEY, database_schema=database_schema)
