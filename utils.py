class CommandParser:

    @staticmethod
    def parse_command(input_cmd: str) -> tuple[str, list[str]]:
        splited_cmd = input_cmd.strip().split()
        if not splited_cmd:
            return ("", [])

        command = splited_cmd[0].upper()
        args = splited_cmd[1:]
        return (command, args)
