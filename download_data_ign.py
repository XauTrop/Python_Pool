## Download seismic data from the IGN (Spain) catalogue ##
## Modify the url string according to the Min Max Lat Lon, date, EQ magnitude, ...
import requests
out_file_name = "IGN_catalogue.csv"
def download_data():
	url = 'http://contenido.ign.es/web/ign/portal/sis-catalogo-terremotos?p_p_id=IGNSISCatalogoTerremotos_WAR_IGNSISCatalogoTerremotosportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_IGNSISCatalogoTerremotos_WAR_IGNSISCatalogoTerremotosportlet_jspPage=%2Fjsp%2Fterremoto.jsp&latMin=28.1&latMax=29.1&longMin=-18.2&longMax=-17.5&startDate=10/09/2021&endDate=10/11/2021&selIntensidad=N&intMin=&intMax=&selMagnitud=Y&magMin=-2&magMax=11&selProf=Y&profMin=0&profMax=100&fases=no&cond=&tipoDescarga=txt'
	try:
		r = requests.post(url)
	except:
		print ('IGN Server not recheable')
		exit(0)
	if r.status_code == 200:
		with open(out_file_name,"wb") as f:
			f.write(r.content)
		f.close()