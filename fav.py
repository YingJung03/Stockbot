import pymysql
import flex
import requests
from bs4 import BeautifulSoup

def checkid(id):
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    
    cursor = db.cursor()
    lst = []
    sql = "SELECT userid FROM fav"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        a = ''.join(i)
        lst.append(a)
    db.close()
    
    if id in lst:
        text = "Y"
    else:
        text = "N"
    return text

def addid(id):
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    # SQL 查詢語句
    record = (id)
    sql = "INSERT INTO fav (userid) VALUES (%s)"
    cursor.execute(sql, record)

    db.commit()
    db.close()
    return 0

def checkcol(id):
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    
    cursor = db.cursor()
    lst = []
    uid = id
    sql = "SELECT stock1,stock2,stock3 FROM fav WHERE userid = %s"
    cursor.execute(sql,uid)
    data = cursor.fetchall()
    db.close()
    
    for i in data[0]:
        lst.append(i)
    
    if lst[0] == None:
        col = "stock1"
    elif lst[1] == None:
        col = "stock2"
    elif lst[2] == None:
        col = "stock3"
    else:
        col = "N"
    return col

def addstock(data, id):
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    # SQL 查詢語句
    record = (int(data),id)
    col = checkcol(id)
    if col == "stock1":
      sql = "UPDATE fav SET stock1 = (%s) WHERE userid = %s"
      cursor.execute(sql, record)
      db.commit()
      db.close()
      text = "成功新增至最愛列表"
    elif col == "stock2":
      sql = "UPDATE fav SET stock2 = (%s) WHERE userid = %s"
      cursor.execute(sql, record)
      db.commit()
      db.close()
      text = "成功新增至最愛列表"
    elif col == "stock3":
      sql = "UPDATE fav SET stock3 = (%s) WHERE userid = %s"
      cursor.execute(sql, record)
      db.commit()
      db.close()
      text = "成功新增至最愛列表"
    else:
      text = "最愛清單已滿！刪除一股便能再次新增。"
    return text

def checkstock(data, id):
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
  
    cursor = db.cursor()
    lst = []
    uid = id
    sql = "SELECT stock1,stock2,stock3 FROM fav WHERE userid = %s"
    cursor.execute(sql,uid)
    d = cursor.fetchall()
    db.close()
    
    for i in d[0]:
        lst.append(i)
    if int(data) in lst:
      text = "此股票已在最愛清單裡囉！"
    else:
      text = addstock(data, id)
    return text

def mystock(id):
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    
    cursor = db.cursor()
    lst = []
    uid = id
    sql = "SELECT stock1,stock2,stock3 FROM fav WHERE userid = %s"
    cursor.execute(sql,uid)
    data = cursor.fetchall()
    
    db.close()
    
    for i in data[0]:
        if i != None:
            lst.append(i)
      
    return lst

def seldelete(data,id):
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    uid = id
    sql = "SELECT stock1,stock2,stock3 FROM fav WHERE userid = %s"
    cursor.execute(sql,uid)
    lst = cursor.fetchall()
    db.close()
    
    if lst[0][0] == int(data):
      text = "stock1"
    elif lst[0][1] == int(data):
      text = "stock2"
    else:
      text = "stock3"
      
    return text

def delete(data,id):
    col = seldelete(data,id)
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    record = (id)
    if col == "stock1":
      sql = "UPDATE fav SET stock1 = NULL WHERE userid = %s"
    elif col == "stock2":
      sql = "UPDATE fav SET stock2 = NULL WHERE userid = %s"
    else:
      sql = "UPDATE fav SET stock3 = NULL WHERE userid = %s"
    
    cursor.execute(sql, record)

    db.commit()
    db.close()
    return 0

