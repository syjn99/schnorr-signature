import hashlib
import json
import math
import random

from keygen import KeyPair
from paramgen import PublicParameters

sha = hashlib.sha256


class Signature:
    def __init__(self, s: int, e: int, m: str, param: PublicParameters):
        self.s = s
        self.e = e
        self.m = m
        self.param = param

    def __repr__(self):
        return f"Signature(s={self.s}, e={self.e}, m={self.m}, param={self.param})"

    def __str__(self):
        return (
            "Signature:\n"
            f"  s: {self.s}\n"
            f"  e: {self.e}\n"
            f"  m: {self.m}\n"
            "  Public Parameters:\n"
            f"    p: {self.param.p}\n"
            f"    q: {self.param.q}\n"
            f"    g: {self.param.g}"
        )

    def to_json(self) -> str:
        """
        Serialize the object to a JSON string.
        """
        return json.dumps({"s": self.s, "e": self.e, "m": self.m, "param": self.param.to_dict()})

    @classmethod
    def from_json(cls, json_str: str):
        """
        Deserialize the object from a JSON string.
        """
        data = json.loads(json_str)
        return cls(data["s"], data["e"], data["m"], PublicParameters(p=data["param"]["p"], q=data["param"]["q"], g=data["param"]["g"]))

    @classmethod
    def sign(cls, m: str, param: PublicParameters, keypair: KeyPair, k: int = None) -> "Signature":
        """
        Sign a message using the Schnorr signature scheme, with the given public parameters and keypair.
        """
        if k is None:
            # Randomly generate k
            k = random.randint(1, param.q - 1)
        r = pow(param.g, k, param.p)

        input = m.encode() + r.to_bytes((r.bit_length() + 7) // 8, byteorder="big")
        e = hashlib.sha256(input).digest()

        # Only use leftmost n bits (bit length of prime q) of the hash
        n = math.ceil(math.log2(param.q))
        e = int.from_bytes(e, byteorder="big") >> (256 - n)

        s = (keypair.secret_key * e + k) % param.q
        return cls(s, e, m, param)
