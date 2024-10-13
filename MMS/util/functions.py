# =====================================================================
import hashlib
from math import floor

# =====================================================================


def sha(input_string, bits=256):
    sha256_hash = hashlib.sha256(input_string.encode()).digest()
    _bytes = floor(bits / 8)
    sha_digest = sha256_hash[:_bytes]
    return sha_digest.hex()
