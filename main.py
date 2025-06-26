import sys

from cli import DbCLI
from db import CustomDB
from utils import CommandParser


def main() -> None:

    cli = DbCLI(db=CustomDB())

    while True:
        try:
            input_data = input().strip()
            cmd, args = CommandParser.parse_command(input_data)
            cli.execute_command(cmd, *args)

        except EOFError:
            print("\n...")
            sys.exit(0)

        except KeyboardInterrupt:
            print("\nОтмена пользователем")
            sys.exit(0)


if __name__ == "__main__":
    main()
