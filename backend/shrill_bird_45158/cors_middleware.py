# cors_middleware.py
from channels.middleware import BaseMiddleware

class CorsMiddleware(BaseMiddleware):
    """
    Middleware to handle CORS headers for WebSocket connections.
    """

    async def __call__(self, scope, receive, send):
        # Set CORS headers for WebSocket connections
        if scope['type'] == 'websocket':
            # Allow connections from all origins (you might want to restrict this based on your requirements)
            headers = [
                (b'access-control-allow-origin', b'*'),
                (b'access-control-allow-headers', b'content-type'),
            ]
            # Call the next middleware/application in the chain
            await super().__call__(scope, receive, send, headers=headers)
        else:
            # Call the next middleware/application in the chain without modifying headers for non-WebSocket connections
            await super().__call__(scope, receive, send)
