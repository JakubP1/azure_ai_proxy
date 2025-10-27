from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import MappedAsDataclass

class BaseModel(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""

