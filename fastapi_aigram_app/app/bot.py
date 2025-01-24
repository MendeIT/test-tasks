# import aiogram


# bot = aiogram.Bot(token=BOT_TOKEN)
# dp = aiogram.Dispatcher(bot)

# @dp.message_handler(commands=["start"])
# async def start_command(message: aiogram.types.Message):
#     await message.reply("Welcome!")

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
