import sys
from collections import Counter, defaultdict, ChainMap

from src.exceptions import TransactionError
from src.utils import validate_args_count


class CustomDB:
    def __init__(self) -> None:
        self.storage = {}
        self._inverted_index = defaultdict(set)  # Обратный индекс для find операции
        self._transactions = []  # Стек транзакций

    @property
    def available_commands(self) -> set:
        return {
            "SET",
            "GET",
            "UNSET",
            "COUNTS",
            "FIND",
            "END",
            "BEGIN",
            "ROLLBACK",
            "COMMIT",
        }

    @validate_args_count(1)
    def get(self, key) -> None:
        if not self._transactions:
            print(self.storage.get(key, "NULL"))
        else:
            if key in self._transactions[-1]:
                print(self._transactions[-1][key])
            else:
                print(self.storage.get(key, "NULL"))

    @validate_args_count(2)
    def set(self, key, value, is_commit=False) -> None:

        if not self._transactions or is_commit:
            self.storage[key] = value
            self._inverted_index[value].add(key)
        else:
            self._transactions[-1][key] = value

    def unset(self, key=None) -> None:

        if key is None:
            return

        if not self._transactions:
            if key in self.storage:
                value = self.storage[key]
                
                del self.storage[key]
                self._inverted_index[value].discard(key)

                if not self._inverted_index[value]:
                    del self._inverted_index[value]
        else:
            self._transactions[-1][key] = None

    @validate_args_count(1)
    def counts(self, value) -> None:
        if not self._transactions:
            print(len(self._inverted_index[value]))
        else:
            chained_transaction = ChainMap(*self._transactions)
            unseted_value_in_transaction = {k for k, v in chained_transaction.items() if v is None}
            value_in_transaction = {k for k, v in chained_transaction.items() if v == value}
            print(len(self._inverted_index[value] ^ unseted_value_in_transaction) + len(value_in_transaction))

    @validate_args_count(1)
    def find(self, value) -> None:
        if not self._transactions:
            print(self._inverted_index.get(value, set()))
        else:
            keys_for_value_in_transaction = {k for k, v in ChainMap(*self._transactions).items() if v == value}
            print(self._inverted_index.get(value, set()) | keys_for_value_in_transaction)

    def end(self) -> None:
        sys.exit(0)

    def begin(self) -> None:
        self._transactions.append({})

    def commit(self) -> None:
        if not self._transactions:
            raise TransactionError(
                "Операция невозможна, нет активных транзакций для фиксации."
            )
        
        if len(self._transactions) > 1:
            second_to_last_transaction = self._transactions[-2]
            last_transaction = self._transactions.pop()

            for k, v in last_transaction.items():
                second_to_last_transaction[k] = v
        else:
            last_transaction = self._transactions.pop()

            if last_transaction:
                for k, v in last_transaction.items():
                    if v is None:
                        self.unset(key=k)
                    else:
                        self.set(k, v, is_commit=True)
            else:
                raise TransactionError(
                    "Операция невозможна, нет изменений внутри транзакции."
                )

    def rollback(self) -> None:
        if not self._transactions:
            raise TransactionError(
                "Операция невозможна, нет активных транзакций для отката."
            )

        self._transactions.pop()
