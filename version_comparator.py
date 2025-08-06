import re
from copy import copy
from functools import total_ordering
from typing import Container


@total_ordering
class Version:
    """"
    Class for comparing different versions.

    Supports: > < = !=
    Can compare with str object.

    Pre-release suffixes are comparing by it`s fieds from left to right.
    Field that included in 'highest_priority_tags' list is considered as
    the last one.

    :param version: string that meets requirements: https://semver.org/
    """

    pattern: str = (
        r"^(?P<major>0|[1-9]\d*)\."
        r"(?P<minor>0|[1-9]\d*)\."
        r"(?P<patch>0|[1-9]\d*)(?:[-+]?"
        r"(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+"
        r"(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )
    suffix_splitters: str = r'[+.-]'
    highest_priority_tags: Container[str] = ('rc', 'preview')

    def __init__(self, version: str):
        match = re.search(self.pattern, version)
        if not match:
            raise ValueError(f"Version {version} is not valid")
        *self.core, suffix, self.buildmetadata = match.groups()
        self.suffix = re.split(self.suffix_splitters, suffix) if suffix else []
        self._validate_attrs()

    def _validate_attrs(self):
        """Validate core."""
        for i in range(len(self.core)):
            value = self.core[i]
            if len(value) > 1 and value.startswith("0"):
                raise ValueError(f"{value} must not start with `0`")
            try:
                value = int(value)
            except Exception:
                raise ValueError(f"{value} must be int")

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        self_value = (self.core, self.suffix)
        other_value = (other.core, other.suffix)
        return self_value == other_value

    def __lt__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        if self.core != other.core:
            return self.core < other.core
        return self._lt_suffix(other)

    def _lt_suffix(self, other):
        """
        Implements special comparison logic for pre-release suffix.
        """
        if self.suffix and not other.suffix:
            return True
        if not self.suffix and other.suffix:
            return False
        self_suffix = copy(self.suffix)
        other_suffix = copy(other.suffix)
        for i in range(
            min(len(self_suffix), len(other_suffix))
        ):
            if (
                self_suffix[i] in self.highest_priority_tags
                and other_suffix[i] not in self.highest_priority_tags
            ):
                return False
            if (
                self_suffix[i] not in self.highest_priority_tags
                and other_suffix[i] in self.highest_priority_tags
            ):
                return True
            if all(
                (
                    self_suffix[i].isnumeric(),
                    other_suffix[i].isnumeric()
                )
            ):
                self_suffix[i] = int(self_suffix[i])
                other_suffix[i] = int(other_suffix[i])
        return self_suffix < other_suffix

    def __str__(self) -> str:
        core = '.'.join(self.core)
        suffix = f"-{'.'.join(self.suffix)}" if self.suffix else ""
        buildmetadata = f"+{self.buildmetadata}" if self.buildmetadata else ""
        return f"{core}{suffix}{buildmetadata}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.__str__()})>"
