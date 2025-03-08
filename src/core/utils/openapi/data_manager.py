import inspect
from abc import ABC, abstractmethod
from typing import Any, Callable

import polars as pl

from .data_cache import BaseDataCache
from .data_loader import BaseOpenDataLoader


async def execute(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)


class BaseDataManager(ABC):
    """
    REST API 의 데이터를 캐시하는 클래스

    Attributes:
        data (Any): 데이터
    """

    data: Any
    is_initialized: bool

    @abstractmethod
    async def init(self):
        """
        BaseDataManager 의 데이터를 초기화하는 클래스
        """
        pass

    @abstractmethod
    def register_callback(self, callback: Callable):
        """
        BaseDataManager 의 데이터의 변경을 감지해야 하는 경우 콜백 함수를 등록하여 사용할 수 있습니다.

        Args:
            callback: 콜백
        """
        pass


class PolarsDataManager(BaseDataManager):
    def __init__(
        self,
        data_loader: BaseOpenDataLoader,
        data_cache: BaseDataCache,
        path: str,
        params: dict | None = None,
        infer_scheme_length: int = 100000,
    ):
        self.data: pl.DataFrame = pl.DataFrame()
        self.is_initialized = False
        self._data_loader = data_loader
        self._data_cache = data_cache
        self._path = path
        self._params = params or {}
        self._infer_scheme_length = infer_scheme_length
        self._callbacks: list[Callable] = []

    async def init(self, reload: bool = False):
        if not reload:
            data = await self._data_cache.get_cache(self._path)
        else:
            data = None

        if data is None:
            data = await self._data_loader.get_data(self._path, self._params)
            await self._data_cache.set_cache(self._path, data)

        self.data = pl.DataFrame(data, infer_schema_length=self._infer_scheme_length)
        self.is_initialized = True
        await self._notify_callbacks()

    async def _notify_callbacks(self):
        [await execute(callback) for callback in self._callbacks]

    def register_callback(self, callback: Callable):
        self._callbacks.append(callback)
