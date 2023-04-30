from github.Repository import Repository
from github import UnknownObjectException

# bootstrap langs for [0, 1] and Generated by env for [2, 3]
lang_ignore = ["CSS", "JavaScript", "PureBasic", "PowerShell"]


class Gh_repo:
    def __init__(self, repo: Repository) -> None:
        self.repo_name = repo.name
        self.description = repo.description
        self.repo_url = repo.html_url
        self.creator = repo.owner.login
        self.last_updated = repo.updated_at
        self.creation_date = repo.created_at

        try:
            self.license_info = repo.get_license().license.name if repo.get_license() else None
        except UnknownObjectException:
            self.license_info = None

        self.languages = [language for language in repo.get_languages().keys() if language not in lang_ignore]

    def __str__(self) -> str:
        return f"{self.repo_name} ({self.repo_url}) by {self.creator}"

    def __repr__(self) -> str:
        return f"<Gh_repo name={self.repo_name}, creator={self.creator}>"
