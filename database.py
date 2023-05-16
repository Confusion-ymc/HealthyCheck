from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/sql_app.db"
from sqlalchemy.ext.asyncio import create_async_engine

# 创建异步SQLite连接
engine = create_async_engine('sqlite+aiosqlite:///./database/sql_app.db', echo=True, future=True)

# 创建异步会话工厂
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


# 创建表的异步函数
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
