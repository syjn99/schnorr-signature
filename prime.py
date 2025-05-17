import random

import gmpy2


# Use Baillie–PSW primality test that is reliable, and also provided by gmpy2.
# Reference: https://en.wikipedia.org/wiki/Baillie%E2%80%93PSW_primality_test
def is_prime(n: int) -> bool:
    return gmpy2.is_strong_bpsw_prp(n)


def is_order_of_q(g: int, q: int, p: int, check_prime: bool = False) -> bool:
    """
    Check if g is a generator of the group of order q.
    """
    if check_prime:
        assert is_prime(p), "p must be a prime number."
        assert is_prime(q), "q must be a prime number."

    return pow(g, q, p) == 1 and pow(g, 1, p) != 1


# From the Betrand's postulate, there is always a prime number in the range (n, 2n).
# Reference: https://en.wikipedia.org/wiki/Bertrand's_postulate
def random_prime(lower: int, upper: int) -> int:
    """
    Generate a random prime number in the range [lower, upper).
    """
    assert lower < upper, "Lower bound must be less than upper bound."
    assert lower > 0, "Lower bound must be a positive integer."

    while True:
        # Generate a random number in the range
        num = random.randint(lower, upper - 1)

        # Check if the number is prime
        if is_prime(num):
            return num


def get_n_bit_prime(n: int) -> int:
    """
    Generate a random n-bit prime number.
    """
    assert n > 0, "n must be a positive integer."

    lower_bound = 2 ** (n - 1)
    upper_bound = 2**n

    # Find the random prime number in the range
    return random_prime(lower_bound, upper_bound)


def get_p_from_q(l: int, q: int) -> int:
    """
    Generate a l-bit prime number, with q (also prime) being a divisor of p-1.
    """
    assert l > 0, "l must be a positive integer."
    assert q > 0, "q must be a positive integer."

    k_min = (2 ** (l - 1)) // q
    k_max = (2**l) // q

    while True:
        k = random.randint(k_min, k_max)
        p = k * q + 1

        # Check if p is prime
        if is_prime(p):
            return p


def select_generator(p: int, q: int, check_prime: bool = False) -> int:
    """
    Select a generator g for the group of order q.
    """
    if check_prime:
        assert is_prime(p), "p must be a prime number."
        assert is_prime(q), "q must be a prime number."

    assert (p - 1) % q == 0, "q must divide p - 1"
    exponent = (p - 1) // q

    # Select a random integer g in the range [2, p-1]
    while True:
        g = random.randint(2, p - 1)
        alpha = pow(g, exponent, p)

        if alpha != 1:
            return alpha
