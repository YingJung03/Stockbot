from __future__ import unicode_literals
from crypt import methods
from inspect import getclasstree
import os
from struct import pack

from sqlalchemy import create_engine
from flask import Flask, request, abort, render_template, redirect, flash, url_for

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

import configparser
import flex, m1, m2, m3, sb1, sfinance, fav, c, linereply
import pic
#分頁
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
# crawler package
import requests
from bs4 import BeautifulSoup
import urllib
import re
import random

import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import plotly
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import json
from json import dumps as json_dumps
import yfinance as yf
import math
from finta import TA as ta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

#database
from flask_sqlalchemy import SQLAlchemy
import pymysql
# import mysql.connector
from backtesting import Backtest, Strategy #引入回測和交易策略功能
from backtesting.lib import crossover #從lib子模組引入判斷均線交會功能
from backtesting.test import SMA #從test子模組引入繪製均線功能
import numpy as np
import pandas as pd
import datetime

config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__)
app.config['SECRET_KEY']='hellostockbot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://be59caf2e81229:75242529@us-cdbr-east-05.cleardb.net/heroku_da386d83e593c1d"

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
# stock_name
def s_name(id):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    select = 'select * from stock where id= '  + str(id)
    cursor.execute(select)
      
    message = []
    message.extend(cursor.fetchall())

    cursor.close()
    conn.close()
    return message

# news     
def news1():
   conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
   cursor = conn.cursor()
   select = 'SELECT * FROM news,stock where news.id=stock.id order by date desc;'
   cursor.execute(select) 
   message2 = []
   message2.extend(cursor.fetchmany(20))
   cursor.close()
   conn.close()
   return message2


# 網頁
@app.route("/home")
def home():
    return render_template("home.html")

#技術圖 
@app.route('/picture', methods=['POST','GET'])
def pictures():
  id = request.args.get("id")
  name = request.args.getlist('pics')
  width=request.args.get('screen_width')
  picday=request.args.get('picday')
  graphJSON = []
  for i in name:
    if i=='price' or i=="['price']":
      graphJSON.append(pic.pic(id,width,picday))  #ok
    elif i=='kd' or i=="['kd']":
      graphJSON.append(pic.pic3(id,width,picday))  #ok
    elif i=='macd' or i=="['macd']":
      graphJSON.append(pic.pic4(id,width,picday))
    elif i=='rsi' or i=="['rsi']":
      graphJSON.append(pic.pic2(id,width,picday))
    else:
      graphJSON.append(pic.pic5(id,width,picday))
  return render_template("javas.html",graphJSON=graphJSON,id=id,name=name,picday=picday)

@app.route("/choose")
def choose():
    s = sb1.refin()
    return render_template("choose.html", stock = s)
  
