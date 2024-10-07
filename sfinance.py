import pymysql

#個股表
def income(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    # SQL 查詢語句
    sql = "SELECT * FROM income_statement WHERE id =" + str(id)
    cursor.execute(sql)
    lst.extend(cursor.fetchall())
    db.close()
    return lst

def balance(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    # SQL 查詢語句
    sql = "SELECT * FROM balance_sheet WHERE id =" + str(id)
    cursor.execute(sql)
    lst.extend(cursor.fetchall())
    db.close()
    return lst

def finance(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    record = (str(id))
    # SQL 查詢語句
    sql = "SELECT * FROM quarter_financial_ratio WHERE id =%s ORDER BY quarter desc"
    cursor.execute(sql,record)
    lst.extend(cursor.fetchall())
    db.close()
    return lst

def bargain(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    # SQL 查詢語句
    sql = "SELECT * FROM bargain WHERE id =" + str(id)
    cursor.execute(sql)
    lst.extend(cursor.fetchall())
    db.close()
    return lst

def b1(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT income FROM income_statement WHERE id = %s ORDER BY quarter desc LIMIT 1"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst

def b2(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT eps, book_value_per_share FROM quarter_financial_ratio WHERE id = %s ORDER BY quarter desc LIMIT 1"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst
    
def b3(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT Dividends, d_yield, capital, Date FROM stock_year WHERE id = %s ORDER BY Date desc LIMIT 1"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst
    
def b4(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT pe FROM stock_pe WHERE id = %s ORDER BY q desc LIMIT 1"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst
    
def b5(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT market_value FROM stock_value WHERE id = %s ORDER BY quarter desc LIMIT 1"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst

def info1(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT income FROM income_statement WHERE id = %s ORDER BY quarter desc LIMIT 8"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst

def info2(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT eps, book_value_per_share FROM quarter_financial_ratio WHERE id = %s ORDER BY quarter desc LIMIT 8"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst
    
def info3(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT Dividends, d_yield, capital, Date FROM stock_year WHERE id = %s ORDER BY Date desc LIMIT 8"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst
    
def info4(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT pe FROM stock_pe WHERE id = %s ORDER BY q desc LIMIT 8"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst
    
def info5(id):
    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()
    lst = []
    sql = "SELECT market_value FROM stock_value WHERE id = %s ORDER BY quarter desc LIMIT 8"
    cursor.execute(sql,id)
    lst.extend(cursor.fetchall())
    db.close()
    return lst

