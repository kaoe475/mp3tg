from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message


token = "7721117978:AAEYSaW9j2FqsvoUfG1HvnyUIz9qFXIzPu0"

bot = Bot(token)
dp = Dispatcher()

ch = 0
kt = 0
rec = 0

@dp.message(Command(commands=["start"]))
async def process_start_comand(message: Message):
    await message.answer("На писюне напиши страрт!")
    await message.answer("Тут есть команды такие как :\n/rand_sound - Рандомный звук")

@dp.message(Command(commands=["rand_sound"]))
async def random_sound(message: Message):
    from pars import pars_sound
    sound = pars_sound()
    await message.answer(text=sound)
    print(sound)




@dp.message(Command(commands=["chat_admin"]))
async def flag(message: Message):
    kt = 0
    if rec == 1:
        await message.answer("Занят")
    else:
        ch = 1



@dp.message(Command(commands=["kto"]))
async def flag(mess: Message):
    kt = 1
    ch = 0



@dp.message()
async def chek(mess: Message):
    if kt == 1:
        async def kto(message: Message):
            from pars import rand_nick
            print(f"{message.chat.first_name}: {message.text}")
            await message.answer(f"{message.text} - {rand_nick()}")
    elif ch == 1:
        async def send_echo(message: Message):
            await message.answer("Жди ответа от Titanusa")
            rec = 1
            text = input(f"Запрашивают ответ на: {message.text}\n:")
            await message.answer(text=text)
            rec = 0
    else:
        async def echo(mes: Message):
            await mess.answer(mes)
    



if __name__ == '__main__':
    print("Start bot: t.me/TOJETIanus_bot")
    dp.run_polling(bot)