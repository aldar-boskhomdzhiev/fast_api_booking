from fastapi import FastAPI, Query , Body, APIRouter
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels")


hotels = [
    {"id":1,"title":"Sochi","name":"sochi"},
    {"id":2,"title":"Dubai","name":"dubai"},
]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        ):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
        global hotels
        hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
        return {"status:OK"}


@router.post ("")
def create_hotels(hotel_data: Hotel,):

    global hotels

    hotels.append({"id":hotels[-1]["id"] + 1,
                   "title": hotel_data.title,
                   "name": hotel_data.name,
                  })    

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
            return {"status": "updated","hotel": hotel}
    return {"status": "not_found"}, 404




@router.patch("/{hotel_id}",
            summary= "Частичное обновление данных об отеле",
            description= "Можно отправить name, а можно title")
            
def part_update_hotel(hotel_id: int, 
                      title: str | None = Body(None),
                      name: str  | None = Body(None),):

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:                        
                hotel["name"] = name
            return {"status": "updated","hotel": hotel}
    return {"status": "not_found"}, 404

