import pytest

from src.storage.connection import get_connection
from src.storage.item_repository import (
    create_item,
    delete_item,
    get_item,
    list_items,
    update_item,
)


@pytest.fixture
def conn():
    with get_connection(":memory:") as connection:
        yield connection


def test_create_and_get_item(conn):
    item_id = create_item(conn, "품목A", 10)
    row = get_item(conn, item_id)
    assert row["name"] == "품목A"
    assert row["quantity"] == 10


def test_list_items_returns_all_rows(conn):
    create_item(conn, "품목A", 10)
    create_item(conn, "품목B", 20)
    rows = list_items(conn)
    assert [row["name"] for row in rows] == ["품목A", "품목B"]


def test_update_item_changes_fields(conn):
    item_id = create_item(conn, "품목A", 10)
    update_item(conn, item_id, "품목A-수정", 99)
    row = get_item(conn, item_id)
    assert row["name"] == "품목A-수정"
    assert row["quantity"] == 99


def test_delete_item_removes_row(conn):
    item_id = create_item(conn, "품목A", 10)
    delete_item(conn, item_id)
    assert get_item(conn, item_id) is None


def test_get_item_missing_id_returns_none(conn):
    assert get_item(conn, 999) is None
