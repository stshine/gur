import os

from celery import shared_task

from app.models import Ebuild, Package
from app.hookmodel import PushPayload
from app.services import ForgejoService


class RepoFileProcessor:
    repo_owner: str
    repo_name: str
    ref: str
    service: ForgejoService

    def __init__(self, repo_owner: str, repo_name: str, ref: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.ref = ref
        self.service = ForgejoService(
            os.environ.get("FORGEJO_APIKEY", ""),
            os.environ.get("FORGEJO_URL", "http://localhost:3000") + "/api/v1",
        )

    def is_ebuild_file(self, file_path: str) -> bool:
        file_name = file_path.split("/")[-1]
        return file_name.endswith(".ebuild") and file_name.startswith(self.repo_name)

    def create_ebuild(self, file_path: str) -> Ebuild:
        version = file_path.split("/")[-1].removeprefix(self.repo_name + "-").removesuffix(".ebuild")
        # file_url = f"{self.repo_url}/raw/{self.ref}/{file_path}"
        content = self.service.get_file_content(
            self.repo_owner, self.repo_name, file_path, self.ref
        )
        package = Package.objects.filter(name=self.repo_name).first()
        ebuild = Ebuild(
            package=package,
            version=version,
            content="".join(chunk.decode() for chunk in content),
        )
        ebuild.save()
        return ebuild

    def update_ebuild(self, file_path: str):
        # Generally we should not update ebuild files, do nothing for now.
        pass

    def delete_ebuild(self, file_path: str):
        version = file_path.split("/")[-1].replace(".ebuild", "")
        package = Package.objects.filter(name=self.repo_name).first()
        ebuild = Ebuild.objects.filter(package=package, version=version).first()
        if ebuild:
            ebuild.delete()


@shared_task(
    pydantic=True, name="process_forgejo_event", max_retries=3, default_retry_delay=60
)
def process_forgejo_event(payload_dict: dict):
    # Example processing logic for a Forgejo event
    print(f"Processing Forgejo event: {payload_dict}")
    payload = PushPayload.model_validate(payload_dict)

    processor = RepoFileProcessor(
        repo_owner=payload.repository.owner.login,
        repo_name=payload.repository.name,
        ref=payload.ref,
    )

    for commit in payload.commits:
        print(f"Commit {commit.id}: {commit.message} by {commit.author.name}")
        for file in commit.added:
            print(f"  Added: {file}")
            if processor.is_ebuild_file(file):
                processor.create_ebuild(file)

        for file in commit.modified:
            print(f"  Modified: {file}")
            if processor.is_ebuild_file(file):
                processor.update_ebuild(file)

        for file in commit.removed:
            print(f"  Removed: {file}")
            if processor.is_ebuild_file(file):
                processor.delete_ebuild(file)
