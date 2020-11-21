# Dcard Crawler

## 實作步驟

* 1.Dcard為動態網頁，觀察測試後，以找出存在文章資料的json檔做爬取
* 2.用Xpath爬取標籤裡面的資料
* 3.以json檔的方式存檔
* 4.更新爬蟲資料，與之前的文章ID做比對，若有重複就停止爬取

# Carrefour Crawler

## 實作步驟

* 1.觀察網頁後，用request.post帶入參數得到資料
* 2.建立cvs檔的欄位，將所需的資料刮取出來
* 3.存入csv檔
