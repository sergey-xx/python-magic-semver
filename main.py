import re
from functools import total_ordering


@total_ordering
class Version:

    pattern = r"^(\d+)\.(\d+)\.(\d+)-?(\S+)?$"

    def _validate_attrs(self):
        for attr in ("major", "minor", "patch"):
            value = getattr(self, attr)
            if len(value) > 1 and value.startswith("0"):
                raise ValueError(f"{attr} must not start with `0`")
            try:
                int_value = int(value)
                setattr(self, attr, int_value)
            except Exception:
                raise ValueError(f"{attr} must be int")

    def __init__(self, version):
        match = re.search(self.pattern, version)
        if not match:
            raise ValueError("Version is not valid")
        self.major, self.minor, self.patch, self.suffix = match.groups()
        self._validate_attrs()

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        self_value = (self.major, self.minor, self.patch, self.suffix)
        other_value = (other.major, other.minor, other.patch, other.suffix)
        return self_value == other_value

    def __lt__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        self_value = (self.major, self.minor, self.patch)
        other_value = (other.major, other.minor, other.patch)
        if self_value != other_value:
            return self_value < other_value
        if self.suffix and not other.suffix:
            return True
        if not self.suffix and other.suffix:
            return False
        return self.suffix < other.suffix

    def __str__(self) -> str:
        suffix = f"-{self.suffix}" if self.suffix else ""
        return f"{self.major}.{self.minor}.{self.patch}{suffix}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.__str__()})>"


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for left, right in to_test:
        assert Version(left) < Version(right), "le failed"
        assert Version(right) > Version(left), "ge failed"
        assert Version(right) != Version(left), "neq failed"


if __name__ == "__main__":
    main()
