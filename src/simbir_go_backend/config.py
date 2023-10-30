import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432

    password = os.environ.get("DB_PASSWORD", "sOm_e_dum8_p*ssw0|^d")
    user, db_name = "simbir_go", "simbir_go"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_secret_key():
    return "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


def get_token_expire_minutes():
    return 30


def get_algorithm():
    return "HS256"
