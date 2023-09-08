from app.endpoints.ping import api_router as application_health_router
from app.endpoints.calculate import api_router as calculate_router

list_of_routes = [
    application_health_router,
    calculate_router,
]


__all__ = [
    "list_of_routes",
]
