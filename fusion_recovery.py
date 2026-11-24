"""Recover terminal results from the trusted local journal."""
from journal import Journal
from transactional import verify_record
from omega import proof

def recover_result(database, ident, key):
    status,evidence=Journal(database).get(ident)
    if status!="completed" or not verify_record(ident,status,evidence,key):
        raise ValueError("no authenticated completed result")
    record=evidence["record"]
    if "result" not in record or proof(record["result"])!=record.get("result_digest"):
        raise ValueError("missing or inconsistent result")
    return record["result"]
