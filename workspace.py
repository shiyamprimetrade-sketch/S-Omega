"""POSIX-only containment for a trusted root; no arbitrary execution."""
import os
import re
import stat

def read_artifact(root, task_id, limit=1048576):
    if type(limit) is not int or not 1 <= limit <= 1048576:
        raise ValueError("invalid artifact limit")
    if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", task_id):
        raise ValueError("invalid task id")
    if not hasattr(os, "O_NOFOLLOW") or os.open not in os.supports_dir_fd:
        raise NotImplementedError("secure descriptor traversal unavailable")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    rootfd = os.open(root, flags)
    try:
        taskfd = os.open(task_id, flags, dir_fd=rootfd)
        try:
            fd = os.open("compute.py", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=taskfd)
            try:
                info = os.fstat(fd)
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                    raise ValueError("not a single-link regular file")
                with os.fdopen(fd, "rb", closefd=False) as stream:
                    data = stream.read(limit + 1)
                if len(data) > limit:
                    raise ValueError("artifact too large")
                return data
            finally:
                os.close(fd)
        finally:
            os.close(taskfd)
    finally:
        os.close(rootfd)
