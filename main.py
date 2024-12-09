from fastapi import FastAPI, Query , Body
import uvicorn

app = FastAPI()

hotels = [
    {"id":1,"title":"Sochi","name":"sochi"},
    {"id":2,"title":"Dubai","name":"dubai"},
]


@app.get("/hotels")
def get_hotels(
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


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
        global hotels
        hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
        return {"status:OK"}


@app.post ("/hotels")
def create_hotels(
        title: str = Body(embed= True),
):

    global hotels

    hotels.append({"id":hotels[-1]["id"] + 1,
                   "title": title,
                  })    

    return {"status:OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: dict = Body(...)):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update(hotel_data)
            return {"status": "updated","hotel": hotel}
    return {"status": "not_found"}, 404




@app.patch("/hotels/{hotel_id}")
def partial_update_hotel(hotel_id: int, hotel_data: dict = Body(...)):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            for key, value in hotel_data.items():
                if key in hotel:
                    hotel[key]= value
            return {"status": "updated","hotel": hotel}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)



