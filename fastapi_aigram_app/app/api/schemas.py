from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    article: int


class ProductSchema(ProductBaseSchema):
    name: str
    price: float
    price_sale: float | None
    rating: int | None
    total_quantity: int


# # APScheduler Setup
# jobstores = {"default": SQLAlchemyJobStore(url=DATABASE_URL)}
# scheduler = BackgroundScheduler(jobstores=jobstores)
# scheduler.start()


# # Background job for periodic fetching
# async def periodic_fetch(artikul: int):
#     async with async_session() as session:
#         product_data = await fetch_product_data(artikul)
#         await save_product_to_db(session, product_data)

# @app.get("/api/v1/subscribe/{artikul}")
# async def subscribe_to_product(artikul: int):
#     job_id = f"product_{artikul}"

#     if scheduler.get_job(job_id):
#         return {"message": "Subscription already active."}

    # scheduler.add_job(
    #     periodic_fetch,
    #     "interval",
    #     minutes=30,
    #     id=job_id,
    #     kwargs={"artikul": artikul}
    # )
    # return {"message": "Subscription created."}

# # Telegram Bot Setup
# BOT_TOKEN = "your_bot_token"
# bot = aiogram.Bot(token=BOT_TOKEN)
# dp = aiogram.Dispatcher(bot)

# @dp.message_handler(commands=["start"])
# async def start_command(message: aiogram.types.Message):
#     await message.reply(
#         "Welcome! Use the 'Get Product Data'"
#         " button to fetch product information."
#     )

# @dp.message_handler(lambda message: message.text == "Get Product Data")
# async def request_product_data(message: aiogram.types.Message):
#     await message.reply("Please provide the product artikul.")

# @dp.message_handler()
# async def send_product_data(message: aiogram.types.Message):
#     try:
#         artikul = int(message.text)
#         async with async_session() as session:
#             result = await session.execute(
#                 select(Product).where(Product.artikul == artikul)
#             )
#             product = result.scalar_one_or_none()

#             if not product:
#                 await message.reply("Product not found in the database.")
#                 return

#             response = (f"Product: {product.name}\n"
#                         f"Artikul: {product.artikul}\n"
#                         f"Price: {product.price} RUB\n"
#                         f"Rating: {product.rating}\n"
#                         f"Total Quantity: {product.total_quantity}")
#             await message.reply(response)
#     except ValueError:
#         await message.reply("Invalid artikul. Please enter a valid number.")

# # Docker Setup Instructions
# # Ensure you create a Dockerfile and docker-compose.yml for the application
# # Example docker-compose.yml
# # setup includes services for FastAPI, PostgreSQL, and the Telegram bot.
