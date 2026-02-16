import requests
import json
import re
from datetime import datetime

WEATHER_API_KEY = ""
STEAM_API_KEY = ""

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"]
        }
    except Exception as e:
        return {"error": str(e)}

def get_steam_news(appid=440, count=5):
    url = "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/"
    params = {
        "key": STEAM_API_KEY,
        "appid": appid,
        "count": count,
        "format": "json"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        news_items = data["appnews"]["newsitems"]
        result = []
        for item in news_items:
            result.append({
                "title": item["title"],
                "author": item.get("author", "Unknown"),
                "date": datetime.fromtimestamp(item["date"]).strftime("%Y-%m-%d %H:%M:%S"),
                "contents_preview": (item["contents"][:200] + "...") if len(item["contents"]) > 200 else item["contents"],
                "url": item["url"]})
        return result
    except Exception as e:
        return {"error": str(e)}

def main():
    city = input("Введите название города: ").strip()
    if not city:
        print("Город не введён.")
        return

    weather = get_weather(city)
    if "error" in weather:
        print("Ошибка погоды:", weather["error"])
    else:
        print("\n=== Погода ===")
        print(f"Город: {weather['city']}")
        print(f"Температура: {weather['temp']}°C (ощущается как {weather['feels_like']}°C)")
        print(f"Описание: {weather['description']}")
        print(f"Влажность: {weather['humidity']}%")
        print(f"Давление: {weather['pressure']} гПа")
        print(f"Скорость ветра: {weather['wind_speed']} м/с")
    print("\n=== Последние новости Steam (appid=440) ===")
    news = get_steam_news()
    if isinstance(news, dict) and "error" in news:
        print("Ошибка Steam:", news["error"])
    elif isinstance(news, list):
        for idx, item in enumerate(news, 1):
            print(f"\n--- Новость {idx} ---")
            print(f"Заголовок: {item['title']}")
            print(f"Автор: {item['author']}")
            print(f"Дата: {item['date']}")
            print(f"Превью: {item['contents_preview']}")
            print(f"Ссылка: {item['url']}")
    else:
        print("Не удалось получить новости.")

if __name__ == "__main__":

    main()
