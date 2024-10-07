import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import os
import pandas as pd
import app_core
import plotly
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import pandas as pd
import json
import pymysql
from flask import Flask, render_template,flash,redirect,url_for
import yfinance as yf
import math

from finta import TA as ta
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta
app = Flask(__name__)
#app.secret_key=config.get('flask','secret key')
app.config['SECRET_KEY']='hellostockbot'

def pic(id,width,picday): 
    ticker = str(id)+".TW"
    p2= datetime.strptime(picday, '%Y-%m-%d')       
    a_m =p2  - timedelta(days=58)
    x= a_m.strftime('%Y-%m-%d')
    df = yf.download(ticker,x)
    data=pd.DataFrame()
    data['Open']=df['Open']
    data['High']=df['High']
    data['Low']=df['Low']
    data['Close']=df['Close']
    data['Volume']=df['Volume']
    data['Adj Close']=df['Adj Close']
    data['MA5'] = ta.SMA(df, 5)
    data['MA10'] = ta.SMA(df, 10)
    data['MA20'] = ta.SMA(df, 20)
    data['RSI5'] = ta.RSI(df, 5)
    data['RSI10'] = ta.RSI(df, 10)
    data['k'] = ta.STOCH(df)
    data['d'] = ta.STOCHD(df)
    data['CCI'] = ta.CCI(df)
    data['ADX'] = ta.ADX(df)
    data['DMP'] = ta.DMI(df, 14, True)["DI+"]
    data['DMN'] = ta.DMI(df, 14, True)["DI-"]
    data['AO'] = ta.AO(df)
    data['MOM10'] = ta.MOM(df,10)
    MACD = ta.MACD(df)
    data['DIF'] = MACD.MACD
    data['MACD'] = MACD.SIGNAL
    data['DIF-MACD'] = data['DIF'] - data['MACD']
    data['WILL10'] = ta.WILLIAMS(df, 10)
    data['UO'] = ta.UO(df)
    data = data.dropna(axis=0, how='any')
    colors = ['red' if data['Open'] - data['Close'] >= 0 
        else 'green' for index, data in data.iterrows()]
    fig = go.Candlestick(x=data.index, xaxis='x1',
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                increasing_line_color='red',
                                decreasing_line_color='green',
                                    # showlegend=False
                                )
    fig1=go.Scatter(x=data.index,  xaxis='x1',
                                        y=data['MA5'], 
                                        opacity=0.7, 
                                        
                                        line=dict(color='#2894FF', width=2), 
                                        name='5日均線')
    fig2=go.Scatter(x=data.index, xaxis='x1',
                        
                                        y=data['MA10'], 
                                        opacity=0.7, 
                                        line=dict(color='orange', width=2), 
                                        name='10日均線')
    fig3=go.Scatter(x=data.index,xaxis='x1',
                                        y=data['MA20'], 
                                        opacity=0.7, 
                                        line=dict(color='pink', width=2), 
                                        name='20日均線')
        
    fig4=go.Scatter(x=data.index,  xaxis='x3',
                                        yaxis='y3',
                                        y=data['RSI10'], 
                                        opacity=0.7, 
                                        line=dict(color='#01ACBD', width=2), 
                                        name='RSI10')
    fig5=go.Scatter(x=data.index,  xaxis='x3',
                                        yaxis='y3',
                                        y=data['RSI5'], 
                                        opacity=0.7, 
                                        line=dict(color='#867182', width=2), 
                                        name='RSI5')
        
    fig6=go.Scatter(x=data.index,  xaxis='x4',
                                        yaxis='y4',
                                        y=data['k'], 
                                        opacity=0.7, 
                                        line=dict(color='#E6AECF', width=2), 
                                        name='k')
        
    fig7=go.Scatter(x=data.index,  xaxis='x4',
                                        yaxis='y4',
                                        y=data['d'], 
                                        opacity=0.7, 
                                        line=dict(color='#7F9871', width=2), 
                                        name='d')
        
        
    fig8=go.Scatter(x=data.index,  xaxis='x5',
                                        yaxis='y5',
                                        y=data['DIF'], 
                                        opacity=0.7, 
                                        line=dict(color='#7F9871', width=2), 
                                        name='DIF快線')
        
        
    fig9=go.Scatter(x=data.index,  xaxis='x5',
                                        yaxis='y5',
                                        y=data['MACD'], 
                                        opacity=0.7, 
                                        line=dict(color='#FFA289', width=2), 
                                        name='MACD慢線')
        
    fig10=go.Bar(x=data.index,  xaxis='x5',
                                        yaxis='y5',
                                        y=data['DIF-MACD'], 
                                        opacity=1,
                                        marker=dict(color=colors),
                                        name='DIF-MACD')
        
    fig11=go.Bar(x=data.index,  xaxis='x6',
                                        yaxis='y6',
                                        opacity=1,
                                        y=data['Volume'], 
                                        marker=dict(color=colors),
                                        name='成交量')

    color1 = '#00bfff'
    color2 = '#ff4000'
    color3='#800080'
    # data = [fig,fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10,fig11]
    data = [fig,fig1,fig2,fig3]
    # data2 = [fig4,fig5,fig6,fig]
    layout = go.Layout(
        dict(width=390,height=600),
            title= '',
                titlefont=dict(
                
                family='Courier New, monospace',
                size=15,
                
                
                color='#7f7f7f'
                ),
                xaxis1  =
                dict( 
                    
                    tickfont=dict(
                        color='#7f7f7f',size=8, 
                    
                    )
                ),   
                #paper_bgcolor='rgba(0,0,0,0)',
                #plot_bgcolor='rgba(0,0,0,0)',

                yaxis=dict(
                domain=[0.8,1],
                    title='股價',
                    titlefont=dict(
                        color='#7f7f7f'
                    ),
                    tickfont=dict(
                        color='#7f7f7f',size=8, 
        
                    )
                ),
            
                xaxis3=
                dict( 
                    anchor='y3',     
                
                    side='left',
                    titlefont=dict(
                        color='#7f7f7f'
                    ),
                    tickfont=dict(
                        color='#7f7f7f',size=8, 
                    
                    )
                ),
                
                yaxis3=
                dict(
                    title='RSI',
                    domain=[0.21,0.35],
                    anchor='x3',
                    side='left',
                    titlefont=dict(
                        color='#7f7f7f'
                    ),
                    tickfont=dict(
                        color='#7f7f7f'
                    
                    )

                ),
                xaxis4=
                dict( 
                    anchor='y4',        
                    side='left',
                    titlefont=dict(
                        color='#7f7f7f'
                    ),
                    tickfont=dict(
                        color='#7f7f7f',size=8, 
                    
                    )
                ),
                
                yaxis4=
                dict( 
                    title='KD',
                    anchor='x4',  
                    domain=[0.42,0.53],         
                    side='left',
                    titlefont=dict(
                        color='#7f7f7f'
                    ),
                    tickfont=dict(
                        color='#7f7f7f'
                    
                    )
                ),
                
                xaxis5=
                dict( 
                    anchor='y5',        
                    side='left',
                    titlefont=dict(
                        color='#7f7f7f'
                    ),
                    tickfont=dict(
                        color='#7f7f7f',size=8, 
                    
                    )
                ),
                
                yaxis5=
                dict( 
                    title='MACD',
                    anchor='x5',  
                    domain=[0,0.13],         
                    side='left',
                    titlefont=dict(
                        color='#7f7f7f'
                    ),
                    tickfont=dict(
                        color='#7f7f7f'
                    
                    )
                ),
                
                yaxis6=
                dict( 
                    title='成交量',
                
                    anchor='x5',  
                    domain=[0.62,0.71],         
                    side='left',
                    titlefont=dict(
                        color='#7f7f7f'
                    ),
                    tickfont=dict(
                        color='#7f7f7f'
                    
                    )
                ),
                xaxis6=
                dict( 
                    anchor='y6',        
                    side='left',
                    titlefont=dict(
                        color='#7f7f7f',   
                    ),
                    tickfont=dict(
                        color='#7f7f7f',size=8, 
                    
                    )
                ),
                
                
            
        xaxis_rangeslider_visible=False,
            

            )
        
        #fig99 = go.Figure(data,layout=dict(width=500,height=500))
    fig99 = go.Figure(data,layout)
    fig99.update_xaxes(rangeslider_visible=False)
    graphJSON = json.dumps(fig99, cls=plotly.utils.PlotlyJSONEncoder)
        
    
        
    return graphJSON