@app.route("/choo",  methods=['POST','GET'])
def choo():
  a=[]
  value=[]
  try:
    if request.form["com"]:
      com = request.form["com"]
      n = int(request.form["n"])
      value.append("現金股利今年 %s %d" %(com,n))
      ans=c.fun1(com,n)
      a.append(ans)
  except:
    print("None")

  try:
    if request.form["com2"]:
      t=request.form["t2"]
      com = request.form["com2"]
      n = int(request.form["n2"])
      value.append("每股稅後盈餘 %s %s %d" %(t,com,n))
      col="eps"
      t1=int(t[1])
      if t.find("季") != -1:
        ans2=c.fun2(t1,com, col, n)
      else:
        ans2=c.fun5(t1, com, col, n)
      a.append(ans2)
  except:
    print("None")
    
  try:
    if request.form["com3"]:
      com = request.form["com3"]
      n = int(request.form["n3"])
      value.append("市值 %s %d億" %(com,n))
      ans3=c.fun3(com,n)
      a.append(ans3)
  except:
    print("None")
    
  try:
    if request.form["com4"]:
      com = request.form["com4"]
      n = int(request.form["n4"])
      value.append("本益比 %s %d倍" %(com,n))
      ans4=c.fun4(com, n)
      a.append(ans4)
  except:
    print("None")
    
  try:
    if request.form["com5"]:
      t=request.form["t5"]
      com = request.form["com5"]
      n = int(request.form["n5"])
      value.append("股東權益報酬 %s %s %d%%" %(t,com,n))
      col="roe"
      t1=int(t[1])
      if t.find("季") != -1:
        ans5=c.fun2(t1,com, col, n)
      else:
        ans5=c.fun5(t1, com, col, n)
      a.append(ans5)
  except:
    print("None")
   
  try:
    if request.form["com6"]:
      t=request.form["t6"]
      com = request.form["com6"]
      n = int(request.form["n6"])
      value.append("資產報酬率 %s %s %d%%" %(t,com,n))
      col="roa"
      t1=int(t[1])
      if t.find("季") != -1:
        ans6=c.fun2(t1,com, col, n)
      else:
        ans6=c.fun5(t1, com, col, n)
      a.append(ans6)
  except:
    print("None")
   
  try:
    if request.form["com7"]:
      t=request.form["t7"]
      com = request.form["com7"]
      n = int(request.form["n7"])
      value.append("毛利率 %s %s %d%%" %(t,com,n))
      col="gross_margin"
      t1=int(t[1])
      ans7=c.fun2(t1,com, col, n)
      a.append(ans7)
  except:
    print("None")
    
  try:
    if request.form["com8"]:
      t=request.form["t8"]
      com = request.form["com8"]
      n = int(request.form["n8"])
      value.append("稅後淨利率 %s %s %d%%" %(t,com,n))
      t1=int(t[1])
      if t.find("季") != -1:
        col="profit_after_tax"
        ans8=c.fun2(t1,com, col, n)
      else:
        col="net_income_margin"
        ans8=c.fun5(t1, com, col, n)
      a.append(ans8)
  except:
    print("None")
    
  try:
    if request.form["com9"]:
      t=request.form["t9"]
      com = request.form["com9"]
      n = int(request.form["n9"])
      value.append("營業利益率 %s %s %d%%" %(t,com,n))
      col="operating_profit_margin"
      t1=int(t[1])
      if t.find("季") != -1:
        ans9=c.fun2(t1,com, col, n)
      else:
        ans9=c.fun5(t1, com, col, n)
      a.append(ans9)
  except:
    print("None")
    
  try:
    if request.form["com10"]:
      t=request.form["t10"]
      com = request.form["com10"]
      n = int(request.form["n10"])
      value.append("營收年成長率 %s %s %d%%" %(t,com,n))
      col="revenue_yoy"
      t1=int(t[1])
      ans10=c.fun5(t1, com, col, n)
      a.append(ans10)
  except:
    print("None")
    
  try:
    if request.form["com11"]:
      t=request.form["t11"]
      com = request.form["com11"]
      n = int(request.form["n11"])
      value.append("毛利年成長率 %s %s %d%%" %(t,com,n))
      col="gross_margin_yoy"
      t1=int(t[1])
      ans11=c.fun5(t1, com, col, n)
      a.append(ans11)
  except:
    print("None")
    
  try:
    if request.form["com12"]:
      t=request.form["t12"]
      com = request.form["com12"]
      n = int(request.form["n12"])
      value.append("存貨週轉率 %s %s %d次" %(t,com,n))
      col="inventory_turnover"
      t1=int(t[1])
      if t.find("季") != -1:
        ans12=c.fun2(t1,com, col, n)
      else:
        ans12=c.fun5(t1, com, col, n)
      a.append(ans12)
  except:
    print("None")
    
  try:
    if request.form["com13"]:
      t=request.form["t13"]
      com = request.form["com13"]
      n = int(request.form["n13"])
      value.append("應收帳款週轉率 %s %s %d次" %(t,com,n))
      col="receivables_turnover_ratio"
      t1=int(t[1])
      if t.find("季") != -1:
        ans13=c.fun2(t1,com, col, n)
      else:
        ans13=c.fun5(t1, com, col, n)
      a.append(ans13)
  except:
    print("None")
    
  try:
    if request.form["com14"]:
      t=request.form["t14"]
      com = request.form["com14"]
      n = int(request.form["n14"])
      value.append("應付帳款週轉率 %s %s %d次" %(t,com,n))
      col="accounts_payable_turnover_ratio"
      t1=int(t[1])
      if t.find("季") != -1:
        ans14=c.fun2(t1,com, col, n)
      else:
        ans14=c.fun5(t1, com, col, n)
      a.append(ans14)
  except:
    print("None")
    
  try:
    if request.form["com15"]:
      t=request.form["t15"]
      com = request.form["com15"]
      n = float(request.form["n15"])
      value.append("固定資產週轉率 %s %s %.1f次" %(t,com,n))
      t1=int(t[1])
      if t.find("季") != -1:
        col="fixed_asset_turnover"
        ans15=c.fun2f(t1,com, col, n)
      else:
        col="fixed_assets_turnover"
        ans15=c.fun5f(t1, com, col, n)
      a.append(ans15)
  except:
    print("None")
    
  try:
    if request.form["com16"]:
      t=request.form["t16"]
      com = request.form["com16"]
      n = float(request.form["n16"])
      value.append("總資產週轉率 %s %s %.1f次" %(t,com,n))
      col="total_asset_turnover"
      t1=int(t[1])
      if t.find("季") != -1:
        ans16=c.fun2f(t1,com, col, n)
      else:
        ans16=c.fun5f(t1, com, col, n)
      a.append(ans16)
  except:
    print("None")
   
  try:
    if request.form["com17"]:
      t=request.form["t17"]
      com = request.form["com17"]
      n = int(request.form["n17"])
      value.append("流動比 %s %s %d%%" %(t,com,n))
      col="current_ratio"
      t1=int(t[1])
      ans17=c.fun2(t1,com, col, n)
      a.append(ans17)
  except:
    print("None")
   
  try:
    if request.form["com18"]:
      t=request.form["t18"]
      com = request.form["com18"]
      n = int(request.form["n18"])
      value.append("速動比 %s %s %d%%" %(t,com,n))
      col="quick_ratio"
      t1=int(t[1])
      ans18=c.fun2(t1,com, col, n)
      a.append(ans18)
  except:
    print("None")
    
  try:
    if request.form["com19"]:
      t=request.form["t19"]
      com = request.form["com19"]
      n = int(request.form["n19"])
      value.append("現金流量比 %s %s %d%%" %(t,com,n))
      col="cash_flow_ratio"
      t1=int(t[1])
      ans19=c.fun2(t1,com, col, n)
      a.append(ans19)
  except:
    print("None")
    
  from functools import reduce
  lst = list(sorted(reduce(set.intersection, [set(x) for x in a ])))
  if len(lst)==0:
    flash('您的篩選條件組合選不出股票喔！ 請重新設定篩選條件！！')
    return redirect(url_for("choose"))
  else:
    intersect = c.fin(lst) 
    return render_template("choose2.html",intersect=intersect,value=value)
 

