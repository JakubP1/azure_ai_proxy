import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
)

from .BaseGQLModel import BaseGQLModel


@strawberry.federation.type(
    description="""Entity representing an usage of the API key"""
)
class UsageGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return info.context["loaders"].UsageModel

    ts: str | None = strawberry.field(
        description="Timestamp of the usage",
        permission_classes=[OnlyForAuthentized],
    )
    stream: bool | None = strawberry.field(
        description="Whether the response was streamed",
        permission_classes=[OnlyForAuthentized],
    )
    route: str | None = strawberry.field(
        description="API route used in this usage",
        permission_classes=[OnlyForAuthentized],
    )
    deployment: str | None = strawberry.field(
        description="Deployment used in this usage",
        permission_classes=[OnlyForAuthentized],
    )
    status: int | None = strawberry.field(
        description="HTTP status code of the response",
        permission_classes=[OnlyForAuthentized],
    )
    prompt_tokens: int | None = strawberry.field(
        description="Number of prompt tokens used",
        permission_classes=[OnlyForAuthentized],
    )
    completion_tokens: int | None = strawberry.field(
        description="Number of completion tokens used",
        permission_classes=[OnlyForAuthentized],
    )
    total_tokens: int | None = strawberry.field(
        description="Total number of tokens used",
        permission_classes=[OnlyForAuthentized],
    )
    stream_bytes: int | None = strawberry.field(
        description="Number of bytes streamed",
        permission_classes=[OnlyForAuthentized],
    )
    cost_usd: float | None = strawberry.field(
        description="Cost in USD for this usage",
        permission_classes=[OnlyForAuthentized],
    )
    meta_json: str | None = strawberry.field(
        description="Additional metadata in JSON format",
        permission_classes=[OnlyForAuthentized],
    )