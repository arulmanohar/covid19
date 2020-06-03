x=[]
y=[]
y1=[]
y2=[]
y3=[]
dic = {'x':x,'nifty 50':y,'nifty bank':y1, 'FTSE':y2,'FTSE MIB':y3}
#df=pd.DataFrame(dic)
source = ColumnDataSource(data=dic)
p = figure(plot_width=400, plot_height=400,title="Nifty 50 points")
p.line(x='x',y='nifty 50', line_width=2,source = source, color = 'violet')
p.xgrid.visible=False
p.ygrid.visible=False
p.title.align = "center"
p.title.text_font_size = "15px"
p.title.text_font_style='bold'
p1 = figure(plot_width=400, plot_height=400,title="Nifty Bank")
p1.line(x='x',y='nifty bank', line_width=2,source = source, color = 'darkblue')
p1.xgrid.visible=False
p1.ygrid.visible=False
p1.title.align = "center"
p1.title.text_font_size = "15px"
p1.title.text_font_style='bold'
p2 = figure(plot_width=400, plot_height=400,title="FTSE UK STOCK MARKET")
p2.line(x='x',y='FTSE', line_width=2,source = source, color = 'red')
p2.xgrid.visible=False
p2.ygrid.visible=False
p2.title.align = "center"
p2.title.text_font_size = "15px"
p2.title.text_font_style='bold'
p3 = figure(plot_width=400, plot_height=400,title="FTSE MIB ITALY STOCK MARKET")
p3.line(x='x',y='FTSE MIB', line_width=2,source = source, color = 'darkgreen')
p3.xgrid.visible=False
p3.ygrid.visible=False
p3.title.align = "center"
p3.title.text_font_size = "15px"
p3.title.text_font_style='bold'
#print(dic)
def update():
    x=[]
    y=[]
    y1=[]
    y2=[]
    y3=[]
    url="https://www.nseindia.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    nse = requests.get(url, headers=headers).text
    nse_soup = BeautifulSoup(nse,"lxml")
    value=nse_soup.find('a', href = "#NIFTY 50").find('p', class_="tb_val").text
    value = re.sub(r',', "",value)
    value=float(value.strip())
    name=nse_soup.find('a', href = "#NIFTY 50").find('p', class_="tb_name").text
    value1=nse_soup.find('a',href="#NIFTY BANK").find('p', class_="tb_val").text
    name1 = nse_soup.find('a',href="#NIFTY BANK").find('p', class_="tb_name").text
    value1 = re.sub(r',', "",value1)
    value1=float(value1.strip())
    #url="https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/ftse-indices.html"
    #lse = requests.get(url, headers=headers).text
    #lse_soup = BeautifulSoup(lse,"lxml")
    #name2=lse_soup.find_all("table", class_="table_dati")[0].find_all('td')[0].text
    #name2=name2.strip()
    #value2=lse_soup.find_all("table", class_="table_dati")[0].find_all('td')[1].text
    #value2 = re.sub(r',', "",value2)
    #value2=float(value2)
    #url="https://www.borsaitaliana.it/borsa/azioni/tutti-gli-indici.html?lang=en"
    #headers = {'User-Agent': 'Mozilla/5.0'}
    #ise = requests.get(url, headers=headers).text
    #ise_soup = BeautifulSoup(ise,"lxml")
    #value3=ise_soup.find_all('span', class_="t-text -center")[8].text
    #value3 = re.sub(r',', "",value3)
    #value3=float(value3)
    #display.clear_output(wait=True)
    i=len(source.data['x'])+1
    x.append(i)
    y.append(value)
    y1.append(value1)
    #y2.append(value2)
    #y3.append(value3)
    new_data = {'x':x,'nifty 50':y,'nifty bank':y1,'FTSE':y1,'FTSE MIB':y1}
    print(source.data)
    source.stream(new_data)
    
    
curdoc().add_root(row(p,p1,p2,p3))
curdoc().add_periodic_callback(update, 5000)
curdoc().title = "LURA"