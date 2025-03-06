from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.requests import requests as rq

router = Router()


class AddProductState(StatesGroup):
    product_url = State()
    price = State()
    
    


@router.message(Command('start'))
async def start(message: types.Message):
    try:
        await rq.set_user(message.from_user.id)

        await message.answer('Привет! Я бот, который может отслеживать цену товара и отправлять уведомление о достижении заданной цены.')
    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}')


@router.message(F.text == 'Добавить товар')
async def add_product_first(message: types.Message, state: FSMContext):
    await message.answer('Отправь ссылку на товар, который ты хочешь отследить')
    await state.set_state(AddProductState.product_url)


@router.message(AddProductState.product_url)
async def add_product_second(message: types.Message, state: FSMContext):
    await message.answer('Отправь целевую цену')
    await state.update_data(product_url=message.text)
    await state.set_state(AddProductState.price)


@router.message(AddProductState.price)
async def add_product_third(message: types.Message, state: FSMContext):

    data = await state.update_data(price=float(message.text))
    await state.clear()

    await rq.add_product(tg_id=message.from_user.id, product_url=data['product_url'], price=data['price'])
    await message.answer(f'Для ссылки {data["product_url"]} целевая цена {data["price"]}')
