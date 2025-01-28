import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from api.schemas import ProductBaseSchema
from core.conf import settings
from database.crud import get_product_by_article
from database.db import get_session


logging.basicConfig(
    level=logging.INFO,
    format=('%(asctime)s - %(levelname)s - %(name)s '
            '- %(funcName)s[%(lineno)d] - %(message)s'),
    encoding='utf-8'
)

BOT: Bot = Bot(token=settings.BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.reply(
        text=f"Добро пожаловать, {message.from_user.full_name}!\n"
        "Я бот-ассистент для работы с маркеплейсом Wildberries.\n"
        "Чтобы получить данные о товаре, отправьте мне артикул товара.",
    )


@dp.message((F.text.regexp(r"^(\d+)$").as_("digits")) & (F.text.len() <= 12))
async def send_product_data(message: Message):
    logging.debug('Обработка артикула товара.')

    article = int(message.text)
    product = ProductBaseSchema(article=article)
    async with get_session() as session:
        product_db = await get_product_by_article(session, product)

        if not product_db:
            await message.reply("Товар отсутствет в базе данных.")
            return

        await message.reply(
            text=(
                f"Наименование товара:\n{product_db.name}\n"
                f"Артикул: {product_db.article}\n"
                f"Цена: {product_db.price} руб\n"
                f"Цена со скидкой: {product_db.price_sale} руб\n"
                f"Рейтинг товара: {product_db.rating}\n"
                f"Общее количество на складах: {product_db.total_quantity}"
            )
        )


@dp.message()
async def send_not_found_data(message: Message):
    await message.reply(
        "Мы не нашли товар по данному артиклу.\n"
        "Пожалуйста проверьте артикул.\n"
        "Он должен состоять из цифр от 0-9."
    )
