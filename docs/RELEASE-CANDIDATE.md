# Omega release candidate

Run `python -m unittest discover -s tests -v`, `python acceptance.py`, `python benchmark.py`, and `python alpha_acceptance.py /path/to/trusted/S-Alpha` on POSIX. Android instructions: ANDROID.md. Supported interface: api.py. Use a fresh dedicated database and independently protected random 32-byte key. Do not mix legacy adapters.

Verified integration run 45459185809: Alpha commit f4976e3d5ef39d9c75a24a1c5460ce162e77170b, 12/12 Alpha cases, 48-byte artifact, matching SHA-256 f80d90fa9ee901703a5841268830e7e4c2a8c67c781faf60f0fee767a96f68fc, authenticated and persisted true. Omega acceptance CI run 45459085340 succeeded. New pinned integration and benchmark execution pending.

Scope: local trusted prototype, not a sandbox or independent semantic proof. POSIX artifact containment only. Offline recovery requires exclusive ownership; external anchors require independent storage. No production key management or full rollback defense. Physical Android and original SBI/SCC conformance pending. No license granted. No additional spending.
