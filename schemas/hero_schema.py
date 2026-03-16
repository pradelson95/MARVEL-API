from pydantic import BaseModel


class HeroBase(BaseModel):
    """
    Campos base de un héroe
    """
    name: str
    real_name: str | None = None
    team: str | None = None
    power_level: int | None = None
    image_url: str | None = None


class HeroCreate(HeroBase):
    """
    Esquema para crear un héroe
    """
    pass


class HeroResponse(HeroBase):
    """
    Esquema de respuesta de la API
    """
    id: int

    class Config:
        from_attributes = True