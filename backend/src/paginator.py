import logging
from typing import List, Optional

from fastapi import Depends, Query, Request
from furl import furl
from pydantic import BaseModel, create_model

logger = logging.getLogger(__name__)


class Parameters(BaseModel):
    offset: int = Query(0, ge=0)
    limit: int = Query(50, gt=0, le=1000)


def Paginate(example):
    model_name = f"Paginated{example.__name__}"
    model = create_model(
        model_name,
        previous=(Optional[str], ...),
        self=(Optional[str], ...),
        next=(Optional[str], ...),
        count=(int, ...),
        results=(List[example], ...),
    )
    return model


class Page:
    def __init__(
        self,
        request: Request,
        parameters: Parameters = Depends(Parameters),
    ):
        self.request = request
        self.limit: int = parameters.limit
        self.offset: int = parameters.offset

    def __str__(self) -> str:
        return f"Page offset: {self.offset} limit: {self.limit}"

    def _create_link(self, parameters: Parameters) -> str:
        query_url = furl(self.request.url)
        query_url.args["limit"] = parameters.limit
        query_url.args["offset"] = parameters.offset
        return query_url.url

    def build(self, results: List, total_results: int):
        previous_url: Optional[str] = None
        self_url: Optional[str] = None
        next_url: Optional[str] = None

        previous_offset: int = (
            max(0, self.offset - self.limit)
            if self.offset < total_results
            else max(0, total_results - self.limit)
        )

        previous_url_params = Parameters(limit=self.limit, offset=previous_offset)
        previous_url = (
            self._create_link(parameters=previous_url_params)
            if self.offset > 0
            else None
        )

        self_url = self._create_link(
            parameters=Parameters(limit=self.limit, offset=self.offset)
        )

        next_url = (
            self._create_link(
                parameters=Parameters(limit=self.limit, offset=self.offset + self.limit)
            )
            if self.offset + self.limit < total_results
            else None
        )

        return {
            "previous": previous_url,
            "self": self_url,
            "next": next_url,
            "count": total_results,
            "results": results,
        }
