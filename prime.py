from sympy import isprime


def is_prime(n: int) -> bool:
    return isprime(n)


def is_order_of_q(g: int, q: int, p: int, check_prime: bool) -> bool:
    """
    Check if g is a generator of the group of order q.
    """
    if check_prime:
        assert is_prime(p), "p must be a prime number."
        assert is_prime(q), "q must be a prime number."

    return pow(g, q, p) == 1 and pow(g, 1, p) != 1
