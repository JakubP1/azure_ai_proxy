import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
)

from .BaseGQLModel import BaseGQLModel


@strawberry.federation.type(
    description="""Entity representing an API key"""    
)
class ApiKeyGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return info.context["loaders"].ApiKeyModel
    
    user_id: strawberry.ID | None = strawberry.field(
        description="ID of the user owning this API key",
        permission_classes=[OnlyForAuthentized],
    )
    prefix: str | None = strawberry.field(
        description="Prefix of the API key",
        permission_classes=[OnlyForAuthentized],
    )
    name: str | None = strawberry.field(
        description="Name of the API key",
        permission_classes=[OnlyForAuthentized],
    )
    is_active: bool = strawberry.field(
        description="Whether the API key is active",
        permission_classes=[OnlyForAuthentized],
    )
    created_at: str = strawberry.field(
        description="Creation timestamp of the API key",
        permission_classes=[OnlyForAuthentized],
    )
    expires_at: str | None = strawberry.field(
        description="Expiration timestamp of the API key, if any",
        permission_classes=[OnlyForAuthentized],
    )
    rate_limit_per_minute: int | None = strawberry.field(
        description="Rate limit per minute for this API key, if any",
        permission_classes=[OnlyForAuthentized],
    )
    last_used_at: str | None = strawberry.field(
        description="Last used timestamp of the API key, if any",
        permission_classes=[OnlyForAuthentized],
    )
