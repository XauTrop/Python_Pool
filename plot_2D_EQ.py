import pandas as pd
import plotly.express as px
from pyproj import Proj
import os
import download_data_ign as ddi


eq_file = os.getcwd() + '\\IGN_catalogue.csv'

## Download EQ data from IGN catalogue ##
ddi.download_data()

## Parse string values to float
def parse_to_float(v):
	try:
		float(v)
		r = float(v)
		return r
	except ValueError:
		if v == '':
			r = ''
		else:
			r = v
		return r
	return r
## Reshape the input file earthquake catalogue ##
def clean_table(file):
	a=[]
	b=[]
	c=[]
	d=[]
	e=[]
	f=[]
	g=[]
	h=[]
	k=[]
	t = 0
	reading_file = open(file, "r", encoding="utf8")
	for strl in reading_file:
		# Get each column from its starting position
		stripped_line = [strl[0:12], strl[17:27], strl[34:42], strl[50:57],
				   strl[64:73], strl[77:87], strl[96:102], strl[113:117],
				   strl[123:132]]
		nln = [" ".join(i.split()) for i in stripped_line]
		if t >0:
			a.append(nln[0])
			b.append(nln[1])
			c.append(nln[2])
			d.append(parse_to_float(nln[3]))
			e.append(parse_to_float(nln[4]))
			f.append(parse_to_float(nln[5]))
			g.append(parse_to_float(nln[6]))
			h.append(parse_to_float(nln[7]))
			k.append(parse_to_float(nln[8]))
		t+=1
	reading_file.close()

	df = pd.DataFrame(list(zip(a, b, c, d, e, f, g, h, k)),
					columns =['Evento', 'Fecha', 'Hora', 'Latitud', 'Longitud',
				   'Prof', 'Inten', 'Mag', 'TipoMag'])
	# Clean white spaces
	df = df[df.Prof != '']
	return df

data = clean_table (eq_file)
## Reproject Lat Lon data to UTM
ZoneNo = "28" #Manually input, or calcuated from Lat Lon
myProj = Proj("+proj=utm +zone="+ZoneNo+",+north +ellps=WGS84 +datum=WGS84 +units=m +no_defs") #north for north hemisphere
Lat = data['Latitud'].tolist()
Lon = data['Longitud'].tolist()
Depth_km = [i*-1 for i in data['Prof'].tolist()]
Mag = data['Mag'].tolist()
size = [i**2.3 for i in Mag]
date = data['Fecha'].tolist()
UTMx, UTMy = myProj(Lon, Lat)
df_sct = pd.DataFrame(list(zip(date, UTMx, UTMy, Depth_km, Mag, size)),
					  columns=['Date', 'X', 'Y', 'Z', 'Mag', 'size'])
# Release memory from data dataframe
data = {}

## Plot 2D scatter animated plot
config = {'displayModeBar': False}
fig =px.scatter(df_sct, x='Mag', y='Z',animation_frame='Date', size='size',
					range_y=[-40.1,0], range_x=[0.95,5.1],
					color=df_sct['Mag'], range_color=(1,5),
					color_continuous_scale=px.colors.sequential.Rainbow,
					labels={
					'Mag': "Magnitude",
					'Z': "Depth (km)",
					},)
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 700
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5
fig.update_layout(
	autosize=False,
	width=1000,
	height=550,)
fig.show( config=config)