# IM3907 - Stockbot

## 專案介紹
Stockbot 是一個專為新手與忙碌的上班族所設計的股票選股系統，旨在幫助投資者快速獲取個股資訊與投資建議。透過 **LINE 聊天機器人** 提供服務，使用者可輕鬆查詢股市資訊、產業動態，並根據基本面進行選股，避免繁雜的財報分析。

Stockbot 利用 Smart Beta 選股法，根據六個長期穩定的投資因子來推薦股票：規模、品質、價值、動能、高股息、低波動。系統會自動篩選出符合條件的股票，並透過 LINE 即時提供選股結果。

## 安裝說明



### 1. 資料庫設定
Stockbot 使用 Heroku 支援的 ClearDB MySQL 資料庫，若不使用雲端資料庫，也可以設定本地 MySQL 資料庫。

1. **下載資料庫 SQL 檔**：下載 `IM3907-Stockbot.sql`。
2. **匯入資料庫**：
   - 進入 MySQL 的 Server，使用 `Data Import` 功能匯入資料庫檔案，不需預先創建資料庫。
3. **設定資料庫連線**：
   - 修改專案中的 `.py` 檔案，將資料庫連線改為您自己的資料庫設定：
     ```python
     db = pymysql.connect(host='localhost',
                          user='root',
                          password='your_password',
                          db='heroku_da386d83e593c1d',
                          charset='utf8mb4')
     ```

### 2. LINE Bot 註冊
1. **註冊 LINE Developers**：前往 [LINE Developers](https://developers.line.biz/zh-hant/) 註冊帳號。
2. **創建 Messaging API**：根據[LINE 官方文件](https://ithelp.ithome.com.tw/m/articles/10216620)與[教學文章](https://ithelp.ithome.com.tw/m/articles/10217350)創建 API。
3. **設定 LINE Bot**：
   - 在 `config.ini` 中填入 Messaging API 的 `channel_access_token` 和 `channel_secret`。

---

## 系統操作說明

#### 聊天室功能
在 LINE 聊天室中輸入以下指令，即可獲取相關資訊：
- **加權指數查詢**：輸入「加權指數」。
- **個股股價查詢**：輸入「股票號 + 股價」，例如「2330股價」。
- **個股新聞查詢**：輸入「股票號 + 新聞」，例如「2330新聞」。
- **最愛清單**：查詢已加入最愛的股票。

快捷鍵與圖文選單也可協助快速查詢這些功能。

#### 網站功能
- **產業一覽**：點選圖文選單中的「產業一覽」，選擇產業並瀏覽其上下游公司的基本資訊。
- **選股專區**：可進行「大師選股」、「自訂選股」及「推薦選股」。
- **新聞瀏覽**：點選股市新聞回傳訊息中的「查看更多」，可跳轉至最新新聞頁面。

---


