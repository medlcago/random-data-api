from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import config

engine = create_async_engine(url=config.database.construct_sqlalchemy_url())
async_session_maker = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)