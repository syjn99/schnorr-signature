from keygen import KeyPair
from paramgen import PublicParameters
from signature import Signature


def test_with_vector(file_path: str):
    values = {}

    with open(file_path) as f:
        for line in f:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                key = key.strip().lstrip("[+] ").strip()
                value = value.strip()
                values[key] = value

    param = PublicParameters(p=int(values["p"]), q=int(values["q"]), g=int(values["g"]))
    keypair = KeyPair(secret_key=int(values["x"]), public_key=int(values["y"]))

    signature = Signature.sign(values["m"], param, keypair, int(values["k"]))

    assert signature.s == int(values["s"]), f"Signature s does not match: {signature.s} != {values['s']}"
    assert signature.e == int(values["e"]), f"Signature e does not match: {signature.e} != {values['e']}"
