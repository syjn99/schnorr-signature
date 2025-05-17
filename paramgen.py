import json

from sympy import isprime


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
            # Basic checks
            assert args.p > 0 and args.q > 0 and args.g > 0, "p, q, and g must be positive integers."
            assert args.p > args.q, "p must be greater than q."
            assert (args.p - 1) % args.q == 0, "q must divide (p-1)."

            # Check if p and q are prime
            assert isprime(args.p), "p must be a prime number."
            assert isprime(args.q), "q must be a prime number."

            # Check if g is a generator of the group of order q
            assert pow(args.g, args.q, args.p) == 1 and pow(args.g, 1, args.p) != 1, "g must be a generator of the group of order q."

            return cls(args.p, args.q, args.g)
        else:
            # Generate with l and n
            raise Exception("Not yet implemented")

    def to_json(self) -> str:
        """
        Serialize the object to a JSON string.
        """
        return json.dumps({"p": self.p, "q": self.q, "g": self.g})

    @classmethod
    def from_json(cls, json_str: str) -> "PublicParameters":
        """
        Deserialize the object from a JSON string.
        """
        data = json.loads(json_str)
        return cls(data["p"], data["q"], data["g"])
