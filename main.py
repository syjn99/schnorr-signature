import argparse
import os

from keygen import KeyPair
from paramgen import PublicParameters
from signature import Signature


def main():
    parser = argparse.ArgumentParser(description="Python implementation of Schnorr signature scheme")
    subparsers = parser.add_subparsers(dest="command", required=True)

    paramgen = subparsers.add_parser("paramgen", help="Generate public parameters for Schnorr signature scheme")
    paramgen.add_argument(
        "--output",
        type=str,
        default="params/param.json",
        help="Output file for the generated parameters (default: params/param.json)",
    )
    paramgen.add_argument("--l", type=int, default=20, help="Bit length of p")
    paramgen.add_argument("--n", type=int, default=10, help="Bit length of q")
    paramgen.add_argument("--p", type=int, help="(Optional) Prime number p")
    paramgen.add_argument("--q", type=int, help="(Optional) Prime number q")
    paramgen.add_argument("--g", type=int, help="(Optional) Generator g")

    keygen = subparsers.add_parser("keygen", help="Generate keypair for Schnorr signature scheme")
    keygen.add_argument(
        "--output",
        type=str,
        default="keys/keypair.json",
        help="Output file for the generated keypair (default: keys/keypair.json)",
    )
    keygen.add_argument("--param_file", type=str, required=True, help="Path to the public parameters file")
    keygen.add_argument("--x", type=int, help="(Optional) Secret key x")
    keygen.add_argument("--y", type=int, help="(Optional) Public key y")

    sign = subparsers.add_parser("sign", help="Sign a message using the Schnorr signature scheme")
    sign.add_argument(
        "--output",
        type=str,
        help="(Optional) Output file for the generated signature.",
    )
    sign.add_argument("--param_file", type=str, required=True, help="Path to the public parameters file")
    sign.add_argument("--key_file", type=str, required=True, help="Path to the keypair file")
    sign.add_argument("--message", type=str, required=True, help="Message to sign")
    sign.add_argument("--k", type=int, help="(Optional) Random integer k for signing")

    args = parser.parse_args()

    if args.command == "paramgen":
        param = PublicParameters.from_args(args)

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(param.to_json())
        print(f"Public parameters saved to {args.output}")
    elif args.command == "keygen":
        key = KeyPair.from_args(args)

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(key.to_json())
        print(f"Keypair saved to {args.output}")
    elif args.command == "sign":
        with open(args.param_file) as f:
            param = PublicParameters.from_json(f.read())

        with open(args.key_file) as f:
            key = KeyPair.from_json(f.read())

        signature = Signature.sign(args.message, param, key, args.k)
        print(f"Signature: {signature}")

        if args.output:
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            with open(args.output, "w") as f:
                f.write(signature.to_json())
            print(f"Signature saved to {args.output}")


if __name__ == "__main__":
    main()