@app.route("/cm/<path:master>")
def master(master):
  if master == 'pe':
    p = m2.fin()
    return render_template("master/pe.html", master=master, pe = p)
  elif master == 'bu':
    b = m1.fin()
    return render_template("master/bu.html", master=master, bu = b)
  else:
    m = m3.fin()
    return render_template("master/mm.html", master=master, mm = m)
  
@app.route("/cc/<path:cc>")
def cc(cc):
  if cc == 'cement':
    name = "'水泥工業'"
    lst = sb1.ff(name)
    cement = sb1.fin(lst)
    if len(cement) >= 1:
      return render_template("cc/cement.html", cc=cc, cement = cement)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'food':
    name = "'食品工業'"
    lst = sb1.ff(name)
    food = sb1.fin(lst)
    if len(food) >= 1:
      return render_template("cc/food.html", cc=cc, food = food)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'plastic':
    name = "'塑膠工業'"
    lst = sb1.ff(name)
    plastic = sb1.fin(lst)
    if len(plastic) >= 1:
      return render_template("cc/plastic.html", cc=cc, plastic = plastic)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'bio':
    name = "'生技醫療業'"
    lst = sb1.ff(name)
    bio = sb1.fin(lst)
    if len(bio) >= 1:
      return render_template("cc/bio.html", cc=cc, bio = bio)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'building':
    name = "'建材營造業'"
    lst = sb1.ff(name)
    building = sb1.fin(lst)
    if len(building) > 1:
      return render_template("cc/building.html", cc=cc, building = building)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'car':
    name = "'汽車工業'"
    lst = sb1.ff(name)
    car = sb1.fin(lst)
    if len(car) >= 1:
      return render_template("cc/car.html", cc=cc, car = car)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'chemical':
    name = "'化學工業'"
    lst = sb1.ff(name)
    chemical = sb1.fin(lst)
    if len(chemical) >= 1:
      return render_template("cc/chemical.html", cc=cc, chemical = chemical)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'com':
    name = "'通信網路業'"
    lst = sb1.ff(name)
    com = sb1.fin(lst)
    if len(com) >= 1:
      return render_template("cc/com.html", cc=cc, com = com)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'computer':
    name = "'電腦及週邊設備業'"
    lst = sb1.ff(name)
    computer = sb1.fin(lst)
    if len(computer) >= 1:
      return render_template("cc/computer.html", cc=cc, computer = computer)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'ec':
    name = "'電子通路業'"
    lst = sb1.ff(name)
    ec = sb1.fin(lst)
    if len(ec) >= 1:
      return render_template("cc/ec.html", cc=cc, ec = ec)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'elec':
    name = "'電子零組件業'"
    lst = sb1.ff(name)
    elec = sb1.fin(lst)
    if len(elec) >= 1:
      return render_template("cc/elec.html", cc=cc, elec = elec)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'eother':
    name = "'通信網路業'"
    lst = sb1.ff(name)
    eother = sb1.fin(lst)
    if len(eother) >= 1:
      return render_template("cc/eother.html", cc=cc, eother = eother)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'gas':
    name = "'油電燃氣業'"
    lst = sb1.ff(name)
    gas = sb1.fin(lst)
    if len(gas) >= 1:
      return render_template("cc/gas.html", cc=cc, gas = gas)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'glance':
    name = "'電氣電纜'"
    lst = sb1.ff(name)
    glance = sb1.fin(lst)
    if len(glance) >= 1:
      return render_template("cc/glance.html", cc=cc, glance = glance)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'glass':
    name = "'玻璃陶瓷'"
    lst = sb1.ff(name)
    glass = sb1.fin(lst)
    if len(glass) >= 1:
      return render_template("cc/glass.html", cc=cc, glass = glass)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'info':
    name = "'資訊服務業'"
    lst = sb1.ff(name)
    info = sb1.fin(lst)
    if len(info) >= 1:
      return render_template("cc/info.html", cc=cc, info = info)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'insurance':
    name = "'金融保險業'"
    lst = sb1.ff(name)
    insurance = sb1.fin(lst)
    if len(insurance) >= 1:
      return render_template("cc/insurance.html", cc=cc, insurance = insurance)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'motor':
    name = "'電機機械'"
    lst = sb1.ff(name)
    motor = sb1.fin(lst)
    if len(motor) >= 1:
      return render_template("cc/motor.html", cc=cc, motor = motor)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'opt':
    name = "'光電業'"
    lst = sb1.ff(name)
    opt = sb1.fin(lst)
    if len(opt) >= 1:
      return render_template("cc/opt.html", cc=cc, opt = opt)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'other':
    name = "'其他業'"
    lst = sb1.ff(name)
    other = sb1.fin(lst)
    if len(other) >= 1:
      return render_template("cc/other.html", cc=cc, other = other)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'paper':
    name = "'造紙工業'"
    lst = sb1.ff(name)
    paper = sb1.fin(lst)
    if len(paper) >= 1:
      return render_template("cc/paper.html", cc=cc, paper = paper)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'rubber':
    name = "'橡膠工業'"
    lst = sb1.ff(name)
    rubber = sb1.fin(lst)
    if len(rubber) >= 1:
      return render_template("cc/rubber.html", cc=cc, rubber = rubber)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'semi':
    name = "'半導體業'"
    lst = sb1.ff(name)
    semi = sb1.fin(lst)
    if len(semi) >= 1:
      return render_template("cc/semi.html", cc=cc, semi = semi)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'ship':
    name = "'航運業'"
    lst = sb1.ff(name)
    ship = sb1.fin(lst)
    if len(ship) >= 1:
      return render_template("cc/ship.html", cc=cc, ship = ship)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'steel':
    name = "'鋼鐵工業'"
    lst = sb1.ff(name)
    steel = sb1.fin(lst)
    if len(steel) >= 1:
      return render_template("cc/steel.html", cc=cc, steel = steel)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'tex':
    name = "'紡織纖維'"
    lst = sb1.ff(name)
    tex = sb1.fin(lst)
    if len(tex) >= 1:
      return render_template("cc/tex.html", cc=cc, tex = tex)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'tour':
    name = "'觀光事業'"
    lst = sb1.ff(name)
    tour = sb1.fin(lst)
    if len(tour) >= 1:
      return render_template("cc/tour.html", cc=cc, tour = tour)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))
  elif cc == 'trade':
    name = "'貿易百貨業'"
    lst = sb1.ff(name)
    trade = sb1.fin(lst)
    if len(trade) >= 1:
      return render_template("cc/trade.html", cc=cc, trade = trade)
    else:
      flash('此產業沒有推薦的股票喔！')
      return redirect(url_for("choose"))

