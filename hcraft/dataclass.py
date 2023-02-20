import dataclasses
from hcraft.common import recursive_handle


def advanced_asdict(instance, ignore_default: bool = True, ignore_none: bool = True):
    d = {}
    for name, field in instance.__dataclass_fields__.items():
        value = recursive_handle(
            getattr(instance, name),
            dataclasses.is_dataclass,
            advanced_asdict,
            ignore_default=ignore_default,
            ignore_none=ignore_none,
        )
        if dataclasses.is_dataclass(value):
            d[name] = advanced_asdict(value, ignore_default, ignore_none)
            continue
        ignore = False
        if ignore_default:
            ignore = field.default is not dataclasses.MISSING and field.default == value
        if ignore_none:
            ignore = ignore or value is None
        if not ignore:
            d[name] = value
    return d
