"""
Module to read GPS XML and plot the course on a map
"""
import pandas
import xml.etree.ElementTree as ET
import geoplotlib
from sys import argv
from random import choice


COLORS = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r','BuGn',
		  'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2',
		  'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys',
		  'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn',
		  'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2',
		  'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 
		  'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples',
		  'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r',
		  'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 
		  'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral',
		  'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r',
		  'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot',
		  'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone',
		  'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r',
		  'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r',
		  'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth',
		  'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat',
		  'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow',
		  'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg',
		  'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r',
		  'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno',
		  'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral',
		  'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma',
		  'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic',
		  'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10',
		  'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c',
		  'tab20c_r', 'terrain', 'terrain_r', 'twilight', 'twilight_r',
		  'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r',
		  'winter', 'winter_r']

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
	files = argv[1:]

	for file in files:
		points = get_points(file)
		geoplotlib.graph(points[:-1], src_lat='lat', src_lon='lon', dest_lat='lat2', dest_lon='lon2', color=choice(COLORS), linewidth=3)

	geoplotlib.show()