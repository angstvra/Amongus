import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output, State
import random
import time
import datetime
import calendar
import plotly.graph_objs as go
import numpy as np
import flask
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import pyrebase
import datetime
import random
import sched, time
from bs4 import BeautifulSoup
import requests
from nets import helperAverageData, predict_weather, function_to_scale, linearRegression1d
from weatherBase2 import Weather_Database
from weather_utils import heat_danger, heat_index, rain_advisories, beaufort, advisory_in_beaufort
##########################MAPS##########################################################

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.PULSE],suppress_callback_exceptions=True)
server = app.server
app.title = 'Among Us'

url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
attribution = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"


#url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
#attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

#UPDATE LINKS FUNCTIONS
def updateIRLink(inputHours):
    image_url_IR = f"https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_b13_" +inputHours+".jpg"
    return image_url_IR 

def updateHRPLink(inputHours):
    image_url_HRP = f"https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_hrp_"+inputHours+".jpg"
    return image_url_HRP

image_url_IR = "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_b13_0000.jpg"
image_url_HRP = "https://www.data.jma.go.jp/mscweb/data/himawari/img/se2/se2_hrp_0000.jpg"
image_bounds = [[29.5, 105],[-0.5, 140]]
phil_bound = [[18.525989, 112.019504],[6.261694, 139.189708]]


