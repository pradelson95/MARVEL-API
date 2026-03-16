from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.hero import Hero
from schemas.hero_schema import HeroCreate, HeroResponse


router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.post("/", response_model=HeroResponse)
def create_hero(hero: HeroCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo héroe
    """

    new_hero = Hero(**hero.model_dump())

    db.add(new_hero)
    db.commit()
    db.refresh(new_hero)

    return new_hero


@router.get("/", response_model=list[HeroResponse])
def get_heroes(db: Session = Depends(get_db)):
    heroes = db.query(Hero).all()
    return heroes


@router.get("/{hero_id}", response_model=HeroResponse)
def get_hero(hero_id: int, db: Session = Depends(get_db)):

    hero = db.query(Hero).filter(Hero.id == hero_id).first()

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    return hero


@router.delete("/{hero_id}")
def delete_hero(hero_id: int, db: Session = Depends(get_db)):

    hero = db.query(Hero).filter(Hero.id == hero_id).first()

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    db.delete(hero)
    db.commit()

    return {"message": f"Hero {hero.name} deleted"}


# Actualizar un héroe con patch
@router.patch("/{hero_id}", response_model=HeroResponse)
def update_hero(hero_id: int, hero: HeroCreate, db: Session = Depends(get_db)):

    existing_hero = db.query(Hero).filter(Hero.id == hero_id).first()

    if not existing_hero:
        raise HTTPException(status_code=404, detail=f"Hero {hero_id} not found")
    # Actualizar solo los campos que se han proporcionado en el request
    for key, value in hero.model_dump().items():
        setattr(existing_hero, key, value)

    db.commit()
    db.refresh(existing_hero)

    return existing_hero