from sqlalchemy import select

from src.db.models import async_session, User, UserProduct


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()


async def add_product(tg_id: int, product_url: str, price: float) -> None:
    async with async_session() as session:
        try:
            user_product = UserProduct(user_id=tg_id, product_url=product_url, user_price=price)
            session.add(user_product)
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Ошибка: {e}")