list_x = [[[15.148268747733908, 117.70157268219941], [15.15076874773391, 117.69907268219941]], [[15.895768747733946, 119.91907268219953], [15.898268747733946, 119.91657268219953]], [[16.323268747733966, 119.99657268219953], [16.325768747733967, 119.99657268219953]], [[15.070768747733904, 120.06157268219953], [15.070768747733904, 120.05907268219953]], [[15.680768747733936, 120.11657268219953], [15.683268747733935, 120.11407268219953]], [[15.698268747733936, 120.17157268219954], [15.700768747733935, 120.16907268219954]], [[14.995768747733901, 120.22657268219953], [14.998268747733901, 120.22407268219953]], [[14.683268747733885, 120.28157268219954], [14.683268747733885, 120.27907268219954]], [[15.493268747733925, 120.32907268219954], [15.495768747733926, 120.32907268219954]], [[17.61076874773403, 120.36407268219955], [17.61076874773403, 120.36157268219955]], [[15.910768747733947, 120.39157268219955], [15.913268747733948, 120.38907268219954]], [[14.59076874773388, 120.41657268219954], [14.59076874773388, 120.41407268219955]], [[17.545768747734027, 120.44157268219955], [17.548268747734028, 120.43907268219955]], [[17.293268747734015, 120.46157268219955], [17.293268747734015, 120.45907268219955]], [[15.240768747733913, 120.47907268219956], [15.240768747733913, 120.47657268219955]], [[13.288268747733817, 120.49657268219956], [13.290768747733816, 120.49407268219954]], [[17.41576874773402, 120.51657268219955], [17.41576874773402, 120.51407268219955]], [[17.228268747734013, 120.53407268219955], [17.23076874773401, 120.53407268219955]], [[17.260768747734012, 120.55157268219955], [17.263268747734013, 120.55157268219955]], [[17.700768747734035, 120.56907268219956], [17.700768747734035, 120.56657268219955]], [[17.530768747734026, 120.58657268219956], [17.530768747734026, 120.58407268219956]], [[18.078268747734054, 120.60407268219956], [18.080768747734055, 120.60157268219956]], [[15.713268747733938, 120.61907268219956], [15.715768747733936, 120.61657268219956]], [[18.475768747734072, 120.63657268219956], [18.475768747734072, 120.63407268219956]], [[16.740768747733988, 120.65157268219956], [16.74326874773399, 120.65157268219956]], [[16.183268747733962, 120.66657268219956], [16.183268747733962, 120.66407268219956]], [[15.133268747733908, 120.68157268219956], [15.13576874773391, 120.67907268219956]], [[13.473268747733826, 120.69657268219956], [13.475768747733825, 120.69407268219956]], [[17.480768747734025, 120.71407268219956], [17.483268747734023, 120.71157268219956]], [[17.24576874773401, 120.72907268219956], [17.248268747734013, 120.72907268219956]], [[16.723268747733986, 120.74407268219956], [16.725768747733987, 120.74157268219956]], [[15.850768747733945, 120.75907268219956], [15.850768747733945, 120.75657268219956]], [[16.15326874773396, 120.77407268219956], [16.15326874773396, 120.77157268219956]], [[16.83076874773399, 120.78907268219956], [16.833268747733992, 120.78907268219956]], [[13.073268747733806, 120.80157268219956], [13.075768747733806, 120.80157268219956]], [[16.293268747733965, 120.81657268219956], [16.293268747733965, 120.81407268219957]], [[12.995768747733802, 120.82907268219957], [12.995768747733802, 120.82657268219957]], [[16.085768747733955, 120.84407268219957], [16.085768747733955, 120.84157268219957]], [[18.040768747734052, 120.85907268219957], [18.040768747734052, 120.85657268219957]], [[16.043268747733954, 120.87157268219957], [16.043268747733954, 120.86907268219957]], [[14.035768747733854, 120.88407268219957], [14.038268747733854, 120.88407268219957]], [[18.36576874773407, 120.89907268219957], [18.368268747734067, 120.89657268219958]], [[16.983268747734, 120.91157268219958], [16.985768747734, 120.90907268219956]], [[16.32826874773397, 120.92407268219958], [16.330768747733966, 120.92407268219958]], [[16.123268747733956, 120.93657268219957], [16.125768747733957, 120.93657268219957]], [[15.970768747733949, 120.94907268219957], [15.97326874773395, 120.94657268219957]], [[16.270768747733964, 120.96157268219957], [16.273268747733965, 120.96157268219957]], [[16.690768747733983, 120.97407268219958], [16.690768747733983, 120.97157268219958]], [[17.220768747734013, 120.98657268219958], [17.22326874773401, 120.98657268219958]], [[17.825768747734042, 120.99907268219958], [17.828268747734043, 120.99657268219957]], [[12.548268747733779, 121.00907268219957], [12.55076874773378, 121.00907268219957]], [[13.230768747733814, 121.02157268219958], [13.233268747733813, 121.01907268219958]], [[14.423268747733873, 121.03407268219958], [14.425768747733873, 121.03157268219958]], [[15.58576874773393, 121.04657268219958], [15.588268747733931, 121.04407268219958]], [[17.243268747734014, 121.05907268219958], [17.24576874773401, 121.05907268219958]], [[13.16576874773381, 121.06907268219958], [13.16576874773381, 121.06657268219958]], [[16.318268747733967, 121.08157268219958], [16.318268747733967, 121.07907268219958]], [[12.35576874773377, 121.09157268219958], [12.35826874773377, 121.09157268219958]], [[14.525768747733878, 121.10407268219959], [14.528268747733879, 121.10157268219959]], [[16.340768747733968, 121.11657268219957], [16.34326874773397, 121.11407268219958]], [[18.23826874773406, 121.12907268219958], [18.240768747734062, 121.12907268219958]], [[13.843268747733845, 121.13907268219958], [13.845768747733844, 121.13657268219958]], [[15.638268747733933, 121.15157268219959], [15.640768747733933, 121.15157268219959]], [[17.490768747734023, 121.16407268219959], [17.490768747734023, 121.16157268219959]], [[13.35826874773382, 121.17407268219958], [13.35826874773382, 121.17157268219958]], [[16.278268747733964, 121.18657268219958], [16.278268747733964, 121.18407268219958]], [[18.23826874773406, 121.19907268219958], [18.240768747734062, 121.19657268219959]], [[14.280768747733866, 121.20907268219959], [14.283268747733866, 121.20907268219959]], [[16.478268747733974, 121.2215726821996], [16.480768747733975, 121.21907268219958]], [[12.400768747733773, 121.23157268219958], [12.400768747733773, 121.22907268219959]], [[16.083268747733953, 121.24407268219959], [16.083268747733953, 121.24157268219959]], [[18.515768747734075, 121.25657268219959], [18.518268747734076, 121.25407268219959]], [[14.083268747733856, 121.2665726821996], [14.085768747733857, 121.26407268219958]], [[15.54326874773393, 121.2790726821996], [15.545768747733929, 121.2790726821996]], [[16.950768747734, 121.29157268219959], [16.950768747734, 121.28907268219959]], [[18.275768747734062, 121.30407268219959], [18.275768747734062, 121.30157268219959]], [[13.110768747733808, 121.3140726821996], [13.113268747733807, 121.3115726821996]], [[14.35826874773387, 121.3265726821996], [14.36076874773387, 121.3265726821996]], [[15.163268747733909, 121.3390726821996], [15.163268747733909, 121.33657268219959]], [[15.94326874773395, 121.35157268219959], [15.945768747733949, 121.34907268219959]], [[16.708268747733985, 121.36407268219959], [16.708268747733985, 121.3615726821996]], [[17.708268747734035, 121.3765726821996], [17.710768747734036, 121.3765726821996]], [[19.325768747734116, 121.3890726821996], [19.328268747734118, 121.3865726821996]], [[12.878268747733797, 121.3990726821996], [12.880768747733796, 121.39657268219959]], [[12.978268747733802, 121.41157268219959], [12.978268747733802, 121.4090726821996]], [[12.9382687477338, 121.4240726821996], [12.9382687477338, 121.4215726821996]], [[18.86076874773409, 121.4390726821996], [18.863268747734093, 121.4365726821996]], [[17.488268747734026, 121.4515726821996], [17.490768747734023, 121.4490726821996]], [[15.625768747733932, 121.4640726821996], [15.625768747733932, 121.4615726821996]], [[12.638268747733784, 121.4765726821996], [12.638268747733784, 121.4740726821996]], [[15.893268747733945, 121.4915726821996], [15.893268747733945, 121.4890726821996]], [[16.17576874773396, 121.5065726821996], [16.17826874773396, 121.5040726821996]], [[14.463268747733874, 121.5215726821996], [14.463268747733874, 121.5190726821996]], [[16.74576874773399, 121.5390726821996], [16.74576874773399, 121.5365726821996]], [[18.265768747734064, 121.5565726821996], [18.268268747734062, 121.5540726821996]], [[17.248268747734013, 121.5740726821996], [17.250768747734014, 121.5715726821996]], [[14.59326874773388, 121.59157268219961], [14.595768747733882, 121.59157268219961]], [[15.703268747733937, 121.61157268219961], [15.703268747733937, 121.60907268219961]], [[18.043268747734054, 121.6340726821996], [18.04576874773405, 121.6315726821996]], [[14.270768747733865, 121.65407268219961], [14.273268747733866, 121.65407268219961]], [[17.58326874773403, 121.6790726821996], [17.58576874773403, 121.6765726821996]], [[14.34576874773387, 121.70157268219961], [14.34576874773387, 121.69907268219961]], [[16.15826874773396, 121.72657268219962], [16.15826874773396, 121.72407268219962]], [[17.53576874773403, 121.75407268219962], [17.538268747734026, 121.75407268219962]], [[17.598268747734032, 121.78157268219961], [17.60076874773403, 121.78157268219961]], [[20.325768747734166, 121.80907268219961], [20.328268747734167, 121.80657268219962]], [[13.900768747733848, 121.83157268219962], [13.900768747733848, 121.82907268219962]], [[17.73576874773404, 121.85657268219961], [17.73576874773404, 121.85407268219961]], [[17.908268747734045, 121.87907268219962], [17.910768747734046, 121.87907268219962]], [[18.01826874773405, 121.90157268219963], [18.020768747734053, 121.89907268219962]], [[17.14326874773401, 121.92157268219962], [17.14326874773401, 121.91907268219963]], [[20.39326874773417, 121.94157268219962], [20.39576874773417, 121.93907268219962]], [[16.39576874773397, 121.95907268219962], [16.398268747733972, 121.95907268219962]], [[17.97326874773405, 121.97907268219963], [17.97576874773405, 121.97907268219963]], [[12.53826874773378, 121.99657268219963], [12.540768747733779, 121.99407268219963]], [[16.658268747733985, 122.01657268219962], [16.658268747733985, 122.01407268219963]], [[17.64576874773403, 122.03657268219963], [17.648268747734033, 122.03657268219963]], [[11.853268747733745, 122.05407268219963], [11.853268747733745, 122.05157268219963]], [[11.55076874773373, 122.07407268219963], [11.55076874773373, 122.07157268219963]], [[12.600768747733783, 122.09407268219962], [12.603268747733782, 122.09157268219963]], [[12.588268747733782, 122.11407268219963], [12.590768747733781, 122.11157268219964]], [[12.658268747733786, 122.13407268219963], [12.658268747733786, 122.13157268219963]], [[11.693268747733738, 122.15407268219964], [11.695768747733737, 122.15157268219963]], [[14.848268747733893, 122.17657268219963], [14.850768747733895, 122.17407268219964]], [[18.128268747734055, 122.20157268219964], [18.128268747734055, 122.19907268219964]], [[17.008268747734, 122.22657268219963], [17.010768747734, 122.22657268219963]], [[11.638268747733735, 122.25157268219964], [11.638268747733735, 122.24907268219964]], [[11.190768747733712, 122.27907268219964], [11.193268747733713, 122.27907268219964]], [[18.363268747734068, 122.31157268219964], [18.36576874773407, 122.30907268219964]], [[11.428268747733725, 122.34157268219964], [11.428268747733725, 122.33907268219964]], [[16.76326874773399, 122.37657268219965], [16.76326874773399, 122.37407268219964]], [[11.250768747733716, 122.40907268219965], [11.253268747733715, 122.40657268219965]], [[13.845768747733844, 122.44657268219964], [13.845768747733844, 122.44407268219965]], [[14.325768747733868, 122.48657268219965], [14.328268747733869, 122.48407268219965]], [[14.090768747733856, 122.52907268219965], [14.093268747733857, 122.52907268219965]], [[13.433268747733823, 122.57407268219966], [13.433268747733823, 122.57157268219966]], [[13.195768747733812, 122.61907268219966], [13.195768747733812, 122.61657268219966]], [[11.220768747733715, 122.66407268219966], [11.220768747733715, 122.66157268219966]], [[11.260768747733716, 122.71657268219965], [11.263268747733717, 122.71657268219965]], [[10.870768747733697, 122.77407268219966], [10.870768747733697, 122.77157268219966]], [[13.915768747733848, 122.83907268219967], [13.918268747733848, 122.83907268219967]], [[13.95076874773385, 122.90157268219967], [13.95326874773385, 122.90157268219967]], [[13.725768747733838, 122.96157268219967], [13.728268747733837, 122.95907268219968]], [[14.053268747733854, 123.01407268219968], [14.053268747733854, 123.01157268219967]], [[10.638268747733685, 123.06657268219968], [10.638268747733685, 123.06407268219968]], [[10.900768747733698, 123.13157268219967], [10.900768747733698, 123.12907268219968]], [[10.770768747733692, 123.20157268219968], [10.773268747733692, 123.20157268219968]], [[10.568268747733681, 123.25407268219969], [10.570768747733682, 123.25407268219969]], [[13.903268747733847, 123.2990726821997], [13.903268747733847, 123.2965726821997]], [[10.900768747733698, 123.33407268219969], [10.900768747733698, 123.33157268219969]], [[12.388268747733772, 123.3715726821997], [12.390768747733771, 123.3690726821997]], [[13.635768747733835, 123.4140726821997], [13.638268747733834, 123.41157268219969]], [[13.37576874773382, 123.45657268219969], [13.378268747733822, 123.4540726821997]], [[13.855768747733844, 123.5040726821997], [13.858268747733845, 123.50157268219971]], [[13.028268747733804, 123.5565726821997], [13.028268747733804, 123.5540726821997]], [[13.038268747733804, 123.6165726821997], [13.038268747733804, 123.6140726821997]], [[13.828268747733842, 123.66907268219971], [13.830768747733844, 123.66657268219971]], [[13.798268747733841, 123.71657268219971], [13.800768747733843, 123.71407268219971]], [[13.848268747733844, 123.75907268219972], [13.850768747733845, 123.75657268219972]], [[10.670768747733687, 123.80907268219971], [10.673268747733687, 123.80907268219971]], [[12.063268747733755, 123.86157268219972], [12.065768747733756, 123.85907268219972]], [[12.16326874773376, 123.90907268219972], [12.16326874773376, 123.90657268219972]], [[12.078268747733757, 123.95407268219972], [12.080768747733757, 123.95407268219972]], [[11.235768747733715, 123.99657268219973], [11.238268747733715, 123.99407268219973]], [[12.648268747733784, 124.04657268219972], [12.650768747733785, 124.04657268219972]], [[10.090768747733657, 124.12407268219974], [10.093268747733658, 124.12157268219973]], [[14.025768747733853, 124.19157268219973], [14.028268747733852, 124.19157268219973]], [[10.11326874773366, 124.26657268219974], [10.115768747733659, 124.26657268219974]], [[11.418268747733723, 124.32907268219974], [11.420768747733725, 124.32907268219974]], [[12.313268747733767, 124.37907268219975], [12.315768747733769, 124.37657268219974]], [[12.193268747733763, 124.42157268219975], [12.195768747733762, 124.42157268219975]], [[10.693268747733688, 124.46407268219974], [10.695768747733688, 124.46157268219974]], [[11.275768747733716, 124.50907268219976], [11.278268747733717, 124.50907268219976]], [[11.095768747733707, 124.55407268219975], [11.095768747733707, 124.55157268219975]], [[12.12826874773376, 124.62907268219976], [12.13076874773376, 124.62657268219975]], [[10.900768747733698, 124.70907268219976], [10.903268747733698, 124.70907268219976]], [[12.058268747733756, 124.76657268219977], [12.060768747733755, 124.76407268219977]], [[10.375768747733671, 124.80407268219976], [10.375768747733671, 124.80157268219976]], [[10.225768747733664, 124.83907268219977], [10.225768747733664, 124.83657268219977]], [[11.540768747733729, 124.87407268219977], [11.54326874773373, 124.87157268219977]], [[11.96326874773375, 124.90657268219977], [11.96326874773375, 124.90407268219977]], [[11.13826874773371, 124.93907268219976], [11.14076874773371, 124.93907268219976]], [[11.620768747733734, 124.97157268219978], [11.623268747733734, 124.97157268219978]], [[11.965768747733751, 125.00407268219978], [11.96826874773375, 125.00407268219978]], [[12.008268747733753, 125.04157268219977], [12.010768747733753, 125.04157268219977]], [[12.340768747733769, 125.08407268219977], [12.34326874773377, 125.08407268219977]], [[12.418268747733773, 125.12657268219978], [12.420768747733774, 125.12657268219978]], [[12.445768747733775, 125.16907268219978], [12.448268747733774, 125.16657268219979]], [[12.14576874773376, 125.21407268219978], [12.14576874773376, 125.21157268219979]], [[12.255768747733764, 125.25907268219979], [12.258268747733766, 125.25657268219979]], [[12.028268747733755, 125.3140726821998], [12.030768747733754, 125.3140726821998]], [[11.250768747733716, 125.3765726821998], [11.250768747733716, 125.3740726821998]], [[11.828268747733745, 125.4365726821998], [11.830768747733744, 125.4340726821998]], [[11.225768747733714, 125.4990726821998], [11.228268747733715, 125.4965726821998]], [[9.393268747733623, 125.5715726821998], [9.395768747733623, 125.5715726821998]], [[9.895768747733648, 125.64157268219981], [9.895768747733648, 125.63907268219981]], [[11.028268747733705, 125.75907268219981], [11.030768747733704, 125.75907268219981]], [[9.395768747733623, 125.98407268219982], [9.395768747733623, 125.98157268219983]]]



