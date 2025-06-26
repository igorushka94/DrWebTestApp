from src.exceptions import InvalidArgsCountError

class CommandParser:
    @staticmethod
    def parse_command(input_cmd: str) -> tuple[str, list[str]]:
        splited_cmd = input_cmd.strip().split()
        if not splited_cmd:
            return ("", [])

        command = splited_cmd[0].upper()
        args = splited_cmd[1:]
        return (command, args)


def validate_args_count(expected_count):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) - 1 != expected_count:
                raise InvalidArgsCountError(
                    f"Команда {func.__name__.upper()} ожидает {expected_count} аргумент(ов), получено {len(args) - 1}."
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
