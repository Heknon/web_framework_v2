from abc import ABC
from typing import Tuple


class Decorator(ABC):
    """
    Decorate a route to change it's pre-execution functionality
    """

    def __init__(self, fail_on_null_result=True):
        """
        :param fail_on_null_result:  fail is result (2 argument in return tuple from should_execute_endpoint) is None
        """
        self.fail_on_null_result = fail_on_null_result

    def should_execute_endpoint(self, request, request_body) -> Tuple[bool, object, object]:
        raise NotImplementedError(f"Must implement should_execute_route() in {type(self)}")

    def on_fail(self, request, response, data):
        pass

    def __call__(self, fun):
        decorators = getattr(fun, "decorators", [])
        decorators.append(self)
        setattr(fun, "decorators", decorators)

        return fun