list_polyline = []



for i in range(0,len(list_x)):
    polyline = dl.Polyline(positions=list_x[i])
    patterns = [dict(offset='100%', repeat='0', arrowHead=dict(pixelSize=15, polygon=False, pathOptions=dict(stroke=True)))]
    arrow = dl.PolylineDecorator(children=polyline, patterns=patterns)
    list_polyline.append(arrow)
    
#SUBMIT BUTTON
subButton = html.Div(
    [html.Button('Submit', id='submit-button-1', n_clicks=0)],
        style={
        "position":"fixed",
        "bottom":"60px",
        "left":"150px",
        "background-color":"white"
    })

#DROPDOWNS
options = []
for i in range(0, 24):
    for j in range(0, 6):
        if(i<10):
            options.append({'label':'0' + str(i) + ':'+str(j) + '0', 'value': '0'+str(i)+str(j)+'0'})
        else:
            options.append({'label':str(i) + ':'+str(j) + '0', 'value': str(i)+str(j)+'0'})
#DROPDOWNS
stormProfileDD = html.Div([
        dcc.Dropdown(id='dropdown-1', 
            options=options,
                value = "0000",
                searchable=False, 
                clearable=False,
                placeholder="Select Time",
                style=dict(
                width='40%',
                height='10%',
                verticalAlign="middle"
                )
                ),

        html.Div(id="output1", children="0000", style={'display':'none'})
        ],
        style={ "position":"absolute",
                "bottom":"150px",
                "left":"400px",
                "width":"450px",
                "height":"100px",}
    )



