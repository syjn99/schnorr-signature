import json


class KeyPair:
    def __init__(self, public_key: int, secret_key: int):
        self.public_key = public_key
        self.secret_key = secret_key

    def __repr__(self):
        return f"KeyPair(public_key={self.public_key}, secret_key={self.secret_key})"

    def __str__(self):
        return f"Key Pair:\n Public Key: {self.public_key}\n Secret Key: {self.secret_key}"

    @classmethod
    def from_args(cls, args):
        """
        Create KeyPair from command line arguments.
        """
        if args.x and args.y:
            x = args.x
            y = args.y

            # Sanity checks
            assert x > 0 and y > 0, "x and y must be positive integers."

            with open(args.param_file) as f:
                param = json.load(f)
                p = param["p"]
                q = param["q"]
                g = param["g"]

            # Check if p, q, and g are valid
            assert x >= 1 and x <= (q - 1), "x must be in the range [1, q-1]."
            assert y == pow(g, x, p), "y must be equal to g^x mod p."

            return cls(y, x)
        else:
            raise Exception("Not yet implemented")

    def to_json(self) -> str:
        """
        Serialize the object to a JSON string.
        """
        return json.dumps({"public_key": self.public_key, "secret_key": self.secret_key})

    @classmethod
    def from_json(cls, json_str: str) -> "KeyPair":
        """
        Deserialize the object from a JSON string.
        """
        data = json.loads(json_str)
        return cls(data["public_key"], data["secret_key"])


def generate_key():
    """
    Generates a keypair for Schnorr signatures.
    """
    print("Generating key...")
