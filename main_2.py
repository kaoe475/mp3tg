import asyncio
import logging
import os
from aiogram.types import FSInputFile
from random import randint
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from tok import TOKEN


try:
    list_mus=os.listdir('Audio')
except:
    print("Запустите скрипт в папке с папкой Audio")
    exit(0)



game_data = {1111:["count_users", {"id": ["name", ["url"]], 'id2':['name',['url']]} ] }
active_user = {'id':['list_mus', 'key']}





def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Правила игры", callback_data="z_info"),

        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
# Отправляет новое сообщение о количестве участников
async def update_count(message: types.Message, count_users):
    await message.answer(
        f"К нам присоединились, теперь нас: {count_users}!"
    )
# Важная функция после успешной регестрации
async def add_prof(message: types.Message, key):
    
    count_users = game_data[key][0]
    count_users += 1
    game_data[key][0]=count_users
    await update_count(message,count_users)
# ----

    list_mus=os.listdir('Audio')
    mus = []
    for i in range(4):
        audio = list_mus[randint(0,len(list_mus))]
        audio_file = FSInputFile(os.path.join(os.path.abspath('Audio'),audio))
        await message.answer(f'{i})')
        await message.answer_audio(audio=audio_file, title=f'{i})')
        mus.append(audio)
    await message.answer(f"Выберите два звука! На тему {game_data[key][2]}")
    active_user[message.from_user.id] = [mus, key]
    
async def scan(mess:types.Message, command):
    await mess.answer("Активные ключи!")
    for key in game_data:
            await mess.answer(f'`/{command} {key}`', parse_mode="MARKDOWN")




logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()

#Страрт
@router.message(Command(commands=['start']))
async def start(message:types.Message):
    await message.answer("Это бот для игры в мп3\nКоманды:\n/gomp3 + тема - запустить игру(не лс)\n/join + ключ - присоединиться к игре(только лс)\n/resolt - посмотреть результат\n/leave - выйти из активных")


#Запуск игры только для канала
@router.message(Command(commands=['gomp3']))
async def gomp3(message:types.Message):
    
    tema = message.text.replace("/gomp3", " ")
    if tema != " ":
        count_users = 0
        key = randint(1000,9999)
        await message.answer(f"Запущен мп3 на тему:{tema}\nКлюч: {key}", reply_markup=get_keyboard())
        await message.answer(f'Количество участников: {count_users}')
        await message.answer(f'Команды: `/join {key}`', parse_mode="MARKDOWN")
        game_data[key] = [count_users, {}, tema]
    else:
        await message.reply("Укажите тему\nПример:`/gomp3 Новая заставка стим`", parse_mode="MARKDOWN")
        

@router.message(Command(commands=['join']))
async def join_game(message:types.Message):
    key_c = message.text.replace('/join ', '')
    if  message.text == '/join':
        await scan(message, 'join')
    else: 
        for id in active_user:
            if message.from_user.id == id:
                return await message.answer("Вы уже присоединились к игре!")

        # Проверка пользователя на активного если есть то проверка на веденный ключ
        # Проверка ключей
        if key_c == '1111':
            await message.answer("Это тестируемый ключ")
        else:
            for key in game_data:            
                if key_c == str(key):
                    await message.answer("Вы успешно подключились к игре")
                    return await add_prof(message, int(key_c))#Запуск задач при усешном входе !!!!!
        #Условия ключей, не менять кароч        
            await message.answer("Игра не найдена")
                
        



#Срабатывание кнопок
@dp.callback_query(F.data.startswith("z_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "info":
        await callback.message.answer("Создатель игры задла тему, после того к игра запуститься тебе придет 4 рандомных звука, ты выбираешь два, потом в канал придут рещультаты, чья музыка оказалась смешнее и по теме тот и выйграл\nВеселой игры!")

    elif action == "finish":
        await callback.message.edit_text(f"Итого: ")
    await callback.answer()


@router.message(Command(commands='resolt'))
async def finish(message:types.Message):
    key_c = message.text.replace('/resolt ', '')
    if  message.text == '/resolt':
        await scan(message, 'resolt')
    else:
        #Проверка ключей
        if key_c == '1111':
        
            await message.answer("WTF bro! You stupid?")
        else:
            for key in game_data:
                if key_c == str(key):
                    memb = game_data[int(key_c)][0]
                    await message.answer("Итак подводим итоги!!!")
                    await message.answer(f'В этом матче участвовало: {memb}')
                    for id in game_data[int(key_c)][1]:
                        name = game_data[int(key_c)][1][id][0]
                        await message.answer(f"{name} выбрал:")
                        for i in range(2):#Отправляем выбранные звуки
                            audio_file = FSInputFile(os.path.join(os.path.abspath('Audio'),game_data[int(key_c)][1][id][1][i]), filename='Выбранный звук -_-')
                            await message.answer_audio(audio=audio_file)
                    return
        
            return await message.answer("Игра не найдена")
            

@router.message()
async def defolt(message:types.Message):
    for id in active_user:
        if id == message.from_user.id:
        
            id = message.from_user.id
            try:
                user_name = message.from_user.first_name + message.from_user.last_name
            except:
                try:
                    user_name = message.from_user.username
                except:
                    user_name = 'Щавель'
            new_mus = []
            new_mus.append(active_user[id][0][int(message.text[0])])
            new_mus.append(active_user[id][0][int(message.text[1])])
            key = active_user[id][1]
            game_data[key][1][id] = [user_name, new_mus]
            del active_user[id]
            return await message.answer("Ваши ответы отправлены, ждите результатов в канале!")
    return await message.answer(message.text)
        






async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot started!")
    asyncio.run(main())