#SIDE PANEL BOXES
stormProfileBoxes = dcc.Checklist(
    options=[
        {'label': 'Infrared', 'value': 'ir'},
        {'label': 'Heavy Rain', 'value': 'hr'}
    ],
    value=['ir', 'hr'],
    labelStyle={'display': 'block','color':'black'},
    id="sideboxes-1"
)


affectedCommunitiesBoxes = dcc.Checklist(
    options=[
        {'label': 'Population Density', 'value': 'populationCount'},
    ],
    labelStyle={'display': 'block','color':'black'},
    id="sideboxes-2"
)

agriculturalDamageBoxes = dcc.Checklist(
    options=[
        {'label': 'Option31', 'value': 'val31'},
        {'label': 'Option32', 'value': 'val32'}
    ],
    labelStyle={'display': 'block','color':'black'},
    id="sideboxes-3"
)

coastalRegionsBoxes = dcc.Checklist(
    options=[
        {'label': 'Coast Lines', 'value': 'coastLines'},
    ],
    labelStyle={'display': 'block','color':'black'},
    id="sideboxes-4"
)

essentialFacilitiesBoxes = dcc.Checklist(
    options=[
        {'label': 'Option51', 'value': 'val51'},
        {'label': 'Option52', 'value': 'val52'}
    ],
    labelStyle={'display': 'block','color':'black'},
    id="sideboxes-5"
)

floodAreasBoxes = dcc.Checklist(
    options=[
        {'label': 'Flood Distribution', 'value': 'floodDist'},
        {'label': 'Flood Flow', 'value' : 'floodFlow'}
    ],
    labelStyle={'display': 'block','color':'black'},
    id="sideboxes-6"
)

windEffectBoxes = dcc.Checklist(
    options=[
        {'label': 'Option71', 'value': 'val71'},
        {'label': 'Option72', 'value': 'val72'}
    ],
    labelStyle={'display': 'block','color':'black'},
    id="sideboxes-7"
)

#SIDE CARDS
stormProfile = dbc.Card([
        dbc.CardHeader(
            html.H2(
                dbc.Button(
                    "Storm Profile",
                    color="link",
                    id="group-1-toggle",
                    n_clicks=0,
                )
            )
        ),
        dbc.Collapse(
            dbc.CardBody(["Select the checkbox or checkboxes to overlay. Indicate the time (in military hours) to display and submit.", stormProfileBoxes],
            style={'color':'black'}
            ),
            id="collapse-1",
            is_open=False,
            
        ),
    ]
)


affectedCommunities = dbc.Card([
        dbc.CardHeader(
            html.H2(
                dbc.Button(
                    "Affected Communities",
                    color="link",
                    id="group-2-toggle",
                    n_clicks=0,
                )
            )
        ),
        dbc.Collapse(
            dbc.CardBody(["This is the content of group...", affectedCommunitiesBoxes],
            style={'color':'black'}
            ),
            id="collapse-2",
            is_open=False,
        )
    ]
)




coastalRegions = dbc.Card([
        dbc.CardHeader(
            html.H2(
                dbc.Button(
                    "Coastal Regions",
                    color="link",
                    id="group-3-toggle",
                    n_clicks=0,
                )
            )
        ),
        dbc.Collapse(
            dbc.CardBody(["This is the content of group...", coastalRegionsBoxes],
            style={'color':'black'}
            ),
            id="collapse-3",
            is_open=False,
        )
    ]
)






floodAreas = dbc.Card([
        dbc.CardHeader(
            html.H2(
                dbc.Button(
                    "Flooded Areas",
                    color="link",
                    id="group-4-toggle",
                    n_clicks=0,
                )
            )
        ),
        dbc.Collapse(
            dbc.CardBody(["This is the content of group...", floodAreasBoxes],
            style={'color':'black'}
            ),
            id="collapse-4",
            is_open=False,
        )
    ]
)




#SIDE PANEL LAYOUT
sidePanel = html.Div([
        stormProfile,
        affectedCommunities,
    
        coastalRegions,

        floodAreas,
    
    ],
    className="accordion",
    style={"height":"85vh","overflow-x":"hidden","overflow-y":"visible"}
)


@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, 5)],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, 5)],
    [State(f"collapse-{i}", "is_open") for i in range(1, 5)]
)


