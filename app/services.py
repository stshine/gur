import logging
from pyforgejo import PyforgejoApi, RepoGetContentsResponse, Repository, User
from typing import Iterator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ForgejoError(Exception):
    pass


class ForgejoService:
    """
    High level service for Forgejo operations
    """

    client: PyforgejoApi
    token: str
    base_url: str


    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

        if not self.token:
            raise ForgejoError("Token must be provided")

        self.client = PyforgejoApi(
            base_url=self.base_url,
            api_key=self.token,
        )


    def create_user(self, username: str, email: str, password: str) -> User:
        """
        Create a new user
        """
        try:
            user = self.client.admin.create_user(
                username=username,
                email=email,
                password=password,
            )
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise ForgejoError(f"Error creating user: {e}")

        return user


    def create_repository(self, username: str, name: str, description: str) -> Repository:
        """
        Create a new repository
        """
        try:
            repo = self.client.admin.create_repo(
                username=username,
                name=name,
                description=description,
            )
        except Exception as e:
            logger.error(f"Error creating repository: {e}")
            raise ForgejoError(f"Error creating repository: {e}")

        return repo


    def list_repo_entries(self, owner: str, repo: str) -> RepoGetContentsResponse:
        """
        List repository entries
        """
        try:
            entries = self.client.repository.repo_get_contents(
                owner=owner,
                repo=repo,
                filepath="/",
            )
        except Exception as e:
            logger.error(f"Error listing repository contents: {e}")
            raise ForgejoError(f"Error listing repository contents: {e}")

        return entries


    def get_file_content(self, owner: str, repo: str, file_path: str) -> Iterator[bytes]:
        """
        Get file content
        """
        try:
            content = self.client.repository.repo_get_raw_file(
                owner=owner,
                repo=repo,
                filepath=file_path,
            )
        except Exception as e:
            logger.error(f"Error getting file content: {e}")
            raise ForgejoError(f"Error getting file content: {e}")

        return content