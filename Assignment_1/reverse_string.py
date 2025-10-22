"""Simple utility to reverse a string.

Provides a pure function `reverse_string(s)` and a small CLI that asks the
user for a string and prints its reversed form.
"""
from __future__ import annotations

import sys
from typing import Optional


def reverse_string(s: str) -> str:
    """Return a new string which is the reverse of `s`.

    Args:
        s: input string

    Returns:
        Reversed string

    Raises:
        TypeError: if `s` is not a string

    Examples:
        >>> reverse_string('abc')
        'cba'
        >>> reverse_string('')
        ''
    """
    if not isinstance(s, str):
        raise TypeError('s must be a str')
    # Pythonic slice-based reversal (O(n) time, O(n) memory)
    return s[::-1]


def main() -> None:
    try:
        s: Optional[str] = input("Enter a string: ")
    except EOFError:
        print("No input received.", file=sys.stderr)
        sys.exit(1)

    # Print the reversed string
    print(reverse_string(s))


if __name__ == '__main__':
    main()
