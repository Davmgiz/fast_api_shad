import pytest
from sqlalchemy import select
from src.models.books import Book
from src.models.sellers import Seller
from fastapi import status
from icecream import ic


@pytest.mark.asyncio
async def test_register_seller(async_client):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john@example.com",
        "password": "securepassword"
    }

    response = await async_client.post("/api/v1/seller/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    resp_seller_id = result_data.pop("id", None)
    assert resp_seller_id, "Seller id not returned from endpoint"

    assert result_data == {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john@example.com",
    }


@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):

    seller = Seller(first_name="John", last_name="Doe", e_mail="john@example.com", password="123456789")
    seller_2 = Seller(first_name="John2", last_name="Doe2", e_mail="john22@example.com", password="123456789")

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")

    assert response.status_code == status.HTTP_200_OK

    assert (
        len(response.json()["sellers"]) == 2
    )  # Опасный паттерн! Если в БД есть данные, то тест упадет

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "sellers": [
            {
                "first_name": "John",
                "last_name": "Doe",
                "e_mail": "john@example.com",
                "id": seller.id
            },
            {
                "first_name": "John2",
                "last_name": "Doe2",
                "e_mail": "john22@example.com",
                "id": seller_2.id
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):

    seller = Seller(first_name="John", last_name="Doe", e_mail="john@example.com", password="123456789")
    seller_2 = Seller(first_name="John2", last_name="Doe2", e_mail="john22@example.com", password="123456789")

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    book = Book(author="Pushkin", title="Eugeny Onegin", year=2025, pages=104, seller_id=seller.id)


    db_session.add(book)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{seller.id}")

    assert response.status_code == status.HTTP_200_OK

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john@example.com",
        "id": seller.id,
        "books": [
            {
                "id": book.id,
                "title": "Eugeny Onegin",
                "author": "Pushkin",
                "year": 2025,
                "count_pages": 104
            }
        ]
    }

@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = Seller(first_name="John", last_name="Doe", e_mail="john@example.com", password="123456789")

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/seller/{seller.id}",
        json={
            "id": seller.id,
            "first_name": "John3",
            "last_name": "Doe3",
            "e_mail": "john33@example.com",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    # Проверяем, что обновились все поля
    res = await db_session.get(Seller, seller.id)
    assert res.first_name == "John3"
    assert res.last_name == "Doe3"
    assert res.e_mail == "john33@example.com"


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):

    seller = Seller(first_name="John", last_name="Doe", e_mail="john@example.com", password="123456789")

    db_session.add(seller)
    await db_session.flush()
    ic(seller.id)

    response = await async_client.delete(f"/api/v1/seller/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    await db_session.flush()
    all_sellers = await db_session.execute(select(Seller))
    res = all_sellers.scalars().all()

    assert len(res) == 0