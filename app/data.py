from typing import Dict
from app.models import Mushroom, MushroomCreate, Basket, BasketCreate
import asyncio

mushrooms_db: Dict[int, Mushroom] = {}
baskets_db: Dict[int, Basket] = {}

mushroom_id_counter = 1
basket_id_counter = 1
db_lock = asyncio.Lock()


async def create_mushroom(mushroom: MushroomCreate) -> Mushroom:
    global mushroom_id_counter

    async with db_lock:
        mushroom_id = mushroom_id_counter
        mushroom_id_counter += 1

        new_mushroom = Mushroom(
            id=mushroom_id,
            **mushroom.dict()
        )

        mushrooms_db[mushroom_id] = new_mushroom
        return new_mushroom


async def get_mushroom(mushroom_id: int) -> Mushroom:
    async with db_lock:
        return mushrooms_db[mushroom_id]


async def update_mushroom(mushroom_id: int, mushroom: MushroomCreate) -> Mushroom:
    async with db_lock:
        if mushroom_id not in mushrooms_db:
            raise KeyError("Mushroom not found")

        updated_mushroom = Mushroom(
            id=mushroom_id,
            **mushroom.dict()
        )

        mushrooms_db[mushroom_id] = updated_mushroom
        return updated_mushroom


async def create_basket(basket: BasketCreate) -> Basket:
    global basket_id_counter

    async with db_lock:
        basket_id = basket_id_counter
        basket_id_counter += 1

        new_basket = Basket(
            id=basket_id,
            **basket.dict(),
            mushrooms=[]
        )

        baskets_db[basket_id] = new_basket
        return new_basket


async def get_basket(basket_id: int) -> Basket:
    async with db_lock:
        basket = baskets_db[basket_id]

        detailed_mushrooms = []
        current_weight = 0

        for mushroom_id in [m.id for m in basket.mushrooms]:
            try:
                mushroom = mushrooms_db[mushroom_id]
                detailed_mushrooms.append(mushroom)
                current_weight += mushroom.weight
            except KeyError:
                continue

        if current_weight > basket.capacity:
            raise ValueError(f"Basket is over capacity: {current_weight}/{basket.capacity}g")

        return Basket(
            id=basket.id,
            owner=basket.owner,
            capacity=basket.capacity,
            mushrooms=detailed_mushrooms
        )


async def add_mushroom_to_basket(basket_id: int, mushroom_id: int) -> Basket:
    async with db_lock:
        if basket_id not in baskets_db:
            raise KeyError(f"Basket with id {basket_id} not found")

        if mushroom_id not in mushrooms_db:
            raise KeyError(f"Mushroom with id {mushroom_id} not found")

        basket = baskets_db[basket_id]
        mushroom = mushrooms_db[mushroom_id]

        if any(m.id == mushroom_id for m in basket.mushrooms):
            raise ValueError("Mushroom already in this basket")

        current_weight = sum(m.weight for m in basket.mushrooms)
        if current_weight + mushroom.weight > basket.capacity:
            raise ValueError(
                f"Cannot add mushroom. Basket capacity exceeded: "
                f"{current_weight + mushroom.weight}g > {basket.capacity}g"
            )

        basket.mushrooms.append(mushroom)

        return Basket(
            id=basket.id,
            owner=basket.owner,
            capacity=basket.capacity,
            mushrooms=basket.mushrooms.copy()
        )


async def remove_mushroom_from_basket(basket_id: int, mushroom_id: int) -> Basket:
    async with db_lock:
        if basket_id not in baskets_db:
            raise KeyError("Basket not found")

        basket = baskets_db[basket_id]

        found_index = None
        for i, mushroom in enumerate(basket.mushrooms):
            if mushroom.id == mushroom_id:
                found_index = i
                break

        if found_index is None:
            raise ValueError("Mushroom not found in basket")

        del basket.mushrooms[found_index]

        return Basket(
            id=basket.id,
            owner=basket.owner,
            capacity=basket.capacity,
            mushrooms=[m for m in basket.mushrooms if m.id in mushrooms_db]
        )