def pic2(id,width,picday): 

    ticker = str(id)+".TW"
    p2= datetime.strptime(picday, '%Y-%m-%d')
    a_m =p2  - timedelta(days=58)
    x= a_m.strftime('%Y-%m-%d')
    df = yf.download(ticker,x)
    data=pd.DataFrame()
    data['Open']=df['Open']
    data['High']=df['High']
    data['Low']=df['Low']
    data['Close']=df['Close']
    data['Volume']=df['Volume']
    data['Adj Close']=df['Adj Close']
    data['up_down']=np.where(data['Adj Close'] >= data['Adj Close'].shift(1), 1, -1)

    bbands = ta.BBANDS(df, 30)
    data['bbandsU'] = bbands.BB_UPPER
    data['bbandsL'] = bbands.BB_LOWER
    data['MA5'] = ta.SMA(df, 5)
    data['MA10'] = ta.SMA(df, 10)
    data['MA20'] = ta.SMA(df, 20)
    data['RSI5'] = ta.RSI(df, 5)
    data['RSI10'] = ta.RSI(df, 10)
    data['k'] = ta.STOCH(df)
    data['d'] = ta.STOCHD(df)
    data['CCI'] = ta.CCI(df)
    data['ADX'] = ta.ADX(df)
    data['DMP'] = ta.DMI(df, 14, True)["DI+"]
    data['DMN'] = ta.DMI(df, 14, True)["DI-"]
    data['AO'] = ta.AO(df)
    data['MOM10'] = ta.MOM(df,10)
    MACD = ta.MACD(df)
    data['DIF'] = MACD.MACD
    data['MACD'] = MACD.SIGNAL
    data['DIF-MACD'] = data['DIF'] - data['MACD']
    data['WILL10'] = ta.WILLIAMS(df, 10)
    data['UO'] = ta.UO(df)
    data = data.dropna(axis=0, how='any')
    colors = ['green' if data['Open'] - data['Close'] >= 0 
          else 'red' for index, data in data.iterrows()]
    fig = go.Candlestick(x=data.index, xaxis='x1',
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                increasing_line_color='red',
                                decreasing_line_color='green',
                                # showlegend=False
                                )
    
    fig1=go.Scatter(x=data.index,  xaxis='x1',
                                    y=data['MA5'], 
                                    opacity=0.7, 
                                    
                                    line=dict(color='#2894FF', width=2), 
                                    name='5日均線')
    fig2=go.Scatter(x=data.index, xaxis='x1',
                    
                                    y=data['MA10'], 
                                    opacity=0.7, 
                                    line=dict(color='orange', width=2), 
                                    name='10日均線')
    fig3=go.Scatter(x=data.index,xaxis='x1',
                                    y=data['MA20'], 
                                    opacity=0.7, 
                                    line=dict(color='pink', width=2), 
                                    name='20日均線')
    
    fig4=go.Scatter(x=data.index,  xaxis='x3',
                                    yaxis='y3',
                                    y=data['RSI10'], 
                                    opacity=0.7, 
                                    line=dict(color='#01ACBD', width=2), 
                                    name='RSI10')
    fig5=go.Scatter(x=data.index,  xaxis='x3',
                                    yaxis='y3',
                                    y=data['RSI5'], 
                                    opacity=0.7, 
                                    line=dict(color='#867182', width=2), 
                                    name='RSI5')
    
    fig6=go.Scatter(x=data.index,  xaxis='x4',
                                    yaxis='y4',
                                    y=data['k'], 
                                    opacity=0.7, 
                                    line=dict(color='#E6AECF', width=2), 
                                    name='k')
    
    fig7=go.Scatter(x=data.index,  xaxis='x4',
                                    yaxis='y4',
                                    y=data['d'], 
                                    opacity=0.7, 
                                    line=dict(color='#7F9871', width=2), 
                                    name='d')
    
    
    fig8=go.Scatter(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['DIF'], 
                                    opacity=0.7, 
                                    line=dict(color='#7F9871', width=2), 
                                    name='DIF快線')
    
    
    fig9=go.Scatter(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['MACD'], 
                                    opacity=0.7, 
                                    line=dict(color='#FFA289', width=2), 
                                    name='MACD慢線')
    
    fig10=go.Bar(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['DIF-MACD'], 
                                    opacity=1,
                                    marker=dict(color=colors),
                                    name='DIF-MACD')
    
    fig11=go.Bar(x=data.index,  xaxis='x6',
                                    yaxis='y6',
                                    opacity=1,
                                    y=data['Volume'], 
                                    marker=dict(color=colors),
                                    name='成交量')

    color1 = '#00bfff'
    color2 = '#ff4000'
    color3='#800080'
   # data = [fig,fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10,fig11]
    #data = [fig,fig1,fig2,fig3]
    data = [fig4,fig5]
    layout = go.Layout(
    dict(width=400,height=600),
        title= '',
            titlefont=dict(
              
            family='Courier New, monospace',
            size=15,
            
            
            color='#7f7f7f'
            ),
            xaxis1  =
            dict( 
                
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),   
            #paper_bgcolor='rgba(0,0,0,0)',
            #plot_bgcolor='rgba(0,0,0,0)',

            yaxis=dict(
              domain=[0.8,1],
                title='股價',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
     
                )
            ),
           
             xaxis3=
            dict( 
                anchor='y3',     
            
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
            yaxis3=
            dict(
                title='RSI',
                domain=[0.21,0.35],
                anchor='x3',
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )

            ),
             xaxis4=
            dict( 
                anchor='y4',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
             yaxis4=
            dict( 
                 title='KD',
                anchor='x4',  
                domain=[0.42,0.53],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
            
             xaxis5=
            dict( 
                anchor='y5',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
             yaxis5=
            dict( 
                 title='MACD',
                anchor='x5',  
                domain=[0,0.13],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
            
             yaxis6=
            dict( 
                 title='成交量',
              
                anchor='x5',  
                domain=[0.62,0.71],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
             xaxis6=
            dict( 
                anchor='y6',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f',   
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
            
        
       xaxis_rangeslider_visible=False,
          

        )
    
    #fig99 = go.Figure(data,layout=dict(width=500,height=500))
    fig99 = go.Figure(data,layout)
    fig99.update_xaxes(rangeslider_visible=False)
    graphJSON = json.dumps(fig99, cls=plotly.utils.PlotlyJSONEncoder)
  
    
    return graphJSON

def pic3(id,width,picday): 

    ticker = str(id)+".TW"
    p2= datetime.strptime(picday, '%Y-%m-%d')
    a_m =p2  - timedelta(days=58)
    x= a_m.strftime('%Y-%m-%d')
    df = yf.download(ticker,x)
    data=pd.DataFrame()
    data['Open']=df['Open']
    data['High']=df['High']
    data['Low']=df['Low']
    data['Close']=df['Close']
    data['Volume']=df['Volume']
    data['Adj Close']=df['Adj Close']
    data['up_down']=np.where(data['Adj Close'] >= data['Adj Close'].shift(1), 1, -1)

    bbands = ta.BBANDS(df, 30)
    data['bbandsU'] = bbands.BB_UPPER
    data['bbandsL'] = bbands.BB_LOWER
    data['MA5'] = ta.SMA(df, 5)
    data['MA10'] = ta.SMA(df, 10)
    data['MA20'] = ta.SMA(df, 20)
    data['RSI5'] = ta.RSI(df, 5)
    data['RSI10'] = ta.RSI(df, 10)
    data['k'] = ta.STOCH(df)
    data['d'] = ta.STOCHD(df)
    data['CCI'] = ta.CCI(df)
    data['ADX'] = ta.ADX(df)
    data['DMP'] = ta.DMI(df, 14, True)["DI+"]
    data['DMN'] = ta.DMI(df, 14, True)["DI-"]
    data['AO'] = ta.AO(df)
    data['MOM10'] = ta.MOM(df,10)
    MACD = ta.MACD(df)
    data['DIF'] = MACD.MACD
    data['MACD'] = MACD.SIGNAL
    data['DIF-MACD'] = data['DIF'] - data['MACD']
    data['WILL10'] = ta.WILLIAMS(df, 10)
    data['UO'] = ta.UO(df)
    data = data.dropna(axis=0, how='any')
    colors = ['green' if data['Open'] - data['Close'] >= 0 
          else 'red' for index, data in data.iterrows()]
    fig = go.Candlestick(x=data.index, xaxis='x1',
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                increasing_line_color='red',
                                decreasing_line_color='green',
                                # showlegend=False
                                )
    
    fig1=go.Scatter(x=data.index,  xaxis='x1',
                                    y=data['MA5'], 
                                    opacity=0.7, 
                                    
                                    line=dict(color='#2894FF', width=2), 
                                    name='5日均線')
    fig2=go.Scatter(x=data.index, xaxis='x1',
                    
                                    y=data['MA10'], 
                                    opacity=0.7, 
                                    line=dict(color='orange', width=2), 
                                    name='10日均線')
    fig3=go.Scatter(x=data.index,xaxis='x1',
                                    y=data['MA20'], 
                                    opacity=0.7, 
                                    line=dict(color='pink', width=2), 
                                    name='20日均線')
    
    fig4=go.Scatter(x=data.index,  xaxis='x3',
                                    yaxis='y3',
                                    y=data['RSI10'], 
                                    opacity=0.7, 
                                    line=dict(color='#01ACBD', width=2), 
                                    name='RSI10')
    fig5=go.Scatter(x=data.index,  xaxis='x3',
                                    yaxis='y3',
                                    y=data['RSI5'], 
                                    opacity=0.7, 
                                    line=dict(color='#867182', width=2), 
                                    name='RSI5')
    
    fig6=go.Scatter(x=data.index,  xaxis='x4',
                                    yaxis='y4',
                                    y=data['k'], 
                                    opacity=0.7, 
                                    line=dict(color='#E6AECF', width=2), 
                                    name='k')
    
    fig7=go.Scatter(x=data.index,  xaxis='x4',
                                    yaxis='y4',
                                    y=data['d'], 
                                    opacity=0.7, 
                                    line=dict(color='#7F9871', width=2), 
                                    name='d')
    
    
    fig8=go.Scatter(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['DIF'], 
                                    opacity=0.7, 
                                    line=dict(color='#7F9871', width=2), 
                                    name='DIF快線')
    
    
    fig9=go.Scatter(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['MACD'], 
                                    opacity=0.7, 
                                    line=dict(color='#FFA289', width=2), 
                                    name='MACD慢線')
    
    fig10=go.Bar(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['DIF-MACD'], 
                                    opacity=1,
                                    marker=dict(color=colors),
                                    name='DIF-MACD')
    
    fig11=go.Bar(x=data.index,  xaxis='x6',
                                    yaxis='y6',
                                    opacity=1,
                                    y=data['Volume'], 
                                    marker=dict(color=colors),
                                    name='成交量')

    color1 = '#00bfff'
    color2 = '#ff4000'
    color3='#800080'
   # data = [fig,fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10,fig11]
    #data = [fig,fig1,fig2,fig3]
    data = [fig6,fig7]
    layout = go.Layout(
    dict(width=390,height=1200),
        title= '',
            titlefont=dict(
              
            family='Courier New, monospace',
            size=15,
            
            
            color='#7f7f7f'
            ),
            xaxis1  =
            dict( 
                
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),   
            #paper_bgcolor='rgba(0,0,0,0)',
            #plot_bgcolor='rgba(0,0,0,0)',

            yaxis=dict(
              domain=[0.8,1],
                title='股價',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
     
                )
            ),
           
             xaxis3=
            dict( 
                anchor='y3',     
            
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
            yaxis3=
            dict(
                title='RSI',
                domain=[0.21,0.35],
                anchor='x3',
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )

            ),
             xaxis4=
            dict( 
                anchor='y4',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
             yaxis4=
            dict( 
                 title='KD',
                anchor='x4',  
                domain=[0.42,0.53],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
            
             xaxis5=
            dict( 
                anchor='y5',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
             yaxis5=
            dict( 
                 title='MACD',
                anchor='x5',  
                domain=[0,0.13],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
            
             yaxis6=
            dict( 
                 title='成交量',
              
                anchor='x5',  
                domain=[0.62,0.71],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
             xaxis6=
            dict( 
                anchor='y6',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f',   
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
            
        
       xaxis_rangeslider_visible=False,
          

        )
    
    #fig99 = go.Figure(data,layout=dict(width=500,height=500))
    fig99 = go.Figure(data,layout)
    fig99.update_xaxes(rangeslider_visible=False)
    graphJSON = json.dumps(fig99, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
   
def pic4(id,width,picday): 
    ticker = str(id)+".TW"
    p2= datetime.strptime(picday, '%Y-%m-%d')
    a_m =p2  - timedelta(days=58)
    x= a_m.strftime('%Y-%m-%d')
    df = yf.download(ticker,x)
    data=pd.DataFrame()
    data['Open']=df['Open']
    data['High']=df['High']
    data['Low']=df['Low']
    data['Close']=df['Close']
    data['Volume']=df['Volume']
    data['Adj Close']=df['Adj Close']
    data['up_down']=np.where(data['Adj Close'] >= data['Adj Close'].shift(1), 1, -1)

    bbands = ta.BBANDS(df, 30)
    data['bbandsU'] = bbands.BB_UPPER
    data['bbandsL'] = bbands.BB_LOWER
    data['MA5'] = ta.SMA(df, 5)
    data['MA10'] = ta.SMA(df, 10)
    data['MA20'] = ta.SMA(df, 20)
    data['RSI5'] = ta.RSI(df, 5)
    data['RSI10'] = ta.RSI(df, 10)
    data['k'] = ta.STOCH(df)
    data['d'] = ta.STOCHD(df)
    data['CCI'] = ta.CCI(df)
    data['ADX'] = ta.ADX(df)
    data['DMP'] = ta.DMI(df, 14, True)["DI+"]
    data['DMN'] = ta.DMI(df, 14, True)["DI-"]
    data['AO'] = ta.AO(df)
    data['MOM10'] = ta.MOM(df,10)
    MACD = ta.MACD(df)
    data['DIF'] = MACD.MACD
    data['MACD'] = MACD.SIGNAL
    data['DIF-MACD'] = data['DIF'] - data['MACD']
    data['WILL10'] = ta.WILLIAMS(df, 10)
    data['UO'] = ta.UO(df)
    data = data.dropna(axis=0, how='any')
    colors = ['green' if data['Open'] - data['Close'] >= 0 
          else 'red' for index, data in data.iterrows()]
    fig = go.Candlestick(x=data.index, xaxis='x1',
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                increasing_line_color='red',
                                decreasing_line_color='green',
                                # showlegend=False
                                )
    
    fig1=go.Scatter(x=data.index,  xaxis='x1',
                                    y=data['MA5'], 
                                    opacity=0.7, 
                                    
                                    line=dict(color='#2894FF', width=2), 
                                    name='5日均線')
    fig2=go.Scatter(x=data.index, xaxis='x1',
                    
                                    y=data['MA10'], 
                                    opacity=0.7, 
                                    line=dict(color='orange', width=2), 
                                    name='10日均線')
    fig3=go.Scatter(x=data.index,xaxis='x1',
                                    y=data['MA20'], 
                                    opacity=0.7, 
                                    line=dict(color='pink', width=2), 
                                    name='20日均線')
    
    fig4=go.Scatter(x=data.index,  xaxis='x3',
                                    yaxis='y3',
                                    y=data['RSI10'], 
                                    opacity=0.7, 
                                    line=dict(color='#01ACBD', width=2), 
                                    name='RSI10')
    fig5=go.Scatter(x=data.index,  xaxis='x3',
                                    yaxis='y3',
                                    y=data['RSI5'], 
                                    opacity=0.7, 
                                    line=dict(color='#867182', width=2), 
                                    name='RSI5')
    
    fig6=go.Scatter(x=data.index,  xaxis='x4',
                                    yaxis='y4',
                                    y=data['k'], 
                                    opacity=0.7, 
                                    line=dict(color='#E6AECF', width=2), 
                                    name='k')
    
    fig7=go.Scatter(x=data.index,  xaxis='x4',
                                    yaxis='y4',
                                    y=data['d'], 
                                    opacity=0.7, 
                                    line=dict(color='#7F9871', width=2), 
                                    name='d')
    
    
    fig8=go.Scatter(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['DIF'], 
                                    opacity=0.7, 
                                    line=dict(color='#7F9871', width=2), 
                                    name='DIF快線')
    
    
    fig9=go.Scatter(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['MACD'], 
                                    opacity=0.7, 
                                    line=dict(color='#FFA289', width=2), 
                                    name='MACD慢線')
    
    fig10=go.Bar(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['DIF-MACD'], 
                                    opacity=1,
                                    marker=dict(color=colors),
                                    name='DIF-MACD')
    
    fig11=go.Bar(x=data.index,  xaxis='x6',
                                    yaxis='y6',
                                    opacity=1,
                                    y=data['Volume'], 
                                    marker=dict(color=colors),
                                    name='成交量')

    color1 = '#00bfff'
    color2 = '#ff4000'
    color3='#800080'
   # data = [fig,fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10,fig11]
    #data = [fig,fig1,fig2,fig3]
    data = [fig8,fig9,fig10]
    layout = go.Layout(
    dict(width=390,height=1200),
        title= '',
            titlefont=dict(
              
            family='Courier New, monospace',
            size=15,
            
            
            color='#7f7f7f'
            ),
            xaxis1  =
            dict( 
                
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),   
            #paper_bgcolor='rgba(0,0,0,0)',
            #plot_bgcolor='rgba(0,0,0,0)',

            yaxis=dict(
              domain=[0.8,1],
                title='股價',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
     
                )
            ),
           
             xaxis3=
            dict( 
                anchor='y3',     
            
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
            yaxis3=
            dict(
                title='RSI',
                domain=[0.21,0.35],
                anchor='x3',
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )

            ),
             xaxis4=
            dict( 
                anchor='y4',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
             yaxis4=
            dict( 
                 title='KD',
                anchor='x4',  
                domain=[0.42,0.53],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
            
             xaxis5=
            dict( 
                anchor='y5',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
             yaxis5=
            dict( 
                 title='MACD',
                anchor='x5',  
                domain=[0,0.13],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
            
             yaxis6=
            dict( 
                 title='成交量',
              
                anchor='x5',  
                domain=[0.62,0.71],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
             xaxis6=
            dict( 
                anchor='y6',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f',   
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
            
        
       xaxis_rangeslider_visible=False,
          

        )
    
    #fig99 = go.Figure(data,layout=dict(width=500,height=500))
    fig99 = go.Figure(data,layout)
    fig99.update_xaxes(rangeslider_visible=False)
    graphJSON= json.dumps(fig99, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
   
def pic5(id,width,picday): 
    ticker = str(id)+".TW"
    p2= datetime.strptime(picday, '%Y-%m-%d')
    a_m =p2  - timedelta(days=58)
    x= a_m.strftime('%Y-%m-%d')
    df = yf.download(ticker,x)
    data=pd.DataFrame()
    data['Open']=df['Open']
    data['High']=df['High']
    data['Low']=df['Low']
    data['Close']=df['Close']
    data['Volume']=df['Volume']
    data['Adj Close']=df['Adj Close']
    data['up_down']=np.where(data['Adj Close'] >= data['Adj Close'].shift(1), 1, -1)

    bbands = ta.BBANDS(df, 30)
    data['bbandsU'] = bbands.BB_UPPER
    data['bbandsL'] = bbands.BB_LOWER
    data['MA5'] = ta.SMA(df, 5)
    data['MA10'] = ta.SMA(df, 10)
    data['MA20'] = ta.SMA(df, 20)
    data['RSI5'] = ta.RSI(df, 5)
    data['RSI10'] = ta.RSI(df, 10)
    data['k'] = ta.STOCH(df)
    data['d'] = ta.STOCHD(df)
    data['CCI'] = ta.CCI(df)
    data['ADX'] = ta.ADX(df)
    data['DMP'] = ta.DMI(df, 14, True)["DI+"]
    data['DMN'] = ta.DMI(df, 14, True)["DI-"]
    data['AO'] = ta.AO(df)
    data['MOM10'] = ta.MOM(df,10)
    MACD = ta.MACD(df)
    data['DIF'] = MACD.MACD
    data['MACD'] = MACD.SIGNAL
    data['DIF-MACD'] = data['DIF'] - data['MACD']
    data['WILL10'] = ta.WILLIAMS(df, 10)
    data['UO'] = ta.UO(df)
    data = data.dropna(axis=0, how='any')
    colors = ['green' if data['Open'] - data['Close'] >= 0 
          else 'red' for index, data in data.iterrows()]
    fig = go.Candlestick(x=data.index, xaxis='x1',
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                increasing_line_color='red',
                                decreasing_line_color='green',
                                # showlegend=False
                                )
    
    fig1=go.Scatter(x=data.index,  xaxis='x1',
                                    y=data['MA5'], 
                                    opacity=0.7, 
                                    
                                    line=dict(color='#2894FF', width=2), 
                                    name='5日均線')
    fig2=go.Scatter(x=data.index, xaxis='x1',
                    
                                    y=data['MA10'], 
                                    opacity=0.7, 
                                    line=dict(color='orange', width=2), 
                                    name='10日均線')
    fig3=go.Scatter(x=data.index,xaxis='x1',
                                    y=data['MA20'], 
                                    opacity=0.7, 
                                    line=dict(color='pink', width=2), 
                                    name='20日均線')
    
    fig4=go.Scatter(x=data.index,  xaxis='x3',
                                    yaxis='y3',
                                    y=data['RSI10'], 
                                    opacity=0.7, 
                                    line=dict(color='#01ACBD', width=2), 
                                    name='RSI10')
    fig5=go.Scatter(x=data.index,  xaxis='x3',
                                    yaxis='y3',
                                    y=data['RSI5'], 
                                    opacity=0.7, 
                                    line=dict(color='#867182', width=2), 
                                    name='RSI5')
    
    fig6=go.Scatter(x=data.index,  xaxis='x4',
                                    yaxis='y4',
                                    y=data['k'], 
                                    opacity=0.7, 
                                    line=dict(color='#E6AECF', width=2), 
                                    name='k')
    
    fig7=go.Scatter(x=data.index,  xaxis='x4',
                                    yaxis='y4',
                                    y=data['d'], 
                                    opacity=0.7, 
                                    line=dict(color='#7F9871', width=2), 
                                    name='d')
    
    
    fig8=go.Scatter(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['DIF'], 
                                    opacity=0.7, 
                                    line=dict(color='#7F9871', width=2), 
                                    name='DIF快線')
    
    
    fig9=go.Scatter(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['MACD'], 
                                    opacity=0.7, 
                                    line=dict(color='#FFA289', width=2), 
                                    name='MACD慢線')
    
    fig10=go.Bar(x=data.index,  xaxis='x5',
                                    yaxis='y5',
                                    y=data['DIF-MACD'], 
                                    opacity=1,
                                    marker=dict(color=colors),
                                    name='DIF-MACD')
    
    fig11=go.Bar(x=data.index,  xaxis='x6',
                                    yaxis='y6',
                                    opacity=1,
                                    y=data['Volume'], 
                                    marker=dict(color=colors),
                                    name='成交量')

    color1 = '#00bfff'
    color2 = '#ff4000'
    color3='#800080'
   # data = [fig,fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10,fig11]
    #data = [fig,fig1,fig2,fig3]
    data = [fig11]
    layout = go.Layout(
    dict(width=390,height=1200),
        title= '',
            titlefont=dict(           
            family='Courier New, monospace',
            size=15,
            color='#7f7f7f'
            ),
            xaxis1  =
            dict( 
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),   
            #paper_bgcolor='rgba(0,0,0,0)',
            #plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(
              domain=[0.8,1],
                title='股價',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                )
            ),
           
             xaxis3=
            dict( 
                anchor='y3',     
            
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
            yaxis3=
            dict(
                title='RSI',
                domain=[0.21,0.35],
                anchor='x3',
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )

            ),
             xaxis4=
            dict( 
                anchor='y4',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
             yaxis4=
            dict( 
                 title='KD',
                anchor='x4',  
                domain=[0.42,0.53],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
            
             xaxis5=
            dict( 
                anchor='y5',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
             yaxis5=
            dict( 
                 title='MACD',
                anchor='x5',  
                domain=[0,0.13],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
            
             yaxis6=
            dict( 
                 title='成交量',
              
                anchor='x5',  
                domain=[0.62,0.71],         
                side='left',
                titlefont=dict(
                    color='#7f7f7f'
                ),
                tickfont=dict(
                    color='#7f7f7f'
                
                )
            ),
             xaxis6=
            dict( 
                anchor='y6',        
                side='left',
                titlefont=dict(
                    color='#7f7f7f',   
                ),
                tickfont=dict(
                    color='#7f7f7f',size=8, 
                
                )
            ),
            
            
        
       xaxis_rangeslider_visible=False,
          

        )
    
    #fig99 = go.Figure(data,layout=dict(width=500,height=500))
    fig99 = go.Figure(data,layout)
    fig99.update_xaxes(rangeslider_visible=False)
    graphJSON = json.dumps(fig99, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON