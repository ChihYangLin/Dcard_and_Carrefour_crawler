#載入套件 :no return
import requests
import json
import os
from lxml import etree
import random
import time
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

#讀json檔案into list
def read_file_into_list(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        json_load_list = json.load(file)
    return json_load_list

#建立dcardCvs資料夾 :no return
def make_directory(dictPath):
    #dictPath = './dcardCvs'
    if not os.path.exists(dictPath):
        os.mkdir(dictPath)

#取得最新網頁的json list :return jsonUrl
def get_latest_jsonUrl():
    url_latest = 'https://www.dcard.tw/f/cvs?latest=true' #超商版-所有文章-最新頁
    res_latest = requests.get(url=url_latest, headers=headers)
    page = etree.HTML(res_latest.text)
    top_id = page.xpath('//div//h2//a/@href')[0].split('/')[-1] #取第一頁第一篇的id
    jsonUrl = 'https://www.dcard.tw/service/api/v2/forums/cvs/posts?limit=30&before=%s'%top_id #用 top_id 找出第一頁的json
    return jsonUrl

#睡s1~s2秒 :no return
def sleep(s1,s2):
    rdnumber = random.randint(s1, s2)
    print('睡',rdnumber,'秒')
    time.sleep(rdnumber)

#從jsonUrl裡, 將n頁裡的文章分別變成字典,放進list :return json_CVS_list
def get_json_list(n,jsonUrl,json_load_list,id_list):
    i = 0 #爬取時觀察進度用
    json_CVS_list = json_load_list
    for times in range(n):
        res = requests.get(url=jsonUrl, headers=headers)
        js = json.loads(res.text)  # js is a list
        try:
            last_id = js[-1]['id']  # 最後一篇文章的id
        except:
            print('底下沒有文章囉!')
            break
        #造訪每一篇文章
        for article in js:
            #確認是否與資料庫資料重複
            id = article['id']
            if id in id_list:
                break
            #取得文章基本資訊
            article_dict = dict()
            article_dict['id'] = article['id']
            try:
                article_dict['categories'] = article['categories']
            except:
                article_dict['categories'] = 'No categories'
            article_dict['article_No'] = i
            article_dict['title'] = article['title']
            article_dict['topics'] = article['topics']
            article_dict['commentCount'] = article['commentCount']
            article_dict['likeCount'] = article['likeCount']
            article_dict['createdDate'] = article['createdAt'].split('T')[0]
            #取得文章HTML
            article_url = 'https://www.dcard.tw/f/cvs/p/%s'%article['id']
            res_article = requests.get(url=article_url, headers=headers)
            article_page = etree.HTML(res_article.text)
            #取得文章內容、熱門回應
            article_dict['content'] = article_page.xpath('//div[@class="sc-1eorkjw-5 fsPttV"]//div[@class="phqjxq-0 iHjLwQ"]/span/text()')
            article_dict['hot_reply'] = article_page.xpath('//div[@id="comment-anchor"]//span/text()')
            #把字典新增進list
            json_CVS_list.insert(i,article_dict)
            #觀察進度,且可知程式停在哪裡
            print(i,article_url)
            i += 1
        if id in id_list:
            break
        #睡3~10秒
        sleep(3,10)
        #取得下一篇的json
        jsonUrl = 'https://www.dcard.tw/service/api/v2/forums/cvs/posts?limit=30&before=%s'%last_id
    return json_CVS_list

#寫入json
def dumps_json_file(file_name,json_list):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_list, ensure_ascii=False))

def main():
    #變數設定
    global headers
    dictPath = './dcardCvs'
    filename = 'Dcard_CVS.json'
    page_number = 200

    #讀取json檔
    json_load_list = read_file_into_list('{}/{}'.format(dictPath,filename))

    #原有json檔裡的id放進list
    id_list = [each_dict['id'] for each_dict in json_load_list]

    #建立放置檔案的目錄(若沒有的話)
    make_directory(dictPath)

    #獲得最新超商版的josn_url
    jsonUrl = get_latest_jsonUrl()

    #抓取資料放進list(一篇文章為一個字典, 且與id list做比較, 若有重複就停止)
    json_CVS_list = get_json_list(page_number,jsonUrl,json_load_list,id_list)

    #寫回原本的檔案
    dumps_json_file('{}/{}'.format(dictPath,filename),json_CVS_list)

    # 確認筆數
    print(len(json_CVS_list))

if __name__ == '__main__':
    main()