def f3(lst):
    lst3 = lst
    conlst = []
    for i in range(len(lst3)):
        id1 = lst3[i]
        url = "https://tw.stock.yahoo.com/quote/" + str(id1)
        re = requests.get(url)
        soup = BeautifulSoup(re.text, "html.parser")
        data0 = soup.find_all("h1", {"class": "C($c-link-text) Fw(b) Fz(24px) Mend(8px)"})
        result0 = [h1.get_text() for h1 in data0]
        name = "{} {}".format(id1, result0[0])
        data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
        data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-up)"})
        data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-up)"})
        result = [span.get_text() for span in data1]
        c1="#ff0000"
        c2="#ff0000"
        if len(result) == 0:
          data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)"})
          data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c)"})
          data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c)"})
          result = [span.get_text() for span in data1]
          c1="#000000"
          c2="#000000"
          if len(result) == 0:
            data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"})
            data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-down)"})
            data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-down)"})
            result = [span.get_text() for span in data1]
            c1="#06bf00"
            c2="#06bf00"
          else:
            result = result
        else:
          result = result
        nowprice = result[0]
        up_down = ''
        increase = ''
        for i in data2:
            up_down = i.text
        for i in data3:
            increase = i.text
        trend = "{} {}".format(up_down, increase)
        data4 = soup.find_all("span", {"class": "C(#6e7780) Fz(12px) Fw(b)"})
        result4 = [span.get_text() for span in data4]
        num4 = result4[0]
        data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-down)"})
        result7 = [span.get_text() for span in data7]
        c3="#06bf00"
        if len(result7) == 0:
          data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-up)"})
          result7 = [span.get_text() for span in data7]
          c3="#ff0000"
          if len(result7) == 0:
            data7 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
            result7 = [span.get_text() for span in data7]
            c3="#000000"
          else:
            result7 = result7
        else:
          result7 = result7
        text3 = result7[0]
        data5 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
        result5 = [span.get_text() for span in data5]
        text4 = result5[0]
        text5 = result5[1]
          
        conlst.append(name)
        conlst.append(nowprice)
        conlst.append(trend)
        conlst.append(text3)
        conlst.append(text4)
        conlst.append(text5)
        conlst.append(num4)
        conlst.append(c1)
        conlst.append(c2)
        conlst.append(c3)
    s1 = conlst[0]
    s2 = conlst[10]
    s3 = conlst[20]
    p1 = conlst[1]
    p2 = conlst[11]
    p3 = conlst[21]
    text1 = conlst[2]
    text5 = conlst[12]
    text9 = conlst[22]
    text2 = conlst[3]
    text6 = conlst[13]
    text10 = conlst[23]
    text3 = conlst[4]
    text7 = conlst[14]
    text11 = conlst[24]
    text4 = conlst[5]
    text8 = conlst[15]
    text12 = conlst[25]
    c1 = conlst[7]
    c2 = conlst[8]
    c3 = conlst[9]
    c4 = conlst[17]
    c5 = conlst[18]
    c6 = conlst[19]
    c7 = conlst[27]
    c8 = conlst[28]
    c9 = conlst[29]
    date = conlst[6]
    return flex.makeFlex5_1(c1,c2,c3,c4,c5,c6,c7,c8,c9,s1,s2,s3,p1,p2,p3,text1,text2,text3,text4,text5,text6,text7,text8,text9,text10,text11,text12,date)

def f2(lst):
    lst2 = lst
    conlst = []
    for i in range(len(lst2)):
        id1 = lst2[i]
        url = "https://tw.stock.yahoo.com/quote/" + str(id1)
        re = requests.get(url)
        soup = BeautifulSoup(re.text, "html.parser")
        data0 = soup.find_all("h1", {"class": "C($c-link-text) Fw(b) Fz(24px) Mend(8px)"})
        result0 = [h1.get_text() for h1 in data0]
        name = "{} {}".format(id1, result0[0])
        data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
        data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-up)"})
        data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-up)"})
        result = [span.get_text() for span in data1]
        c1="#ff0000"
        c2="#ff0000"
        if len(result) == 0:
          data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)"})
          data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c)"})
          data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c)"})
          result = [span.get_text() for span in data1]
          c1="#000000"
          c2="#000000"
          if len(result) == 0:
            data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"})
            data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-down)"})
            data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-down)"})
            result = [span.get_text() for span in data1]
            c1="#06bf00"
            c2="#06bf00"
          else:
            result = result
        else:
          result = result
        nowprice = result[0]
        up_down = ''
        increase = ''
        for i in data2:
            up_down = i.text
        for i in data3:
            increase = i.text
        trend = "{} {}".format(up_down, increase)
        data4 = soup.find_all("span", {"class": "C(#6e7780) Fz(12px) Fw(b)"})
        result4 = [span.get_text() for span in data4]
        num4 = result4[0]
        data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-down)"})
        result7 = [span.get_text() for span in data7]
        c3="#06bf00"
        if len(result7) == 0:
          data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-up)"})
          result7 = [span.get_text() for span in data7]
          c3="#ff0000"
          if len(result7) == 0:
            data7 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
            result7 = [span.get_text() for span in data7]
            c3="#000000"
          else:
            result7 = result7
        else:
          result7 = result7
        text3 = result7[0]
        data5 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
        result5 = [span.get_text() for span in data5]
        text4 = result5[0]
        text5 = result5[1]
          
        conlst.append(name)
        conlst.append(nowprice)
        conlst.append(trend)
        conlst.append(text3)
        conlst.append(text4)
        conlst.append(text5)
        conlst.append(num4)
        conlst.append(c1)
        conlst.append(c2)
        conlst.append(c3)
    s1 = conlst[0]
    s2 = conlst[10]
    p1 = conlst[1]
    p2 = conlst[11]
    text1 = conlst[2]
    text5 = conlst[12]
    text2 = conlst[3]
    text6 = conlst[13]
    text3 = conlst[4]
    text7 = conlst[14]
    text4 = conlst[5]
    text8 = conlst[15]
    c1 = conlst[7]
    c2 = conlst[8]
    c3 = conlst[9]
    c4 = conlst[17]
    c5 = conlst[18]
    c6 = conlst[19]
    date = conlst[6]
    return flex.makeFlex5_2(c1,c2,c3,c4,c5,c6,s1,s2,p1,p2,text1,text2,text3,text4,text5,text6,text7,text8,date)
 
