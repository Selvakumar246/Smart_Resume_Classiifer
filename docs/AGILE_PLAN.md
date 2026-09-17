# Agile delivery plan

## Product backlog themes

- Identity and trust
- Resume ingestion
- Classification quality
- ATS transparency
- Job-description alignment
- Career action plan
- Reporting and history
- Recruiter workflow
- Billing and entitlements
- Platform operations

## Sprint 1 — Foundation

**User stories:** As a visitor, I can understand the value proposition. As a user, I can register, sign in, remember my session, reset my password locally, and switch theme.

**Acceptance:** responsive landing and auth; protected routes; JWT validation; accessible focus states; error handling.

## Sprint 2 — Resume ingestion

**User stories:** I can drag and drop PDF, DOCX, or TXT; invalid files are rejected; readable text and contact details are extracted.

**Acceptance:** file-size limit, MIME/extension checks, parser errors, no analysis created for unreadable content.

## Sprint 3 — Classification

**User stories:** I receive five ranked domains, confidence values, evidence, and an explanation.

**Acceptance:** deterministic baseline; supervised artifact support; holdout metrics saved during training; no unsupported accuracy claim.

## Sprint 4 — ATS engine

**User stories:** I see overall and component scores with specific deductions.

**Acceptance:** formatting, keywords, skills, projects, experience, education, grammar, and section completeness are returned.

## Sprint 5 — JD matching

**User stories:** I can paste a job description and see semantic similarity, matched terms, missing terms, soft-skill gaps, and actions.

**Acceptance:** empty JD is handled; score is bounded 0–100; gaps are deduplicated.

## Sprint 6 — Dashboard and history

**User stories:** I can see recent reports, ATS trend, top direction, search history, reopen, and delete.

**Acceptance:** user isolation at every endpoint; free-plan monthly limit; responsive charts and tables.

## Sprint 7 — Reports and career preparation

**User stories:** I can export a PDF, review skill roadmaps, improved bullet structures, career projects, and interview questions.

**Acceptance:** PDF opens correctly; placeholders never invent achievements; salary is not guessed without current market context.

## Sprint 8 — Quality and deployment

**Stories:** Docker deployment, PostgreSQL, health checks, PWA metadata, backend tests, security review, performance budgets, and observability plan.

## Review and retrospective prompts

- Which recommendation changed a user action?
- Where did parsing fail?
- Which categories have low recall or class imbalance?
- Are scores understandable and calibrated?
- What should be removed because it does not support classification?
