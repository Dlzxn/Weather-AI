import aiohttp
import asyncio

API_KEY = "7e7e5eb06be149acaa9162633251805"

async def get_weather(city: str) -> list | None:
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                weather = await resp.json()
                temp_c = weather["current"]["temp_c"]
                condition = weather["current"]["condition"]["text"]
                print(f"Погода в {city}: {temp_c}°C, {condition}")
                temp = weather["current"]["feelslike_c"]
                condition = weather["current"]["condition"]["text"].lower()
                wind = weather["current"]["wind_kph"]
                precip = weather["current"]["precip_mm"]
                uv = weather["current"]["uv"]
                return [temp, condition, wind, precip]

            else:
                print("Ошибка при запросе:", resp.status)
                return None

print(asyncio.run(get_weather("Moscow")))
