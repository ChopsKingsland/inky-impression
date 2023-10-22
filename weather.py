import requests
from inky.auto import auto
import datetime
import config
from PIL import Image, ImageDraw, ImageFont

# Constants
API_KEY = config.OWM_API_KEY
CITY = config.OWM_LOCATION
UNITS = "metric"

# Function to get weather data from API
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"
    response = requests.get(url)
    data = response.json()
    return data


normal36 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
extralight24 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf", 24)
bold36 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)

# Function to display weather data on Inky Impression display


def display_weather():
    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_border(inky_display.WHITE)
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), 1)
    draw = ImageDraw.Draw(img)

    # Get weather data
    data = get_weather()
    temp = data["main"]["temp"]
    maxTemp = data["main"]["temp_max"]
    minTemp = data["main"]["temp_min"]

    condition = data["weather"][0]["main"]
    conditionDesc = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]

    location = data["name"]

    # Draw weather data on display
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    draw.text((35, 30), location, inky_display.BLACK, font=normal36)
    draw.text((35, 72), f"{temp}°C", inky_display.BLACK, font=extralight24)
    draw.text((150, 198), condition, inky_display.BLACK, font=bold36)
    draw.text((150, 240), conditionDesc, inky_display.BLACK, font=normal36)

    # TODO: Draw weather icon
    
    icon = data["weather"][0]["icon"]
    icon_path = f"weather-icons/{icon}.png"
    icon = Image.open(icon_path)

    # resize to 97x97
    icon = icon.resize((97, 97))

    img.paste(icon, (42, 192), icon)



    inky_display.set_image(img)
    inky_display.show()

# Call function to display weather data
display_weather()
