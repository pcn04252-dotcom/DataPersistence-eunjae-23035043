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


def test_get_connection_creates_parent_directory_and_file(tmp_path):
    """:memory:가 아닌 실제 파일 경로를 사용할 때 상위 폴더/DB 파일이 정상 생성되는지 확인."""
    db_path = tmp_path / "nested" / "app.db"
    assert not db_path.parent.exists()

    with get_connection(db_path) as connection:
        create_item(connection, "품목A", 10)

    assert db_path.exists()


def test_data_persists_across_separate_connections_to_same_file(tmp_path):
    """앱 재시작(=connection을 새로 여는 것) 후에도 데이터가 유지되는지 확인 (영속성 요건)."""
    db_path = tmp_path / "app.db"

    with get_connection(db_path) as connection:
        create_item(connection, "품목A", 10)

    with get_connection(db_path) as connection:
        rows = list_items(connection)

    assert [row["name"] for row in rows] == ["품목A"]
