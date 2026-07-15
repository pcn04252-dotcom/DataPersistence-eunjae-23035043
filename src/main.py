import sys

from src.storage.connection import get_connection
from src.storage.item_repository import (
    create_item,
    delete_item,
    get_item,
    list_items,
    update_item,
)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    with get_connection() as conn:
        print("1) 생성")
        item_id = create_item(conn, "실리콘 웨이퍼", 100)
        print(f"   생성된 Item ID: {item_id}")

        print("2) 조회")
        print(f"   {dict(get_item(conn, item_id))}")

        print("3) 수정")
        update_item(conn, item_id, "실리콘 웨이퍼-8인치", 150)
        print(f"   수정 후: {dict(get_item(conn, item_id))}")

        print("4) 전체 목록")
        for item in list_items(conn):
            print(f"   {dict(item)}")

        print("5) 삭제")
        delete_item(conn, item_id)
        print(f"   삭제 후 조회 결과: {get_item(conn, item_id)}")


if __name__ == "__main__":
    main()
