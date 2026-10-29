# Malaysia Fuel Price ELT Pipeline

A batch ELT pipeline that pulls weekly Malaysian fuel prices from data.gov.my,
loads them into Postgres, and transforms them with dbt.

## Status
- [x] Phase 0: Project setup
- [x] Phase 1: Extract + Load
- [ ] Phase 2: dbt transformations
- [ ] Phase 3: Tests
- [ ] Phase 4: Dashboard
- [ ] Phase 5: Airflow scheduling
- [ ] Phase 6: Docs + CI

## Known data quirks
- ~16 weeks missing between 2017-03-30 and 2026-10-29 (485 of ~501 expected weeks). To investigate.
- `change_weekly` rows use the same columns as prices; always filter by `series_type`.
- Diesel split into Peninsular/East Malaysia from June 2024.