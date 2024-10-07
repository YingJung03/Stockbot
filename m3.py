import pymysql

#近三年營收成長率，平均大於15％
def f1():
    lst1=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                             user='be59caf2e81229',
                             password='75242529',
                             db='heroku_da386d83e593c1d',
                             charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql = "select id from (select id,sum(revenue_qoq) as sfr from quarter_financial_ratio where LEFT(quarter,4) in ('2021','2020','2019') group by id, LEFT(quarter,4)) as T group by id HAVING avg(sfr)>15"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst1.append(a)
    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
    db.close()
    return lst1

#近4季股東全亦報仇率大於7％
def f2():
    lst2=[]
        # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                        user='be59caf2e81229',
                        password='75242529',
                        db='heroku_da386d83e593c1d',
                        charset='utf8mb4')

        # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

        # SQL 查詢語句
    sql =  "SELECT id FROM quarter_financial_ratio WHERE quarter in ('2021Q4','2021Q3','2021Q2','2021Q1') group by id HAVING sum(roe)>7"

    try:
            # 執行SQL語句
        cursor.execute(sql)
            # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst2.append(a)

    except:
        print("Error: unable to fetch data")

        # 關閉資料庫連線
    db.close()
    return lst2

#最新營業利率大於1％
def f3():
    lst3=[]
        # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                        user='be59caf2e81229',
                        password='75242529',
                        db='heroku_da386d83e593c1d',
                        charset='utf8mb4')

        # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

        # SQL 查詢語句
    sql =  "SELECT id FROM quarter_financial_ratio WHERE quarter = '2021Q4' and operating_profit_margin > 1"

    try:
            # 執行SQL語句
        cursor.execute(sql)
            # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst3.append(a)

    except:
        print("Error: unable to fetch data")

        # 關閉資料庫連線
    db.close()
    return lst3

#近3年營益率每年都大於3％
def f4():
    lst4=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                             user='be59caf2e81229',
                             password='75242529',
                             db='heroku_da386d83e593c1d',
                             charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql = "select id from (select id,sum(operating_profit_margin) as sfo from quarter_financial_ratio where LEFT(quarter,4) in ('2021','2020','2019') group by id, LEFT(quarter,4)) as T group by id HAVING min(sfo)>12"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst4.append(a)
    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
    db.close()
    return lst4

#過濾股價5元以下,五日均量在500張以下的個股
def f5():
    lst5=[]
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                             user='be59caf2e81229',
                             password='75242529',
                             db='heroku_da386d83e593c1d',
                             charset='utf8mb4')

    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql = "select T.id from (select id,(sum(Volume)/5000) as sv from stock_daily where Date in ('2022-05-13','2022-05-12','2022-05-11','2022-05-10','2022-05-09') group by id) as T, stock_daily where stock_daily.Date = '2022-05-13' and stock_daily.Close > 5 and T.sv > 500 and T.id = stock_daily.id group by id"

    try:
        # 執行SQL語句
        cursor.execute(sql)
        # 獲取所有記錄列表
        data = cursor.fetchall()
        for i in data:
            a = int(''.join(map(str, i)))
            lst5.append(a)

    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
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
    lst6 = []
    for i in range(len(lst)):
        # SQL 查詢語句
        sql = "SELECT * FROM stock WHERE id =" + str(lst[i])

        cursor.execute(sql)
        lst6.extend(cursor.fetchall())

    # 關閉資料庫連線
    db.close()
    return lst6