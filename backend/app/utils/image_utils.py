import hashlib

def get_image_hash(image_bytes: bytes) -> str:
    """
    Generates a SHA-256 hash for the given image bytes.
    Used for caching prediction results.
    """
    return hashlib.sha256(image_bytes).hexdigest()
