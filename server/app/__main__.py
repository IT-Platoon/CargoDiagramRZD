from fastapi import FastAPI

from app.config import DefaultSettings, get_settings
from app.endpoints import list_of_routes


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "My new FastAPI project"

    tags_metadata = [
        {
            "name": "cargo_diagram_rzd",
            "description": "My new FastAPI project",
        },
    ]

    application = FastAPI(
        title="app",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi.json",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()
