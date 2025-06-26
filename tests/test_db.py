from src.db import CustomDB

import pytest

from collections import Counter, defaultdict


def test_initial_state(db):
    assert db.storage == {}
    assert db._inverted_index == defaultdict(set)
    assert db._transactions == []


def test_available_commands(db):
    assert db.available_commands == {
        "SET", "GET", "UNSET", "COUNTS", "FIND", 
        "END", "BEGIN", "ROLLBACK", "COMMIT"
    }


def test_get(db):
    db.set("A", "1")
    assert db.storage["A"] == "1"
    assert db._inverted_index["1"] == {"A"}
    assert len(db._transactions) == 0


def test_set(db):
    db.set("A", "1")
    assert db.storage["A"] == "1"
    assert db._inverted_index["1"] == {"A"}
    assert len(db._transactions) == 0


def test_unset(db_with_data):

    assert "A" in db_with_data.storage
    assert "A" in db_with_data._inverted_index["1"]

    db_with_data.unset("A")

    assert "A" not in db_with_data.storage
    assert "1" not in db_with_data._inverted_index


def test_counts(db_with_data, capsys):
    db_with_data.counts("3")
    captured = capsys.readouterr()
    assert captured.out.strip() == "1"
    

def test_find(db_with_data, capsys):
    db_with_data.find("3")
    captured = capsys.readouterr()
    assert captured.out.strip() == "{'C'}"


def test_begin(db):
    db.begin()
    assert len(db._transactions) == 1
    db.begin()
    assert len(db._transactions) == 2


def test_commit(db):
    db.begin()
    assert len(db._transactions) == 1
    db.set("A", "1")
    assert "A" in db._transactions[0]
    assert "A" not in db.storage
    db.commit()
    assert len(db._transactions) == 0
    assert "A" in db.storage


def test_rollback(db):
    db.begin()
    assert len(db._transactions) == 1
    db.set("A", "1")
    assert "A" in db._transactions[0]
    assert "A" not in db.storage
    db.rollback()
    assert len(db._transactions) == 0
    assert "A" not in db.storage


def test_get_with_transaction(db_in_transaction):
    assert len(db_in_transaction._transactions) == 1
    assert db_in_transaction.storage["C"] == "3"
    assert db_in_transaction._transactions[0]["C"] == "5"


def test_set_with_transaction(db_in_transaction):
    assert len(db_in_transaction._transactions) == 1
    assert db_in_transaction.storage["C"] == "3"
    db_in_transaction.set("C", "8")
    assert db_in_transaction._transactions[0]["C"] == "8"


# TODO Пофиксить методы ниже в состоянии транзакции
def test_unset_with_transaction(db_in_transaction):
    # db_in_transaction.unset("C")
    # assert db_in_transaction.storage["C"] == "3"
    ...


def test_counts_with_transaction(db_in_transaction, capsys):
    # db_in_transaction.counts("5")
    # captured = capsys.readouterr()
    # assert captured.out.strip() == "1"

    # db_in_transaction.set("Y", "5")
    # captured = capsys.readouterr()
    # assert captured.out.strip() == "2"
    ...


def test_find_with_transaction(db_in_transaction, capsys):
    ...
