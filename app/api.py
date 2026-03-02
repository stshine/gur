from django.http import HttpRequest
from ninja import ModelSchema, NinjaAPI
from app.models import Package
from django.contrib.postgres.search import SearchQuery, SearchVector


class PackageOut(ModelSchema):
    class Meta:
        model = Package
        fields = ["name", "description", "git_url", "upstream_url", "license", "category"]

    @staticmethod
    def resolve_category(obj: Package) -> str:
        return obj.category.name


api = NinjaAPI()

@api.get("/search", response={200: list[PackageOut]})
def search(request: HttpRequest, q: str):
    query = SearchQuery(q, config="english", search_type="websearch")
    packages = Package.objects.annotate(
        search=SearchVector("name", "description", "keywords__name", config="english"),
    ).filter(search=query)
    return packages.all()


# def package_deps(package_name: str):
#     package = Package.objects.filter(name=package_name).first()
#     if not package:
#         return {"error": "Package not found"}
#     dependencies = package.get_dependencies()
#     return {"dependencies": dependencies}