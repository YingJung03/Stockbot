#m2舊的
import pymysql

#近5年稅前淨利成長率，平均大於7%
def f1():
    lst1=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql = "select T.id from (select id,sum(profit_before_tax) as sfr from quarter_financial_ratio where LEFT(quarter,4) in ('2021', '2020','2019','2018','2017') group by id, LEFT(quarter,4)) as T group by id HAVING avg(sfr)>7"
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

#本益比小於20
def f2():
    lst2=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql =  "SELECT id FROM stock_pe WHERE q = '21Q4' and pe < 20"
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

#近2年營收成長率，平均大於25%
def f3():
    lst3=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql = "select T.id from (select id,sum(revenue_qoq) as sfr from quarter_financial_ratio where LEFT(quarter,4) in ('2021','2020') group by id, LEFT(quarter,4)) as T group by id HAVING avg(sfr)>25"
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


#最近一季負債比例小於30%
def f4():
    lst4=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql =  "SELECT id FROM quarter_financial_ratio WHERE quarter = '2021Q4' and total_liabilities < 30"
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

#股價5元以下,五日均量在500張以下的個股
def f5():
    lst5=[]
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    cursor = db.cursor()
    sql = "select T.id from (select id,(sum(Volume)/5000) as sv from stock_daily where Date in ('2022-05-13','2022-05-12','2022-05-11','2022-05-10','2022-05-09') group by id) as T, stock_daily where stock_daily.Date = '2021-12-30' and stock_daily.Close > 5 and T.sv > 500 and T.id = stock_daily.id group by id"
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

def f():
    lst1 = f1()
    lst2 = f2()
    lst3 = f3()
    lst4 = f4()
    lst5 = f5()
    return sorted(set(lst1) & set(lst2) & set(lst3) & set(lst4) & set(lst5))

def fin():
    lst = f()
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lsta = []
    for i in range(len(lst)):
        # SQL 查詢語句
        sql = "SELECT * FROM stock WHERE id =" + str(lst[i])

        cursor.execute(sql)
        lsta.extend(cursor.fetchall())

    # 關閉資料庫連線
    db.close()
    return lsta