@app.route("/news")
def news():
  n = news1()
  return render_template("news.html", news1 = n)
@app.route("/search")
def search():
  submit_btn = request.args.get("submit")
  if submit_btn != None:
    stock = request.args.get("search")
    print("search_value",stock)
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    cursor.execute(f"SELECT id,company from stock where id = '{stock}'")                      
    conn.commit()
    data = cursor.fetchall()
    data = data[0] if len(data) else 0
    # For text    
    if data == 0 : 
      cursor.execute(f"SELECT id,company from stock where company like '%{stock}%'")
      conn.commit()
      data = cursor.fetchall()
      data = data[0] if len(data) else 0
      cursor.close()
      conn.close()
      
    if data == 0:
       flash('查無資料，請重新輸入股票號或股票名')
       return render_template('home.html')    
    else :
      return redirect(url_for('income',id=data[0]))
#搜尋新聞
@app.route("/searchnews")
def searchnews():
  submit_btn = request.args.get("submitnews")
  if submit_btn != None:
    stock = request.args.get("searchnews")
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * from news,stock where news.id = '{stock}' and news.id=stock.id order by date desc") 
                           
    conn.commit()
    # 產出 tuple
    data = cursor.fetchall()
    data= list(data) 
    print(data)
    # [(1001,),(1101,)]
    cursor.close()
    conn.close()
    new_item = []
    if len(data) ==0:
      flash('查無資料，請重新輸入股票號')
      return redirect(url_for("news"))
    else:
      for data in data:   
          data=list(data)
          new_item.append(data)
      stock = str(new_item[0][0])
      return render_template("searchnews.html",new_item=new_item,stock=stock)

    
