# PLAN: DataPersistence

> 이 문서는 구현이 진행됨에 따라 갱신되는 living document입니다. 실제 구현 중 발견된 이슈나 구조 변경 사항을 반영해 계속 업데이트합니다.

## 1. 목적

애플리케이션을 재시작해도 데이터가 유지되는 영속성 구조를 검증하는 PoC. CRUD 전체를 포함한다.

## 2. 영속성 방식 결정

**SQLite** (Python 표준 라이브러리 `sqlite3`, 외부 서버 설치 불필요).

- 이유: 파일 하나로 동작하는 embedded DB라 콘솔 애플리케이션에 적합하고, `DummyDataGenerator`가 "연결된 DB에 추가"한다는 과제 요구사항과도 자연스럽게 맞물린다. `DataMonitor` PoC에서도 동일한 방식(SQLite 파일)을 별도로 읽어 조회하는 시나리오를 검증한다.
- DB 파일 경로: `data/app.db` (`.gitignore`에 이미 제외 처리됨).

## 3. 데모 도메인: Item(품목)

필드: `id`(PK, autoincrement), `name`(TEXT), `quantity`(INTEGER).

## 4. 폴더 구조

```
src/
  storage/
    connection.py   # DB 연결 관리 (context manager), 스키마 초기화
    item_repository.py  # CRUD 함수
  main.py           # CRUD 데모 시나리오 실행 스크립트
tests/
  test_item_repository.py
```

## 5. 구현 단계

- [x] 1단계 - `connection.py`: DB 파일 연결 함수(`get_connection`), 최초 실행 시 `items` 테이블 자동 생성(`CREATE TABLE IF NOT EXISTS`).
- [x] 2단계 - `item_repository.py`: `create_item`, `get_item`, `list_items`, `update_item`, `delete_item` 구현. **설계 변경**: 함수가 `db_path`를 직접 받는 대신 이미 열린 `sqlite3.Connection`을 인자로 받도록 했다 (이유: `:memory:` DB는 연결을 닫는 순간 사라지므로, 함수마다 자체적으로 연결을 열고 닫으면 테스트에서 여러 CRUD 호출 간 데이터가 유지되지 않는다).
- [x] 3단계 - `main.py`: CRUD 시나리오를 순차 실행하는 데모 스크립트 (생성 → 조회 → 수정 → 삭제 → 재조회).
- [x] 4단계 - `tests/test_item_repository.py`: `:memory:` DB로 격리된 CRUD 단위 테스트. pytest fixture로 테스트마다 새 connection 제공. 5개 테스트 통과.
- [x] 5단계 - 수동 검증: 별도 프로세스에서 데이터 삽입 후 재시작하여 `data/app.db`에서 재조회, 데이터 유지 확인.

## 6. 완료 기준 (Definition of Done)

- 외부 의존성 없이 표준 라이브러리(`sqlite3`)만으로 동작한다.
- `data/app.db` 파일에 데이터가 저장되며, 프로세스를 재시작해도 데이터가 유지된다.
- CRUD 4종 함수가 모두 테스트로 검증된다.
- DB 연결은 `with` 구문(context manager)으로 안전하게 열고 닫힌다.
- `pytest` 전체 통과.

## 7. 미결정/추후 논의 사항

- (없음, 발견 시 추가)

## 8. 변경 이력

- 최초 작성
- Repository 함수 시그니처를 `db_path` 대신 `conn`(열린 connection)을 받도록 변경 (`:memory:` 테스트 격리 문제 해결)
- Harness 도입: `pyproject.toml`(pytest/ruff 설정), `requirements-dev.txt`(pytest, ruff), GitHub Actions CI(`.github/workflows/ci.yml`) 추가. `ruff check` 결과 자동 수정 가능한 사소한 스타일(구식 `Optional[X]` 표기) 1건만 발견되어 `X | None`으로 수정.
