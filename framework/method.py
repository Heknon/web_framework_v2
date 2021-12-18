import inspect
import json

import jsonpickle

import framework.annotations
from framework.http import HttpRequest, ContentType, HttpResponse


class Method:
    encodable_content_types = [ContentType.json, ContentType.text]

    def __init__(self, method):
        self._method = method

    def execute(self, request, response):
        argspec = inspect.getfullargspec(self._method)
        args_len = len(argspec.args)
        defaults_len = len(argspec.defaults) if argspec.defaults is not None else 0
        kwargs = dict()
        defaults_map = dict()

        if defaults_len > 0:
            for i, default_value in enumerate(argspec.defaults):
                defaults_map[argspec.args[args_len - defaults_len + i]] = default_value

        print(argspec.annotations)
        if args_len > 0 and len(argspec.annotations) > 0:
            for parameter_name, annotation in argspec.annotations.items():
                if issubclass(type(annotation), framework.annotations.Annotation):
                    kwargs[parameter_name] = annotation.value_generator(request)
                    if kwargs[parameter_name] is None and parameter_name in defaults_map:
                        kwargs[parameter_name] = defaults_map[parameter_name]
                else:
                    if annotation is HttpRequest or type(annotation) is HttpRequest:
                        kwargs[parameter_name] = request
                        defaults_map.pop(parameter_name)
                    elif annotation is HttpResponse or type(annotation) is HttpResponse:
                        kwargs[parameter_name] = response
                        defaults_map.pop(parameter_name)

        if defaults_len > 0:
            for parameter_name, default_value in defaults_map.items():
                if parameter_name in kwargs:
                    continue

                kwargs[parameter_name] = default_value

        print(kwargs)
        method_result = self._method(**kwargs)
        return jsonpickle.encode(method_result, unpicklable=False) if response.content_type in self.encodable_content_types else method_result
