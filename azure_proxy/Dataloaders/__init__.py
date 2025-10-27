# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
# from functools import cache

from ..DBDefinitions import BaseModel
from ..DBDefinitions import (
    UsageModel as _UsageModel,
    ApiKeyModel as _ApiKeyModel,
    UserModel as _UserModel,
)

from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader

class LoaderMap(LoaderMapBase[BaseModel]):
    """LoaderMap is a map of IDLoaders for all models in the BaseModel registry.
    It is used to create loaders for all models in the BaseModel registry.
    """
    BaseModel = BaseModel

    UsageModel: IDLoader[_UsageModel] = None
    ApiKeyModel: IDLoader[_ApiKeyModel] = None
    UserModel: IDLoader[_UserModel] = None

    def __init__(self, session):
        super().__init__(session)

        self.UsageModel = self.get(_UsageModel)
        self.ApiKeyModel = self.get(_ApiKeyModel)
        self.UserModel = self.get(_UserModel)

        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session) -> dict[str, LoaderMap]:
    return {
        "loaders": LoaderMap(session)
    }