def toggle_accordion(n1,n2,n3,n4,is_open1,is_open2,is_open3,is_open4):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False,False,False,False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1,False,False,False
    elif button_id == "group-2-toggle" and n2:
        return False,not is_open2,False,False,
    elif button_id == "group-3-toggle" and n3:
        return False,False,not is_open3,False
    elif button_id == "group-4-toggle" and n4:
        return False,False,False,not is_open4
    



#LEAFLET MAP HOLDER
mapPanel = dl.Map([dl.TileLayer(url=url, maxZoom=20, attribution=attribution)],
    bounds=phil_bound, id = 'Map',
                  center = (13,124),
)



#STATUS BAR LAYOUT
statusBar = html.Div([
    stormProfileDD,
    subButton,
    ],id ='stateBar',
    style={
        "background-color":"secondary",
        "width":"100vw",
        "height":"3vh",
        "position":"fixed",
        "bottom":"0px"
    }
)


#MAIN BODY LAYOUT
mainBody = html.Div([
        html.Div(sidePanel,style={"width":"30%"}),
        html.Div(mapPanel,style={
            "width":"70%",
            "position":"absolute",
            "height":"85vh",
            "top":"0vh",
            "right":"0px",
            "text-color": "black",
        })
    ],
    
)


@app.callback(
    dash.dependencies.Output('Map', 'children'),
    [dash.dependencies.Input('submit-button-1', 'n_clicks'),dash.dependencies.Input('Map', 'zoom')],
    [dash.dependencies.State('sideboxes-1','value'),
    dash.dependencies.State('dropdown-1','value'),dash.dependencies.State('sideboxes-6', 'value'),dash.dependencies.State('sideboxes-2', 'value'),
     dash.dependencies.State('sideboxes-4', 'value')
     ])

def update_output(n_clicks,zoom,value,hoursMinutes,flooded, communities, coastlines):
    array = [dl.TileLayer()]
    IRurl = updateIRLink(hoursMinutes)
    HRPurl = updateHRPLink(hoursMinutes)
    ctx = dash.callback_context
    if(value is not None and 'ir' in value):
         array.append(dl.ImageOverlay(opacity=0.3, url=IRurl, bounds=image_bounds))
    if(value is not None and 'hr' in value):
        array.append(dl.ImageOverlay(opacity=0.3, url=HRPurl, bounds=image_bounds))
    if(flooded is not None and 'floodDist' in flooded):
        array.append(dl.WMSTileLayer(url="https://sedac.ciesin.columbia.edu/geoserver/wms",
                                            layers="ndh:ndh-flood-hazard-frequency-distribution", format="image/png", transparent=True, opacity = 0.8))

    if(communities is not None and 'populationCount' in communities):
        array.append(dl.WMSTileLayer(url="https://sedac.ciesin.columbia.edu/geoserver/wms",
                                            layers="gpw-v3:gpw-v3-population-count-future-estimates_2015", format="image/png", transparent=True,opacity = 0.8))

    if(coastlines is not None and 'coastLines' in coastlines):
        array.append(dl.WMSTileLayer(url="https://sedac.ciesin.columbia.edu/geoserver/wms",
                                            layers="gpw-v3:gpw-v3-coastlines", format="image/png", transparent=True,opacity = 0.8))
    if(flooded is not None and 'floodFlow' in flooded and zoom is not None and zoom > 6):
        array.extend(list_polyline)

    return array









weatherBase = Weather_Database()





###### LOCAL DATA ################
temperature = [random.randrange(20,45)]
humidity = [random.randrange(60,90)]
pressure = [random.randrange(10,30)+1000]
wind = [random.randrange(0,10)]
water = [random.randrange(0,10)]
times = [int(datetime.datetime.utcnow().timestamp())]

times2 = [int(datetime.datetime.utcnow().timestamp())]
temperature2 = [random.randrange(20,45)]
humidity2 = [random.randrange(60,90)]
pressure2 = [random.randrange(180,230)+1000]
water2 = [random.randrange(0,10)]
wind2 = [random.randrange(0,10)]

times3 = [int(datetime.datetime.utcnow().timestamp())]
temperature3 = [random.randrange(20,45)]
humidity3 = [random.randrange(60,90)]
pressure3 = [random.randrange(180,230)+1000]
water3 = [random.randrange(0,10)]
wind3 = [random.randrange(0,10)]

averaged_data = []
averaged_data2 = []
averaged_data3 = []

#====AWS LOCATIONS====#
batangas = 1
qc = 2
caloocan = 3

#====DATA DICTIONARIES====#
data_dict = {'Temperature':temperature,
             'Humidity':humidity,
             'Pressure':pressure,
             'Wind Speed': wind,
             "Rainfall":water,
             "Date": times 
             }

data_dict2 = {'Temperature':temperature2,
             'Humidity':humidity2,
             'Pressure':pressure2,
              'Wind Speed': wind2,
              "Rainfall":water2,
              "Date": times2
             }
data_dict3 = {'Temperature':temperature3,
              'Humidity':humidity3,
              'Pressure':pressure3,
              'Wind Speed': wind3,
              "Rainfall":water3,
              "Date": times3
              }

data_loc = {'Batangas':data_dict,
            'Q.C':data_dict2,
            'Caloocan':data_dict3}



custom_tab = {
    'padding': '28px 10px',
    'backgroundColor': '#111111',
    'fontSize': '38px',
    'border': 'none',
    'height': '100px',
    'width': 'auto',
    'textAlign': 'center',
    'color': 'white'
   
}

