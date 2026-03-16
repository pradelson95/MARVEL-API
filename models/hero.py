from sqlalchemy import Column, Integer, String
from app.database import Base


class Hero(Base):
    __tablename__ = "heroes"

    # ID único del héroe
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    real_name = Column(String)
    # Equipo (Avengers, X-Men, etc.)
    team = Column(String)
    # Nivel de poder
    power_level = Column(Integer)
    # URL de la imagen del héroe
    image_url = Column(String)