from nredarwin.webservice import DarwinLdbSession
import config
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

inky_display = auto(ask_user=True, verbose=True)

darwin_sesh = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=config.NRE_API_KEY)

board = darwin_sesh.get_station_board('HMT')

locationName = board.location_name
#print(locationName)

# Define font sizes
FONT_SIZE_LARGE = 25
FONT_SIZE_SMALL = 21

# Define font paths
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
#FONT_REGULAR_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_REGULAR_PATH = FONT_BOLD_PATH

# Load fonts
font_bold = ImageFont.truetype(FONT_BOLD_PATH, FONT_SIZE_LARGE)
font_regular = ImageFont.truetype(FONT_REGULAR_PATH, FONT_SIZE_SMALL)


def getServices():
    services = board.train_services
    print("got services")
    return services

def drawBoard(services, locationName):        
    # Define table layout
    table_layout = [
        ("Time", 0.15),
        ("Destination", 0.45),
        ("Platform", 0.2),
        ("Expected", 0.2)
    ]

    # Define table column widths
    table_widths = [int(inky_display.WIDTH * width) for _, width in table_layout]

    # Create new image
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), 1)

    # Create drawing object
    draw = ImageDraw.Draw(img)

    # Draw station name at top of image
    station_name = locationName.upper()
    station_name_width, _ = draw.textsize(station_name, font=font_bold)
    station_name_x = int((inky_display.WIDTH - station_name_width) / 2)
    draw.text((station_name_x, 0), station_name, inky_display.BLACK, font=font_bold)

    # Draw table headings
    table_x = 0
    table_y = FONT_SIZE_LARGE + FONT_SIZE_SMALL
    for heading, width in table_layout:
        column_width = int(inky_display.WIDTH * width)
        draw.rectangle((table_x, table_y, table_x + column_width, table_y + FONT_SIZE_LARGE), fill=inky_display.BLACK)
        draw.text((table_x + 5, table_y), heading, inky_display.WHITE, font=font_bold)
        table_x += column_width

    # Draw table rows
    table_y += FONT_SIZE_LARGE
    for serv in services:
        row_y = table_y + 7
        for i, (heading, width) in enumerate(table_layout):
            column_width = int(inky_display.WIDTH * width)
            column_x = sum(table_widths[:i])
            text = ""
            colour = inky_display.BLACK
            if heading == "Time":
                text = serv.std
            elif heading == "Destination":
                text = serv.destination_text
            elif heading == "Platform":
                text = serv.platform
            elif heading == "Expected":
                text = serv.etd
                if text == "On time":
                    colour = inky_display.GREEN
                elif text == "Delayed":
                    colour = inky_display.ORANGE
                elif text == "Cancelled":
                    colour = inky_display.RED
                else:
                    colour = inky_display.ORANGE
            if text == None:
                text = ""
            # print(text)
            draw.text((column_x + 5, row_y), text, colour, font=font_regular)
            # row_y += FONT_SIZE_SMALL
        table_y += (FONT_SIZE_SMALL * len(table_layout))/2

    # Display image on Inky pHAT
    inky_display.set_image(img)
    inky_display.show()


def update():
    services = getServices()
    drawBoard(services, locationName)

if __name__ == "__main__":
    update()