import inspect
import logging

import jsonpickle

import web_framework_v2.annotations
import web_framework_v2.decorator as decorator_module
import web_framework_v2.http.http_request as http_request
import web_framework_v2.http.http_response as http_response

from web_framework_v2.http import ContentType

logger = logging.getLogger(__name__)


class Method:
    encodable_content_types = [ContentType.json, ContentType.text]

    def __init__(self, method):
        """
        Wraps a web_framework_v2 function that has a route into a class that handles
        the execution of the function.
        :param method: the function
        """
        self._method = method

    def execute(self, request: http_request.HttpRequest, response: http_response.HttpResponse):
        argspec = inspect.getfullargspec(self._method)
        args_len = len(argspec.args)
        defaults_len = len(argspec.defaults) if argspec.defaults is not None else 0
        kwargs = dict()
        defaults_map = dict()
        decorator_result_map = dict()

        # Build defaults map
        if defaults_len > 0:
            for i, default_value in enumerate(argspec.defaults):
                defaults_map[argspec.args[args_len - defaults_len + i]] = default_value

        # Execute decorator functionality
        if hasattr(self._method, "decorators"):
            decorators = getattr(self._method, "decorators", [])
            logger.debug(f"Method's decorators: {decorators}")
            request_body = list(filter(lambda annot: type(annot) is web_framework_v2.annotations.RequestBody, argspec.annotations.values()))

            if len(request_body) > 0:
                request_body = request_body[0].value_generator(request)
            else:
                request_body = web_framework_v2.annotations.RequestBody().value_generator(request)

            decorator: decorator_module.Decorator
            for decorator in decorators:
                should_exec, result, data = \
                    decorator.should_execute_endpoint(request, request_body)
                if not should_exec:
                    logger.debug(f"Decorator failed. Calling on_fail. {decorator}")
                    return decorator.on_fail(request, response, data)

                if result is not None:
                    decorator_result_map[type(decorator)] = result  # Used when building kwargs to set result based on annotation
                elif decorator.fail_on_null_result:
                    logger.debug(f"Decorator returned null result and is set to fail on null result. Calling on_fail. {decorator}")
                    return decorator.on_fail(request, response, data)

        # Build kwargs
        if args_len > 0 and len(argspec.annotations) > 0:
            for parameter_name, annotation in argspec.annotations.items():
                if issubclass(type(annotation), web_framework_v2.annotations.Annotation):
                    kwargs[parameter_name] = annotation.value_generator(request)
                    if kwargs[parameter_name] is None and parameter_name in defaults_map:
                        kwargs[parameter_name] = defaults_map[parameter_name]
                else:
                    if annotation is http_request.HttpRequest or type(annotation) is http_request.HttpRequest:
                        kwargs[parameter_name] = request
                        defaults_map.pop(parameter_name, None)
                    elif annotation is http_response.HttpResponse or type(annotation) is http_response.HttpResponse:
                        kwargs[parameter_name] = response
                        defaults_map.pop(parameter_name, None)
                    elif annotation in decorator_result_map:
                        kwargs[parameter_name] = decorator_result_map[annotation]
                        defaults_map.pop(parameter_name, None)

        # Build defaults
        if defaults_len > 0:
            for parameter_name, default_value in defaults_map.items():
                if parameter_name in kwargs:
                    continue

                kwargs[parameter_name] = default_value

        logger.debug(f"Finished building method kwargs. {kwargs}")
        method_result = self._method(**kwargs)
        return Method.encode_result(method_result, response)

    @staticmethod
    def encode_result(result: object, response: http_response.HttpResponse):
        return jsonpickle.encode(result, unpicklable=False) if response.content_type in Method.encodable_content_types else result
