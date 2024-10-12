from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv 

import os
import requests


start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Используй команду /weather город, чтобы узнать погоду.")

@start_router.message(Command('weather'))
async def get_weather(message: Message):
    city = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    
    if city is None:
        await message.answer("Пожалуйста, укажите название города после команды /weather.")
        return

    load_dotenv()
    OPENWEATHER_API=os.getenv('OPENWEATHER_API')    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}&units=metric&lang=ru"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        await message.answer(f"Погода в городе {city}:\n"
                             f"Температура: {temperature}°C\n"
                             f"Ощущается как: {feels_like}°C\n"
                             f"Описание: {weather_description}\n"
                             f"Влажность: {humidity}%\n"
                             f"Скорость ветра: {wind_speed} м/с")
    else:
        await message.answer("Город не найден. Попробуйте еще раз.")


