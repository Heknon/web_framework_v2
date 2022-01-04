import inspect

import jsonpickle

import web_framework_v2.annotations
from web_framework_v2.http import HttpRequest, ContentType, HttpResponse


class Method:
    encodable_content_types = [ContentType.json, ContentType.text]

    def __init__(self, method):
        """
        Wraps a web_framework_v2 function that has a route into a class that handles
        the execution of the function.
        :param method: the function
        """
        self._method = method

    def execute(self, request, response):
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

            for decorator in decorators:
                should_exec, result, data = decorator.should_execute_endpoint(request, web_framework_v2.annotations.RequestBody().value_generator(request))
                if not should_exec:
                    return decorator.on_fail(request, response, data)

                if result is not None:
                    decorator_result_map[type(decorator)] = result  # Used when building kwargs to set result based on annotation

        # Build kwargs
        if args_len > 0 and len(argspec.annotations) > 0:
            for parameter_name, annotation in argspec.annotations.items():
                if issubclass(type(annotation), web_framework_v2.annotations.Annotation):
                    kwargs[parameter_name] = annotation.value_generator(request)
                    if kwargs[parameter_name] is None and parameter_name in defaults_map:
                        kwargs[parameter_name] = defaults_map[parameter_name]
                else:
                    if annotation is HttpRequest or type(annotation) is HttpRequest:
                        kwargs[parameter_name] = request
                        defaults_map.pop(parameter_name, None)
                    elif annotation is HttpResponse or type(annotation) is HttpResponse:
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

        method_result = self._method(**kwargs)
        return jsonpickle.encode(method_result, unpicklable=False) if response.content_type in self.encodable_content_types else method_result
