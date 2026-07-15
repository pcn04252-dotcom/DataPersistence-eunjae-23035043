# DataPersistence

SQLite 기반 데이터 영속성 및 CRUD 구조를 검증하기 위한 PoC 프로젝트입니다.

- 언어: Python (`sqlite3` 표준 라이브러리)
- 상태: 구현 완료 (Item CRUD 데모)
- 상세 계획: [`PLAN.md`](./PLAN.md), 세션 참고 문서: [`CLAUDE.md`](./CLAUDE.md)

## 실행 방법

```
python -m src.main
```

`data/app.db`에 데이터가 저장되며, 다시 실행해도 이전 데이터가 유지됩니다.

## 테스트 방법

```
pip install -r requirements-dev.txt
pytest
```

## 검증한 것

- `sqlite3` 표준 라이브러리만으로 CRUD(생성/조회/수정/삭제) 전체 구현
- 프로세스를 재시작해도 데이터가 유지되는지 수동 검증 완료
- `:memory:` DB를 이용한 격리된 단위 테스트 5종 통과
