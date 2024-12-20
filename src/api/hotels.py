from fastapi import FastAPI, Query, Body, APIRouter
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

from sqlalchemy import insert, select
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.database import async_session_maker

router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация"),
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)

        if title:
            query = query.where(HotelsOrm.title.ilike(f'%{title}%'))
        if location:
            query = query.where(HotelsOrm.location.ilike(f'%{location}%'))
            #print(query.compile(compile_kwargs={"literal_binds": True})) Дебаг - просмотр сформированного запроса
        
        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page - 1))
        )

        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status:OK"}


@router.post("")
async def create_hotels(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель 5 звезд",
        "location": "sochi_u_mory"
    }},
    "2":
        {"summary": "Дубай", "value": {
        "title": "Отель 100 звезд",
        "location": "dubai_u_mory"
        }}
})
):
    async with async_session_maker() as session:
        add_hotel_smt = insert(HotelsOrm).values(**hotel_data.model_dump())
#       print(add_hotel_smt.compile(compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_smt)
        await session.commit()

    return {"status:OK"}


@router.put("/{hotel_id}")
def update_hotel(hotel_id: int,
                 hotel_data: Hotel
                 ):

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status": "updated", "hotel": hotel}
    return {"status": "not_found"}, 404


@router.patch("/{hotel_id}",
              summary="Частичное обновление данных об отеле",
              description="Можно отправить name, а можно title")
def part_update_hotel(hotel_id: int,
                      title: str | None = Body(None),
                      name: str | None = Body(None),):

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
            return {"status": "updated", "hotel": hotel}
    return {"status": "not_found"}, 404
