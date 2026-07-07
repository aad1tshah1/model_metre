import sys

from modelmetre.cli.router import route


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print("No command or prompt provided.")
        raise SystemExit(1)

    route(args)


if __name__ == "__main__":
    main()