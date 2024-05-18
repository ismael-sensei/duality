from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class CharacterModel(Base):
    __tablename__ = 'characters'
    
    id: int = mapped_column(default=None, metadata={"sa": Column(Integer, primary_key=True)})
    name: str = field(default="", metadata={"sa": Column(String)})
    level: int = field(default=1, metadata={"sa": Column(Integer)})

# Setup de SQLAlchemy
engine = create_engine('postgresql://user:password@localhost/mydatabase')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)