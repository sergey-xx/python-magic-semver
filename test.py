from version_comparator import Version

TO_TEST = [
        # default test cases
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        # special test cases
        ("2.0.0a-yy", "2.0.0a-rc",),
        # test cases from https://semver.org/
        ("1.0.0-alpha", "1.0.0-alpha.1"),
        ("1.0.0-alpha.1", "1.0.0-alpha.beta"),
        ("1.0.0-alpha.beta", "1.0.0-beta"),
        ("1.0.0-beta", "1.0.0-beta.2"),
        ("1.0.0-beta.2", "1.0.0-beta.11"),
        ("1.0.0-beta.11", "1.0.0-rc.1"),
        ("1.0.0-rc.1", "1.0.0"),
    ]


def main():
    for left, right in TO_TEST:
        assert Version(left) < Version(right), f"le failed {left} < {right}"
        assert Version(right) > Version(left), f"ge failed {right} > {left}"
        assert Version(right) != Version(left), f"neq failed {right} != {left}"


if __name__ == "__main__":
    main()
