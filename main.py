import argparse
import os

from paramgen import PublicParameters


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

    args = parser.parse_args()

    if args.command == "paramgen":
        param = PublicParameters.from_args(args)

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(param.to_json())
        print(f"Public parameters saved to {args.output}")


if __name__ == "__main__":
    main()
