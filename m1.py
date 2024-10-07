import pymysql

#5年毛利率
def f1():
    lst1=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql = "select id from quarter_financial_ratio where LEFT(quarter,4) in ('2021','2020','2019','2018','2017') group by id HAVING min(gross_margin)>10"
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst1.append(a)
    except:
        print("Error: unable to fetch data")
    db.close()
    return lst1

#5年EPS
def f2():
    lst2=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql = "select id from (select id,sum(eps) as seps from quarter_financial_ratio where LEFT(quarter,4) in ('2021','2020','2019','2018','2017') group by id, LEFT(quarter,4)) as T group by id HAVING min(seps)>1"
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst2.append(a)
    except:
        print("Error: unable to fetch data")
    db.close()
    return lst2

#近12個月每股營收大於1.5元
def f3():
    lst3=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql = "select T.id from (select id,sum(income) as sin from income_statement where quarter in ('2021Q4','2021Q3','2021Q2','2021Q1') group by id) as T, stock_year where (T.sin/stock_year.capital)>1.5 and T.id = stock_year.id group by id"
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst3.append(a)
    except:
        print("Error: unable to fetch data")
    db.close()
    return lst3

#股價淨值比小於1.5
def f4():
    lst4=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql =  "SELECT quarter_financial_ratio.id FROM quarter_financial_ratio, stock_daily WHERE quarter_financial_ratio.quarter = '2021Q4' and stock_daily.date = '2022-05-13' and round(stock_daily.Close/quarter_financial_ratio.book_value_per_share, 2)<1.5 and quarter_financial_ratio.id = stock_daily.id group by id"
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst4.append(a)
    except:
        print("Error: unable to fetch data")
    db.close()
    return lst4

#過濾股價5元以下,五日均量在500張以下的個股
def f5():
    lst5=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql = "select T.id from (select id,(sum(Volume)/5000) as sv from stock_daily where Date in ('2022-05-13','2022-05-12','2022-05-11','2022-05-10','2022-05-09') group by id) as T, stock_daily where stock_daily.Date = '2022-05-13' and stock_daily.Close > 5 and T.sv > 500 and T.id = stock_daily.id group by id"
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst5.append(a)
    except:
        print("Error: unable to fetch data")
    db.close()
    return lst5

#近4季股東權益報酬率大於5%
def f6():
    lst6=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql = "SELECT id FROM quarter_financial_ratio WHERE quarter in ('2021Q4','2021Q3','2021Q2','2021Q1') group by id HAVING sum(roe)>5"
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst6.append(a)
    except:
        print("Error: unable to fetch data")
    db.close()
    return lst6

def f():
    lst1 = f1()
    lst2 = f2()
    lst3 = f3()
    lst4 = f4()
    lst5 = f5()
    lst6 = f6()
    return sorted(set(lst1) & set(lst2) & set(lst3) & set(lst4) & set(lst5) & set(lst6))

def fin():
    lst = f()
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    lst7 = []
    for i in range(len(lst)):
        sql = "SELECT * FROM stock WHERE id =" + str(lst[i])
        cursor.execute(sql)
        lst7.extend(cursor.fetchall())
    db.close()
    return lst7