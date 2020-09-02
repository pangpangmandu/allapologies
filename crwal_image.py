import re
import os
import collections
import requests

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote_plus


# 에러 리스트 생성 함수
def insert_error(blog_id, error, error_doc):
    for i in error_doc:
        error_log = str(error_doc["page"]) + "page / " + str(error_doc["post_number"]) \
                    + "th post / " + error + " / http://blog.naver.com/PostList.nhn?blogId=" + blog_id + "&currentPage=" + str(error_doc["page"])
    error_list.append(error_log)

# print("블로그 ID->")
# blog_id = input()


print("\n탐색 시작 페이지 수->")
start_p = int(input())

print("\n탐색 종료 페이지 수->")
end_p = int(input())


# 페이지 단위
for page in range(start_p, end_p + 1):

    url = "http://blog.naver.com/PostList.nhn?blogId=hotleve"+ "&currentPage=" + str(page)
    r = requests.get(url)
    if (not r.ok):
        print("Page" + page + "연결 실패, Skip")
        continue
    # html 파싱
    soup = BeautifulSoup(r.text.encode("utf-8"), "html.parser")
    postcategory = soup.find("span",{"class":"cate pcol2"})
    if postcategory == None:
      continue
    if "일상" in postcategory.text:
      print("일상")
    else:
      continue

    post = soup.find("table", {"id": "printPost1" })

    title = post.find("span", {"class": "pcol1 itemSubjectBoldfont"})
    tt= title.text 
    tt =tt.replace("\\","_").replace("/","_").replace(":","_").replace("*","_").replace("?","_").replace("<","_").replace(">","_").replace("|","_")
    if tt in os.listdir("C:/Users/srbin/Desktop/test/allapologies/일상_이미지/"):
        print("already in")
    else:
        os.mkdir("C:/Users/srbin/Desktop/test/allapologies/일상_이미지/"+tt)
    
    img = post.find_all("img")
    count =1
    for i in img:
        imgUrl = i.get('src')
        if "blogfiles" in imgUrl:
         imgUrl = imgUrl.replace('w80_blur','w1')
         print(imgUrl)
         with urlopen(imgUrl) as f:
            with open('.\일상_이미지\\' + tt+'\\'+str(count)+'.jpg','wb') as h: # w - write b - binary
              im = f.read()
              h.write(im)
              h.close()
        count +=1
