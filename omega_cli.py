"""Offline desktop preview commands."""
import argparse
import json
from pathlib import Path
from omega import proof
from semantic import verify_source

def main():
    parser=argparse.ArgumentParser(description="S-Omega developer preview")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    p=sub.add_parser("fingerprint")
    p.add_argument("json_file",type=Path)
    p=sub.add_parser("verify")
    p.add_argument("spec",type=Path)
    p.add_argument("source",type=Path)
    args=parser.parse_args()
    if args.command=="doctor":
        import os
        import sys
        print(json.dumps({"python":sys.version.split()[0],"platform":sys.platform,"descriptor_containment":hasattr(os,"O_NOFOLLOW") and os.open in os.supports_dir_fd}))
        return 0
    if args.command=="fingerprint":
        print(proof(json.loads(args.json_file.read_text(encoding="utf-8"))))
        return 0
    with args.source.open("rb") as stream:
        source=stream.read(16385)
    valid=verify_source(json.loads(args.spec.read_text(encoding="utf-8")),source)
    print(json.dumps({"verified":valid}))
    return 0 if valid else 1

if __name__=="__main__":
    raise SystemExit(main())
