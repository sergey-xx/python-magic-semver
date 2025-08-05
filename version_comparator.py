from copy import copy
import re
from functools import total_ordering


@total_ordering
class Version:
    """"
    Class for comparing different versions.

    Supports: > < = !=
    Can compare with str object.

    :param version: string that meets requirements: https://semver.org/
    """

    pattern = (
        r"^(?P<major>0|[1-9]\d*)\."
        r"(?P<minor>0|[1-9]\d*)\."
        r"(?P<patch>0|[1-9]\d*)(?:[-+]?"
        r"(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+"
        r"(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )

    def __init__(self, version: str):
        match = re.search(self.pattern, version)
        if not match:
            raise ValueError(f"Version {version} is not valid")
        *self.core, suffix, self.buildmetadata = match.groups()
        self.suffix = re.split(r'[+.-]', suffix) if suffix else []
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
        """implements special comparison logic for pre-release suffix."""
        if self.suffix and not other.suffix:
            return True
        if not self.suffix and other.suffix:
            return False
        # using separate var not to change any in object
        self_comparing_suffix = copy(self.suffix)
        other_comparing_suffix = copy(other.suffix)
        for i in range(
            min(len(self_comparing_suffix),
                len(other_comparing_suffix))
        ):
            if (
                self_comparing_suffix[i].isnumeric()
                and other_comparing_suffix[i].isnumeric()
            ):
                self_comparing_suffix[i] = int(self_comparing_suffix[i])
                other_comparing_suffix[i] = int(other_comparing_suffix[i])
        return self_comparing_suffix < other_comparing_suffix

    def __str__(self) -> str:
        core = '.'.join(self.core)
        suffix = f"-{'.'.join(self.suffix)}" if self.suffix else ""
        buildmetadata = f"+{self.buildmetadata}" if self.buildmetadata else ""
        return f"{core}{suffix}{buildmetadata}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.__str__()})>"
