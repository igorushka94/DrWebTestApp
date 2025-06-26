import sys

from src.cli import DbCLI
from src.db import CustomDB
from src.exceptions import CustomDBError
from src.utils import CommandParser


def main() -> None:
    cli = DbCLI(db=CustomDB())

    while True:
        try:
            input_data = input("> ").strip()
            cmd, args = CommandParser.parse_command(input_data)
            
            if cmd:
                cli.execute_command(cmd, *args)
            else:
                continue

        except CustomDBError as ex:
            print(f"{ex.__class__.__name__}: ",  ex)

        except EOFError:
            print("\nКонец ввода")
            sys.exit(0)

        except KeyboardInterrupt:
            print("\nОтмена пользователем")
            sys.exit(0)


if __name__ == "__main__":
    main()
