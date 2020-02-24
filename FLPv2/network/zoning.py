# LIBRARIES
import json
# FILES
import settings


def load_json(filename):
	with open(filename, 'r') as json_file:
		json_dict = json.load(json_file)
	return  json_dict


def save_dict(dict_to_be_saved):
	json_file = json.dumps(dict_to_be_saved)
	fp = open(settings.contained_in_zone, 'w')
	fp.write(json_file)
	fp.close()


def save_list(list_to_be_saved):
	json_file = json.dumps(list_to_be_saved)
	fp = open(settings.zones, 'w')
	fp.write(json_file)
	fp.close()


def get_zoning(graph, candidates):
	from shapely.geometry import Point
	from shapely.geometry.polygon import Polygon
	from tqdm import tqdm
	contained_dict = dict()
	zones_list = list()
	zones = load_json(settings.zoning)
	for candidate in tqdm(candidates):
		y = graph.node[int(candidate)]['y']
		x = graph.node[int(candidate)]['x']
		point = Point(x,y)
		for zone in zones['features']:
			polygon = Polygon(zone['geometry']['coordinates'][0][0])
			if polygon.contains(point):
				contained_dict[candidate] = int(zone['properties']['zoning_id'])
				break
	for zone in zones['features']:
		zones_list.append(int(zone['properties']['zoning_id']))
	print(f'contained_dict contains {len(contained_dict.keys())} keys')
	save_dict(contained_dict)
	save_list(zones_list)

