
"""Small utility: is_prime function with a CLI that asks the user for input."""
import math
import sys


def is_prime(n: int) -> bool:
    """Return True if n is prime, otherwise False.

    Handles n < 2 as non-prime. Uses 6k ± 1 optimization for checking.
    """
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    if n % 3 == 0:
        return n == 3
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def main() -> None:
    try:
        s = input("Enter an integer: ").strip()
        n = int(s)
    except (ValueError, EOFError):
        print("Invalid input: please enter an integer.", file=sys.stderr)
        sys.exit(1)

    if is_prime(n):
        print(f"{n} is prime")
    else:
        print(f"{n} is not prime")


if __name__ == "__main__":
    main()
