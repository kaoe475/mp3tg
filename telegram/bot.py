import asyncio
import logging
from pars import pars_sound
from random import randint
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

import os, sys

from telegram.keyboard import get_keyboard
from assets.vars import game_data, active_user

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("Token is not set")
    sys.exit(0)

# Отправляет новое сообщение о количестве участников
async def update_count(count_users, key):
    for id in game_data[key][1]:
        await bot.send_message(text=f"К нам присоединились, теперь нас: {count_users}!", chat_id=id)


# Важная функция после успешной регестрации
async def add_prof(message: types.Message, key):
    count_users = game_data[key][0]
    count_users += 1
    game_data[key][0]=count_users
    await update_count(count_users, key)
    list_mus=[]
    try:
        for i in range(4):
            url=pars_sound()
            list_mus.append(url)
        for mus in range(len(list_mus)):
            await message.answer(f"{mus})-{list_mus[mus]}")
        await message.answer(f"Выберите два звука! На тему {game_data[key][2]}")
        active_user[message.from_user.id] = [list_mus, key]
    except:
        await message.answer("Ошибка парса повторите команду снова!")
        await message.answer(f"`/join {key}`", parse_mode="MARKDOWN")
        count_users -= 1
        game_data[key][0]=count_users


# Выводит подсказку с ключами        
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
    await message.answer("Это бот для игры в мп3\nКоманды:\n/gomp3 + тема - запустить игру\n/join + ключ - присоединиться к игре\n/resolt + ключ - посмотреть результат игры")


#Запуск игры только для канала
@router.message(Command(commands=['gomp3']))
async def gomp3(message:types.Message):
    
    tema = message.text.replace("/gomp3", " ")
    if tema != " ":
        count_users = 0
        key = randint(1000,9999)
        await message.answer(f"Запущен мп3 на тему:{tema}\nКлюч: {key}", reply_markup=get_keyboard())
        msg = await message.answer(f'Количество участников: {count_users}')
        await message.answer(f'Команды: `/join {key}`', parse_mode="MARKDOWN")
        chat_id = msg.message_id
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
        #Проверка ключей
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
        for key in game_data:
            if key_c == str(key):
                
        #Условия ключей, не менять кароч        
        
                memb = game_data[int(key_c)][0]
                await message.answer("Итак подводим итоги!!!")
                await message.answer(f'В этом матче участвовало: {memb}')
                for id in game_data[int(key_c)][1]:                        
                    name = game_data[int(key_c)][1][id][0]                 
                    await message.answer(f"{name} выбрал:")               
                #print(game_data[int(key_c)][1][id][1])
                    for i in range(len(game_data[int(key_c)][1][id][1])):
                        return await message.answer(f"{game_data[int(key_c)][1][id][1][i]}")
                    #print(game_data[int(key_c)][1][id][1][i])
        
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
                    user_name = id
            list_mus = active_user[id][0]
            new_mus = []
            new_mus.append(list_mus[int(message.text[0])])
            new_mus.append(list_mus[int(message.text[1])])
            key = active_user[id][1]
            #print(key)
            #print(game_data[key])
            game_data[key][1][id] = [user_name, new_mus]
            #game_data[key][1][id] = [game_data[key][1][id][0], new_mus]
            #print(game_data.items())
            await message.answer("Ваши ответы отправлены, ждите результатов в канале!")
            del active_user[id]
        
        else:
            await message.answer(message.text)
    