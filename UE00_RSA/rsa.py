__author__ = "Karun Sandhu"


import argparse
import math
from typing import Generator
from UE00_RSA.miller_rabin import generate_prime
from random import SystemRandom


def generate_keys(
    number_of_bits: int,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """
    Generates a pair of RSA keys.

    :param number_of_bits: The desired bit length of the modulus n.
    :return: A tuple containing the public key (e, n, number_of_bits) and the private key (d, n, number_of_bits).

    >>> public, private = generate_keys(256)
    >>> e, n, _ = public
    >>> d, _, _ = private
    >>> test_values = [
    ...     0,
    ...     1,
    ...     42,
    ...     123456,
    ...     2**16,
    ...     2**128 - 1,
    ...     n - 1,
    ... ]

    >>> for x in test_values:
    ...     c = pow(x, e, n)
    ...     y = pow(c, d, n)
    ...     assert x == y, f"Round‑trip failed for {x}"
    """
    while True:
        p = generate_prime(number_of_bits // 2)
        q = generate_prime(number_of_bits // 2)
        n = p * q
        if p != q and n.bit_length() >= number_of_bits:
            break

    phi = (p - 1) * (q - 1)

    while True:
        e = SystemRandom().randint(phi**2, phi**8)
        if math.gcd(e, phi) == 1:
            break

    d = pow(e, -1, phi)

    return (e, n, number_of_bits), (d, n, number_of_bits)


def file2ints(filename: str, number_of_bytes: int) -> Generator[int]:
    """
    Reads a binary file and converts its contents into a list of integers, where
    each integer represents a block of bytes of the specified size.

    :param filename: The path to the binary file to read.
    :param number_of_bytes: The number of bytes per block to convert into an integer.
    """
    with open(filename, "rb") as f:
        while block := f.read(number_of_bytes):
            yield int.from_bytes(block, "big")


def ints2file(ints: list[int], filename: str, number_of_bytes: int) -> None:
    """
    Writes a list of integers to a binary file, converting each integer back into
    its byte representation.
    """
    with open(filename, "wb") as f:
        for i in ints:
            f.write(i.to_bytes(number_of_bytes, "big"))


def save_keys(key_length: int) -> None:
    """
    Saves the public and private keys to files named 'public.key' and 'private.key
    """
    public, private = generate_keys(key_length)

    with open(f"rsa{key_length}", "w") as f:
        f.write(f"{public[0]}\n{public[1]}")

    with open(f"rsa{key_length}.pub", "w") as f:
        f.write(f"{private[0]}\n{private[1]}")


if __name__ == "__main__":
    import doctest

    _ = doctest.testmod()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbosity", help="increase output verbosity", action="store_true"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-k",
        "--keygen",
        metavar="KEY_LENGTH",
        help="generate new keys with the given length",
        type=int,
    )
    group.add_argument(
        "-e", "--encrypt", metavar="FILE", help="file to encrypt", type=str
    )
    group.add_argument(
        "-d", "--decrypt", metavar="FILE", help="file to decrypt", type=str
    )

    args = parser.parse_args()

    if args.keygen:
        save_keys(args.keygen)
        exit()
