import requests
from inky.auto import auto
import datetime
import config

# Constants
API_KEY = config.OWN_API_KEY
CITY = "Hamstreet"
UNITS = "metric"

# Function to get weather data from API
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to convert temperature from Kelvin to Fahrenheit
def kelvin_to_fahrenheit(temp):
    return round((temp - 273.15) * 9/5 + 32)

# Function to display weather data on Inky Impression display
def display_weather():
    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_border(inky_display.WHITE)
    img = inky_display.create_image()
    draw = inky_display.get_drawable(img)

    # Get weather data
    data = get_weather()
    temp = kelvin_to_fahrenheit(data["main"]["temp"])
    desc = data["weather"][0]["description"].title()
    icon = data["weather"][0]["icon"]

    # Draw weather data on display
    draw.text((10, 10), f"{temp}°F", inky_display.BLACK)
    draw.text((10, 30), desc, inky_display.BLACK)
    draw.text((10, 50), datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"), inky_display.BLACK)
    inky_display.set_image(img)
    inky_display.show()

# Call function to display weather data
display_weather()
