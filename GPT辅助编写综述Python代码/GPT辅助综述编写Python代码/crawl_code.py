import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor
import time
import re
import os


class CnkiSpider:
    def __init__(self, topic_1, topic_2, start_year="", end_year=""):
        self.session = requests.Session()
        self.topic_1 = topic_1
        self.topic_2 = topic_2
        self.start_year = start_year
        self.end_year = end_year
        self.SearchSql = ""
        self.dic = {
            "Platform": "",
            "DBCode": "CFLQ",
            "KuaKuCode": "",
            "QNode": {
                "QGroup": [
                    {
                        "Key": "Subject",
                        "Title": "",
                        "Logic": 4,
                        "Items": [],
                        "ChildItems": [
                            {
                                "Key": "input[data-tipid=gradetxt-1]",
                                "Title": "主题",
                                "Logic": 0,
                                "Items": [
                                    {
                                        "Key": "",
                                        "Title": self.topic_1,
                                        "Logic": 1,
                                        "Name": "SU",
                                        "Operate": "%=",
                                        "Value": self.topic_1,
                                        "ExtendType": 1,
                                        "ExtendValue": "中英文对照",
                                        "Value2": ""
                                    }
                                ],
                                "ChildItems": []
                            },
                            {
                                "Key": "input[data-tipid=gradetxt-2]",
                                "Title": "主题",
                                "Logic": 1,
                                "Items": [
                                    {
                                        "Key": "",
                                        "Title": self.topic_2,
                                        "Logic": 1,
                                        "Name": "SU",
                                        "Operate": "%=",
                                        "Value": self.topic_2,
                                        "ExtendType": 1,
                                        "ExtendValue": "中英文对照",
                                        "Value2": ""
                                    }
                                ],
                                "ChildItems": []
                            }
                        ]
                    },
                    {
                        "Key": "ControlGroup",
                        "Title": "",
                        "Logic": 1,
                        "Items": [],
                        "ChildItems": [
                            {
                                "Key": ".tit-startend-yearbox",
                                "Title": "",
                                "Logic": 1,
                                "Items": [
                                    {
                                        "Key": ".tit-startend-yearbox",
                                        "Title": "出版年度",
                                        "Logic": 1,
                                        "Name": "YE",
                                        "Operate": "",
                                        "Value": self.start_year,
                                        "ExtendType": 2,
                                        "ExtendValue": "",
                                        "Value2": self.end_year,
                                        "BlurType": ""
                                    }
                                ],
                                "ChildItems": []
                            },
                            {
                                "Key": ".extend-tit-checklist",
                                "Title": "",
                                "Logic": 1,
                                "Items": [
                                    {
                                        "Key": 0,
                                        "Title": "CSSCI",
                                        "Logic": 2,
                                        "Name": "CSI",
                                        "Operate": "=",
                                        "Value": "Y",
                                        "ExtendType": 14,
                                        "ExtendValue": "",
                                        "Value2": "",
                                        "BlurType": ""
                                    }
                                ],
                                "ChildItems": []
                            }
                        ]
                    }
                ]
            },
            "CodeLang": "",
            "View": "中国学术期刊网络出版总库,WWJD"
        }
        self.headers = {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "$Cookie": "Ecp_notFirstLogin=iNfrDo; cangjieStatus_NZKPT2=true; cangjieConfig_NZKPT2=%7B%22status%22%3Atrue%2C%22startTime%22%3A%222022-10-20%22%2C%22endTime%22%3A%222023-10-20%22%2C%22orginHosts%22%3A%22kns.cnki.net%22%2C%22type%22%3A%22mix%22%2C%22poolSize%22%3A%2210%22%2C%22intervalTime%22%3A10000%2C%22persist%22%3Afalse%7D; Ecp_ClientId=1230517192203051319; knsLeftGroupSelectItem=1%3B2%3B; Ecp_ClientIp=223.129.28.85; Ecp_loginuserjf=13008175520; dperpage=20; ASP.NET_SessionId=qcoy1deyircouw2atcw0flzt; SID_kns8=123146; LID=WEEvREcwSlJHSldSdmVpaVVVQVRBOXRLbHk5L1ZOVFlKNnFaTGpMbmRxZz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw\\u0021\\u0021; Ecp_session=1; Ecp_loginuserbk=XN0097; SID_recommendapi=126001; CurrSortField=%e7%9b%b8%e5%85%b3%e5%ba%a6%2frelevant%2c(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27time%27)+desc; CurrSortFieldType=desc; SID_kns_new=kns25128008; dblang=ch; Ecp_LoginStuts={\"IsAutoLogin\":false,\"UserName\":\"XN0097\",\"ShowName\":\"%E8%A5%BF%E5%8D%97%E6%B0%91%E6%97%8F%E5%A4%A7%E5%AD%A6\",\"UserType\":\"bk\",\"BUserName\":\"\",\"BShowName\":\"\",\"BUserType\":\"\",\"r\":\"iNfrDo\",\"Members\":[]}; c_m_LinID=LinID=WEEvREcwSlJHSldSdmVpaVVVQVRBOXRLbHk5L1ZOVFlKNnFaTGpMbmRxZz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw\\u0021\\u0021&ot=06%2F12%2F2023%2010%3A18%3A10; c_m_expire=2023-06-12%2010%3A18%3A10",
            "Origin": "https://kns.cnki.net",
            "Referer": "https://kns.cnki.net/kns8/AdvSearch?dbprefix=CFLS&&crossDbcodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCJD%2CCCVD%2CCJFN",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.cookies = {
            "cangjieStatus_NZKPT2": "true",
            "cangjieConfig_NZKPT2": "%7B%22status%22%3Atrue%2C%22startTime%22%3A%222022-10-20%22%2C%22endTime%22%3A%222023-10-20%22%2C%22orginHosts%22%3A%22kns.cnki.net%22%2C%22type%22%3A%22mix%22%2C%22poolSize%22%3A%2210%22%2C%22intervalTime%22%3A10000%2C%22persist%22%3Afalse%7D",
            "Ecp_ClientId": "1230517192203051319",
            "Ecp_ClientIp": "223.129.28.85",
            "Ecp_loginuserjf": "13008175520",
            "dperpage": "20",
            "Ecp_loginuserbk": "XN0097",
            "knsLeftGroupSelectItem": "1%3B2%3B",
            "Ecp_IpLoginFail": "230623182.138.84.171",
            "SID_kns_new": "kns25128007",
            "ASP.NET_SessionId": "5mhvnpaijvkmtpvcpns1zzmr",
            "SID_kns8": "123154",
            "CurrSortField": "%e7%9b%b8%e5%85%b3%e5%ba%a6%2frelevant%2c(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27time%27)+desc",
            "CurrSortFieldType": "desc",
            "SID_recommendapi": "126002",
            "dblang": "ch"
        }
        self.titles = []
        self.authors = []
        self.first_authors = []
        self.sources = []
        self.public_time = []
        self.quotes = []
        self.downloads = []
        self.links = []
        self.abstracts = []
        self.keywords = []
        self.fundings = []
        self.dois = []
        self.numss = []
        self.units = []

    def get_first_page(self):
        url = "https://kns.cnki.net/kns8/Brief/GetGridTableHtml"
        data = {
            "IsSearch": "true",
            "QueryJson": str(self.dic),
            "PageName": "AdvSearch",
            "DBCode": "CFLS",
            "KuaKuCodes": "CJFQ,CCND,CIPD,CDMD,BDZK,CISD,SNAD,CCJD,CJFN,CCVD",
            "CurPage": "1",
            "RecordsCntPerPage": "50",
            "CurDisplayMode": "listmode",
            "CurrSortField": "",
            "CurrSortFieldType": "desc",
            "IsSentenceSearch": "false",
            "Subject": ""
        }
        response = self.session.post(url, headers=self.headers, cookies=self.cookies, data=data)
        response.encoding = 'utf-8'
        return response

    def get_total_page(self, response):
        text = response.text
        total_page = re.findall(r"<span class='countPageMark'>1/(\d+)</span>", text)[0]
        return total_page

    def get_SearchSql(self, response):
        text = response.text
        html = etree.HTML(text)
        value = html.xpath("//input[@id='sqlVal']/@value")[0]
        return value

    def get_other_page(self, page):
        data = {
            "IsSearch": "false",
            "QueryJson": self.dic,
            "SearchSql": self.SearchSql,
            "PageName": "AdvSearch",
            "HandlerId": "9",
            "DBCode": "CFLQ",
            "KuaKuCodes": "CJFQ,CDMD,CIPD,CCND,BDZK,CISD,SNAD,CCJD,GXDB_SECTION,CJFN,CCVD",
            "CurPage": "1",
            "RecordsCntPerPage": "50",
            "CurDisplayMode": "listmode",
            "CurrSortField": "DOWNLOAD",
            "CurrSortFieldType": "desc",
            "IsSortSearch": "false",
            "IsSentenceSearch": "false",
            "Subject": ""
        }
        url = "https://kns.cnki.net/kns8/Brief/GetGridTableHtml"
        data['CurPage'] = page
        response = requests.post(url, headers=self.headers, data=data)
        return response

    def get_msg(self, response, page=1):
        text = response.text
        tree = etree.HTML(text)

        # 使用XPath表达式提取目标元素
        xpath_expression = '//table[@class="result-table-list"]//tr'
        trs = tree.xpath(xpath_expression)

        for num, tr in enumerate(trs[1:], start=1):
            title = ''.join(tr.xpath("./td[2]/a//text()")).strip()
            authors = tr.xpath("./td[@class='author']/a//text()")
            if authors == []:
                first_author = None
                author = None
            else:
                first_author = authors[0]
                author = ';'.join(authors).strip()
            try:
                source = ''.join([i.strip() for i in tr.xpath("./td[4]/a//text()") if i.strip()])
            except:
                source = None
            date = tr.xpath("./td[5]/text()")[0].strip()
            try:
                quote = ''.join([i.strip() for i in tr.xpath("./td[@class='quote']//text()") if i.strip()])
            except Exception as e:
                print(e)
                quote = None
            try:
                download = ''.join([i.strip() for i in tr.xpath('./td[@class="download"]//text()') if i.strip()])
            except Exception as e:
                print(e)
                download = None
            href = 'https://kns.cnki.net' + tr.xpath("./td[2]/a/@href")[0]
            # results.append([title, author, first_author, source, date, quote, download, href])
            self.titles.append((title))
            self.authors.append(author)
            self.first_authors.append(first_author)
            self.sources.append(source)
            self.public_time.append(date)
            self.quotes.append(quote)
            self.downloads.append(download)
            self.links.append(href)
            self.get_detail(href)
            print(f"[{page}-{num}]《{title}》爬取成功")

    @staticmethod
    def get_text_by_xpath(tree, xpath):
        try:
            element = tree.xpath(xpath)
            if element:
                return element[0].strip()
            else:
                return None
        except Exception as e:
            print(f"Failed to get text by xpath due to {e}")
            return None

    @staticmethod
    def get_texts_by_xpath(tree, xpath):
        try:
            elements = tree.xpath(xpath)
            return [element.strip() for element in elements if element.strip()]
        except Exception as e:
            print(f"Failed to get texts by xpath due to {e}")
            return []

    def get_detail(self, url):
        retry = 1
        for i in range(20):
            try:
                res = self.session.get(url,timeout=50)
                break
            except Exception as e:
                print(f"{url}:获取摘要信息失败{e}……正在重试[{retry}]")
                time.sleep(2)
                retry += 1
        tree = etree.HTML(res.text)
        abstract = CnkiSpider.get_text_by_xpath(tree, '//*[@id="ChDivSummary"]/text()')
        keywords = CnkiSpider.get_texts_by_xpath(tree, '//p[@class="keywords"]/text()')
        fundings = CnkiSpider.get_texts_by_xpath(tree, '//p[@class="funds"]/a/text()')
        numss = CnkiSpider.get_texts_by_xpath(tree, '//div[@class="top-tip"]/span/a[2]/text()')
        units = CnkiSpider.get_texts_by_xpath(tree, '//div[@class="wx-tit"]/h3[2]//text()')

        # 获取 DOI
        doi = None
        info_items = tree.xpath('/html/body/div[2]/div[1]/div[3]/div/div/div[7]/ul/li')
        for item in info_items:
            name = item.xpath('./span/text()')
            value = item.xpath('./p/text()')
            if name and value and name[0].strip() == 'DOI：':
                doi = value[0].strip()
        self.abstracts.append(abstract)
        self.keywords.append(','.join(keywords))
        self.fundings.append(','.join(fundings))
        self.numss.append(','.join(numss))
        self.units.append(','.join(units))
        self.dois.append(doi)

    def crawl_paper_data(self):
        first_response = self.get_first_page()
        search_sql = self.get_SearchSql(first_response)
        self.SearchSql = search_sql
        total_page = self.get_total_page(first_response)
        print(f"共需要爬取{total_page}页")
        with ThreadPoolExecutor(max_workers=10) as executor:
        # 使用 map 方法提交任务并等待结果
            # 假设 self.get_other_page 是获取其他页的函数
            executor.map(self.crawl_page_data, range(1, int(total_page) + 1))
        # for page in range(1, int(total_page) + 1):
        #     self.crawl_page_data(page)
        df_dic = {
            '篇名': self.titles,
            '作者': self.authors,
            '第一责任人': self.first_authors,
            '文献来源': self.sources,
            '发表时间': self.public_time,
            '摘要': self.abstracts,
            '基金资助': self.fundings,
            '所属期数': self.numss,
            '所属单位': self.units,
            'DOI': self.dois,
            '被引频次': self.quotes,
            '下载频次': self.downloads,
            '网址': self.links
        }
        print("爬取完成！导出为字典")
        return df_dic

    def crawl_page_data(self, page):
        print(f"正在爬取第{page}页...\n")
        res = self.get_other_page(page)
        self.get_msg(res, page)
        print(f"\n第{page}页获取成功！\n")

    def save_as_csv(self, df_dic,save_name='result.csv'):
        field_names = df_dic.keys()
        rows = zip(*df_dic.values())
        file_path = f'./{self.topic_1}+{self.topic_2}'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        save_path = f"{file_path}/{save_name}"
        with open(f'{save_path}', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)
            writer.writerows(rows)

if __name__ == '__main__':
    topic1 = '数字金融'
    topic2 = '企业创新'
    Cnki = CnkiSpider(topic1, topic2)

    df_dic = Cnki.crawl_paper_data()
    print("开始导出文件……")
    Cnki.save_as_csv(df_dic)
