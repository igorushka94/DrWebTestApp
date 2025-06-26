from src.exceptions import OperationError


class DbCLI:
    def __init__(self, db):
        self.db = db

    def execute_command(self, cmd: str, *args, **kwargs) -> None:
        operation = getattr(self.db, cmd.lower(), None)

        if operation is None:
            raise OperationError(
                f"Команда {cmd} не поддерживается {self.db.__class__.__name__}. Доступные команды {self.db.available_commands}"
            )

        operation(*args)
