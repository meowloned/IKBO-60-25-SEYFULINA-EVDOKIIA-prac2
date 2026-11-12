from src.config import parse_args


def main(argv=None):
    args = parse_args(argv)

    for key, value in vars(args).items():
        print(f"{key}={value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())