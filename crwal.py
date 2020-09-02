import codecs

import re

import collections
import requests

from bs4 import BeautifulSoup


# 에러 리스트 생성 함수
def insert_error(blog_id, error, error_doc):
    for i in error_doc:
        error_log = str(error_doc["page"]) + "page / " + str(error_doc["post_number"]) \
                    + "th post / " + error + " / http://blog.naver.com/PostList.nhn?blogId=" + blog_id + "&currentPage=" + str(error_doc["page"])
    error_list.append(error_log)

total_num = 0;

error_list = []

# print("블로그 ID->")
# blog_id = input()


print("\n탐색 시작 페이지 수->")
start_p = int(input())

print("\n탐색 종료 페이지 수->")
end_p = int(input())

print("\nCreating File Naver_Blog_Crawling_Result.txt...\n")

# 파일 열기
# file = codecs.open("Naver_Blog_Crawling_Result.txt", 'w', encoding="utf-8")

# 페이지 단위
for page in range(start_p, end_p + 1):

    # print("=" * 50)
    # file.write("=" * 50 + "\n")
    doc = collections.OrderedDict()

    url = "http://blog.naver.com/PostList.nhn?blogId=hotleve"+ "&currentPage=" + str(page)
    r = requests.get(url)
    if (not r.ok):
        print("Page" + page + "연결 실패, Skip")
        continue

    # html 파싱
    soup = BeautifulSoup(r.text.encode("utf-8"), "html.parser")

    postcategory = soup.find("span",{"class":"cate pcol2"})
    # if postcategory == None:
    #   continue
    # # print(postcategory.text)
    # if "일상" in postcategory.text:
    #   print("일상")
    # else:
    #   continue


    # 페이지 당 포스트 수 (printPost_# 형식의 id를 가진 태그 수)
    # post_count = len(soup.find_all("table", {"id": re.compile("printPost.")}))

    doc["page"] = page
    post = soup.find("table", {"id": "printPost1"})

        # 제목 찾기---------------------------
    if postcategory == None:
      continue

        # 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)

    title = post.find("span", {"class": "pcol1 itemSubjectBoldfont"})
    if (title == None):
      title = post.find("span", {"class": "pcol1 itemSubjectBoldfont"})

    if (title != None):
      doc["title"] = title.text.strip()
    else:
      doc["title"] = "TITLE ERROR"
    title= title.text.replace("/", '_').replace("[", '_').replace("]", '_').replace("<", '_').replace(">", '_').replace(" ", '_').replace('"', '_').replace(",", '_').replace("'", '_').replace("*", '_')
    file = codecs.open(".\\"+ str(postcategory.text.strip())+"\\"+title+".txt", 'w', encoding="utf-8")
    file.write(postcategory.text + "\n")
        # 날짜 찾기---------------------------

    date = post.find("span", {"class": re.compile("se_publishDate.")})

        # 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)
    if (date == None):
      date = post.find("p", {"class": "date fil5 pcol2 _postAddDate"})

    if (date != None):
      doc["date"] = date.text.strip()
    else:
      doc["date"] = "DATE ERROR"

        # 내용 찾기---------------------------


        # 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)

    content_up = post.find("div", {"id": "postViewArea"})
    content = content_up.find_all("p")
    diary = ""
    for wrapper in content:
      diary += "\n"+ wrapper.text
        
    doc["content"] = diary
        # if (title != None):
        #     # Enter 5줄은 하나로
        #     doc["content"] = "\n" + content.text
        #     # .strip().replace("\n" * 5, "\n")
        # else:
        #     doc["content"] = "CONTENT ERROR"

        # doc 출력 (UnicodeError - 커맨드 창에서 실행 시 발생)
    for i in doc:
      str_doc = str(i) + ": " + str(doc[i])
      try:
        print(str_doc)
      except UnicodeError:
        print(str_doc.encode("utf-8"))

            # 파일 쓰기
    file.write(str_doc + "\n")

            # 에러 처리
    if ("ERROR" in str(doc[i])):
                insert_error(blog_id, doc[i], doc)

        # 전체 수 증가
    file.close()