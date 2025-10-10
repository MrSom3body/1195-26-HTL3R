__author__ = "Karun Sandhu"


import argparse
import logging
import math
from pathlib import Path
from random import SystemRandom
from typing import Generator

from UE00_RSA.miller_rabin import generate_prime

logger = logging.getLogger()


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

    :param strip_padding: if True, remove trailing zero bytes from each block (for decryption)
    """
    with open(filename, "wb") as f:
        for i in ints:
            f.write(i.to_bytes(number_of_bytes, "big"))
    logger.info("Wrote %d blocks to %s", len(ints), filename)


def save_keys(key_length: int) -> None:
    """
    Saves the public and private keys to files named 'public.key' and 'private.key
    """
    logger.info("Generating %d-bit RSA keys...", key_length)
    public, private = generate_keys(key_length)
    logger.debug("Public key: %s", public)
    logger.debug("Private key: %s", private)

    pub_file = f"id_rsa{key_length}.pub"
    priv_file = f"id_rsa{key_length}"

    with open(pub_file, "w") as f:
        f.write(f"{public[0]}\n{public[1]}")
        logger.info("Saved public key to %s", pub_file)

    with open(priv_file, "w") as f:
        f.write(f"{private[0]}\n{private[1]}")
        logger.info("Saved private key to %s", priv_file)


def encrypt_file(filename: str) -> None:
    """
    Encrypts a file with the first file it finds named id_rsa*.pub
    :param filename: The path to the file to encrypt
    """
    logger.info("Encrypting file: %s", filename)

    keyfile = next(
        (
            f"id_rsa{bits}.pub"
            for bits in (2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2)
            if Path(f"id_rsa{bits}.pub").is_file()
        ),
        None,
    )
    if keyfile is None:
        logger.error("No public key file found.")
        raise FileNotFoundError("No public key file found.")

    with open(keyfile, "r") as f:
        e = int(f.readline().strip())
        n = int(f.readline().strip())
        number_of_bits = n.bit_length()
    logger.info("Using public key from %s", keyfile)

    integer_blocks: list[int] = list(
        file2ints(filename, number_of_bytes=(number_of_bits - 1) // 8)
    )
    logger.debug("Read %d blocks from %s", len(integer_blocks), filename)

    encrypted_blocks: list[int] = [pow(block, e, n) for block in integer_blocks]
    logger.debug("Encrypted all blocks.")

    ints2file(
        encrypted_blocks,
        f"{filename}.enc",
        number_of_bytes=(number_of_bits + 7) // 8,
    )
    logger.info("Encryption complete: %s.enc", filename)


def decrypt_file(filename: str) -> None:
    """
    Decrypts a file with the first file it finds named id_rsa*
    :param filename: The path to the file to decrypt
    """
    keyfile = next(
        (
            f"id_rsa{bits}"
            for bits in (2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2)
            if Path(f"id_rsa{bits}").is_file()
        ),
        None,
    )
    if keyfile is None:
        logger.error("No private key file found.")
        raise FileNotFoundError("No private key file found.")

    with open(keyfile, "r") as f:
        d = int(f.readline().strip())
        n = int(f.readline().strip())
        number_of_bits = n.bit_length()
    logger.info("Using private key from %s", keyfile)

    integer_blocks = list(
        file2ints(filename, number_of_bytes=(number_of_bits + 7) // 8)
    )
    logger.debug("Read %d encrypted blocks from %s", len(integer_blocks), filename)

    decrypted_blocks = [pow(block, d, n) for block in integer_blocks]
    logger.debug("Decrypted all blocks.")

    ints2file(
        decrypted_blocks,
        f"{filename}.dec",
        number_of_bytes=(number_of_bits - 1) // 8,
    )
    logger.info("Decryption complete: %s.dec", filename)


if __name__ == "__main__":
    import doctest

    _ = doctest.testmod()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--loglevel",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
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

    if args.loglevel:
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s", level=args.loglevel
        )
        logger.setLevel(args.loglevel)

    if args.keygen:
        save_keys(args.keygen)
        exit()

    if args.encrypt:
        encrypt_file(args.encrypt)
        exit()

    if args.decrypt:
        decrypt_file(args.decrypt)
        exit()