custom_tab_selected = {
    'fontWeight': 'bold',
    'border': 'none',
    'backgroundColor':' Gray',
    'color': 'white',
    'padding': '28px 10px',
    'fontSize': '38px',
    'height': '100px',
    'width': 'auto'
}
#====WEBSITE LAYOUT====#
app.layout = html.Div(className="body", children=[
    #====HEADERS====#
    html.Div(className="div_header", children=[
        html.H1("Amongus"),
        html.H3("WEATHER ADVISORY SYSTEM"),
        
        ]),
    #====NAVIGATION====#
    html.Div(className="div_navigation", children=[
        dcc.Tabs(children=[
            dcc.Tab(label='HOME',value='home', style=custom_tab, selected_style=custom_tab_selected),
            dcc.Tab(label='ADVISORIES', value='advisories', style=custom_tab, selected_style=custom_tab_selected),
            
            dcc.Tab(label='STATIONS',value='stations',style=custom_tab,selected_style=custom_tab_selected),
            dcc.Tab(label='DATA REQUEST',value='dataReq',style=custom_tab,selected_style=custom_tab_selected),
            dcc.Tab(label='MAPS',value='mapsss',style=custom_tab,selected_style=custom_tab_selected),
            dcc.Tab(label='ABOUT',value='about', style=custom_tab, selected_style=custom_tab_selected)
            ],
            value='home',
            id="nav_bar"
            )
        ]),
    #====FOOTER====#
   
    
    #====MAIN CONTENT====#
    html.Div(className="div_maincontent", children=[
        #====HOME PAGE====#
        html.Div(children=[
            html.Div(id = "home",style={'display':'block'},children=[
                html.Img(src="/assets/1.jpg", width="100%"),
                
                html.Div(className="home_title_1", children=[
                    html.P("PROJECT Amongus;"),
                    html.Span("WEATHER ADVISORY SYSTEM"),
                    ]),
                
                html.Div(className="home_title_2", children=[
                    html.Span("WEATHER FORECASTS"),
                    ]),
                html.Div(className="forecast_section", children=[
                    html.P("""Lorems ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                            consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                            cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                            proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""),
                    html.Img(src="/assets/2.jpg", width="100%")
                    ]),

                
                html.Div(className="home_title_2", children=[
                    html.Span("WEATHER ADVISORIES"),
                    ]),
                html.Div(className="forecast_section", children=[
                    html.P("""Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                            consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                            cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                            proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""),
                    html.Img(src="/assets/2.jpg", width="100%")
                    ]),
                
                html.Div(className="home_title_2", children=[
                    html.Span("WEATHER STATIONS"),
                    ]),
                html.Div(className="forecast_section", children=[
                    html.P("""Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                            tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                            quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                            consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
                            cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                            proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""),
                    html.Img(src="/assets/2.jpg", width="100%")
                    ]),
                
            ]),

        #====ADVISORIES PAGE====# #ADVISORIES CONTAINER IS  ADSNATIN
        html.Div(children=[html.H1('Advisories'),dcc.Dropdown(
            className="Advisory",id="advisory-data-name",options=[{'label': s, 'value': s} for s in data_loc.keys()],value='Batangas',style={'color':'black'}),
			html.Div(id='Adsnatin',children=[])
                           ],id = "advisories",style={'display':'none','color':'black'}),

        

        html.Div(children = [], id = 'map-holder' ,style={'display':'none'}, className = 'map_content'),
        #===========DATA REQUEST====================# 
        html.Div(children = [
            dcc.Download(id = "download-csv"),
            dcc.DatePickerRange(
                id='date-pickers',
                min_date_allowed=datetime.date(2022, 1, 1),
                max_date_allowed=datetime.date(2023, 10, 1),
                initial_visible_month=datetime.date(2022, 9, 1),
                end_date=datetime.date(2022, 2, 2)
            ),
            dcc.Dropdown(className="data_reqs",id="data-reqs-data-name",options=[{'label': s, 'value': s} for s in data_loc.keys()], value = 'Batangas',style={'color':'black'})
            ,
            html.Div(children = [],
                     id = 'interval-container')],
                 id = "dataReqs", style = {'display':'none'}),

        #====STATIONS PAGE====#
        html.Div(children=[
            #====STATIONS LOCATION DROPDOWN====#
            dcc.Dropdown(className="station_location_dropdown", id='location-data-name', options=[{'label': s, 'value': s} for s in data_loc.keys()], value='Batangas', multi=False),
            #====STATIONS TITLE BLOCK====#
            html.Div(className="station_title", children=[
                html.P("Amongus WEATHER STATION"),
                html.Span("PAGASA SCIENCE GARDEN"),
                html.Br(),
                html.Span("QUEZON CITY")
                ]),
            #====Station Image====#
            html.Div(className="station_img", children=[
                html.Img(src="/assets/3.jpg", width="100%")
                ]),
            #====Graphs====#
            html.Div(id='graph_loc',children=[html.Div()])],id = "stations",style={'display':'none',}),

        #====ABOUT PAGE====#
       html.Div( children=[html.H1('About'),
            html.P("THE TEAM"),
            html.P("Meet the team behind this Project"),
            html.Br(),
            html.Br(),
            html.Div(className = "about-team", children=[
            html.Div([
            html.Div([
                html.Img(src="/assets/matthew.png", width="300px",height="300px"),
                html.P("Matthew Muralidharan",style={'color':'white'}),
           ]), 
            html.Div([
                html.Img(src="/assets/Iverson.jpg", width="300px",height="300px"),
                html.P("Jason Iverson Vinas",style={'color':'white'}),
            ]),  
            html.Div([
                html.Img(src="/assets/Albert.png", width="300px",height="300px"),
                html.P("Albert Pangan",style={'color':'white'}),
            ]), 
            html.Div([
                html.Img(src="/assets/pat.jpg", width="300px",height="300px"),
                html.P("Patrick Collera",style={'color':'white'}),
            ]), 
            html.Div([
                 html.Img(src="/assets/jer.png", width="300px",height="300px"),
                html.P("Jeremy Reuel Cesista",style={'color':'white'}),
            ]),
            ]),  
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Span("Amongus Team"),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
              ], ),
        ],id = "about")], className='main_content2'),
    ]),
    statusBar,
    #====GRAPH UPDATE INTERVAL====#
    dcc.Interval(id = "SensorValuesUpdate",interval = 8000),
    dcc.Interval(id="AdvisoryUpdate",interval = 1000*20),
    dcc.Interval(id="AveAllData",interval = 86404000), #interval is milliseconds
    html.Div(id="hidden_divs2",children = [],style ={'display':'none'}),
    html.Div(id="hidden_divs3",children = [],style ={'display':'none'}),
    dcc.Interval(id="MakePredictions",interval = 86404000),
    dcc.Interval(id = "UpdateDatass", interval = 4000),
    dcc.Interval(id = "DailyUpdate", interval = 86404000),
    html.Div(id='hidden_divs5', children = [], style = {'display':'none'}),
    dcc.Interval(id = "ClearLocalData", interval = 1000*60*60)
    

])



def scrape():
    html = requests.get('https://www.yr.no/nb/detaljer/tabell/2-1692192/Filippinene/Metro%20Manila/Eastern%20Manila%20District/Quezon%20City')
    soup = BeautifulSoup(html.content,'html.parser')
    row = soup.find('table','fluid-table__table').tbody.tr.find_all('td')
    features = ['Temp.','Feels like','Precipitation mm',
            'Wind m/s','Press hPa','Humidity %']
    data = {}
    for iter in range(2,8):
        feature = features[iter-2]
        if iter >= 6:
            value = soup.find('table','fluid-table__table').tbody.tr.find_all('td')[iter].span.span.text
        else:
            value = soup.find('table','fluid-table__table').tbody.tr.find_all('td')[iter].span.span.span.text
        value = value.replace('°','')
        value = value.replace(',','.')
        value = value.split(' ')[0]
        data[feature] = float(value)
    return data





def updateLoc(loc):
    date = int(datetime.datetime.utcnow().timestamp())
    data = scrape()
    humid_data = round((random.random()*0.5 + 1),2)*data['Humidity %']
    precip_data = round((random.random()*0.5 + 1),2)*data['Precipitation mm']
    press_data = round((random.random()*0.5 + 1),2)*data['Press hPa']
    temp_data = round((random.random()*0.5 + 1),2)*data['Temp.']
    wind_data = round((random.random()*0.5 + 1),2)*data['Wind m/s']
    weatherBase.uploadData(date, humid_data, precip_data,press_data, temp_data, wind_data, location = loc)



def updateLocalData():
    weatherDict = weatherBase.getData(limit = 50)
    for s in data_loc.keys():
        for i in range(len(weatherDict[s][0])):
            if(data_loc[s]["Date"][-1] >= weatherDict[s][0][i]):
                continue
            
            data_loc[s]["Date"].append(weatherDict[s][0][i])
            data_loc[s]["Humidity"].append(weatherDict[s][1][i])
            data_loc[s]["Rainfall"].append(weatherDict[s][2][i])
            data_loc[s]["Pressure"].append(weatherDict[s][3][i])
            data_loc[s]["Temperature"].append(weatherDict[s][4][i])
            data_loc[s]["Wind Speed"].append(weatherDict[s][5][i])
            

    
#=====HELPER FUNCS=========#


@app.callback(Output('hidden_divs5', 'children'),
              [Input('ClearLocalData', 'n_intervals')])
def clear_data(vals):

    for i in data_loc.values():
        for j in i.values():
            if(len(j) > 100):
                del j[:-40]
    return html.Div([])

@app.callback(Output('interval-container', 'children'),
              [Input('date-pickers', 'start_date'),
               Input('date-pickers', 'end_date'),
               Input('data-reqs-data-name', 'value')])
def getInterval(start_date, end_date, location):
    class_choice = 'col s12'
    if start_date is None or end_date is None:
        return html.H1("Please Select a Date To Print out the Graph")

    start_date_object = datetime.datetime.combine(datetime.date.fromisoformat(start_date), datetime.datetime.min.time())
    end_date_object = datetime.datetime.combine(datetime.date.fromisoformat(end_date), datetime.datetime.min.time()) + datetime.timedelta(hours = 23, minutes = 59, seconds = 59) 
    timestampStart = int(start_date_object.timestamp())
    timestampEnd = int(end_date_object.timestamp())
    dictionary = weatherBase.getByDayDate(timestampStart,timestampEnd)
    
    if(location not in dictionary):
        return html.H1("No Data Available")
    dictionaryRefactor = {"Humidity": dictionary[location][1],
                          "Rainfall": dictionary[location][2],
                          "Pressure": dictionary[location][3],
                          "Temperature": dictionary[location][4],
                          "Wind Speed": dictionary[location][5],
                          }
    data_dict = dictionaryRefactor
    times = dictionary[location][0]
    graphs = []
    graphs.append(html.Button("Download CSV", id = "btn_csv", n_clicks = 0, style ={'color': 'black','background-color':'white'}))
    
    for data_name in data_dict.keys():
        if(data_name == "Date"):
            continue
        graphs.append(html.H1(data_name))
        min_val = "Min: " + str(min(data_dict[data_name]))
        graphs.append(html.H1(min_val))
        max_val = "Max: " + str(max(data_dict[data_name]))
        graphs.append(html.H1(max_val))
        ave_val = "Ave: " + str(sum(data_dict[data_name])/len(data_dict[data_name]))
        graphs.append(html.H1(ave_val))
        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='actual',
            marker = dict(color = 'red')
            )
       
        graphs.append(html.Div(dcc.Graph(
            id=data_name + str('interval'),
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                            yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                            margin={'l':50,'r':1,'t':45,'b':1},
                                            title='{}'.format(data_name),
                                            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')}
                ), className=class_choice))
	
	
               
    return graphs


@app.callback(Output('download-csv', 'data'),
              State('date-pickers', 'start_date'),
               State('date-pickers', 'end_date'),
               State('data-reqs-data-name', 'value'),
               Input("btn_csv", "n_clicks"),
              prevent_initial_call = True)
def download_csv(start_date, end_date, location, n_clicks):
    if(n_clicks == 0):
        return None
    start_date_object = datetime.datetime.combine(datetime.date.fromisoformat(start_date), datetime.datetime.min.time())
    end_date_object = datetime.datetime.combine(datetime.date.fromisoformat(end_date), datetime.datetime.min.time()) + datetime.timedelta(hours = 23, minutes = 59, seconds = 59) 
    timestampStart = int(start_date_object.timestamp())
    timestampEnd = int(end_date_object.timestamp())
    dictionary = weatherBase.getByDayDate(timestampStart,timestampEnd)
    
    if(location not in dictionary):
        return None
    dictionaryRefactor = {"Humidity": dictionary[location][1],
                          "Rainfall": dictionary[location][2],
                          "Pressure": dictionary[location][3],
                          "Temperature": dictionary[location][4],
                          "Wind Speed": dictionary[location][5],
                          }

    strContent = "Date, Humidity, Rainfall, Pressure, Temperature, Wind Speed"
    times = dictionary[location][0]
    for i in range(len(times)):
        strContent += "\n"
        strContent += str(datetime.datetime.fromtimestamp(times[i])) + "," + str(dictionaryRefactor["Humidity"][i]) + "," + str(dictionaryRefactor["Rainfall"][i]) \
                      + "," + str(dictionaryRefactor["Pressure"][i]) + "," + str(dictionaryRefactor["Temperature"][i]) + "," + str(dictionaryRefactor["Wind Speed"][i])
    return dict(content = strContent, filename = start_date + "_" + end_date +"_" + location + ".csv")

@app.callback(Output('date-pickers', 'max_date_allowed'),
              [Input('DailyUpdate', 'n_intervals')])
def updateDatePicker(interval):
    return datetime.datetime.utcnow()
    
@app.callback(Output('hidden_divs3', 'children'),
              [Input('UpdateDatass', 'n_intervals')])
def updateDatabse(val):
    for s in data_loc.keys():
        updateLoc(s)
    return html.H1("Hellos")

#====NAVIGATION CALLBACKS=====#



@app.callback(Output('map-holder','style'),
              Output('map-holder','children'),
              Output('stateBar','style'),
              [Input('nav_bar','value')])
def show_maps(my_input):
    if my_input == 'mapsss':
        return {'display':'block',"overflow":"hidden"}, mainBody,{
        "background-color":"secondary",
        "width":"100vw",
        "height":"3vh",
        "position":"fixed",
        "bottom":"0px"
    }
    else:
        return {'display':'none'}, html.Div(),{'display':'none'}

    
@app.callback(Output('home','style'),
              [Input('nav_bar','value')])
def show_home(my_input):
    if my_input == 'home':
        return {'display':'block'}
    else:
        return {'display':'none'}

@app.callback(Output('advisories','style'),
              [Input('nav_bar','value')])
def show_ads(my_input):
    if my_input == 'advisories':
        return {'display':'block'}
    else:
        return {'display':'none'}



@app.callback(Output('stations','style'),
              [Input('nav_bar','value')])
def show_stations(my_input):
    if my_input == 'stations':
        return {'display':'block'}
    else:
        return {'display':'none'}

@app.callback(Output('about','style'),
              [Input('nav_bar','value')])
def show_about(my_input):
    if my_input == 'about':
        return {'display':'block'}
    else:
        return {'display':'none'}

@app.callback(Output('dataReqs','style'),
              [Input('nav_bar','value')])
def show_req(my_input):
    if my_input == 'dataReq':
        return {'display':'block'}
    else:
        return {'display':'none'}





    
    


    
    


            
                
                  
        
####### ADVISORIES RETURN BLOCK ##########
@app.callback(Output('Adsnatin','children'),
              [Input('advisory-data-name','value'),Input('AdvisoryUpdate','n_intervals')])
def show_adss(location, val):

    ads = []
    data_dictHour = weatherBase.getDataByHour(datetime.datetime.utcnow(), interval = 1)
    data_dictDay = weatherBase.getAverageDataByDay(datetime.datetime.utcnow(), interval = 4, currentDay = True)
    

    ads.append(html.Div(html.H1("Beaufort Reading: " + advisory_in_beaufort(data_loc[location]["Wind Speed"][-1])),id="Temp_ad"))
    if(location not in data_dictHour):
        ads.append(html.Div(html.H1("Can't Generate Rain Data No Values to Base On")))
    else:
        ads.append(html.Div(html.H1("Rain Advisory: " + rain_advisories(data_dictHour[location][2][-1])),id="Rain_ad"))
    if(len(data_dictDay[location][0]) != 5):
        ads.append(html.H1("Not enough data points To Predict Rain for Tomorrow"))
    averaged_data = helperAverageData(data_dictDay[location])
    averaged_data = function_to_scale(averaged_data)
    
    cop = predict_weather(averaged_data)
    if cop[0][0] >=0.5:
        ads.append(html.H1("Chance of Rain Tomorrow is High about:"+str(cop[0][0]*100)))
    else:
        ads.append(html.H1("Chance of Rain Tomorrw is Low about:"+str(cop[0][0]*100)))
    
    ads.append(html.Div(html.H1("Heat Index Reading(How the Heat Feels): " + heat_danger(data_loc[location]["Humidity"][-1],data_loc[location]["Temperature"][-1])),id="Heat_I"))
    ads.append(html.Img(src='/assets/Beaufort-Wind-Scale-948x1024.jpeg', width="948px",height="1024px"))
    return ads
        
        

#====LIVE GRAPHS====#
@app.callback(Output('graph_loc','children'),
              [Input('location-data-name','value'), Input('SensorValuesUpdate','n_intervals')])
def show_graphs(loc_name, val):
    updateLocalData()
    graphs = []
    class_choice = 'col s12'
    data_dict = data_loc[loc_name]
    times = data_dict["Date"]
    for data_name in data_dict.keys():
        if(data_name == "Date"):
            continue
        graphs.append(html.H1(data_name))
        min_val = "Min: " + str(min(data_dict[data_name][-20:]))
        graphs.append(html.H1(min_val))
        max_val = "Max: " + str(max(data_dict[data_name][-20:]))
        graphs.append(html.H1(max_val))
        ave_val = "Ave: " + str(sum(data_dict[data_name][-20:])/len(data_dict[data_name][-20:]))
        graphs.append(html.H1(ave_val))
        x_data = np.array(times[-20:]).reshape(len(times[-20:]),-1)
        x_data = (x_data - min(times[-20:]))/(max(times[-20:]) - min(times[-20:]))
        y_data = np.array(data_dict[data_name][-20:]).reshape(len(data_dict[data_name][-20:]),-1)
        y_data = (y_data-min(data_dict[data_name][-20:]))/(max(data_dict[data_name][-20:]) - min(data_dict[data_name][-20:]))
        m, b = linearRegression1d(x_data, y_data)
        new_yvals = np.matmul(x_data,m) + b
        new_yvals = new_yvals*(max(data_dict[data_name][-20:]))
        new_yvals = new_yvals.reshape(-1)
        listOfNewYs = new_yvals.tolist()
        data = go.Scatter(
            x=list(times[-20:]),
            y=list(data_dict[data_name][-20:]),
            name='actual',
            marker = dict(color = 'red')
            )
        
        data2 = go.Scatter(
            x=list(times[-20:]),
            y=listOfNewYs,
            name='predicted',
            marker = dict(color = 'green')
            )
        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data,data2],'layout' : go.Layout(xaxis=dict(range=[min(times[-20:]),max(times[-20:])]),
                                            yaxis=dict(range=[min(min(data_dict[data_name][-20:]), min(new_yvals)),max(max(data_dict[data_name][-20:]), max(new_yvals))]),
                                            margin={'l':50,'r':1,'t':45,'b':1},
                                            title='{}'.format(data_name),
                                            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')}
                ), className=class_choice))
	
    
    graphs.append(html.Div('\n\n\n\n\n\n\n\n\n'))           
    return graphs

#needed database size

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

#====CALL FUNCTION====#
app.serve_locally = True

if __name__ == '__main__':
    app.run_server(debug=True)
