from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from pyobs.utils.threads import Future
from .interfaceproxy import InterfaceProxy


class IBinningProxy(InterfaceProxy):
    __module__ = 'pyobs.interfaces.proxies'

    def get_binning(self) -> 'Future[typing.Tuple[int, int]]':
        ...

    def list_binnings(self) -> 'Future[typing.List[typing.Tuple[int, int]]]':
        ...

    def set_binning(self, x: int, y: int) -> 'Future[None]':
        ...

