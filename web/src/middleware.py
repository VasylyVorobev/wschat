from channels.db import database_sync_to_async
from main.services import MainService


@database_sync_to_async
def get_user(user_id):
    return MainService.get_user_client(user_id)


def parse_query_string(query_string):
    from urllib.parse import parse_qs
    return parse_qs(query_string)


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        query_string = parse_query_string(scope["query_string"].decode("utf-8"))
        if user_id := query_string.get('user'):
            scope['user'] = await get_user(int(user_id[0]))
        return await self.app(scope, receive, send)
