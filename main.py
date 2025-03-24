from aiogram import *
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardMarkup
import asyncio
from datetime import datetime
from pytz import *
import os
from weather import weathering, weather_
from dishes import dishes_ingredients
from interpreter import translator


id_users = {}


API_TOKEN = 'your_token'
bot = Bot(token = API_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    global id_users
    with open(f'date.txt', 'r') as file:
        r = file.readlines()
    if not(f'{message.from_user.id}\n' in r):
        with open(f'date.txt', 'a') as file1:
            file1.write(f'{message.from_user.id}\n')
    id_users[message.from_user.id] = ''
    await message.reply('''Привет!
Этот бот поможет тебе в подседневной рутине.
В меню указаны команды.''')
    

@dp.message(Command('plans'))
async def send_welcome(message: types.Message):
    global id_users
    id_users[message.from_user.id] = ''
    kb = []
    try:
        with open(f'{message.from_user.id}.txt', 'r') as file:
            for i in file.readlines():
                kb.append([types.InlineKeyboardButton(text = i[:-1],
        callback_data = f'P{i[:-1]}')])
    except:
        pass
    kb.append([types.InlineKeyboardButton(text = 'Создать напоминание',
        callback_data = 'plans')])
    keyboard = InlineKeyboardMarkup(inline_keyboard = kb)
    await message.reply('Выберите дату или создайте новое напоминание',
            reply_markup = keyboard)


@dp.message(Command('super_weather'))
async def weather(message: types.Message):
    global id_users
    id_users[message.from_user.id] = 'super_weather'
    await message.reply('Напишите нужные кардинаты и рзделите их запятыми. Найти их вы сможете зажав на нужном месте карты в "Навигаторе".')


@dp.message(Command('weather'))
async def weather(message: types.Message):
    global id_users
    id_users[message.from_user.id] = 'weather'
    await message.reply('Напишите название города маленькими буквами.')


@dp.message(Command('dishes'))
async def weather(message: types.Message):
    global id_users
    id_users[message.from_user.id] = 'dishes'
    await message.reply('Напишите продукты через ", "')


@dp.message(F.text)
async def any_answer(message: types.Message):
    global id_users
    try:
        if id_users[message.from_user.id] == 'plans':
            try:
                with open(f'{message.from_user.id}.txt', 'r') as file:
                    if message.text + '\n' in file.readlines():
                        await message.answer('Напоминание на эту дату уже есть')
                        return 0
            except:
                pass
            try:
                days = int(message.text[:2])
                months = int(message.text[3:5])
                years = int(message.text[6:10])
                hours = int(message.text[11:13])
                minutes = int(message.text[14:])
                month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                if message.text[2] == message.text[5] == '.' and message.text[10] == ' ' and message.text[13] == '.':
                    if hours < 24 and minutes < 60 and hours >= 0 and minutes >= 0:
                        if months > 0 and months <= len(month):
                            if month[months - 1] == 28 and ((years % 4 == 0 and years % 100 != 0) or years % 400 == 0):
                                month[months - 1] += 1
                            if days > 0 and month[months - 1] >= days:
                                id_users[message.from_user.id] = f'.plans{message.text}'
                                await message.answer('Запишите напоминание')
                                return 0
                await message.answer('Вы ввели веремя не в правильном формате')
            except:
                await message.answer('Вы ввели веремя не в правильном формате')
        

        elif id_users[message.from_user.id] == 'super_weather':
            xy = message.text
            xy = xy.replace(', ', ',')
            xy = xy.replace(' ', ',')
            xy = xy.split(',')
            try:
                if(len(xy) == 2):
                    await message.answer(weathering(xy[0], xy[1]))
                    id_users[message.from_user.id] = ''
                    return 0
            except:
                pass
            await message.answer('Вы ввели кординаты в неправильном формате.')
        

        elif id_users[message.from_user.id] == 'weather':
            try:
                await message.answer(weather_(str(translator(message.text, 'English'))))
                id_users[message.from_user.id] = ''
            except:
                await message.answer('Вы написали город в неправильном формате.')
        

        elif id_users[message.from_user.id] == 'dishes':
            try:
                json_ = dishes_ingredients(str(translator(message.text, 'English')))
                for _ in json_:
                    a = f"{_['title']}:"
                    for __ in _['missedIngredients']:
                        a += f"\n{__['original']}"
                    for __ in _['usedIngredients']:
                        a += f"\n{__['original']}"
                    try:
                        await message.answer_photo(photo = _['image'], caption = str(translator(a, 'Russian')))
                    except:
                        await message.answer(str(translator(a, 'Russian')))
                id_users[message.from_user.id] = ''
            except:
                await message.answer('Вы написали продукты в неправильном формате.')


        elif len(id_users[message.from_user.id]) > 6 and id_users[message.from_user.id][:6] == '.plans':
            try:
                with open(f'{message.from_user.id}.txt', 'a') as file:
                    file.write(f'{id_users[message.from_user.id][6:]}\n')
                with open(f'{id_users[message.from_user.id][6:]}{message.from_user.id}.txt', 'w') as file1:
                    file1.write(message.text)
            except:
                pass
            id_users[message.from_user.id] = ''
        

        elif len(id_users[message.from_user.id]) > 6 and id_users[message.from_user.id][:6] == 'change':
            try:
                with open(f'{id_users[message.from_user.id][6:]}{message.from_user.id}.txt', 'w') as file1:
                    file1.write(message.text)
            except:
                pass
            id_users[message.from_user.id] = ''
    except:
        pass


@dp.callback_query(F.data[0] == "P")
async def change_or_del_plans(callback: types.CallbackQuery):
    global id_users
    id_users[callback.from_user.id] = ''
    kb = [[
        types.InlineKeyboardButton(text = 'Изменить',
        callback_data = f'change{callback.data[1:]}'),
        types.InlineKeyboardButton(text = 'Удалить',
        callback_data = f'del{callback.data[1:]}')
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard = kb)
    try:
        with open(f'{callback.data[1:]}{callback.from_user.id}.txt', 'r') as file:
            await callback.message.answer(file.read(), reply_markup = keyboard)
    except:
        pass
    await callback.answer()


@dp.callback_query(F.data[:3] == "del")
async def del_plans(callback: types.CallbackQuery):
    id_users[callback.from_user.id] = ''
    try:
        with open(f'{callback.from_user.id}.txt', 'r') as file:
            r = file.readlines()
        del r[r.index(callback.data[3:] + '\n')]
        with open(f'{callback.from_user.id}.txt', 'w') as file1:
            file1.writelines(r)
        os.remove(f'{callback.data[3:]}{callback.from_user.id}.txt')
    except:
        pass
    await callback.answer()


@dp.callback_query(F.data[:6] == "change")
async def change_plans(callback: types.CallbackQuery):
    id_users[callback.from_user.id] = callback.data
    await callback.message.edit_text(text = 'Запишите напоминание')
    await callback.answer()


@dp.callback_query(F.data == "plans")
async def create_plans(callback: types.CallbackQuery):
    global id_users
    id_users[callback.from_user.id] = 'plans'
    await callback.message.edit_text(text = 'Напишите точную дату например 01.07.2024 06.01 (1 июля 2024 года в 6 часов 1 минуту)')
    await callback.answer()


async def main():
    loop = asyncio.create_task(whilik())
    await dp.start_polling(bot), loop


async def whilik():
    while True:
        with open(f'date.txt', 'r') as file:
            for i in file.readlines():
                try:
                    with open(f'{i[:-1]}.txt', 'r') as file1:
                        for j in file1.readlines():
                            days = j[:2]
                            months = j[3:5]
                            years = j[6:10]
                            hours = j[11:13]
                            minutes = j[14:-1]
                            time = datetime.strptime(f'{years}-{months}-{days} {hours}:{minutes}:00', '%Y-%m-%d %H:%M:%S')
                            if datetime.strptime(timezone("Europe/Moscow").localize(datetime.today()).strftime('%d.%m.%y %H.%M'), '%d.%m.%y %H.%M') >= time:
                                with open(f'{j[:-1]}{i[:-1]}.txt', 'r') as file4:
                                    await bot.send_message(chat_id = int(i[:-1]), text = f'{j[:-1]}:\n{file4.read()}')
                                try:
                                    with open(f'{i[:-1]}.txt', 'r') as file2:
                                        r = file2.readlines()
                                    del r[r.index(j)]
                                    with open(f'{i[:-1]}.txt', 'w') as file3:
                                        file3.writelines(r)
                                    os.remove(f'{j[:-1]}{i[:-1]}.txt')
                                except:
                                    pass
                except:
                    pass
        await asyncio.sleep(30)


if __name__ == '__main__':
    asyncio.run(main())