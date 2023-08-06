from __future__ import (
    annotations,
)

from abc import (
    ABC,
    abstractmethod,
)
from inspect import (
    iscoroutinefunction,
)
from typing import (
    Awaitable,
    Callable,
    Final,
    Iterable,
    Optional,
    Union,
)

from ...exceptions import (
    MinosMultipleEnrouteDecoratorKindsException,
)
from ...requests import (
    Request,
    Response,
)
from .kinds import (
    EnrouteDecoratorKind,
)

Adapter = Callable[[Request], Union[Optional[Response], Awaitable[Optional[Response]]]]


class EnrouteDecorator(ABC):
    """Base Decorator class."""

    # noinspection PyFinal
    KIND: Final[EnrouteDecoratorKind]

    def __call__(self, fn: Adapter) -> Adapter:
        if iscoroutinefunction(fn):

            async def _wrapper(*args, **kwargs) -> Optional[Response]:
                return await fn(*args, **kwargs)

        else:

            def _wrapper(*args, **kwargs) -> Optional[Response]:
                return fn(*args, **kwargs)

        _wrapper.__decorators__ = getattr(fn, "__decorators__", set())
        _wrapper.__decorators__.add(self)
        kinds = set(decorator.KIND for decorator in _wrapper.__decorators__)
        if len(kinds) > 1:
            raise MinosMultipleEnrouteDecoratorKindsException(
                f"There are multiple kinds but only one is allowed: {kinds}"
            )
        _wrapper.__base_func__ = getattr(fn, "__base_func__", fn)

        return _wrapper

    def __repr__(self):
        args = ", ".join(map(repr, self))
        return f"{type(self).__name__}({args})"

    def __eq__(self, other: EnrouteDecorator) -> bool:
        return type(self) == type(other) and tuple(self) == tuple(other)

    def __hash__(self) -> int:
        return hash(tuple(self))

    @abstractmethod
    def __iter__(self) -> Iterable:
        raise NotImplementedError

    @property
    def pre_fn_name(self) -> str:
        """Get the pre execution function name.

        :return: A string value containing the function name.
        """
        return self.KIND.pre_fn_name

    @property
    def post_fn_name(self) -> str:
        """Get the post execution function name.

        :return: A string value containing the function name.
        """
        return self.KIND.post_fn_name
