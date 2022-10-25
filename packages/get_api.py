import googlemaps
import re 

def get_crs_api(address,api_key): 

	"""This function is coords systems api (epsg:4326)
	only working for water_spot address

	address : list 
		input address list (주소 넣기)
	api_key : str 
		input your google cloud api key (구글 클라우드 api 키 넣기, 보안 주의)
	"""

	googlemaps_key = api_key 
	gmaps = googlemaps.Client(key=googlemaps_key)

	lat = []
	lng = []
	result = {}

	for addr in address:

		start_pattern = re.search('[\(]',addr)
		end_pattern = re.search('[\)]',addr)

		if start_pattern: 
			st_idx = start_pattern.start()
			end_idx = end_pattern.end()

			micro_addr = addr[0:st_idx]+addr[st_idx+1:end_idx-1]
			macro_addr = addr[0:st_idx]

		else:
			pass 
		
		try: 
			geo_location = gmaps.geocode(micro_addr)[0].get('geometry')

			lat.append(geo_location['location']['lat'])
			lng.append(geo_location['location']['lng'])

		except IndexError as e: 

			geo_location = gmaps.geocode(macro_addr)[0].get('geometry')

			lat.append(geo_location['location']['lat'])
			lng.append(geo_location['location']['lng'])
	
	result['lat'] = lat 
	result['lng'] = lng

	return result



if __name__ == "__main__":
    print("직접 실행")
    print(__name__)
else:
    print("임포트되어 사용됨")
    print(__name__)