from typing import Any

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from schemas import Response, Item, ItemCreate
from database import get_session, create_tables
from task import httpx_request
from apscheduler.triggers.cron import CronTrigger

app = FastAPI()

# 创建调度器
scheduler = AsyncIOScheduler()

# 启动调度器
scheduler.start()


# 重写Cron定时
class MyCronTrigger(CronTrigger):
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], year=values[6], timezone=timezone)


@app.on_event("startup")
async def startup_event():
    # 创建表
    await create_tables()


@app.post("/checker/", response_model=Response[Item], tags=['定时请求'])
async def create_task(item: ItemCreate, db: AsyncSession = Depends(get_session)):
    try:
        data = await crud.create_item(session=db, item=item)
        # 添加定时任务
        scheduler.add_job(httpx_request, MyCronTrigger.my_from_crontab(item.cron_expression),
                          kwargs={"url": item.url, 'return_json': False, 'method': item.method}, id=str(data.id))
        scheduler.print_jobs()
        return Response[Item](data=data)
    except Exception as e:
        return {'message': f'添加失败 {e}', 'success': False}


@app.get("/checker/", response_model=list[Item], tags=['定时请求'])
async def read_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items


@app.delete("/checker/", response_model=Response[Any], tags=['定时请求'])
async def delete_items(id: int, db: AsyncSession = Depends(get_session)):
    scheduler.remove_job(job_id=str(id))
    await crud.delete_item(db, id=id)
    return Response(data=id)


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000)
