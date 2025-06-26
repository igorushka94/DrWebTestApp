import sys
from collections import Counter, defaultdict

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
            print(self.storage.get(key))
        else:
            print(self._transactions[-1].get(key) or self.storage.get(key))

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

        if key in self.storage:
            value = self.storage[key]

            if self._transactions:
                if key not in self._transactions[-1]:
                    self._transactions[-1][key] = value

            del self.storage[key]
            self._inverted_index[value].discard(key)

            if not self._inverted_index[value]:
                del self._inverted_index[value]

    @validate_args_count(1)
    def counts(self, value) -> None:
        if not self._transactions:
            count = Counter(self.storage.values())
            print(count[value])
        else:
            count_in_storage = Counter(self.storage.values())
            count_in_transaction = Counter([i for i in self._transactions.values()])
            print(count_in_storage[value] + count_in_transaction[value])

    @validate_args_count(1)
    def find(self, value) -> None:
        if not self._transactions:
            print(self._inverted_index.get(value, set()))
        else:
            keys_for_value_in_transaction = {k for k, v in self._transactions.items() if v == value}
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
        
        current_transactions: dict = self._transactions.pop()

        if current_transactions:
            key, value = list(current_transactions.items())[0]
            self.set(key, value, is_commit=True)
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
