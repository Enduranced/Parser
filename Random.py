import bs4  
import urllib
from dash_core_components.Graph import Graph
import requests
import pandas as pd

def finder(tick):
    url = "https://finance.yahoo.com/quote/"+tick+"/holders?p="+tick
    cont = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(cont, "lxml")
    table1 = soup.find_all("table", {"class":"W(100%) M(0) BdB Bdc($seperatorColor)"})
    table2 = soup.find_all("table", {"class":"W(100%) BdB Bdc($seperatorColor)"})

    ##############Creating the dataframe#############################################
    #### 1 st table#############################
    for i in table1:
        x = i.find_all('td',{"class":"Py(10px) Va(m) Fw(600) W(15%)"})
        y = i.find_all('td',{"class":"Py(10px) Ta(start) Va(m)"})
    no = {}
    for (i,j) in zip(x,y):
        no[j.string] = i.string

    ######## 2 nd table######################
    for i in table2[0]:
        a = i.find_all('td',{"class":"Ta(start) Pend(10px)"})
        b = i.find_all('td',{"class":"Ta(end) Pstart(10px)"})


    tag = []
    for i in b:
        tag.append(i.string)
    blitz = []
    for i in range(0,len(b),4):
        blitz.append(tag[i])
        
    yes = {}
    for (i,j) in zip(a,blitz):
        yes[i.string] = j

    ############3 rd table####################
    for i in table2[1]:
        s = i.find_all('td',{"class":"Ta(start) Pend(10px)"})
        p = i.find_all('td',{"class":"Ta(end) Pstart(10px)"})

    wanted = []
    for i in p:
        wanted.append(i.string)
    split = []
    for i in range(0,len(p),4):
        split.append(wanted[i])
    maybe = {}
    for (i,j) in zip(s,split):
        maybe[i.string] = j

            
    one = pd.DataFrame({"Name":no.keys(), "Values":no.values()})
    two = pd.DataFrame({"Name":yes.keys(), "Values":yes.values()})
    three = pd.DataFrame({"Name":maybe.keys(), "Values":maybe.values()})

    alt = [one, two ,three]
    return {tick:alt}

#####################Creating the Dashly##########################
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.title = "Dashboard for current holdings"

#----------------------------------------------------------------------------------------------------
# @                @          @          @        @     @@@@@@@@@@@@@@     @         @   @@@@@@@@@@@@ 
# @               @ @         @           @      @      @            @     @         @        @
# @              @   @        @             @   @       @            @     @         @        @
# @             @     @       @               @         @            @     @         @        @
# @            @ @@@@@ @      @               @         @            @     @         @        @
# @           @         @     @               @         @            @     @         @        @  
# @@@@@@@@   @           @    @@@@@@@@@       @         @@@@@@@@@@@@@@     @@@@@@@@@@@        @ 
# ---------------------------------------------------------------------------------------------------


app.layout = html.Div([
    html.H1(id = "StockTicker",
    {"label": "BABA", "value": "BABA"},
    {"label": "PLTR", "value": "PLTR"},
    multi = False,
    value = "BABA"
    style = {"width": "60%"}
    ),
    html.Div(id='output_container'),
    dcc.Graph(id="Table1"),
    html.Div([dcc.Graph(id="Table2"), dcc.Graph(id="Table2")])
])


@app.callback(
    [Output(component_id="output_container", component_property="children"),
    Output(component_id="Table1", component_property="figure"),
    Output(component_property="Table2", component_property="figure"),
    Output(component_property="Table3", component_property="figure")],
    [Input(component_property="StockTicker", component_property="value")]
)






def update_graph(option):
     container = "The ticker chosen by user is: {}".format(option)
     data = finder(option)
     print(data)
     fig1 = 






































def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == '__main__':
    Timer(2,open_browser).start();
    app.run_server(debug=True)