import requests
from models.gh_repo import Gh_repo


def get_database_schema(database_id: str, api_key: str):
    notion_headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": "2022-06-28"
    }
    response = requests.get(f"https://api.notion.com/v1/databases/{database_id}", headers=notion_headers)

    if response.status_code == 200:
        return response.json()["properties"]
    else:
        print("Error:", response.json())
        return None


def get_new_id(database_id: str, api_key: str) -> int:

    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    headers = {
        "Notion-Version": "2022-06-28",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    params = {}

    response = requests.post(url, headers=headers, json=params)

    data = response.json()

    existing_ids = [int(page["properties"]["ID"]["number"]) for page in data["results"]]

    new_id = 1
    while new_id in existing_ids:
        new_id += 1

    return new_id


def get_valid_options_ms(schema_property, items):
    valid_options = {option["name"]: option for option in schema_property["multi_select"]["options"]}
    return [valid_options.get(item) for item in items if item in valid_options]


def insert_repo(repo: Gh_repo, database_id: str, api_key: str, database_schema):

    notion_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    repo_id = get_new_id(database_id=database_id, api_key=api_key)

    new_row = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": repo.repo_name
                    }
                }
            ]
        },
        "Description": {
            "rich_text": [
                {
                    "text": {
                        "content": repo.description if repo.description else ""
                    }
                }
            ]
        },
        "URL": {
            "url": repo.repo_url
        },
        "Languages": {
            "multi_select": [
                {
                    "id": option["id"]
                } for option in get_valid_options_ms(database_schema["Languages"], repo.languages)
            ]
        },
        "ID": {
            "number": repo_id
        },
        "Licence": {
            "rich_text": [
                {
                    "text": {
                        "content": repo.license_info if repo.license_info else ""
                    }
                }
            ]
        },
        "Status": {"select": {"name": "In progress"}},
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=notion_headers,
        json={"parent": {"database_id": database_id}, "properties": new_row}
    )

    if response.status_code == 200:
        print("New row added successfully.")
    else:
        print(f"Error adding new row: {response.status_code} {response.text}")
