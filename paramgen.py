import json

from prime import get_n_bit_prime, get_p_from_q, is_order_of_q, is_prime, select_generator


class PublicParameters:
    def __init__(self, p, q, g):
        self.p = p  # A large prime number
        self.q = q  # A small prime number and a divisor of p-1
        self.g = g  # A generator of the group with order q

    def __repr__(self):
        return f"PublicParameters(p={self.p}, q={self.q}, g={self.g})"

    def __str__(self):
        return f"Public Parameters:\n p: {self.p}\n q: {self.q}\n g: {self.g}"

    @classmethod
    def from_args(cls, args):
        """
        Create PublicParameters from command line arguments.
        """
        if args.p and args.q and args.g:
            # Sanity checks
            assert args.p > 0 and args.q > 0 and args.g > 0, "p, q, and g must be positive integers."
            assert args.p > args.q, "p must be greater than q."
            assert (args.p - 1) % args.q == 0, "q must divide (p-1)."

            # Check if p and q are prime
            assert is_prime(args.p), "p must be a prime number."
            assert is_prime(args.q), "q must be a prime number."

            # Check if g is a generator of the group of order q
            assert is_order_of_q(g=args.g, q=args.q, p=args.p), "g must be a generator of the group of order q."

            return cls(args.p, args.q, args.g)
        else:
            return cls.from_bit_length(args.l, args.n)

    @classmethod
    def from_bit_length(cls, l: int, n: int) -> "PublicParameters":
        """
        Generate public parameters with bit lengths l and n.
        """
        assert l > 0 and n > 0, "l and n must be positive integers."
        assert l > n, "l must be greater than n."

        # Generate prime p and q with l and n
        q = get_n_bit_prime(n)
        p = get_p_from_q(l, q)

        # Select a generator g of order q
        g = select_generator(p, q)

        return cls(p, q, g)

    def to_json(self) -> str:
        """
        Serialize the object to a JSON string.
        """
        return json.dumps({"p": self.p, "q": self.q, "g": self.g})

    def to_dict(self):
        return {"p": self.p, "q": self.q, "g": self.g}

    @classmethod
    def from_json(cls, json_str: str) -> "PublicParameters":
        """
        Deserialize the object from a JSON string.
        """
        data = json.loads(json_str)
        return cls(data["p"], data["q"], data["g"])

    def validate(self):
        """
        Validate the public parameters.
        """
        assert self.p > 0 and self.q > 0 and self.g > 0, "p, q, and g must be positive integers."
        assert self.p > self.q, "p must be greater than q."
        assert (self.p - 1) % self.q == 0, "q must divide (p-1)."
        assert is_prime(self.p), "p must be a prime number."
        assert is_prime(self.q), "q must be a prime number."
        assert is_order_of_q(g=self.g, q=self.q, p=self.p), "g must be a generator of the group of order q."
