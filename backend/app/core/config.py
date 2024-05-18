from dataclasses import dataclass

from environs import Env


@dataclass
class TokenConfig:
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int

    @staticmethod
    def from_env(env: Env) -> "TokenConfig":
        algorithm = env.str("ALGORITHM", "HS256")
        secret_key = env.str("SECRET_KEY")
        access_token_expire_minutes = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8)
        return TokenConfig(
            algorithm=algorithm,
            secret_key=secret_key,
            access_token_expire_minutes=access_token_expire_minutes
        )


@dataclass
class ApiConfig:
    project_name: str
    users_open_registration: bool
    api_v1_str: str
    domain: str
    port: int

    @staticmethod
    def from_env(env: Env) -> "ApiConfig":
        project_name = env.str("PROJECT_NAME", "Random Data API")
        api_v1_str = env.str("API_V1_STR", "/api/v1")
        domain = env.str("DOMAIN", "localhost")
        port = env.int("PORT", 8080)
        return ApiConfig(
            project_name=project_name,
            users_open_registration=True,
            api_v1_str=api_v1_str,
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
