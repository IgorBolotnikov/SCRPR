def generate_cache_key(query):
    key = ",".join(
        [f"{key}-{str(value).lower()}" for key, value in query.items()]
    )
    return str(hash(key))
