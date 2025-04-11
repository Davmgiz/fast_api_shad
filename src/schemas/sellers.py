from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from .books import ReturnedBookForSeller

__all__ = ["RegisterSeller", "ReturnedSeller", "ReturnedAllSeller", "ReturnedSellerWithBooks"]


class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    e_mail: str


class RegisterSeller(BaseSeller):
    password: str


class ReturnedSeller(BaseSeller):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ReturnedSellerWithBooks(BaseSeller):
    id: int
    books: list[ReturnedBookForSeller]

    class Config:
        from_attributes = True


class ReturnedAllSeller(BaseModel):
    sellers: list[ReturnedSeller]
