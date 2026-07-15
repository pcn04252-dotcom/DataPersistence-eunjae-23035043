# CLAUDE.md

> 이 문서는 구현이 진행됨에 따라 갱신되는 living document입니다. 새 세션에서 이 repo를 열었을 때 아래 내용만으로 작업을 이어갈 수 있어야 합니다.

## 프로젝트 개요

SQLite 기반 데이터 영속성 및 CRUD 구조를 검증하는 PoC. 상세 계획은 `PLAN.md` 참고.

## 기술 스택

- Python 3.x + `sqlite3` (표준 라이브러리, 외부 의존성 없음)
- 테스트: `pytest`

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
pytest
```

## 코드 컨벤션

- DB 연결은 항상 `with` 구문으로 열고 닫는다 (연결 누수 방지).
- 테스트는 실제 파일(`data/app.db`)이 아닌 `:memory:` DB를 사용해 격리한다.
- SQL은 항상 파라미터 바인딩(`?` 플레이스홀더)을 사용한다 (문자열 포매팅으로 SQL을 조립하지 않는다 — SQL Injection 방지).
- 타입 힌트를 사용한다.

## 주의사항

- `data/app.db`는 `.gitignore`에 포함되어 있으므로 커밋되지 않는다. 스키마 자체는 코드(`connection.py`)로 재현 가능해야 한다.
- 이 repo의 스키마/영속성 방식(SQLite)은 `DataMonitor`, `DummyDataGenerator`, `SampleOrderSystem`과 설계 방향을 공유하지만, 각 repo는 독립된 저장소이므로 실제 코드/DB 파일을 공유하지 않는다.
