__author__ = "Karun Sandhu"

import argparse
import logging
import math

logger = logging.getLogger(__name__)


def crack_rsa(n: int, max_tries: int | None = None) -> tuple[int, int, int]:
    """
    Crack an RSA modulus
    :param n: the RSA modulus to crack
    :param max_tries: the max tries
    :return: the factors and the tries

    >>> crack_rsa(1000001000000090000037000001961, 125)
    (1000000000000037, 1000001000000053, 125)
    """
    a = math.isqrt(n)
    while a**2 < n:
        a += 1

    tries = 0
    while True:
        tries += 1
        b2 = a**2 - n
        b = math.isqrt(b2)
        if b**2 == b2:
            p = a - b
            q = a + b
            logger.info("Found factors after %d tries", tries)
            return (p, q, tries)

        a += 1

        if max_tries is not None and tries >= max_tries:
            logger.error("Reached max_tries=%s without success", max_tries)
            raise ValueError(f"Fermat factorization failed within {max_tries} tries")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    parser = argparse.ArgumentParser(
        description="Crack an RSA modulus using Fermat factorization."
    )
    parser.add_argument("modulus", type=int, help="The RSA modulus to factor")
    parser.add_argument(
        "-m",
        "--max",
        type=int,
        default=None,
        help="Maximum number of tries (default: unlimited)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    logger.debug("Starting with args: %s", args)
    try:
        p, q, tries = crack_rsa(args.modulus, max_tries=args.max)
        print(f"Success! p = {p}, q = {q}, tries = {tries}")
    except ValueError as e:
        logger.error("Error: %s", e)
        print(f"Failed: {e}")
