# Contributing Guide

Thank you for your interest in improving this project! This repository supports a data analytics stack with **MySQL** (telemetry store) and **Power BI** (dashboards). Below are guidelines to help you contribute effectively and safely.

## Table of Contents
- [Project Goals](#project-goals)
- [Architecture Overview](#architecture-overview)
- [Development Setup](#development-setup)
- [Branching and Workflow](#branching-and-workflow)
- [Coding Standards](#coding-standards)
- [Database Guidelines](#database-guidelines)
- [Testing](#testing)
- [Data Handling & Security](#data-handling--security)
- [Power BI Practices](#power-bi-practices)
- [Commit Messages & PRs](#commit-messages--prs)
- [Release Process](#release-process)
- [Getting Help](#getting-help)

## Project Goals
- Centralize metrics for automation & integration performance.
- Track failures and error rates for **update**, **collection**, and **integration** processes.
- Provide reliable data models and clear, actionable Power BI visuals for operations and engineering.

## Architecture Overview
- **Ingestion/ETL:** Python-based jobs (or your runner of choice) load raw telemetry into staging tables, validate, then upsert into fact and dimension tables.
- **Storage:** MySQL schema with `staging_*`, `dim_*`, `fact_*`, and `mart_*` layers.
- **Analytics:** Power BI model connects to `mart_*` views for curated, versioned semantics.
- **Ops:** Makefile targets orchestrate local DB, migrations, linting, and tests.

## Development Setup
1. **Prerequisites**
   - Python ≥ 3.10
   - Make, Docker, Docker Compose (optional but recommended)
   - MySQL ≥ 8.0
   - Power BI Desktop (for report development)

2. **Bootstrap**
   ```bash
   make setup        # create .venv, install dev dependencies
   make db.up        # start local MySQL via Docker (or configure DB_* env vars)
   make db.migrate   # run SQL migrations
   make test         # run unit tests

3. **Environment**
- Create .env from .env.example (if present) and set:

    ```ini
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=analytics
    DB_PASSWORD=change_me
    DB_NAME=automation_perf
    ```

## Branching and Workflow
- Main is always deployable. Use feature branches:

    - feat/<slug>, fix/<slug>, chore/<slug>, docs/<slug>, data/<slug>

- Open a PR early for visibility. Use draft PRs for WIP.

- Rebase or use “Squash & Merge”; keep history tidy.

## Coding Standards
- Python: PEP 8, type hints, black (88), isort, flake8/mypy.

- SQL: Lowercase keywords, snake_case identifiers, idempotent migrations.

- Docs: Update README/diagrams when architecture or models change.

## Database Guidelines
- Use time-based partitioning for large facts if needed.

- Prefer surrogate keys in dimensions and natural keys as constraints when valid.

- All tables must have:

    - created_at, updated_at (TIMESTAMP)

    - record_source (VARCHAR) if sourced from multiple systems

- Add indexes for common filters: `occurred_at`, `status`, `integration_id`, `automation_id`.

- Provide views in mart_* with business-friendly names and definitions.

## Testing
- Unit test ETL functions and data contracts.

- Add data quality checks (row counts, null ratios, referential integrity).

- Use ephemeral schemas for tests (or transaction rollbacks).

## Data Handling & Security
- Do not commit secrets. Use .env and secret stores.

- Anonymize PII for non-production.

- Apply principle of least privilege to DB users.

## Power BI Practices
- Build a star schema (facts + conformed dimensions).

- Use mart_* views as the only Power BI sources.

- Document measures (DAX) and business logic in the report and /docs.

- For refresh:

    - Configure a gateway (if needed).

    - Prefer Import for curated marts, DirectQuery only for low-latency needs.

- Version PBIX files using exported PBIT templates or Power BI Project (if available) to minimize binary diffs.

## Commit Messages & PRs
- Conventional Commits:

    - feat: add failure-rate mart view

    - fix: correct null handling in staging load

- PR template should include: scope, screenshots of PBIX changes (where possible), roll-out plan.

## Release Process
- Update .changelog.md.

- Tag version vX.Y.Z.

- Publish release notes. Share dashboard changes and migration steps.

## Getting Help
- File an issue with labels: bug, enhancement, question, data-model, powerbi.

- For security incidents, email gabriel.santos@mvprec.com.br