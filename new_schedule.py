from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
from urllib.request import urlopen

sched = BlockingScheduler()

@sched.add_job('interval',days  = 01)
def add_job():
#     url = "https://stockbottttt.herokuapp.com/"
#     conn = urllib.request.urlopen(url)
        
#     for key, value in conn.getheaders():
#         print(key, value)

# sched.start()

    import pymysql
    stock_lst=[]

    # 開啟資料庫連線
    db = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                            user='be59caf2e81229',
                            password='75242529',
                            db='heroku_da386d83e593c1d',
                            charset='utf8mb4',)
    
    # 使用 cursor() 方法建立一個遊標物件 cursor
    cursor = db.cursor()

    # SQL 查詢語句
    sql1 =  "SELECT * FROM stock"
    try:

        # 執行SQL1語句
        cursor.execute(sql1)
        # 獲取所有記錄列表
        stock = cursor.fetchall()
    
        for i in stock:
            stock_lst.append(i)
        
        
    except:
        print("Error: unable to fetch data")

    # 關閉資料庫連線
    db.close()

    id_lst=[]
    for i in range(stock_lst):
        stock_id=str(stock_lst[i][0])
        id_lst.append(stock_id)

    import datatime
    from datatime import date
    now_df = pd.DataFrame()
    for i in id_lst:
        stock_id=i
        url = "https://tw.stock.yahoo.com/quote/"+ stock_id +"/news"
        
        re = requests.get(url)
        soup = BeautifulSoup(re.text, "html.parser")
        data = soup.find_all("a", {"class": "Fw(b) Fz(20px) Fz(16px)--mobile Lh(23px) Lh(1.38)--mobile C($c-primary-text)! C($c-active-text)!:h LineClamp(2,46px)!--mobile LineClamp(2,46px)!--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled"})
                                            #D(ib) Px(0) Py(0) Mend(12px) Lh(24px) Fw(b) Ff($stockSiteFontFamily) Td(n) O(0):f Bd(n) Whs(nw) Fz(14px) C($c-primary-text) Cur(d) C($c-primary-text):h Mstart(0)
                                            #D(ib) Px(0) Py(0) Mstart(12px) Lh(24px) Fw(b) Ff($stockSiteFontFamily) Td(n) O(0):f Cur(p) Bd(n) Whs(nw) Fz(14px) C($c-button) C($c-primary-text):h Mend(0) Mend($mobile-m-module)--mobile
        title_list=[]
        href_list=[]
        for index, d in enumerate(data):
            if index==1:
                title = d.text
                title_list.append(title)
                href = d.get("href")
                href_list.append(href)
        title0=pd.DataFrame(title_list)
        if title0.empty:
            continue
        else:
            title0.columns = ['title']
            link0=pd.DataFrame(href_list)
            link0.columns = ['stock_news']
            df=pd.concat([title0,link0],axis=1)
            today = datetime.date.today()
            df.insert(0, 'id',stock_id)
            df.insert(1,'date',today)
            now_df=now_df.append(df,ignore_index=True)
            news_final = now_df[['id','date','stock_news','title']]
            import pymysql
            import pandas as pd
            from sqlalchemy import create_engine
            from sqlalchemy import exc

            engine = create_engine("mysql+pymysql://be59caf2e81229:75242529@us-cdbr-east-05.cleardb.net:3306/heroku_da386d83e593c1d")

            # Connect to the database
            connection = pymysql.connect(host='us-cdbr-east-05.cleardb.net',
                                    user='be59caf2e81229',
                                    password='75242529',
                                    db='heroku_da386d83e593c1d',
                                    charset='utf8mb4',)    

            # create cursor
            cursor=connection.cursor()
            # Execute the to_sql for writting DF into SQL
            # news_final.to_sql('news', engine, if_exists='append', index=False)  
            for i in range(len(news_final)):
                try:
                    news_final.iloc[i:i+1].to_sql('news', engine,if_exists='append',index=False)

                except exc.IntegrityError:
                    pass #or any other action

            # Execute query
            sql = "SELECT * FROM `news`"
            cursor.execute(sql)

            # Fetch all the records
            result = cursor.fetchall()


            for i in result:
                print(i)
                
            engine.dispose()
            connection.close()

sched.start()



