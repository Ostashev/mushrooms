from fastapi import FastAPI, HTTPException
from app.models import Mushroom, MushroomCreate, Basket, BasketCreate, BasketAddMushroom
from app.data import (
    create_mushroom,
    get_mushroom,
    update_mushroom,
    create_basket,
    get_basket,
    add_mushroom_to_basket,
    remove_mushroom_from_basket,
)

app = FastAPI()


@app.post("/mushrooms/", response_model=Mushroom)
async def create_new_mushroom(mushroom: MushroomCreate):
    return await create_mushroom(mushroom)


@app.put("/mushrooms/{mushroom_id}", response_model=Mushroom)
async def update_existing_mushroom(mushroom_id: int, mushroom: MushroomCreate):
    try:
        return await update_mushroom(mushroom_id, mushroom)
    except KeyError:
        raise HTTPException(status_code=404, detail="Mushroom not found")


@app.get("/mushrooms/{mushroom_id}", response_model=Mushroom)
async def read_mushroom(mushroom_id: int):
    try:
        return await get_mushroom(mushroom_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Mushroom not found")


@app.post("/baskets/", response_model=Basket)
async def create_new_basket(basket: BasketCreate):
    return await create_basket(basket)


@app.post("/baskets/{basket_id}/add_mushroom", response_model=Basket)
async def add_mushroom_to_basket_handler(basket_id: int, data: BasketAddMushroom):
    try:
        return await add_mushroom_to_basket(basket_id, data.mushroom_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/baskets/{basket_id}/remove_mushroom/{mushroom_id}", response_model=Basket)
async def remove_mushroom_from_basket_handler(basket_id: int, mushroom_id: int):
    try:
        return await remove_mushroom_from_basket(basket_id, mushroom_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/baskets/{basket_id}", response_model=Basket)
async def read_basket(basket_id: int):
    try:
        return await get_basket(basket_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Basket not found")
