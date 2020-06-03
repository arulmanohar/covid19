import requests 
from bs4 import BeautifulSoup 
#from tabulate import tabulate 
import os 
import numpy as np 
#import matplotlib.pyplot as plt 
from bokeh.layouts import widgetbox, column,row
from bokeh.models import  LabelSet,ColumnDataSource,Text

extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'
	
SHORT_HEADERS = ['SNo', 'State','Active','Cured','Death','Indian-Confirmed(Including Foreign Confirmed)'] 
	
response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 
#header = extract_contents(soup.tr.find_all('th')) 

stats = [] 
all_rows = soup.find_all('tr') 

for row in all_rows: 
	stat = extract_contents(row.find_all('td')) 
	
	if stat: 
		if len(stat) == 5: 
			# last row 
			stat = ['', *stat] 
			stats.append(stat) 
		elif len(stat) == 6: 
			stats.append(stat) 

#stats[-1][0] = len(stats) 
#stats[-1][1] = "Total Cases"
objects = [] 
for row in stats : 
	objects.append(row[1]) 
	
#y_pos = np.arange(len(objects)) 

#table = tabulate(stats, headers=SHORT_HEADERS) 

performance = [] 
for row in stats[:len(stats)-2] : 
    performance.append(int(row[5]))

performance1 = [] 
for row in stats[:len(stats)-2] : 
    performance1.append(int(row[3])) 

performance2 = [] 
for row in stats[:len(stats)-2] : 
    performance2.append(int(row[4])) 
    
performance3 = [] 
for row in stats[:len(stats)-2] : 
    performance3.append(int(row[2]))

import pandas as pd
df = pd.DataFrame(list(zip(objects,performance,performance3,performance1,performance2)),columns =['states','cases','active','cured','death'])

from bokeh.io import show
from bokeh.models import ColumnDataSource,LabelSet
from bokeh.palettes import Category10
from bokeh.plotting import figure,output_notebook,output_file
from bokeh.models.tools import HoverTool
from bokeh.palettes import Turbo256,linear_palette,Inferno256
from bokeh.io import curdoc
import math
from bokeh.io import curdoc
from bokeh.plotting import figure, show, ColumnDataSource,output_notebook
from bokeh.models import RangeSlider,HoverTool
from bokeh.layouts import widgetbox, column, row
from bokeh.palettes import Greys256,Inferno256,Magma256,Plasma256,Viridis256,Cividis256,Turbo256,linear_palette

x = df['states'].tolist()
y = df['cases'].tolist()
d=len(x)
def changeArea(attr, old, new):
    scale1 = slider.value[0]
    scale2 = slider.value[1]
    dd=len(df.loc[df['cases'].between(scale1,scale2), 'states'])
    new_data = {
        'states' : df.loc[df['cases'].between(scale1,scale2), 'states'],
        'cases'    : df.loc[df['cases'].between(scale1,scale2), 'cases'],
        'colors'  : linear_palette(Turbo256,dd)
    }
    sources.data = new_data
sources = ColumnDataSource(data={'states': x, 'cases': y,'colors': linear_palette(Turbo256,d)})    
plot = figure(x_range=x,plot_height=450,plot_width=1300)

slider = RangeSlider(title='State_wise Slider', start=1, end=100000, step=1, value=(1,100000),bar_color="skyblue")
slider.on_change('value', changeArea)

plot.vbar(x='states',top= 'cases',width=0.7,fill_color='colors', source=sources)
hover=HoverTool(tooltips=([('State','@states'),('Confirmed cases','@cases')]))
plot.add_tools(hover)
plot.y_range.start = 0
plot.xaxis.major_label_orientation = math.pi/2
plot.ygrid.visible=False
plot.xgrid.visible=False
plot.title.text="Confirmed Corona cases in India - State_wise"
plot.title.align = "center"
plot.title.text_font_size = "20px"
#layout = column(widgetbox(slider),plot)
#output_notebook()
#show(layout)
#curdoc().add_root(layout)


state_list = df['states'].tolist()
cured_count =df['cured'].tolist()
color1=linear_palette(Inferno256,35)
data = {'address' : state_list,
        'counts' :  cured_count,
        'colors' : color1}
source = ColumnDataSource(data=data)
p = figure(x_range=state_list, plot_height=450, title="Cured Corona cases in India - State_wise",
           toolbar_location='right', tools="zoom_in,zoom_out,reset,save,pan",plot_width=1300)
p.line(state_list, cured_count, line_width=3,color='navy')
a=p.annulus(x=state_list, y=cured_count, inner_radius=0.1, outer_radius=0.25,color=color1, alpha=0.8)
p.y_range.start = -1000
p.xgrid.visible = False
p.ygrid.visible = False
p.axis.minor_tick_line_color = None
p.title.align = "center"
p.title.text_font_size = "20px"
p.xaxis.major_label_orientation = math.pi/2

hover=HoverTool(tooltips=([('State','@x'),('Cured Cases','@y')]))
p.add_tools(hover)


from bokeh.palettes import Turbo256,linear_palette,Viridis256
state_list = df['states'].tolist()
death_count =df['death'].tolist()
color1=linear_palette(Viridis256,35)
data1 = {'state' : state_list,
        'counts'   :  death_count,
        'colors' : color1}
