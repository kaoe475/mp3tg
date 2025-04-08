import asyncio
from telegram.bot import dp, router, bot

async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot started!")
    asyncio.run(main())



