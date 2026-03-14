from flask import Flask, request
from utilities.environment import env
import functools

app = Flask(__name__)

def new_endpoint(endpoint, func):
    app.add_url_rule(endpoint, view_func=func, methods=["GET"])

def start():
    app.run(port=env('API_PORT'))

true, false = True, False # This makes boolean parameters more web-friendly
def optionalParam(name, default, type=str):
    def annotation(func):
        if not hasattr(func, 'optional_params'):
            func.optional_params = {}
        func.optional_params[name] = default

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for param_name, param_default in wrapper.optional_params.items():
                param_value = request.args.get(param_name, param_default)

                if type != str:
                    param_value = eval(param_value) if isinstance(param_value, str) else param_value
                    # This next fallback prevents attempts to inject code
                    if not isinstance(param_value, type):
                        param_value = param_default
                setattr(wrapper, param_name, param_value)

            return func(*args, **kwargs)

        wrapper.optional_params = func.optional_params
        return wrapper
    return annotation