source1 = ColumnDataSource(data=data1)
p1 = figure(x_range=state_list, plot_height=450, title="Corona Death cases in India - State_wise",
           toolbar_location='right', tools="zoom_in,zoom_out,reset,save,pan",plot_width=1300)
p1.segment(state_list,-100, state_list,death_count, line_width=3, line_color="black", alpha=0.8 )
a=p1.circle(x=state_list,y= death_count, size=15, fill_color=color1, line_color="black", line_width=2 )
p1.xgrid.visible = False
p1.ygrid.visible = False
p1.axis.minor_tick_line_color = None

hover=HoverTool(tooltips=([('State','@x'),('Death Cases','@y')]),renderers=[a])
p1.add_tools(hover)
p1.y_range.start = -100
p1.title.align = "center"
p1.title.text_font_size = "20px"
p1.xaxis.major_label_orientation = math.pi/2

x = df["states"].tolist()
y = df["active"].tolist()
p3= figure(x_range=x,plot_width=1300, plot_height=450)
a=p3.diamond(x=x,y= y, size=17, fill_color=linear_palette(Inferno256,35), line_color="black", line_width=2, )
p3.step(x, y, line_width=2, mode="after",color="black")
hover=HoverTool(tooltips=([('State','@x'),('Active Cases','@y ')]),renderers=[a])
p3.title.text="Corona Active cases in India - State_wise"
p3.title.align = "center"
p3.title.text_font_size = "20px"
p3.xaxis.major_label_orientation = math.pi/2
p3.ygrid.visible=False
p3.xgrid.visible=False
p3.add_tools(hover)

from bokeh.models.widgets import Paragraph,DataTable, TableColumn
df4=df.sort_values(by=['cases'], ascending=False)
source5 = ColumnDataSource(df4)
columns = [
    TableColumn(field="states", title='States'),
    TableColumn(field="cases", title='Confirmed Cases'),
    TableColumn(field="active", title='Active Cases'),
    TableColumn(field="cured", title='Cured Cases'),
    TableColumn(field="death", title='Death cases')
    ]
p6= DataTable(source=source5, columns=columns, width=1300, height=625)


sum1=df['cases'].sum()
sum2=df['cured'].sum()
sum3=df['death'].sum()
a_case=df['active'].sum()
a1_case=soup.find('li', class_ = "bg-blue").find('span').text
s1=str(sum1)
s2=str(sum2)
s3=str(sum3)
s4=str(a_case)
nn=['Total Confirmed Cases in India',a1_case,'Total Cured Cases in India','Total Death Cases in India']
mm=[s1,s4,s2,s3]
source3 = ColumnDataSource(dict(
    t=[2,2,2,2],
    b=[1,1,1,1],
    l=[1,2,3,4],
    r=[2,3,4,5],
    color=['orange','navy','green','red'],
    label=['Total Confirmed Cases in India',a1_case,'Total Cured Cases in India','Total Death Cases in India'],
    lx=[1.05,2.05,3.05,4.05],
    ly=[1.75,1.75,1.75,1.75],
    lx2=[1.4,2.4,3.4,4.4],
    ly2=[1.2,1.2,1.2,1.2],
    label2=mm,
))
p4 = figure(x_range=(1, 5), y_range=(1,2), plot_height=100, plot_width=1300,tools="",toolbar_location=None)
p4.quad(top='t', bottom='b', left='l',right='r',color='color',source=source3)
labels = LabelSet(x='lx', y='ly', text='label',x_offset=0,y_offset=0,
               source=source3, render_mode='canvas',text_font_size="20px",text_color="white")
labels2 = LabelSet(x='lx2', y='ly2', text='label2',x_offset=0,y_offset=0,
               source=source3, render_mode='canvas',text_font_size="40px",text_color="white")
p4.axis.visible = None
p4.xgrid.visible = False
p4.ygrid.visible = False
p4.add_layout(labels)
p4.add_layout(labels2)
#output_notebook()
#show(p4)

updatedon=soup.find('div', class_="status-update").find('h2').text

nn=[updatedon]
source4 = ColumnDataSource(dict(
    t=[2],
    b=[1],
    l=[1],
    r=[2],
    color=['skyblue'],
    label=nn,
    lx=[1.18],
    ly=[1.2]
))
p5 = figure(x_range=(1, 2), y_range=(1,2), plot_height=75, plot_width=1300,tools="",toolbar_location=None)
p5.quad(top='t', bottom='b', left='l',right='r',color='color',source=source4)
labels = LabelSet(x='lx', y='ly', text='label',x_offset=0,y_offset=0,
               source=source4, render_mode='canvas',text_font_size="30px",text_color="white")
p5.axis.visible = None
p5.xgrid.visible = False
p5.ygrid.visible = False
p5.add_layout(labels)
#p4.add_layout(labels2)
#output_file('c.html')
#show(p5)

layout=column(p5,p4,widgetbox(slider),plot,p,p1,p3,p6)
#output_file('coco.html')
#show(layout)
curdoc().add_root(layout)
