Requirements:
- Python 3.11
## Using Version class

It supports all versions described in https://semver.org/
Also "1.0.1b" or "2.0.0a-yy" are supported.
You can change validations by changing pattern attribute.

Pre-release suffixes are comparing by it`s fieds from left to right.
Field that included in 'highest_priority_tags' attribute list has the highest priority. So "2.0.0a-yy" < "2.0.0a-rc".
## How to Start and Run Test cases
To run it, you need to:

- open a terminal or command prompt.
- navigate to the directory where you saved the file.
- un the script using the Python interpreter:

```
python test.py
```
