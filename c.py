from email import message
import pymysql, datetime

# dividends
def fun1(com, n):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    year_now=int(datetime.date.today().strftime("%Y"))
    
    cursor = conn.cursor()
    select = "select id from dividends where Dividends %s %d and Date='%d'" %(com,n,year_now-1)  
    cursor.execute(select)  
    message = []
    data = cursor.fetchall()
    for i in data:
        a = int(''.join(map(str, i)))
        message.append(a)
    cursor.close()
    conn.close()
    return message


# quarter_financial_ratio
def fun2(t1, com, col, n):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    # q=int(datetime.date.today().strftime("%m"))
    # if q == 1 or q == 2 or q == 3:
    #   quarter_now="Q1"
    # elif q == 4 or q == 5 or q == 6:
    #   quarter_now="Q2"
    # elif q == 7 or q == 8 or q == 9:
    #   quarter_now="Q3"
    # else:
    #   quarter_now="Q4"
    quarter_now="Q1"
    
    z=["Q1","Q2","Q3","Q4"]
    year=int(datetime.date.today().strftime("%Y"))
    z1=z.index(quarter_now[:])
    ans=[]
    for i in range(1,t1+1):
        a=z1-i
        if a<0:
            ans.append(str(year-1)+z[a])
        else:
            ans.append(str(year)+z[a])
    
    cursor = conn.cursor()
    if t1==1:
       select = "SELECT id FROM quarter_financial_ratio where quarter='%s' group by id having count(if(%s%s%d, 1, null))>=%d;" %(ans[0],col,com,n,t1) 
    elif t1==2:
       select = "select id from quarter_financial_ratio where quarter between '%s' and '%s' group by id having count(if(%s%s%d, 1, null))>=%d;" %(ans[1],ans[0],col,com,n,t1)
    elif t1==3:
        select = "select id from quarter_financial_ratio where quarter between '%s' and '%s' group by id having count(if(%s%s%d, 1, null))>=%d" %(ans[2],ans[0],col,com,n,t1)
    else:
        select = "select id from quarter_financial_ratio where quarter between '%s' and '%s' group by id having count(if(%s%s%d, 1, null))>=%d" %(ans[3],ans[0],col,com,n,t1)  
   
    cursor.execute(select) 
    message = []
    data = cursor.fetchall()
    for i in data:
        a = int(''.join(map(str, i)))
        message.append(a)
    cursor.close()
    conn.close()
    return message
  
# quarter_financial_ratio_float
def fun2f(t1, com, col, n):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    # q=int(datetime.date.today().strftime("%m"))
    # if q == 1 or q == 2 or q == 3:
    #   quarter_now="Q1"
    # elif q == 4 or q == 5 or q == 6:
    #   quarter_now="Q2"
    # elif q == 7 or q == 8 or q == 9:
    #   quarter_now="Q3"
    # else:
    #   quarter_now="Q4"
    quarter_now="Q1"
    
    z=["Q1","Q2","Q3","Q4"]
    year=int(datetime.date.today().strftime("%Y"))
    z1=z.index(quarter_now[:])
    ans=[]
    for i in range(1,t1+1):
        a=z1-i
        if a<0:
            ans.append(str(year-1)+z[a])
        else:
            ans.append(str(year)+z[a])
    
    cursor = conn.cursor()
    if t1==1:
       select = "SELECT id FROM quarter_financial_ratio where quarter='%s' group by id having count(if(%s%s%f, 1, null))>=%d;" %(ans[0],col,com,n,t1) 
    elif t1==2:
       select = "select id from quarter_financial_ratio where quarter between '%s' and '%s' group by id having count(if(%s%s%f, 1, null))>=%d;" %(ans[1],ans[0],col,com,n,t1)
    elif t1==3:
        select = "select id from quarter_financial_ratio where quarter between '%s' and '%s' group by id having count(if(%s%s%f, 1, null))>=%d" %(ans[2],ans[0],col,com,n,t1)
    else:
        select = "select id from quarter_financial_ratio where quarter between '%s' and '%s' group by id having count(if(%s%s%f, 1, null))>=%d" %(ans[3],ans[0],col,com,n,t1)  
   
    cursor.execute(select) 
    message = []
    data = cursor.fetchall()
    for i in data:
        a = int(''.join(map(str, i)))
        message.append(a)
    cursor.close()
    conn.close()
    return message


