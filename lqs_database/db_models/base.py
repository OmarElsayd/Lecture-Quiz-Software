from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


metadata = MetaData(schema="lqs")
Base = declarative_base(metadata=metadata)
