
from datetime import datetime
from typing import Any, Optional

from ninja.schema import BaseModel
from pydantic import HttpUrl


class GitUser(BaseModel):
    id: int
    login: str
    full_name: Optional[str] = None
    email: str
    avatar_url: Optional[str] = None
    username: Optional[str] = None


class GitRepository(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    private: bool
    fork: bool
    html_url: HttpUrl
    ssh_url: str
    clone_url: HttpUrl
    website: str
    stars_count: int
    forks_count: int
    watchers_count: int
    open_issues_count: int
    default_branch: str
    created_at: datetime
    updated_at: datetime
    owner: GitUser


class CommitUser(BaseModel):
    name: str
    email: str
    username: Optional[str] = None


class Commit(BaseModel):
    id: str
    message: str
    url: Optional[HttpUrl] = None
    author: CommitUser
    commiter: Optional[CommitUser] = None
    timestamp: datetime
    added: list[str] = []
    removed: list[str] = []
    modified: list[str] = []
    verification: Optional[dict[str, Any]] = None


class PushPayload(BaseModel):
    ref: str
    before: str
    after: str
    compare_url: HttpUrl
    commits: list[Commit]
    repository: GitRepository
    pusher: GitUser
    sender: GitUser