# stock_value
def fun3(com, n):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    
    # q=int(datetime.date.today().strftime("%m"))
    # if q == 1 or q == 2 or q == 3:
    #   quarter_now="Q1"
    # elif q == 4 or q == 5 or q == 6:
    #   quarter_now="Q2"
    # elif q == 7 or q == 8 or q == 9:
    #   quarter_now="Q3"
    # else:
    #   quarter_now="Q4"
    quarter_now="Q1"
        
    z=["Q1","Q2","Q3","Q4"]
    year=int(datetime.date.today().strftime("%Y"))
    a=z.index(quarter_now[:])-1
 
    if a<0:
      ans=str(year-1)+z[a]
    else:
      ans=str(year)+z[a]
    
    cursor = conn.cursor()
    select = "select id from stock_value where market_value %s %d and quarter='%s'" %(com,n/100,ans)     
    cursor.execute(select)  
    message = []
    data = cursor.fetchall()
    for i in data:
        a = int(''.join(map(str, i)))
        message.append(a)
    cursor.close()
    conn.close()
    return message


# stock_pe
def fun4(com, n):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    
    q=int(datetime.date.today().strftime("%m"))
    if q == 1 or q == 2 or q == 3:
      quarter_now="Q1"
    elif q == 4 or q == 5 or q == 6:
      quarter_now="Q2"
    elif q == 7 or q == 8 or q == 9:
      quarter_now="Q3"
    else:
      quarter_now="Q4"
        
    z=["Q1","Q2","Q3","Q4"]
    year=int(datetime.date.today().strftime("%y"))
    a=z.index(quarter_now[:])-1
 
    if a<0:
      ans=str(year-1)+z[a]
    else:
      ans=str(year)+z[a]
    
    cursor = conn.cursor()
    select = "select id from stock_pe where pe %s %d and q='%s'" %(com,n,ans)
    cursor.execute(select)  
    message = []
    data = cursor.fetchall()
    for i in data:
        a = int(''.join(map(str, i)))
        message.append(a)
    cursor.close()
    conn.close()
    return message


# year_financial_ratio
def fun5(t1, com, col, n):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    
    year_now=int(datetime.date.today().strftime("%Y"))
    
    cursor = conn.cursor()
    select = "select id from year_financial_ratio where year between %d and %d group by id having count(if(%s%s%d, 1, null))>=%d" %(year_now-t1,year_now,col,com,n,t1)
    cursor.execute(select)  
    message = []
    data = cursor.fetchall()
    for i in data:
        a = int(''.join(map(str, i)))
        message.append(a)
    cursor.close()
    conn.close()
    return message
  
  # year_financial_ratio_float
def fun5f(t1, com, col, n):
    conn = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        user='be59caf2e81229',
        password='75242529',
        db='heroku_da386d83e593c1d',
        charset='utf8'
      )
    
    year_now=int(datetime.date.today().strftime("%Y"))
    
    cursor = conn.cursor()
    select = "select id from year_financial_ratio where year between %d and %d group by id having count(if(%s%s%f, 1, null))>=%d" %(year_now-t1,year_now,col,com,n,t1)
    cursor.execute(select)  
    message = []
    data = cursor.fetchall()
    for i in data:
        a = int(''.join(map(str, i)))
        message.append(a)
    cursor.close()
    conn.close()
    return message
  
 
  
  
#印成表
def fin(lst):
  db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4')
  cursor = db.cursor()
  message = []
  for i in range(len(lst)):
      sql = "SELECT * FROM stock WHERE id =" + str(lst[i])
      cursor.execute(sql)
      message.extend(cursor.fetchall())

  db.close()
  return message