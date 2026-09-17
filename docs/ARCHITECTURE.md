# Architecture

## Runtime boundaries

- **Frontend:** React + TypeScript + Tailwind CSS + Framer Motion + Recharts.
- **Backend:** FastAPI with synchronous SQLAlchemy sessions.
- **Database:** SQLite for zero-configuration local development; PostgreSQL through `DATABASE_URL` for deployed environments.
- **Authentication:** PBKDF2-SHA256 password hashing, signed JWT access tokens, optional Google OAuth, and 15-minute password-reset tokens.
- **Analysis:** file parser → text normalization → classifier → ATS engine → JD matcher → skill-gap engine → recommendations → report renderer.
- **Reports:** ReportLab PDF generated on demand from stored analysis JSON.

## Classification modes

1. **Supervised model**: used automatically when a valid Joblib bundle exists at `MODEL_PATH`. The training command produces accuracy, macro-F1, weighted-F1, per-class metrics, and a held-out report.
2. **Taxonomy baseline**: transparent fallback based on TF-IDF semantic similarity, explicit skill evidence, target-role boosting, and normalized relative confidence.

The fallback keeps the application functional without a proprietary dataset. It is not a substitute for production validation.

## Scaling path

- 100 users: one API instance, SQLite or small PostgreSQL, local reports.
- 1,000 users: PostgreSQL, object storage for reports, reverse proxy, managed TLS.
- 10,000 users: multiple stateless API instances, Redis rate limits/cache, background job queue for parsing and PDF rendering.
- 100,000 users: autoscaling workers, event-driven analysis pipeline, model service separated from API, observability, data retention controls, regional storage, model registry, and drift monitoring.

## Suggested production additions

- Alembic migrations.
- S3-compatible object storage and signed report URLs.
- Celery/RQ/Arq workers for long analyses.
- Redis rate limiting and idempotency keys.
- Stripe billing and webhook validation.
- Transactional email provider for password resets.
- Malware scanning and encrypted temporary uploads.
- OpenTelemetry traces, structured logs, Sentry, and metrics dashboards.
