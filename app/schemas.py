from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    name: constr(min_length=2, max_length=100)
    email: EmailStr
    phone: constr(min_length=10, max_length=20)

class BusResponse(BaseModel):
    route: str
    departure_times: list[str]
    bus_type: str
    formatted_times: list[str] = []