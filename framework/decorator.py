from abc import ABC
from typing import Tuple


class Decorator(ABC):
    """
    Decorate a route to change it's pre-execution functionality
    """

    def should_execute_endpoint(self, request) -> Tuple[bool, object]:
        raise NotImplementedError(f"Must implement should_execute_route() in {type(self)}")

    def __call__(self, fun):
        decorators = getattr(fun, "decorators", [])
        decorators.append(self)
        setattr(fun, "decorators", decorators)

        return fun
