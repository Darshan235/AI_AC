"""Two implementations of factorial: recursive and iterative.

This module provides:
- `recursive_factorial(n)` — straightforward recursive implementation (clear, but limited by recursion depth).
- `iterative_factorial(n)` — iterative loop implementation (recommended for large n).

Both functions validate input and raise `TypeError` or `ValueError` for invalid arguments.
A small CLI at the bottom demonstrates both implementations.
"""
from __future__ import annotations

import sys
from typing import Any


def recursive_factorial(n: int) -> int:
    """Compute n! using recursion.

    Args:
        n: non-negative integer

    Returns:
        n! as an int

    Raises:
        TypeError: if n is not an int
        ValueError: if n is negative

    Notes:
        - This implementation is simple and idiomatic, but Python's recursion depth
          (typically ~1000) limits how large `n` can be. For large values prefer
          the iterative version below or math.factorial.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    # Recursive step
    return n * recursive_factorial(n - 1)


def iterative_factorial(n: int) -> int:
    """Compute n! using an iterative loop.

    Args:
        n: non-negative integer

    Returns:
        n! as an int

    Raises:
        TypeError: if n is not an int
        ValueError: if n is negative

    This implementation uses a simple for-loop and works for much larger n
    than the recursive version (limited only by time/memory).
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def _demo_from_input() -> None:
    """Ask the user for an integer and print both factorials."""
    try:
        s = input("Enter a non-negative integer: ").strip()
        n = int(s)
    except (ValueError, EOFError):
        print("Invalid input: please enter a non-negative integer.", file=sys.stderr)
        sys.exit(1)

    print(f"Iterative: {n}! = {iterative_factorial(n)}")
    print(f"Recursive: {n}! = {recursive_factorial(n)}")


if __name__ == "__main__":
    _demo_from_input()
