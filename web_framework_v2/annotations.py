import inspect
import json
from abc import ABC

import jsonpickle

import web_framework_v2.http.http_request as http_request


class Annotation(ABC):
    def __init__(self, parameter_type, use_json_object_hook=False):
        """
        An annotation is what precedes the parameter name.
        method(self, parameter: annotation).
        this class is meant to be a base class for all custom annotations in the web_framework_v2.

        :param parameter_type: the type of the parameter. the data the annotation supplies will try to be converted to this type.
        """

        self._parameter_type = parameter_type
        self._use_json_object_hook = use_json_object_hook

    def value_generator(self, request: http_request.HttpRequest):
        raise NotImplementedError("Implement value_generator in non abstract class.")

    def adapt(self, data, parameter_type):
        try:
            if not self._use_json_object_hook:
                mapped_data = jsonpickle.decode(data)
                if type(mapped_data) is dict:
                    module = self._parameter_type.__module__
                    mapped_data[
                        "py/object"] = module + '.' + self._parameter_type.__qualname__ if module != "builtins" else self._parameter_type.__qualname__

                return jsonpickle.decode(json.dumps(mapped_data), classes=parameter_type)
            else:
                return json.loads(data, object_hook=lambda json_map: Annotation.json_object_hook(json_map, parameter_type))
        except Exception:
            return data

    @staticmethod
    def json_object_hook(json_map, parameter_type):
        if hasattr(parameter_type, "json_object_hook"):
            return parameter_type.json_object_hook(json_map)
        elif parameter_type is map:
            return json_map

        argspec = inspect.getfullargspec(parameter_type.__init__)
        argspec.args.pop(0)
        new_c = parameter_type(**{arg_name: json_map.get(arg_name, None) for arg_name in argspec.args})
        new_c.__dict__ = json_map
        return new_c


class QueryParameter(Annotation):
    def __init__(self, query_name: str, parameter_type=str, use_json_object_hook=False):
        self.query_name = query_name
        super().__init__(parameter_type, use_json_object_hook)

    def value_generator(self, request: http_request.HttpRequest):
        value = request.query_parameters.get(self.query_name, None) if request.query_parameters is not None else None

        if value is None:
            return None

        value = value if len(value) > 1 else value[0]

        return self.adapt(
            value,
            self._parameter_type
        )


class RequestBody(Annotation):
    def __init__(self, parameter_type=map, raw_format=False, use_json_object_hook=False):
        super().__init__(parameter_type, use_json_object_hook)
        self.raw_format = raw_format

    def value_generator(self, request):
        if self.raw_format:
            return request.body

        value = self.adapt(request.body, self._parameter_type) if request.body is not None else None
        return value if type(value) is not bytes else value.decode()


class PathVariable(Annotation):
    def __init__(self, variable_name, parameter_type=str, use_json_object_hook=False):
        super().__init__(parameter_type, use_json_object_hook)
        self.variable_name = variable_name

    def value_generator(self, request: http_request.HttpRequest):
        value = request.path_variables.get(self.variable_name, None)

        return self.adapt(value, self._parameter_type) if value is not None else None
