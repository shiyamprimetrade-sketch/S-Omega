# OMEGA-003

Implemented provisional HMAC request authentication, SQLite unique task claims, and authenticated immutable snapshot inserts. Six new tests cover replay, mutation, wrong key, restart, tampering and short keys. No test results verified yet. Shared secret must be provisioned securely; no key rotation, freshness window, rollback detection, workspace containment or Alpha execution adapter yet. Exact SBI-001 contract still unverified. No additional spending. Next: execute tests and implement containment.
