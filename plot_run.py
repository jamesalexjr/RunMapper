"""
Module to read GPS XML and plot the course on a map
"""
import pandas
import xml.etree.ElementTree as ET
import geoplotlib
import sys

def get_points(file):
	""" Function to get the points of a GPS File
	inputs:
	--------
	file: file string
	outputs:
	--------
	datapoints: pandas DataFrame of lat,long of points
	"""
	tree = ET.parse(file)
	root = tree.getroot()
	tag = '{http://www.topografix.com/GPX/1/1}'
	track = root.find(tag + 'trk')
	points = track.find(tag + 'trkseg')

	datapoints = pandas.DataFrame([[0,0,0,0]], columns=['lat','lon','lat2','lon2'])

	i = 0
	for point in points.iter(tag + 'trkpt'):
		lat = float(point.get('lat'))
		long = float(point.get('lon'))
		if i == 0:
			datapoints.loc[i] = [lat, long, 0, 0]
		else:
			last_lat = datapoints.loc[i-1]['lat']
			last_lon = datapoints.loc[i-1]['lon']
			datapoints.loc[i - 1] = [last_lat, last_lon, lat, long]
			datapoints.loc[i] = [lat, long, 0, 0]
		i += 1
	return datapoints

if __name__ == '__main__':
	files = sys.argv[1:]

	for file in files:
		points = get_points(file)
		geoplotlib.graph(points[:-1], src_lat='lat', src_lon='lon', dest_lat='lat2', dest_lon='lon2', color='Reds', linewidth=3)

	geoplotlib.show()