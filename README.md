# S-Omega — v0.1 release candidate

Local Python 3.11+ prototype of S-Proof (artifact integrity), S-Guardian (authenticated requests), and S-Continuum (persistent task journal and offline recovery). Standard library only.

## Quick start
On supported POSIX hosts:
```sh
python -m unittest discover -s tests -v
python acceptance.py
python benchmark.py
```
Android: [Termux instructions](docs/ANDROID.md). Windows supports portable primitives, not secure artifact traversal.

## Integration
Use trusted S-Alpha commit f4976e3d5ef39d9c75a24a1c5460ce162e77170b.
```sh
python alpha_acceptance.py /path/to/S-Alpha
```
Supported interface: api.py; fresh dedicated database required. Legacy adapters are historical only.

## Evidence and limitations
[Release candidate](docs/RELEASE-CANDIDATE.md) | [Engineering checkpoints](checkpoints/) | [Verification PR](https://github.com/shiyamprimetrade-sketch/S-Omega/pull/1).
Previous integration verified 12/12 Alpha cases, matching artifact hashes, authenticated persistent evidence. Final pinned CI and physical Android acceptance must be verified before final approval. Not a production security boundary, sandbox or independent semantic proof. External anchors require independent trusted storage. No license granted by this README. No secrets or unpublished patent material in public repository.
