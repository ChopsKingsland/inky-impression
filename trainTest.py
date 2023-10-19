from nredarwin.webservice import DarwinLdbSession
import config

darwin_sesh = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=config.NRE_API_KEY)

board = darwin_sesh.get_station_board('AFK')

locationName = board.location_name

services = board.train_services

for serv in services:
    print(serv.std, serv.etd, serv.platform, serv.destination_text, serv.origin_text)