def f1(lst):
    lst1 = lst
    conlst = []
    for i in range(len(lst1)):
        id1 = lst1[i]
        url = "https://tw.stock.yahoo.com/quote/" + str(id1)
        re = requests.get(url)
        soup = BeautifulSoup(re.text, "html.parser")
        data0 = soup.find_all("h1", {"class": "C($c-link-text) Fw(b) Fz(24px) Mend(8px)"})
        result0 = [h1.get_text() for h1 in data0]
        name = "{} {}".format(id1, result0[0])
        data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
        data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-up)"})
        data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-up)"})
        result = [span.get_text() for span in data1]
        c1="#ff0000"
        c2="#ff0000"
        if len(result) == 0:
          data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)"})
          data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c)"})
          data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c)"})
          result = [span.get_text() for span in data1]
          c1="#000000"
          c2="#000000"
          if len(result) == 0:
            data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"})
            data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-down)"})
            data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-down)"})
            result = [span.get_text() for span in data1]
            c1="#06bf00"
            c2="#06bf00"
          else:
            result = result
        else:
          result = result
        nowprice = result[0]
        up_down = ''
        increase = ''
        for i in data2:
            up_down = i.text
        for i in data3:
            increase = i.text
        trend = "{} {}".format(up_down, increase)
        data4 = soup.find_all("span", {"class": "C(#6e7780) Fz(12px) Fw(b)"})
        result4 = [span.get_text() for span in data4]
        num4 = result4[0]
        data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-down)"})
        result7 = [span.get_text() for span in data7]
        c3="#06bf00"
        if len(result7) == 0:
          data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px) C($c-trend-up)"})
          result7 = [span.get_text() for span in data7]
          c3="#ff0000"
          if len(result7) == 0:
            data7 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
            result7 = [span.get_text() for span in data7]
            c3="#000000"
          else:
            result7 = result7
        else:
          result7 = result7
        text3 = result7[0]
        data5 = soup.find_all("span", {"class": "Fz(16px) C($c-link-text) Mb(4px)"})
        result5 = [span.get_text() for span in data5]
        text4 = result5[0]
        text5 = result5[1]
          
        conlst.append(name)
        conlst.append(nowprice)
        conlst.append(trend)
        conlst.append(text3)
        conlst.append(text4)
        conlst.append(text5)
        conlst.append(num4)
        conlst.append(c1)
        conlst.append(c2)
        conlst.append(c3)
    s1 = conlst[0]
    p1 = conlst[1]
    text1 = conlst[2]
    text2 = conlst[3]
    text3 = conlst[4]
    text4 = conlst[5]
    date = conlst[6]
    c1 = conlst[7]
    c2 = conlst[8]
    c3 = conlst[9]
    return flex.makeFlex5_3(c1,c2,c3,s1,p1,text1,text2,text3,text4,date)
 