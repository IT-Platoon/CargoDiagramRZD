from app.endpoints.ping import api_router as application_health_router

list_of_routes = [
    application_health_router,
]


__all__ = [
    "list_of_routes",
]
