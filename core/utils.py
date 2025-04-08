from datetime import datetime, timezone
from zlib import adler32


def gen_time_hash() -> str:
    current_utc_time = datetime.now(timezone.utc).isoformat()
    time_bytes = current_utc_time.encode("utf-8")
    adler32_hash = adler32(time_bytes)
    return hex(adler32_hash & 0xFFFFFFFF)[2:]
