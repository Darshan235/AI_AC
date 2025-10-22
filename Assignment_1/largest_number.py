"""Find the largest number in a user-provided list.

This module provides:
- `largest_number(numbers)` - returns the largest numeric value from the list.
- A small CLI that asks the user to input numbers separated by spaces or commas
  and prints the largest value.

The functions accept ints and floats. Invalid inputs produce a clear error.
"""
from __future__ import annotations

import re
import sys
from typing import Iterable, List, Union

Number = Union[int, float]


def largest_number(numbers: Iterable[Number]) -> Number:
    """Return the largest number from `numbers`.

    Args:
        numbers: an iterable of int or float values

    Returns:
        The largest number (int or float)

    Raises:
        TypeError: if `numbers` is not iterable or contains non-numeric elements
        ValueError: if `numbers` is empty
    """
    try:
        iterator = iter(numbers)
    except TypeError:
        raise TypeError("numbers must be an iterable of numeric values")

    max_val: Number | None = None
    count = 0
    for x in iterator:
        if not isinstance(x, (int, float)):
            raise TypeError("all elements must be int or float")
        if max_val is None or x > max_val:
            max_val = x
        count += 1

    if count == 0:
        raise ValueError("numbers must contain at least one value")

    return max_val  # type: ignore[return-value]


def _parse_input(s: str) -> List[Number]:
    """Parse a string of numbers separated by spaces or commas into a list of numbers.

    Examples:
        '1 2 3' -> [1.0, 2.0, 3.0]
        '4,5, 6' -> [4.0, 5.0, 6.0]
    """
    if not s:
        raise ValueError("no input provided")

    parts = [p for p in re.split(r"[\s,]+", s.strip()) if p]
    nums: List[Number] = []
    for p in parts:
        try:
            # Try to parse as int first for nicer output, then float
            if re.match(r"^-?\d+$", p):
                nums.append(int(p))
            else:
                nums.append(float(p))
        except ValueError:
            raise ValueError(f"could not parse '{p}' as a number")
    return nums


def main() -> None:
    try:
        s = input("Enter numbers separated by spaces or commas: ")
    except EOFError:
        print("No input received.", file=sys.stderr)
        sys.exit(1)

    try:
        nums = _parse_input(s)
    except ValueError as e:
        print(f"Invalid input: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        largest = largest_number(nums)
    except (TypeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Print without unnecessary .0 for whole numbers
    if isinstance(largest, float) and largest.is_integer():
        # show as int for nicer display
        print(f"Largest number is: {int(largest)}")
    else:
        print(f"Largest number is: {largest}")


if __name__ == "__main__":
    main()