@app.route("/<path:category>")
def category(category):
  if category == '水泥工業':
    return render_template("stock/cement.html", category=category)
  elif category == '食品工業':
    return render_template("stock/food.html", category=category)
  elif category == '塑膠工業':
    return render_template("stock/plastic.html", category=category)
  elif category == '橡膠工業':
    return render_template("stock/rubber.html", category=category)
  elif category == '半導體業':
    return render_template("stock/semiconductor.html", category=category)
  elif category == '電機機械':
    return render_template("stock/motor.html", category=category)
  elif category == '電腦及週邊設備業':
    return render_template("stock/computer.html", category=category)
  elif category == '電器電纜':
    return render_template("stock/glance.html", category=category)
  elif category == '電子零組件業':
    return render_template("stock/electronic_component.html", category=category)
  elif category == '電子通路業':
    return render_template("stock/e_channel.html", category=category)
  elif category == '其他電子業':
    return render_template("stock/other_e.html", category=category)
  elif category == '資訊服務業':
    return render_template("stock/info_service.html", category=category)
  elif category == '光電業':
    return render_template("stock/optoelectronics.html", category=category)
  elif category == '油電燃氣業':
    return render_template("stock/gas.html", category=category)
  elif category == '鋼鐵工業':
    return render_template("stock/steel.html", category=category)
  elif category == '建材營造業':
    return render_template("stock/building.html", category=category)
  elif category == '化學工業':
    return render_template("stock/chemical.html", category=category)
  elif category == '汽車工業':
    return render_template("stock/car.html", category=category)
  elif category == '航運業':
    return render_template("stock/shipping.html", category=category)
  elif category == '生技醫療業':
    return render_template("stock/bio_medic.html", category=category)
  elif category == '造紙工業':
    return render_template("stock/paper.html", category=category)
  elif category == '玻璃陶瓷':
    return render_template("stock/glass.html", category=category)
  elif category == '紡織纖維':
    return render_template("stock/textile.html", category=category)
  elif category == '貿易百貨業':
    return render_template("stock/trade.html", category=category)
  elif category == '金融保險業':
    return render_template("stock/insurance.html", category=category)
  elif category == '觀光事業':
    return render_template("stock/tourism.html", category=category)
  elif category == '通信網路業':
    return render_template("stock/communication.html", category=category)
  elif category == '其他業':
    return render_template("stock/other.html", category=category)

