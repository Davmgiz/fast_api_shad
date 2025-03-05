from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from src.models.sellers import Seller
from src.schemas import RegisterSeller, ReturnedSeller, ReturnedAllSeller, ReturnedSellerWithBooks
from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession
from src.configurations import get_async_session
from sqlalchemy.orm import joinedload

sellers_router = APIRouter(tags=["seller"], prefix="/seller")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@sellers_router.post(
    "/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED
)
async def create_book(
    seller: RegisterSeller,
    session: DBSession,
):

    new_seller = Seller(
        **{
            "first_name": seller.first_name,
            "last_name": seller.last_name,
            "e_mail": seller.e_mail,
            "password": seller.password
        }
    )

    session.add(new_seller)
    await session.flush()

    return new_seller


@sellers_router.get("/", response_model=ReturnedAllSeller)
async def get_all_sellers(session: DBSession):
    query = select(Seller).order_by(Seller.id)
    result = await session.execute(query)
    sellers = result.scalars().unique().all()
    return {"sellers": sellers}


@sellers_router.get("/{seller_id}", response_model=ReturnedSellerWithBooks)
async def get_seller(seller_id: int, session: DBSession):

    query = select(Seller).options(joinedload(Seller.books)).where(Seller.id == seller_id)
    result = await session.execute(query)
    seller = result.scalars().first()

    if not seller:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return seller


@sellers_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: DBSession):
    deleted_seller = await session.get(Seller, seller_id)
    ic(deleted_seller)
    if deleted_seller:
        await session.delete(deleted_seller)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@sellers_router.put("/{seller_id}", response_model=ReturnedSeller)
async def update_seller(seller_id: int, new_seller_data: ReturnedSeller, session: DBSession):
    if updated_seller := await session.get(Seller, seller_id):
        updated_seller.first_name = new_seller_data.first_name
        updated_seller.last_name = new_seller_data.last_name
        updated_seller.e_mail = new_seller_data.e_mail

        await session.flush()

        return updated_seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)
