class CustomDBError(Exception):
    pass


class TransactionError(CustomDBError):
    pass


class OperationError(CustomDBError):
    pass


class InvalidArgsCountError(CustomDBError):
    pass