@app.route('/stock/<int:id>', methods=['POST','GET'])
def income(id):
    s = s_name(id)
    income = sfinance.income(id)
    balance = sfinance.balance(id)
    finance= sfinance.finance(id)
    bargain = sfinance.bargain(id)
    i1 = sfinance.b3(id)
    i2 = sfinance.b4(id)
    i3 = sfinance.b5(id)
    i4 = sfinance.b1(id)
    i5 = sfinance.b2(id)
    #graphJSON=pic.pic(id)
   
    return render_template('stock.html',i1=i1,i2=i2,i3=i3,i4=i4,i5=i5,s_name=s,id=id,income=income,balance=balance,finance=finance,bargain=bargain)
    
@app.route('/info/<int:id>', methods=['POST','GET'])
def info(id):
    s = s_name(id)
    income = sfinance.income(id)
    i1 = sfinance.info3(id)
    i2 = sfinance.info4(id)
    i3 = sfinance.info5(id)
    i4 = sfinance.info1(id)
    i5 = sfinance.info2(id)
    return render_template('info.html',s_name=s,id=id,i1=i1,i2=i2,i3=i3,i4=i4,i5=i5)
 
# 接收 LINE 的資訊 
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(PostbackEvent) 
def postback(event):
  if event.postback.data[0] == "加":
    checkid = fav.checkid(event.source.user_id)
    if checkid == "N":
      try:
        fav.addid(event.source.user_id)
        text = fav.checkstock(event.postback.data[1:5], event.source.user_id)
        line_bot_api.reply_message(
              event.reply_token,
              TextSendMessage(text=text+ chr(0x10008D)))
      except:
        print("Aerror")
    else:
      text = fav.checkstock(event.postback.data[1:5], event.source.user_id)
      line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text+ chr(0x10008D)))
  else:
    fav.delete(event.postback.data[1:5], event.source.user_id)
    line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text="已刪除"+ chr(0x10008D)))

# 以下為 各種回覆訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

#股市新聞
    if "股市" in msg:
       content = linereply.marnews()
       line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ])    
            ))
        
#"公司代號"+新聞
    elif "新聞" in msg:
        id1 = msg[:4]
        url = "https://tw.stock.yahoo.com/quote/" + id1 + "/news"
        con = linereply.news(url)
        if len(con) == 0:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="股票代碼錯誤囉！"+ chr(0x100092) +"\n" +"請重新輸入",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ])))
        else:
          content = flex.makeFlex2_1(con[0], con[1], con[2], con[3], con[4], con[5])
          line_bot_api.reply_message(
                  event.reply_token,
                  FlexSendMessage(
                      alt_text = msg,
                      contents = content,
                      quick_reply=QuickReply(items=[
                                      QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                      QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                      QuickReplyButton(action=MessageAction(label=id1+"股價", text=id1+"股價")),
                                      QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                      QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                      QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),
                                      QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                      QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                  ])
                      
              ))

