from dataclasses import dataclass, field

from environs import Env

BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:3000"
]


@dataclass
class TokenConfig:
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    @staticmethod
    def from_env(env: Env) -> "TokenConfig":
        algorithm = env.str("ALGORITHM", "HS256")
        secret_key = env.str("SECRET_KEY")
        # 60 * 24 = 1 day lifetime of access token
        access_token_expire_minutes = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24)
        # 60 * 24 * 30 = 30 days lifetime of refresh token
        refresh_token_expire_minutes = env.int("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 30)
        return TokenConfig(
            algorithm=algorithm,
            secret_key=secret_key,
            access_token_expire_minutes=access_token_expire_minutes,
            refresh_token_expire_minutes=refresh_token_expire_minutes
        )


@dataclass
class ApiConfig:
    project_name: str
    users_open_registration: bool
    api_v1_str: str
    api_v1_docs_url: str
    domain: str
    port: int
    backend_cors_origins: list[str] = field(default_factory=lambda: BACKEND_CORS_ORIGINS)

    @staticmethod
    def from_env(env: Env) -> "ApiConfig":
        project_name = env.str("PROJECT_NAME", "Random Data API")
        api_v1_str = env.str("API_V1_STR", "/api/v1")
        api_v1_docs_url = env.str("API_V1_DOCS_URL", "/api/v1/docs")
        domain = env.str("DOMAIN", "localhost")
        port = env.int("PORT", 8080)
        return ApiConfig(
            project_name=project_name,
            users_open_registration=True,
            api_v1_str=api_v1_str,
            api_v1_docs_url=api_v1_docs_url,
            domain=domain,
            port=port
        )


@dataclass
class DatabaseConfig:
    host: str
    password: str
    user: str
    database: str
    port: int

    def construct_sqlalchemy_url(self, driver="asyncpg") -> str:
        from sqlalchemy.engine.url import URL

        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env) -> "DatabaseConfig":
        host = env.str("PG_HOST")
        password = env.str("PG_PASSWORD")
        user = env.str("PG_USER")
        database = env.str("PG_DB")
        port = env.int("PG_PORT", 5432)
        return DatabaseConfig(
            host=host,
            password=password,
            user=user,
            database=database,
            port=port
        )


@dataclass
class Config:
    jwt: TokenConfig
    api: ApiConfig
    database: DatabaseConfig


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path=path)

    return Config(
        jwt=TokenConfig.from_env(env=env),
        api=ApiConfig.from_env(env=env),
        database=DatabaseConfig.from_env(env=env)
    )


config = load_config(path=".env")
