def recursive_handle(value, predict, handler, *args, **kwargs):
    if isinstance(value, list):
        return [
            handler(v, *args, **kwargs)
            if predict(v)
            else recursive_handle(v, predict, handler)
            for v in value
        ]
    if isinstance(value, dict):
        return {
            k: handler(v, *args, **kwargs)
            if predict(v)
            else recursive_handle(v, predict, handler)
            for k, v in value.items()
        }
    return value
