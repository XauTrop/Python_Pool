import pandas as pd
import os
import download_data_ign as ddi
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots


eq_file = os.getcwd() + '\\IGN_catalogue.csv'
## Load So2 data from PEVOLCA daily reports
SO2_file = 'SO2.txt'
df_SO = pd.read_csv(SO2_file, delimiter='\t')

## Download EQ data from IGN catalogue ##
# ddi.download_data()

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
Depth_km = [i*-1 for i in data['Prof'].tolist()]
Mag = data['Mag'].tolist()
size = [i**2.3 for i in Mag]
date = data['Fecha'].tolist()
df_sct = pd.DataFrame(list(zip(date, Depth_km, Mag, size)),
					  columns=['Date', 'Z', 'Mag', 'size'])
# Release memory from data dataframe
data = {}
energy =[]
us = sorted(set(df_sct['Date'].tolist()))
unique_days_total = sorted(us, key=lambda x: datetime.strptime(x, '%d/%m/%Y'))
unique_days = unique_days_total[1:-1]
for z in range(0,41):
	zets = []
	egys =[]
	dummy_z = df_sct.loc[df_sct['Z']==-z]
	for day in unique_days:
		dummy = dummy_z.loc[dummy_z['Date'] == day]
		engy = sum(dummy['Mag'].tolist())
		if engy != 0:
			egys.append(int(engy))
		else:
			egys.append(0)
	energy.append(egys)
df_sct = {}

k = [i for i in unique_days if not i in df_SO['Day'].tolist()]
xtra = {'Day': k}
df_SO = df_SO.append(pd.DataFrame(xtra))
df_SO['Day'] = pd.to_datetime(df_SO['Day'], format='%d/%m/%Y')
df_SO= df_SO.sort_values(by='Day', ascending=True)
df_SO['Day'] = df_SO['Day'].dt.strftime('%d/%m/%Y')

fig = make_subplots(
	shared_xaxes=True,
	rows=2, cols=1,
	row_heights=[0.2, 0.8],
	vertical_spacing = 0.05,
	specs=[[{"type": "bar"}], [{"type": "heatmap"}]],
	subplot_titles=(u'SO\u2082 Release', 'Cumulative Earthquake Magnitude'))

fig.add_trace(
	go.Bar(x=df_SO['Day'], y=df_SO['SO2'],
		showlegend=False,
		marker_color = 'tomato'),
		row=1, col=1)

fig .add_trace(
	go.Heatmap(z=energy,
		x=unique_days,
		colorscale='Hot',
		showscale=False),
		row=2, col=1)
# edit axes
fig.update_layout(
	xaxis2={'title' : 'Days', 'tickangle' : -45},
	yaxis={'title': u'SO\u2082 (tons)', 'showgrid' : True, 'gridcolor': 'lightgray'},
	yaxis2={'title': 'Depth (km)', 'autorange': 'reversed'},)
fig.write_image("images/Qlt_evolution.png", width=1664, height=891)
fig.show()


