class DbCLI:
    def __init__(self, db):
        self.db = db

    def execute_command(self, cmd: str, *args, **kwargs) -> None:
        operation = getattr(self.db, cmd, None)

        if operation is None:
            print(
                f"Ошибка. Команда {cmd} не поддерживается {self.db.__class__.__name__}. Доступные команды {self.db.available_commands}"
            )
            return None

        operation(*args)
