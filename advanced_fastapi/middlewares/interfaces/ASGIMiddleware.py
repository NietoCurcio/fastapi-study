from abc import ABC, abstractmethod
from starlette.types import ASGIApp, Receive, Scope, Send

class ASGIMiddleware(ABC):
    @abstractmethod
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    @abstractmethod
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        pass
