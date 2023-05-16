from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

import models, schemas


async def get_items(session: AsyncSession, skip: int = 0, limit: int = 100):
    # 查询所有用户
    items = await session.execute(select(models.Item).offset(skip).limit(limit))
    data = items.scalars().all()
    return data


async def create_item(session: AsyncSession, item: schemas.ItemCreate):
    new_data = models.Item(**item.dict())
    session.add(new_data)
    # 刷新自带的主键
    await session.commit()
    # 释放这个data数据
    session.expunge(new_data)
    return new_data


async def delete_item(session: AsyncSession, id: int):
    stmt = delete(models.Item).where(models.Item.id == id)
    # 执行删除操作
    await session.execute(stmt)
    await session.commit()

    return True
