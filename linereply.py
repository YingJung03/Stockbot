import flex
import requests
from bs4 import BeautifulSoup

#股市新聞
def marnews():
    base = "https://news.cnyes.com"
    url = "https://news.cnyes.com/news/cat/tw_quo"
    re = requests.get(url)

    con = []
    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find_all("a", {"class": "_1Zdp"})
        
    for index, d in enumerate(data):
        if index < 5:
            title = d.text
            href = base + d.get("href")
            con.append(title)
            con.append(href)
        else:
            break
    content = flex.makeFlex2(con[0], con[1], con[2], con[3], con[4], con[5], con[6], con[7], con[8], con[9])
    return content

#個股新聞
def news(url):
    re = requests.get(url)
    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find_all("a", {"class": "Fw(b) Fz(20px) Fz(16px)--mobile Lh(23px) Lh(1.38)--mobile C($c-primary-text)! C($c-active-text)!:h LineClamp(2,46px)!--mobile LineClamp(2,46px)!--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled"})
    con = []
    for index, d in enumerate(data):
        if index < 3:
            title = d.text
            href = d.get("href")
            con.append(title)
            con.append(href)
        else:
            break  
    return con

#check
def check(id1):
    url = "https://tw.stock.yahoo.com/quote/%d"%(int(id1))
    re = requests.get(url)
    soup = BeautifulSoup(re.text, "html.parser")
    data0 = soup.find_all("h1", {"class": "C($c-link-text) Fw(b) Fz(24px) Mend(8px)"})
    result0 = [h1.get_text() for h1 in data0]
    return result0

#股價
def stock(id1):
    url = "https://tw.stock.yahoo.com/quote/%d"%(int(id1))
    re = requests.get(url)
    soup = BeautifulSoup(re.text, "html.parser")
    data0 = soup.find_all("h1", {"class": "C($c-link-text) Fw(b) Fz(24px) Mend(8px)"})
    result0 = [h1.get_text() for h1 in data0]
    name = "{} {}".format(id1, result0[0])
    data1 = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
    data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-up)"})
    data3 = soup.find_all("span", {"class": "Jc(fe) Fz(20px) Lh(1.2) Fw(b) D(f) Ai(c) C($c-trend-up)"})
    result = [span.get_text() for span in data1]
    c1 = "#ff0000"
    c2 = "#ff0000"
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
            c1="#06bf00"
            c2="#06bf00"
            result = [span.get_text() for span in data1]
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
        c3 = "#ff0000"
        if len(result7) == 0:
            data7 = soup.find_all("span", {"class": "Fz(16px) Mb(4px)"})
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

    data9 = soup.find_all("li", {"class": "price-detail-item H(32px) Mx(16px) D(f) Jc(sb) Ai(c) Bxz(bb) Px(0px) Py(4px) Bdbs(s) Bdbc($bd-primary-divider) Bdbw(1px)"})
    result9 = [li.get_text() for li in data9]
    text6 = result9[0][2:]
    text7 = result9[1][2:]
    text8 = result9[2][2:]
    text9 = result9[3][2:]
    text10 = result9[7][3:]

    url2 = "https://tw.stock.yahoo.com/quote/%d/revenue"%(int(id1))
    re2 = requests.get(url2)
    soup2 = BeautifulSoup(re2.text, "html.parser")
    data10 = soup2.find_all("li", {"class": "Jc(c) D(ib) Miw(100px) Fxg(1) Fxs(0) Fxb(100px) Ta(end) Mend(0)"})
    result10 = [li.get_text() for li in data10]
    text11 = result10[4]

    url3 = "https://tw.stock.yahoo.com/quote/%d/eps"%(int(id1))
    re3 = requests.get(url3)
    soup3 = BeautifulSoup(re3.text, "html.parser")
    data12 = soup3.find_all("div", {"class": "Fxg(1) Fxs(1) Fxb(0%) Miw($w-table-cell-min-width) Ta(end) Mend($m-table-cell-space) Mend(0):lc"})
    result12 = [div.get_text() for div in data12]
    text12 = result12[3]
    data11 = soup3.find_all("div", {"class": "W(112px) Ta(start)"})
    result11 = [div.get_text() for div in data11]
    Q = result11[1] 

    url4 = "https://tw.stock.yahoo.com/quote/%d/institutional-trading"%(int(id1))
    re4 = requests.get(url4)
    soup4 = BeautifulSoup(re4.text, "html.parser")
    data13 = soup4.find_all("div", {"class": "Fxg(1) Fxs(1) Fxb(0%) Miw($w-table-cell-min-width) Ta(end) Mend($m-table-cell-space) Mend(0):lc"})
    result13 = [div.get_text() for div in data13]
    text16 = result13[6]
    text17 = result13[10]
    text18 = result13[14]
    text19 = result13[18]
    data131 = soup4.find_all("time", {"class": "Fz(14px) C(#5b636a)"})
    result131 = [time.get_text() for time in data131]
    date2 = result131[1][5:]

    url5 = "https://tw.stock.yahoo.com/quote/%d/profile"%(int(id1))
    re5 = requests.get(url5)
    soup5 = BeautifulSoup(re5.text, "html.parser")
    data14 = soup5.find_all("div", {"class": "Py(8px) Pstart(12px) Bxz(bb)"})
    result14 = [div.get_text() for div in data14]
    text13 = result14[32]
    text14 = result14[27]
    text15 = result14[31]
    text20 = result14[43]
    text21 = result14[40]
    text22 = result14[42]
    data141 = soup5.find_all("span", {"class": "Fz(14px) C(#5b636a)"})
    result141 = [span.get_text() for span in data141]
    date3 = result141[0][5:]
    content = flex.makeFlex3(c1,c2,c3,name, num4, date2, date3, Q, nowprice, trend, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12, text13, text14, text15, text16, text17, text18, text19, text20, text21, text22)
    return content

#加權指數
def taiex():
    url = "https://tw.stock.yahoo.com/quote/%5ETWII"
    re = requests.get(url)
    soup = BeautifulSoup(re.text, "html.parser")
    data = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"})
    result = [span.get_text() for span in data]
    c1 = "#ff0000"
    if len(result) == 0:
        data = soup.find_all("span", {"class": "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"})
        result = [span.get_text() for span in data]
        c1="#06bf00"
    else:
        result = result
    num = result[0]

    data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-up)"})
    result2 = [span.get_text() for span in data2]
    c2="#ff0000"
    if len(result2) == 0:
        data2 = soup.find_all("span", {"class": "Fz(20px) Fw(b) Lh(1.2) Mend(4px) D(f) Ai(c) C($c-trend-down)"})
        result2 = [span.get_text() for span in data2]
        c2="#06bf00"
    else:
        result2 = result2
    num2 = result2[0]

    data3 = soup.find_all("span", {"class": "C(#6e7780) Fz(12px) Fw(b)"})
    result3 = [span.get_text() for span in data3]
    num3 = result3[0]

    content = flex.makeFlex1(c1,c2, num, num2, num3)
    return content