#推薦股票
    elif "推薦" in msg:
      line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請選擇產業"+ chr(0x10008D)+ "\n" + chr(0x100077)+ "所有產業："+ "\n" +"水泥工業" +" "+ "食品工業" + "\n" + "橡膠工業" +" "+ "半導體業" + "\n" +"電腦週邊" +" "+ "電機機械" + "\n" +"電器電纜" +" "+ "電子零組件" + "\n" +"電子通路" +" "+ "其他電子" + "\n" +"資訊服務" +" "+ "光電業" + "\n" +"塑膠工業" +" "+ "鋼鐵工業" + "\n" +"建材營造" +" "+ "化學工業" + "\n" +"汽車工業" +" "+ "航運業" + "\n" +"生技醫療" +" "+ "造紙工業" + "\n" +"玻璃陶瓷" +" "+ "紡織纖維" + "\n" +"貿易百貨" +" "+ "金融保險" + "\n" +"通信網路" +" "+ "觀光業" + " " + "油電燃氣",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
    elif "食品" in msg:
        name = "'食品工業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "塑膠" in msg:
        name = "'塑膠工業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )
        
    elif "水泥" in msg:
        name = "'水泥工業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )
        
    elif "橡膠" in msg:
        name = "'橡膠工業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "半導體" in msg:
        name = "'半導體業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "電機" in msg:
        name = "'電機機械'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "電腦" in msg:
        name = "'電腦及週邊設備業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "電器電纜" in msg:
        name = "'電器電纜'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "電子零組件" in msg:
        name = "'電子零組件業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "電子通路" in msg:
        name = "'電子通路業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "其他電子" in msg:
        name = "'其他電子業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "資訊服務" in msg:
        name = "'資訊服務業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "光電" in msg:
        name = "'光電業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "油電燃氣" in msg:
        name = "'油電燃氣業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "鋼鐵" in msg:
        name = "'鋼鐵工業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "建材營造" in msg:
        name = "'建材營造業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "化學" in msg:
        name = "'化學工業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "汽車" in msg:
        name = "'汽車工業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "航運" in msg:
        name = "'航運業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "生技" in msg:
        name = "'生技醫療業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "造紙" in msg:
        name = "'造紙工業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "玻璃陶瓷" in msg:
        name = "'玻璃陶瓷'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "紡織纖維" in msg:
        name = "'紡織纖維'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "貿易百貨" in msg:
        name = "'貿易百貨業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "金融保險" in msg:
        name = "'金融保險業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "觀光" in msg:
        name = "'觀光事業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "通信網路" in msg:
        name = "'通信網路業'"
        lst = sb1.f(name)
        if len(lst) == 3:
          content = sb1.f3(lst)
        elif len(lst) == 2:
          content = sb1.f2(lst)
        elif len(lst) == 1:
          content = sb1.f1(lst)
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="此產業無符合條件之推薦"+ chr(0x10007C)+"\n" +"請查詢其他產業或綜合推薦",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="綜合", text="綜合")),
                                    QuickReplyButton(action=MessageAction(label="水泥", text="水泥工業")),
                                    QuickReplyButton(action=MessageAction(label="食品", text="食品工業")),
                                    QuickReplyButton(action=MessageAction(label="塑膠", text="塑膠工業")),
                                    QuickReplyButton(action=MessageAction(label="半導體", text="半導體業")),
                                    QuickReplyButton(action=MessageAction(label="電機", text="電機機械")),
                                    QuickReplyButton(action=MessageAction(label="電子零組件", text="電子零組件業")),
                                    QuickReplyButton(action=MessageAction(label="鋼鐵", text="鋼鐵工業")),
                                    QuickReplyButton(action=MessageAction(label="化學", text="化學工業")),
                                    QuickReplyButton(action=MessageAction(label="汽車", text="汽車工業")),
                                    QuickReplyButton(action=MessageAction(label="航運", text="航運業")),
                                    QuickReplyButton(action=MessageAction(label="生技", text="生技醫療業")),
                                    QuickReplyButton(action=MessageAction(label="金融保險", text="金融保險業"))
                                ])
        ))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ]))
        )

    elif "綜合" in msg:
        name = "'綜合推薦'"
        lst = sb1.f(name)
        content = sb1.f5(lst)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ])))

#回傳公司資訊
    elif "股價" in msg:
        id1 = msg[:4]
        result0 = linereply.check(id1)
        if len(result0) == 0:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="股票代碼錯誤囉！"+ chr(0x100092) +"\n" +"請重新輸入",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ])))
        else:
          content = linereply.stock(id1)
          line_bot_api.reply_message(
                  event.reply_token,
                  FlexSendMessage(
                      alt_text = msg,
                      contents = content,
                      quick_reply=QuickReply(items=[
                                      QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                      QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                      QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                      QuickReplyButton(action=MessageAction(label=id1+"新聞", text=id1+"新聞")),
                                      QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                      QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                      QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                  ])
                      ))

