

# -*- encoding:utf8 -*-
import csv
import requests
import re
from bs4 import BeautifulSoup

def spider(url):
    cookie = '''skin=noskin; session-id=136-6182090-1781957; session-id-time=2082787201l; sp-cdn="L5Z9:CN"; ubid-main=131-9980935-5295001; lc-main=en_US; i18n-prefs=USD; session-token="3IsKvOtCmwkpEime4kfSqAfi2t7DOO4UE0blsqLMaSZATXHw5dwotbGFs2pob9uBOENrlq1VVxqg7OvlV2e0iwRdPz5/WrbTpjwfZYCMV95C6peDOJrLFoiAeS/T4WO0TtRs1aqxU5itiC5nK+V8HrmSoNUKjX+3JkE1/v7erZwoxi04Q4lDUU+g+WHv2MfFXmdOEbMBvLPjCPTIbIcAQ8NdWE9DvqH1Hifg59wGJN4="; x-main="CoBAbAI3oEdUdOWo0HrHnQx2gukaQQdKMVxAdM0UQFMAH8TeN@qmj77VErbfb0JK"; at-main=Atza|IwEBINMxChmbFDnQF5JwKSf73WhFG7argYibMx8HnLaKIHqLArvscn10tbim1G035LfSV0q2Fkf0oRVcxOkPQsw_i1LI86najSeezPcwmpvRiDhvsTeMTVSSAa8lyj5RKf1IMvyvv1eK6otzTCkfcLeC2a-q53pHY14Esgy1Br-D6mZoHpEIvwFSlsYx1H7CqAO90-wiONwu1ruicD9C2R97Bf7TjeHPXLNPIfNzLiucTTWgjG4yjfOpCn-Oj2m6aHrchbdW6PzbLO_RdBKKQPD5c9OQA7OpC1NQCrd34-hMUkx7bqwCjkfaNi4m0AkslNng2ansVBF2Oswm2y0e69OJRrYSr4a2rQ7y9VeJ5lR2mR9hs1nrkwggNYwk0Tw0t2uiyRrWLZ7H3dCQniEdArvhlHN9; sess-at-main="4MoZp47aARBF3+OIYpAlk6oLUYFEwcXvftfWx29dIOA="; sst-main=Sst1|PQGFnGITTKG7HM0O7wiOi2mDC3gP339o0dxf4mLGaUC7YQVWJgVPQ6xLS4VckfgNdc-gfVm6Gi1WlHjpw4Z18vzoze0chWN8_aCA9_1OzO92FBabDiUhGs3PGfSxKHhjshd2rOE7D5pou04J2NncpvTrq76Gc766V0BBquJ-2AJvX_1DJkSvOtTkJeITmDMsIc2Z3_26ZwyTzTzbg7QRxSlbD3sC4jiR-C3WAmDgGnMqlk_VlZ6NJvsKsfaedCqtJ0I_mFLqkUUE0GqmFKCeISrZHAoD5nZPXgvdG2sdhwhuuIb4xO_CaoIE2a9NrKNvhkS-4s3VucdmbifSgnd82jLWqQ; x-wl-uid=1MPOZRPRPKiA8AX1pch5yaqpDYdulXSh+Ai+DzXERvIlxkRaPE3+ukOBwAiG+hvb1wj6Ea75SjL9q/MUywVN6sqO68ZsXyYXyyYLHWtEE9Xh31O7pWJ9+9Xctl0rni7v1pfYleal8asg=; csm-hit=tb:Q5N78F9B655T8SMA4XG6+s-E27BYYXJJR1XDX1N20RD|1558406741846&t:1558406741846&adb:adblk_no'''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'cookie':cookie}

    return requests.get(url=url, headers=headers)

def spider_detail(urls):
    response1 = spider(urls[0])
    print(response1.url)
    if response1.text:
        soup1 = BeautifulSoup(response1.text,'lxml')
        #匹配结果result
        result1 = soup1.select('div[class="sg-col-inner"] span')
        pattern11 = re.compile('.*?of(.*?)results.*?',re.S)
        if result1[0].get_text():
            num = re.search(pattern11,result1[0].get_text())
            if num:
                #匹配url中关键字
                pattern12 = re.compile('https://www.amazon.com/s\?k=(.*?)&ref=nb_sb_noss_1', re.S)
                keyword = re.search(pattern12, response1.url)
                Key = ' '.join((keyword.group(1).split("+"))).replace("%22",'"')
                num_o = num.group(1)

    response2 = spider(urls[1])
    print(response2.url)
    if response2.text:
        soup = BeautifulSoup(response2.text, 'lxml')
        # 匹配结果result
        result2 = soup.select('div[class="sg-col-inner"] span')
        pattern21 = re.compile('.*?of(.*?)results.*?', re.S)
        if result2[0].get_text():
            num_h = re.search(pattern21, result2[0].get_text())
            if num_h:
                num_h = num_h.group(1)

    result_num.append([Key,num_o,num_h])

def artical_write(result_num):
    with open('KeyWord2.csv', 'wt',newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(['KeyWrods','num_o','num_h'])
        # 再写入数据
        for res in result_num:
            writer.writerow([res[0],res[1],res[2]])



if __name__ == '__main__':

    global result_num
    result_num = []

    #读取文档中的关键字
    with open('KeyWord.csv', 'r') as KW:
        KeyWrods = KW.readlines()

    # url列表收集
    all_url = []
    url = 'https://www.amazon.com/s?k='
    strings = '&ref=nb_sb_noss_1'
    for i in KeyWrods:
        i_string = '"' +'+'.join(i.split(" ")).strip() + '"'
        all_url.append([url + '+'.join(i.split(" ")).strip() +strings,url + i_string + strings])

    for url in all_url:
        spider_detail(url)
        #print(result_num)
        artical_write(result_num)