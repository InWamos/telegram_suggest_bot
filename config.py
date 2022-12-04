bot_token = "token"
group_id = "INT!!!! Group id"

# Returns url string. Important for create_engine() 
def get_psql_url(
        username: str,
        password: str,
        host_name: str,
        port: int, 
        database_name: str) -> str:

    return f"postgresql://{username}:{password}@{host_name}:{port}/{database_name}"