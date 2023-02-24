import re
from dataclasses import asdict
from typing import Callable, Iterable, List, Optional

from pydantic import root_validator, validator
from pydantic.dataclasses import dataclass

from hcraft.exception import check_at_least_1, check_empty


@dataclass
class RangeFilter:
    str_list: List[str]
    start: int | str | List[str]
    end: int | str | List[str]
    include_end: bool
    use_regex: bool


@dataclass
class ExistenceFilter:
    str_list: List[str]
    patterns: List[str]
    use_regex: bool

    @validator("patterns")
    def check_patterns(cls, v):
        check_empty(v, "patterns")
        return v


@dataclass
class StrListFilter:
    range: RangeFilter | None = None
    include: ExistenceFilter | None = None
    exclude: ExistenceFilter | None = None

    @root_validator
    def check_values(cls, values):
        check_at_least_1(
            [values.get("range"), values.get("include"), values.get("exclude")],
            ["range", "include", "exclude"],
        )
        return values


def get_match_fn(use_regex: bool = False) -> Callable[[str, str], bool]:
    """
    Returns a function to determine if a pattern matches given string.

    :param use_regex:
        `False`(default), matches by existence;
        `True`, matches by regular expression
    """

    def match_by_regex(item: str, ptn: str) -> bool:
        return bool(re.match(ptn, item))

    def match_by_occurrence(item: str, ptn: str) -> bool:
        return ptn in item

    return match_by_regex if use_regex else match_by_occurrence


def get_match_index(
    str_list: Iterable[str],
    pattern: str | List[str],
    use_regex: bool = False,
    reverse: bool = False,
    default: int = 0,
) -> int:
    """
    Find matching index of given patterns from a string list.

    :param str_list: a list of strings.
    :param pattern: pattern(s) used to find matches from `str_list`.
    :param use_regex:
        `False`(default), matches by existence;
        `True`, matches by regular expression.
    :param reverse: if `True`, reverse `str_list`.
    :param default: fallback index if not matches.
    :return: index of the matched item.
    """
    match_fn = get_match_fn(use_regex)
    for index, s in (
        reversed(list(enumerate(str_list))) if reverse else enumerate(str_list)
    ):
        if (
            any(match_fn(s, p) for p in pattern)
            if isinstance(pattern, list)
            else match_fn(s, pattern)
        ):
            return index
    return default


def filter_by_range(
    str_list: List[str],
    start: int | str | List[str] = 0,
    end: int | str | List[str] = 0,
    include_end: bool = False,
    use_regex: bool = False,
) -> List[str]:
    if not isinstance(start, int):
        start = get_match_index(str_list, start, use_regex)
    if not isinstance(end, int):
        end = get_match_index(
            str_list, end, use_regex, reverse=True, default=len(str_list)
        )
    else:
        end = end or len(str_list)
    return str_list[start : end + include_end]


def filter_by_existence(
    str_list: List[str],
    patterns: List[str],
    include: bool = True,
    use_regex: bool = False,
) -> List[str]:
    match_fn = get_match_fn(use_regex)
    return [s for s in str_list if (any(match_fn(s, m) for m in patterns) and include)]


def filter_str_list(
    str_list: List[str], filters: StrListFilter | None = None
) -> List[str]:
    if filters:
        if filters.range:
            str_list = filter_by_range(str_list, **asdict(filters.range))
        if filters.include:
            str_list = filter_by_existence(
                str_list, **asdict(filters.include), include=True
            )
        if filters.exclude:
            str_list = filter_by_existence(
                str_list, **asdict(filters.exclude), include=False
            )

    return str_list
