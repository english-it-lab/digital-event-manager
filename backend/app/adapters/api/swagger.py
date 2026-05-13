# чтобы в сваггере была возможность JWT токен в заголовки проставить
from fastapi.openapi.utils import get_openapi


def configure_openapi(app):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    pass
