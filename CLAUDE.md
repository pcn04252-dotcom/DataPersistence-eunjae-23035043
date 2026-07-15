# CLAUDE.md

> 이 문서는 구현이 진행됨에 따라 갱신되는 living document입니다. 새 세션에서 이 repo를 열었을 때 아래 내용만으로 작업을 이어갈 수 있어야 합니다.

## 프로젝트 개요

SQLite 기반 데이터 영속성 및 CRUD 구조를 검증하는 PoC. 상세 계획은 `PLAN.md` 참고.

## 기술 스택

- Python 3.x + `sqlite3` (표준 라이브러리, 외부 의존성 없음)
- 테스트: `pytest` / 린트: `ruff` (설정은 `pyproject.toml`)
- CI: GitHub Actions (`.github/workflows/ci.yml`) — push/PR 시 `ruff check` + `pytest` 자동 실행

## 폴더 구조

```
src/storage/connection.py      # DB 연결/스키마 초기화
src/storage/item_repository.py # CRUD
src/main.py                    # CRUD 데모 스크립트
tests/                         # :memory: DB 기반 단위 테스트
data/app.db                    # 실제 영속 데이터 (git 추적 제외)
```

## 실행 방법

```
python -m src.main
```

## 테스트 방법

```
pip install -r requirements-dev.txt
pytest
ruff check .
```

## 코드 컨벤션

- DB 연결은 항상 `with` 구문으로 열고 닫는다 (연결 누수 방지).
- `item_repository.py`의 CRUD 함수는 `db_path`가 아니라 이미 열린 `sqlite3.Connection`을 인자로 받는다. (`:memory:` DB는 연결이 닫히면 사라지므로, 하나의 시나리오/테스트 안에서 여러 CRUD 호출이 같은 데이터를 봐야 할 때는 connection을 공유해야 한다.)
- 테스트는 실제 파일(`data/app.db`)이 아닌 `:memory:` DB를 사용해 격리한다 (pytest fixture로 테스트마다 새 connection 제공).
- SQL은 항상 파라미터 바인딩(`?` 플레이스홀더)을 사용한다 (문자열 포매팅으로 SQL을 조립하지 않는다 — SQL Injection 방지).
- 타입 힌트를 사용한다.

## 주의사항

- `data/app.db`는 `.gitignore`에 포함되어 있으므로 커밋되지 않는다. 스키마 자체는 코드(`connection.py`)로 재현 가능해야 한다.
- 이 repo의 스키마/영속성 방식(SQLite)은 `DataMonitor`, `DummyDataGenerator`, `SampleOrderSystem`과 설계 방향을 공유하지만, 각 repo는 독립된 저장소이므로 실제 코드/DB 파일을 공유하지 않는다.
- 콘솔 출력이 있는 진입점(`main.py`)에서는 Windows 콘솔 기본 코드페이지(cp949) 한글 깨짐 방지를 위해 `sys.stdout.reconfigure(encoding="utf-8")`를 적용한다 (`ConsoleMVC` PoC에서 확인된 이슈). 이 repo의 `main.py`는 사용자 입력(`input()`)을 받지 않는 데모 스크립트라 `stdin` 재설정은 불필요하다.
