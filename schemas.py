import datetime
import uuid
from enum import IntEnum
from typing import Any, TypeVar, Generic, Optional, List

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from starlette import status


class ItemBase(BaseModel):
    title: str
    url: str
    cron_expression: str
    method: str
    description: str | None = None

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int


def utc_now_timestamp():
    return int(datetime.datetime.utcnow().timestamp())


DataT = TypeVar('DataT')


class Page(BaseModel):
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=10, description="每页数据条数")


class SortDirection(IntEnum):
    desc = -1
    asc = 1


class SortParams(BaseModel):
    sort_field: str = Field(default='create_time', description='排序字段')
    sort_direction: SortDirection = Field(default=SortDirection.desc, description='排序方向，-1为倒序，1为正序')


class FilterTime(BaseModel):
    start_time: Optional[int] = Field(None, description='查询开始时间')
    end_time: Optional[int] = Field(None, description="查询结束时间")

    def to_mongodb_query(self):
        return {"$gte": self.start_time, "$lte": self.end_time}


class Response(GenericModel, Generic[DataT]):
    data: DataT | None
    message: str = 'success'
    status: int = status.HTTP_200_OK


class PageResponse(GenericModel, Generic[DataT]):
    data: List[DataT] | None
    page_size: Optional[int]
    page: Optional[int]
    total: Optional[int]
    message: str = 'success'
    status: int = status.HTTP_200_OK


class BaseResponse(BaseModel):
    data: Any
    message: str = 'success'
    status: int = 200


class ErrorResponse(BaseModel):
    data: Any
    message: str = 'failed'
    status: int = 500


class BaseCreateModel(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid1().__str__(), description='唯一ID')
    create_time: int = Field(default_factory=utc_now_timestamp, description='创建时间')
    update_time: int = Field(default_factory=utc_now_timestamp, description='更新时间')

    class Config:
        orm_mode = True


class MyBaseModel(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid1().__str__(), description='唯一ID')
    create_time: int = Field(default_factory=utc_now_timestamp, description='创建时间')
    update_time: int = Field(default_factory=utc_now_timestamp, description='更新时间')

    class Config:
        orm_mode = True
