class SingletonMeta(type):
    _members ={}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._members:
            cls._members[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._members[cls]

# From Django (mostly):
def force_bytes(s, encoding="utf-8", strings_only=False, errors="strict"):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(s, bytes):
        if encoding == "utf-8":
            return s
        else:
            return s.decode("utf-8", errors).encode(encoding, errors)

    if isinstance(s, memoryview):
        return bytes(s)
    return str(s).encode(encoding, errors)

def constant_time_compare(val1, val2):
    import secrets
    """Return True if the two strings are equal, False otherwise."""
    return secrets.compare_digest(force_bytes(val1), force_bytes(val2))