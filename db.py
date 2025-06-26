import sys
from collections import Counter, defaultdict


class CustomDB:
    def __init__(self):
        self.storage = {}
        self._inverted_index = defaultdict(set)
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

    def get(self, value):
        print(self.storage.get(value, None))

    def set(self, key, value):
        self.storage[key] = value
        self._inverted_index[value].add(key)

    def unset(self, key):
        if key in self.storage:
            value = self.storage[key]
            del self.storage[key]
            self._inverted_index[value].discard(key)
            # TODO разобраться с удалением из обратного индекса
            # if not self._value_index[value]:
            #     del self._value_index[value]

    def counts(self, value):
        c = Counter(self.storage.values())
        print(c[value])

    def find(self, value):
        """Выводит найденные установленные переменные для заданного значения."""
        print(self._inverted_index.get(value, set()))

    def end(self):
        sys.exit(0)

    def begin(self):
        self._transactions.append({})

    def commit(self):
        if not self._transactions:
            raise RuntimeError(
                "Ошибка. Операция невозможна, нет активных транзакций для комита."
            )

        if len(self._transactions) > 1:
            parent_transactions = self._transactions[-2]
            current_transactions = self._transactions[-1]

            for k, v in current_transactions.items():
                parent_transactions[k] = v

        self._transactions.pop()

    def rollback(self) -> None:
        if not self._transactions:
            raise RuntimeError(
                "Ошибка. Операция невозможна, нет активных транзакций для отката."
            )

        self._transactions.pop()