#加權指數 
    elif "加權指數" in msg:
        content = linereply.taiex()
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text = msg,
                    contents = content,
                    quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),  
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ])
                    ))
    elif "最愛清單" in msg:
        uid = event.source.user_id
        if fav.checkid(uid) == "Y":
          lst = fav.mystock(uid)
          if len(lst) == 3:
            content = fav.f3(lst)
            line_bot_api.reply_message(
              event.reply_token,
              FlexSendMessage(
                      alt_text = msg,
                      contents = content,
                      quick_reply=QuickReply(items=[
                                      QuickReplyButton(action=MessageAction(label=str(lst[0])+"股價", text=str(lst[0])+"股價")),
                                      QuickReplyButton(action=MessageAction(label=str(lst[0])+"新聞", text=str(lst[0])+"新聞")),  
                                      QuickReplyButton(action=MessageAction(label=str(lst[1])+"股價", text=str(lst[1])+"股價")),
                                      QuickReplyButton(action=MessageAction(label=str(lst[1])+"新聞", text=str(lst[1])+"新聞")),  
                                      QuickReplyButton(action=MessageAction(label=str(lst[2])+"股價", text=str(lst[2])+"股價")),
                                      QuickReplyButton(action=MessageAction(label=str(lst[2])+"新聞", text=str(lst[2])+"新聞")),
                                      QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                      QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                      QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                      QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數"))
                                  ])))
          elif len(lst) == 2:
            content = fav.f2(lst)
            line_bot_api.reply_message(
              event.reply_token,
              FlexSendMessage(
                      alt_text = msg,
                      contents = content,
                      quick_reply=QuickReply(items=[
                                      QuickReplyButton(action=MessageAction(label=str(lst[0])+"股價", text=str(lst[0])+"股價")),
                                      QuickReplyButton(action=MessageAction(label=str(lst[0])+"新聞", text=str(lst[0])+"新聞")),  
                                      QuickReplyButton(action=MessageAction(label=str(lst[1])+"股價", text=str(lst[1])+"股價")),
                                      QuickReplyButton(action=MessageAction(label=str(lst[1])+"新聞", text=str(lst[1])+"新聞")),
                                      QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                      QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                      QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                      QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數"))
                                  ])))
          elif len(lst) == 1:
            content = fav.f1(lst)
            line_bot_api.reply_message(
              event.reply_token,
              FlexSendMessage(
                      alt_text = msg,
                      contents = content,
                      quick_reply=QuickReply(items=[
                                      QuickReplyButton(action=MessageAction(label=str(lst[0])+"股價", text=str(lst[0])+"股價")),
                                      QuickReplyButton(action=MessageAction(label=str(lst[0])+"新聞", text=str(lst[0])+"新聞")),
                                      QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                      QuickReplyButton(action=MessageAction(label="介紹", text="介紹")),
                                      QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                      QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數"))
                                  ])))
          else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="清單是空的呦！"+ chr(0x10007C),
                              quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ])))  
        else:
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="尚未新增最愛股票！"+ chr(0x10008D) +"\n" + chr(0x100077)+"新增方法："+"\n"+"輸入指令查詢個股股價，"+ "\n" +"點選下方加入最愛清單按鈕，" +"\n" +"便完成新增！最多能收藏3家個股，"+ "\n" +"並且隨時能做刪除與更換動作。"+chr(0x10002D)+ "",
                              quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ])))
        
#提示訊息
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="哈囉～"+ chr(0x10008D) +"\n" +"歡迎使用StockBot！"+ "\n" +"我們將與您分享台灣股票的相關情報與資訊！"+chr(0x10002D) +"\n" +"您可以在聊天室中，輸入查詢"+ "\n" +"1. ‘公司代號’股價，查閱個公司資訊"+ "\n" +"2. 加權指數"+ "\n" +"3. 股市新聞"+ "\n" +"4. ‘公司代號’新聞"+ "\n" +"5. 推薦（推薦股票）"+ "\n" + "",
                            quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="加權指數", text="加權指數")),
                                    QuickReplyButton(action=MessageAction(label="股市新聞", text="股市新聞")),
                                    QuickReplyButton(action=MessageAction(label="推薦", text="推薦")),
                                    QuickReplyButton(action=MessageAction(label="2330股價", text="2330股價")),
                                    QuickReplyButton(action=MessageAction(label="2330新聞", text="2330新聞")),
                                    QuickReplyButton(action=MessageAction(label="2308股價", text="2308股價")),
                                    QuickReplyButton(action=MessageAction(label="2308新聞", text="2308新聞"))
                                ])
        ))
        

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
#app.run()