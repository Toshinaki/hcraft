from typing import Any, Type

from typing import List, Any

from pydash import duplicates, get


def assertion(condition: Any, *args: Any, error_class: Type[Exception] = ValueError):
    if not condition:
        raise error_class(*args)


class MissingRequiredException(TypeError):
    def __init__(self, name: str, msg: str = "", *args):
        super().__init__(f"Missing required argument: {name}. {msg}", *args)


class MissingRequiredMultipleException(TypeError):
    def __init__(self, names: List[str], msg: str = "", *args):
        super().__init__(
            f"""Missing required arguments: ["{'", "'.join(names)}"]. {msg}""", *args
        )


class EmptyValueException(ValueError):
    def __init__(self, name: str, msg: str = "", *args):
        super().__init__(f"Value is empty: {name}. {msg}", *args)


class AtLeastOneException(ValueError):
    def __init__(self, names: List[str], *args):
        super().__init__(
            f"""At least one of ["{'", "'.join(names)}"] is required.""", *args
        )


class AtMostOneException(ValueError):
    def __init__(self, names: List[str], *args):
        super().__init__(
            f"""None or only one of ["{'", "'.join(names)}"] is required.""", *args
        )


class DuplicationException(ValueError):
    def __init__(self, values: List[Any], msg: str = "", *args):
        super().__init__(
            f"""All values must be unique. Duplicated values: {values}. {msg}""", *args
        )


def check_required(arg: Any, name: str, msg: str = ""):
    assertion(arg is not None, name, msg, error_class=MissingRequiredException)


def check_required_multiple(args: List[Any], names: List[str], msg: str = ""):
    not_none = [arg is not None for arg in args]
    assertion(
        all(not_none),
        [x[1] for x in filter(lambda x: x[0], zip(not_none, names))],
        msg,
        error_class=MissingRequiredMultipleException,
    )


def check_empty(arg: Any, name: str | None = None, msg: str = ""):
    assertion(arg is None or bool(arg), name, msg, error_class=EmptyValueException)


def check_at_least_1(args: List[Any], names: List[str]):
    assertion(
        any(arg is not None for arg in args), names, error_class=AtLeastOneException
    )


def check_at_most_1(args: List[Any], names: List[str]):
    assertion(
        sum(arg is not None for arg in args) <= 1, names, error_class=AtMostOneException
    )


def check_unique(args: List[Any], prop: str | None = None, msg: str = ""):
    if prop:
        args = [get(arg, prop, "") for arg in args]
    args = duplicates(args)
    assertion(len(args) == 0, args, msg, error_class=DuplicationException)
