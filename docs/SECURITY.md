# Security notes

## Included

- PBKDF2-SHA256 password hashing with random salts and 210,000 iterations.
- Signed JWTs with expiry and purpose claims.
- Generic forgot-password response to reduce account enumeration.
- User ownership checks for view, delete, and PDF export.
- Admin dependency for platform analytics.
- CORS allowlist, upload size limit, file-extension allowlist, input validation, and database parameterization.

## Required before public production

- Replace `JWT_SECRET` with a long random secret and rotate through a secret manager.
- Serve only behind HTTPS.
- Add CSRF/state persistence appropriate to the OAuth deployment; replace the in-memory OAuth state set with Redis or a signed state token.
- Add per-IP and per-account rate limits.
- Add malware scanning and isolated temporary processing for uploads.
- Encrypt object storage, define deletion/retention policies, and avoid logging resume text.
- Connect a transactional email service; development reset tokens must never be returned in production.
- Add audit logs for admin actions and privacy request workflows.
- Run dependency, container, and static security scans in CI.
