from __future__ import (
    annotations,
)

from collections import (
    defaultdict,
)
from json import (
    JSONDecodeError,
)
from typing import (
    Any,
    Optional,
    Type,
    Union,
)
from uuid import (
    UUID,
)

from aiohttp import (
    web,
)
from cached_property import (
    cached_property,
)

from minos.common import (
    MinosImportException,
    Model,
    ModelType,
    TypeHintBuilder,
    import_module,
)

from ..requests import (
    Request,
    Response,
    ResponseException,
)


class RestRequest(Request):
    """Rest Request class."""

    def __init__(self, request: web.Request):
        self.raw_request = request

    def __eq__(self, other: RestRequest) -> bool:
        return type(self) == type(other) and self.raw_request == other.raw_request

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.raw_request!r})"

    @cached_property
    def user(self) -> Optional[UUID]:
        """
        Returns the UUID of the user making the Request.
        """
        if "User" not in self.headers:
            return None
        return UUID(self.headers["User"])

    @property
    def headers(self) -> dict[str, str]:
        """Get the headers of the request.

        :return: A dictionary in which keys are ``str`` instances and values are ``str`` instances.
        """
        # noinspection PyTypeChecker
        return self.raw_request.headers

    async def content(self, model_type: Union[ModelType, Type[Model], str] = "Content", **kwargs) -> Any:
        """Get the request content.

        :param model_type: Optional ``ModelType`` that defines the request content structure.
        :param kwargs: Additional named arguments.
        :return: The command content.
        """
        data = await self._raw_json()
        data = [(entry | self.url_args | self.path_args) for entry in data]
        data = self._build_models(data, model_type)

        if len(data) == 1:
            return data[0]
        return data

    async def _raw_json(self) -> list[dict[str, Any]]:
        try:
            data = await self.raw_request.json()
        except JSONDecodeError:
            data = dict()

        if not isinstance(data, list):
            data = [data]
        return data

    @cached_property
    def url_args(self) -> dict[str, Any]:
        """Get the url arguments as a dictionary.

        :return: A dictionary instance.
        """
        args = defaultdict(list)
        for k, v in self._raw_url_args:
            args[k].append(v)
        args = {k: v if len(v) > 1 else v[0] for k, v in args.items()}
        return args

    @property
    def _raw_url_args(self):
        return self.raw_request.rel_url.query.items()  # pragma: no cover

    @cached_property
    def path_args(self) -> dict[str, Any]:
        """Get the path arguments as a dictionary.

        :return: A dictionary instance.
        """
        args = defaultdict(list)
        for k, v in self._raw_path_args:
            args[k].append(v)
        args = {k: v if len(v) > 1 else v[0] for k, v in args.items()}
        return args

    @property
    def _raw_path_args(self):
        return self.raw_request.match_info.items()  # pragma: no cover

    def _build_models(self, data: list[dict[str, Any]], model_type: Union[ModelType, Type[Model], str]) -> list[Model]:
        return [self._build_one_model(entry, model_type) for entry in data]

    @staticmethod
    def _build_one_model(entry: dict[str, Any], model_type: Union[ModelType, Type[Model], str]) -> Model:
        if isinstance(model_type, str):
            try:
                model_type = import_module(model_type)
            except MinosImportException:
                type_hints = {k: TypeHintBuilder(v).build() for k, v in entry.items()}
                model_type = ModelType.build(model_type, type_hints)

        return model_type(**entry)


class RestResponse(Response):
    """Rest Response class."""


class RestResponseException(ResponseException):
    """Rest Response Exception class."""
