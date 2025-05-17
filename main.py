import argparse
import os
import random
import string
import time

from keygen import KeyPair
from paramgen import PublicParameters
from signature import Signature
from test import test_with_vector


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
    paramgen.add_argument("--validate", type=bool, default=False, help="Validate the parameters")

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

    verify = subparsers.add_parser("verify", help="Verify a Schnorr signature")
    verify.add_argument(
        "--signature_file",
        type=str,
        required=True,
        help="Path to the signature file",
    )

    bench = subparsers.add_parser("bench", help="Benchmark the Schnorr signature scheme")
    bench.add_argument("--l", type=int, help="(Optional) Bit length of p")
    bench.add_argument("--n", type=int, help="(Optional) Bit length of q")
    bench.add_argument("--param_file", type=str, help="(Optional) Path to the public parameters file")

    test = subparsers.add_parser("test", help="Run tests for the Schnorr signature scheme with given test vectors")
    test.add_argument(
        "--test_vector_file",
        type=str,
        required=True,
        help="Path to the test vector file",
    )

    args = parser.parse_args()

    if args.command == "paramgen":
        param = PublicParameters.from_args(args)

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(param.to_json())
        print(f"Public parameters saved to {args.output}")

        if args.validate:
            print("Validating the parameters...")
            param.validate()
            print("Parameters are valid.")

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
        print(f"{signature}")

        if args.output:
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            with open(args.output, "w") as f:
                f.write(signature.to_json())
            print(f"Signature saved to {args.output}")
    elif args.command == "verify":
        with open(args.signature_file) as f:
            signature = Signature.from_json(f.read())

        # Verify the signature
        is_valid = Signature.verify(signature)
        if is_valid:
            print("Signature is valid.")
        else:
            print("Signature is invalid.")
    elif args.command == "bench":
        print("Benchmarking the Schnorr signature scheme...")

        start_time = time.time()

        if args.param_file:
            print(f"Loading parameters from {args.param_file}")
            with open(args.param_file) as f:
                param = PublicParameters.from_json(f.read())
        else:
            print("Generating new parameters...")
            param = PublicParameters.from_bit_length(args.l, args.n)
        print(f"{param}")

        print()

        print("Keypair generation...")
        key = KeyPair.from_param(param)
        print(f"{key}")

        print()

        # Generate a random message with a fixed length
        length = 50
        random_string = "".join(random.choices(string.ascii_letters + string.digits, k=length))

        print(f"Signing the message: {random_string}")

        # Sign the message
        signature = Signature.sign(random_string, param, key)
        print(f"{signature}")

        print()

        # Verify the signature
        print("Verifying the signature...")
        is_valid = Signature.verify(signature)
        if is_valid:
            print("Signature is valid.")
        else:
            print("Signature is invalid.")
        end_time = time.time()

        print(f"Benchmarking completed in {end_time - start_time:.2f} seconds.")
    elif args.command == "test":
        test_with_vector(args.test_vector_file)
        print("Test completed.")
    else:
        raise Exception("Invalid command")


if __name__ == "__main__":
    main()
