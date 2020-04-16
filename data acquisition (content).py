import random
import re
import requests
from openpyxl import Workbook
from time import sleep
import pandas as pd
import math

data = pd.read_csv('user&item base data.csv',usecols=['movie'])
df1 = data.iloc[:,0].tolist()

arr = []

for x in df1:
    if math.isnan(x):
        continue
    if x<100000:
        arr.append('00'+str(int(x)))
        continue
    if x<1000000:
        arr.append('0'+str(int(x)))
        continue
    arr.append(str(int(x)))


def find_all_by_pat(pat, string):
    res = re.findall(pat, string)
    return res


def get_html_doc(url):
    pro = ['122.152.196.126', '114.215.174.227', '119.185.30.75']
    head = {
        'user-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36'
    }
    resopnse = requests.get(url, proxies={'http': random.choice(pro)}, headers=head)
    resopnse.encoding = 'utf-8'
    html_doc = resopnse.text
    return html_doc

def get_detail_html(query_id):
    url = 'https://www.imdb.com/title/tt' + query_id
    print(url)
    douban_search_res = get_html_doc(url)
    return douban_search_res

def get_name(pat, doc):
    res = find_all_by_pat(pat, doc)
    try:
        # return res[0].split('/')[1]
        return res[0]
    except:
        return ' '

if __name__ == "__main__":
    # pat = r'<td class="titleColumn">\s*(.*)..*\s*.*\s*title=".*" >(.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span>'
    # pat = r'<td class="titleColumn">\s*(.*)..*\s*(.*)\s*title=".*" >(.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span>'
    # queryid = ['00242653', '00110912']
    res = len(arr)*[[]]
    print(res)
    for i in range(len(arr)):
        doc = get_detail_html(arr[i])
        pat1 = '<meta name="title" content="(.*)\(.*'
        pat4 = '<div\s*class="summary_text">\s*(.*)\s*</div>'
        detail = get_name(pat4, doc)
        title = get_name(pat1, doc)
        print(detail)
        print(title)
        res[i]=[title,detail]
        print(res)
        sleep(random.random() * 3)

    wb = Workbook()
    sheet = wb.active
    for i in range(len(res)):
        for j in range(len(res[i])):
            sheet.cell(row=i + 1, column=j + 1).value = res[i][j]
    wb.save('content based data.xlsx')

