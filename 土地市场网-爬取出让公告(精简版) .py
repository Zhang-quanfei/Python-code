#!/usr/bin/env python
# coding: utf-8

# ### 爬取单个省

# In[1]:


import re
import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException


# In[2]:


# 点击省份
def chooseProvince(browser, province):
    while True:
        try:
            # 点击下拉框
            dropdown = browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[3]/form[1]/div[1]/div/div/div/span/span/i')
            dropdown.click()
            time.sleep(random.uniform(1, 3))
            
            # 在下拉框中查找省份并点击
            provinces = browser.find_elements_by_xpath('//*[@class="el-cascader-node__label"][1]')
            for p in provinces:
                if province in p.text:
                    browser.execute_script("arguments[0].scrollIntoView();", p)
                    p.click()
                    print("成功点击一次省")
                    break
                    
            time.sleep(random.uniform(3, 5))
            break
        except ElementClickInterceptedException:
            print("Province Element click was intercepted by another element.")
            time.sleep(3)
            #取消下拉框
            dropdown = browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[3]/form[1]/div[1]/div/div/div/span/span/i')
            dropdown.click()

# 提取地级市信息
def getCity(browser, province):
    while True:
        try:
            # 点击激活下拉框
            dropdown = browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[3]/form[1]/div[1]/div/div/div/span/span/i')
            dropdown.click()
            time.sleep(random.uniform(3, 5))
            
            # 在下拉框中查找省份并点击
            provinces = browser.find_elements_by_xpath('//*[@class="el-cascader-node__label"][1]')
            for p in provinces:
                if province in p.text:
                    browser.execute_script("arguments[0].scrollIntoView();", p)
                    p.click()
                    print("成功点击一次省")
                    break
                    
            time.sleep(random.uniform(2, 4))
            cityname = (browser.find_elements_by_xpath('//*[@class="el-cascader-node__label"][1]'))[35:]
            break
        except ElementClickInterceptedException:
            print("Element click was intercepted by another element.")
            time.sleep(3)
            dropdown = browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[3]/form[1]/div[1]/div/div/div/span/span/i')
            dropdown.click()
    num = len(cityname)

    return cityname, num


# In[3]:


# 定义一个函数，用于从页面上获取地块总数
def getnum(browser):
    html = browser.page_source
    num=int(re.findall(r'共 (\d+) 条',html)[0])
    return num

# 获取总页码数字
def getSumNum(browser):
    html = browser.page_source
    num = int(re.search(r'max="(\d+)"', html).group(1))
    return num

# 获取当前活动页面
def getActiveNum(browser):
    html = browser.page_source
    num = int(re.findall(r'<li class="number active">(\d+)</li>', html)[0])
    return num


# In[4]:


# 获取页面信息
def getList(browser,pname,cname,countyname,year,anno_time):   #pname自己输入
    global total_num ,error
    id = [browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[3]')[0].text]
    tab1=browser.find_elements_by_class_name('tabCard')  #获取地块信息、出让公告等一级标题，获得的是Webelement
    tab2=browser.find_elements_by_class_name('title')  #获取基础信息等二级标题，获得的是Webelement
    tr = browser.find_elements_by_css_selector('[class^="detailRight"]') #[class^="detailRight"] 是一个 CSS 选择器，它表示选择所有具有以 detailRight 开头的类名的元素
    #开始获取信息
    year = year
    anno_time = anno_time
    province = [pname]
    city = [cname] 
    county = [countyname]
    current_url = [browser.current_url]  #获取当前页面的地址
    for x in tr:
        # 获取基础信息
        distract = [tr[0].text]
        supply = [tr[1].text]
        land_locate = [tr[2].text]
        land_use = [tr[3].text]
        transfer_period = [tr[4].text]
        land_rank = [tr[5].text]
        transfer_area = [tr[6].text]
        building_area = [tr[7].text]
        plot = [tr[8].text]
        green = [tr[9].text]
        building_density = [tr[10].text]
        height_limit = [tr[11].text]
        # 获取土地交易信息
        Starting_time_auction = [tr[12].text]
        Deadline_time_auction = [tr[13].text]
        Starting_time_registration = [tr[14].text]
        Deadline_time_registration = [tr[15].text]
        starting_price = [tr[16].text]
        earnest_money = [tr[17].text]
        Increase_price = [tr[18].text]
        Invest_density  = [tr[19].text]
        sale_price = [tr[20].text]
        assign_person = [tr[21].text]
        sale_announce_date = [tr[22].text]
        # 获取合同信息
        if len(tab2) > 2:
            contract_date = [tr[23].text]
            land_source = [tr[24].text]
            project_name = [tr[25].text]
            contract_id = [tr[26].text]
            land_user = [tr[27].text]
            industry_class = [tr[28].text]
            regulatory_number = [tr[29].text]
            delivery_land_time = [tr[30].text]
            approximate_plot = [tr[31].text]
            complete_time = [tr[32].text]
            open_time = [tr[33].text]
            Instalment_agreement = [tr[-1].text.split("\n")]
        else:
            contract_date = ["--"]
            land_source = ["--"]
            project_name = ["--"]
            contract_id = ["--"]
            land_user = ["--"]
            industry_class = ["--"]
            regulatory_number = ["--"]
            delivery_land_time = ["--"]
            approximate_plot = ["--"]
            complete_time = ["--"]
            open_time = ["--"]
            Instalment_agreement = ["--"]
    # 获取文字
    y = tab1[0].text.split("\n")

    # 判断是否有出让公告
    if "出让公告" in y:
        while 1:
            try:
                p = y.index("出让公告") + 1
                browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[5]/div[{}]'.format(p)).click()
                break
            except IndexError:
                print("出让公告 Index is out of range")
        time.sleep(3)
        h = browser.find_elements_by_class_name('baseList')
        if len(h) > 0: 
            WebElement = [browser.find_elements_by_class_name('baseList')[0]]
            sum_anno = [browser.find_elements_by_class_name('baseList')[0].text]  #获取出让公告
        else:
            u = browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[6]')
            if len(u) > 0:
                WebElement = [browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[6]')[0]]
                sum_anno = [browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[6]')[0].text]
            else:
                WebElement = [browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[6]/table/tbody')[0]]
                sum_anno = [browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[6]/table/tbody')[0].text]  # 获取出让公告

    else:
        WebElement = ["--"]
        sum_anno = ["--"]
    #判断是否有地块公示 
    if "地块公示" in y:
        while 1:
            try:
                p = y.index("地块公示") + 1
                browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[5]/div[{}]'.format(p)).click()
                break
            except IndexError:
                print("地块公示 Index is out of range")
        time.sleep(3)
        h = browser.find_elements_by_class_name('baseList')
        if len(h) > 0:
            Plot_publicity = [browser.find_elements_by_class_name('baseList')[0].text]  #获取地块公示
        else:
            d = browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[6]')
            if len(d) > 0:
                Plot_publicity = [browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[6]')[0].text] #获取地块公示
            else:
                Plot_publicity = [browser.find_elements_by_xpath('//*[@id="appMain"]/div/div[3]/div[6]/table/tbody')[0].text] #获取地块公示

    else:
        Plot_publicity = ["--"]
    if(len(id)==len(distract)==len(supply)==len(land_locate)==len(land_use)==len(transfer_period)==
        len(land_rank)==len(transfer_area)==len(building_area)==len(plot)==len(green)==len(building_density)==len(height_limit )==
        #土地信息
        len(Starting_time_auction)==len(Deadline_time_auction)==len(Starting_time_registration)==len(Deadline_time_registration)==len(starting_price )==
        len(earnest_money)==len(Increase_price)==len(Invest_density)==len(sale_price)==len(assign_person)==len(sale_announce_date)==
        #合同信息
        len(contract_date)==len(land_source)==len(project_name)==len(contract_id)==len(land_user)==len(industry_class)==len(regulatory_number)==
        len(delivery_land_time)==len(approximate_plot)==len(complete_time)==len(open_time)==len(Instalment_agreement)==len(sum_anno)==
        len(current_url)==len(WebElement)==len(Plot_publicity)):

        sum_data=len(id)
        total_num +=1
        print('成功爬取'+str(sum_data)+'条数据','总第'+str(total_num)+'条记录') 
        #,'省份':province,'城市':city,'区县':county
        df=pd.DataFrame({
            '年份':year,'省份':province,'城市':city,'区县':county,'宗地编号':id, '公告发布时间':anno_time,
            #基础信息
            '行政区':distract ,'供应方式':supply ,'土地坐落':land_locate ,'土地用途':land_use ,'出让年限':transfer_period ,'土地级别':land_rank ,
            '出让面积':transfer_area ,'建筑面积':building_area ,'容积率':plot ,'绿化率':green ,'建筑密度':building_density ,'建筑限高':height_limit ,
            #土地交易信息
            '招拍挂起始时间':Starting_time_auction ,'招拍挂截止时间':Deadline_time_auction ,'报名起始时间':Starting_time_registration ,'报名截止时间':Deadline_time_registration ,'起始价':starting_price ,
            '竞买保证金':earnest_money ,'加价幅度':Increase_price ,'投资强度':Invest_density ,'成交价':sale_price ,'受让人':assign_person ,'成交公示日期':sale_announce_date ,
            #合同信息
            '合同签订日期':contract_date ,'土地来源':land_source ,'项目名称':project_name ,'合同编号':contract_id ,'土地使用权人':land_user ,'行业分类':industry_class ,'电子监管号':regulatory_number ,
            '约定交地时间':delivery_land_time ,'约定容积率':approximate_plot ,'约定竣工时间':complete_time ,'约定开工时间':open_time ,'分期支付约定':Instalment_agreement ,
            '出让公告':sum_anno, '地块公示':Plot_publicity, '地块链接':current_url,'公告WebElement':WebElement
    })
    else:
        print('数量不匹配，爬取失败')
        error+=1
        return pd.DataFrame()
    return df


# In[5]:


def save_per10():
    global sumDf
    batch_size = 20
    # 每爬取大于等于10条数据，将数据存入文件并重置计数器和数据列表
    if len(sumDf) >= batch_size:
        filename = r"F:\Users\zhang\Desktop\土地爬取\辽宁省.csv"  # 替换为您要检查的文件路径
        # 如果文件已经存在，将数据追加到文件中，否则创建新文件
        if os.path.exists(filename):
            sumDf.to_csv(filename, index=False, mode='a', header=False,encoding='utf_8_sig')
            print(f"Saved {batch_size} records to {filename}")
        else:
            sumDf.to_csv(filename, index=False, encoding='utf_8_sig')
            print(f"Saved {batch_size} records to {filename}")
        sumDf=pd.DataFrame()


# In[6]:


# 获取页面信息
def process_page(browser, pname, cname, countyname):
    global count_num,sumDf
    for i in range(2, 12):
        while True:
            try:
                # 点击列表项
                table_row_xpath = '//*[@id="appMain"]/div/div[5]/table/tr[{}]'.format(i)
                anno_time = [browser.find_elements_by_xpath(table_row_xpath+'/td[7]')[0].text]
                year = [anno_time[0][0:4]]
                
                browser.find_element_by_xpath(table_row_xpath).click()
                wins = browser.window_handles
                browser.switch_to.window(wins[-1])
                
                xpath = '//*[@id="appMain"]/div/div[3]/div[3]'
                wait = WebDriverWait(browser, 10)  # 最长等待时间为10秒
                wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                df = getList(browser, pname, cname, countyname, year, anno_time)
                break
            except IndexError:
                print("Index is out of range")
                browser.close()
                browser.switch_to.window(wins[-2])
                time.sleep(random.uniform(3, 5))
            except TimeoutException:
                print("等待超时：页面元素未能在指定时间内出现")
                browser.close()
                browser.switch_to.window(wins[-2])
                time.sleep(random.uniform(3,5))
            except:
                print("点击下一条记录失败")
                time.sleep(random.uniform(3, 5))

        sumDf = pd.concat([sumDf, df], ignore_index=True)  # 汇总
        save_per10() 
        
        #返回原页面
        browser.close()
        browser.switch_to.window(wins[-2])

    return sumDf

# 获取最后一页信息
def process_last_page(browser, pname, cname, countyname, end_num):
    global count_num,sumDf
    for i in range(2, end_num+2):
        while i < end_num+2:
            try:
                # 点击列表项
                table_row_xpath = '//*[@id="appMain"]/div/div[5]/table/tr[{}]'.format(i)
                wait = WebDriverWait(browser, 10)  # 最长等待时间为10秒
                element = wait.until(EC.visibility_of_element_located((By.XPATH, table_row_xpath)))
                
                anno_time = [browser.find_elements_by_xpath(table_row_xpath+'/td[7]')[0].text]
                year = [anno_time[0][0:4]]
                browser.find_element_by_xpath(table_row_xpath).click()
                wins = browser.window_handles
                browser.switch_to.window(wins[-1])
                
                xpath = '//*[@id="appMain"]/div/div[3]/div[3]'
                wait = WebDriverWait(browser, 10)  # 最长等待时间为10秒
                wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                df = getList(browser, pname, cname, countyname, year, anno_time)
                break
            except IndexError:
                print("列表  Index is out of range")
                browser.close()
                browser.switch_to.window(wins[-2])
                time.sleep(random.uniform(3, 5))
            except TimeoutException:
                print("等待超时：页面元素未能在指定时间内出现")
                browser.close()
                browser.switch_to.window(wins[-2])
                time.sleep(random.uniform(3,5))
            except:
                print("点击下一条记录失败")
                time.sleep(random.uniform(3, 5))

        sumDf = pd.concat([sumDf, df], ignore_index=True)  # 汇总
        save_per10()
        #返回原页面
        browser.close()
        browser.switch_to.window(wins[-2])

    return sumDf

# 点击总页码小于9的页码
def process_pages(browser, pname, cname, countyname, start_num, end_num):
    global sumDf
    for num in range(start_num, end_num):
        while True:
            try:
                # 点击下一页
                next_page_xpath = '//*[@id="appMain"]/div/div[5]/div/div/ul/li[{}]'.format(num)
                browser.find_element_by_xpath(next_page_xpath).click()
                table_xpath = '/html/body/div/div/div[5]/table/tr[2]'
                wait = WebDriverWait(browser, 10)  # 最长等待时间为10秒
                wait.until(EC.visibility_of_element_located((By.XPATH, table_xpath)))
                break
            except IndexError:
                print("点击下一页 Index is out of range")
                time.sleep(random.uniform(3, 5))
            except TimeoutException:
                print("等待超时：页面元素未能在指定时间内出现")
                browser.close()
                browser.switch_to.window(wins[-2])
                time.sleep(random.uniform(3,5))
            except:
                print("点击下一页失败")
                time.sleep(random.uniform(3, 5))

        print("这是第" + str(getActiveNum(browser)) + "页")
        sumDf = process_page(browser, pname, cname, countyname)

    return sumDf

# 点击总页码大于8的页码
def process_pages1(browser, pname, cname, countyname, start_num, end_num):
    global sumDf
    for num in range(start_num, end_num):
        while True:
            try:
                # 点击下一页
                next_page_xpath = '//*[@id="appMain"]/div/div[5]/div/div/ul/li[6]'
                browser.find_element_by_xpath(next_page_xpath).click()
                table_xpath = '/html/body/div/div/div[5]/table/tr[2]'
                wait = WebDriverWait(browser, 10)  # 最长等待时间为10秒
                wait.until(EC.visibility_of_element_located((By.XPATH, table_xpath)))
                break
            except IndexError:
                print("点击下一页 Index is out of range")
                time.sleep(random.uniform(3, 5))
            except TimeoutException:
                print("等待超时：页面元素未能在指定时间内出现")
                browser.close()
                browser.switch_to.window(wins[-2])
                time.sleep(random.uniform(3,5))
            except:
                print("点击下一页失败")
                time.sleep(random.uniform(3, 5))

        print("这是第" + str(getActiveNum(browser)) + "页")
        sumDf = process_page(browser, pname, cname, countyname)

    return sumDf


# In[7]:


# 切换页码和记录
def chooseNum1(browser, pname, cname, countyname):
    global sumDf
    if getSumNum(browser) < 9:
        k = getSumNum(browser)
        if getActiveNum(browser)<= getSumNum(browser):
            sumDf = process_pages(browser, pname, cname, countyname, getActiveNum(browser), getSumNum(browser))
        # 获取最后一页
        if getActiveNum(browser) == (getSumNum(browser) - 1):
            while True:
                try:
                    browser.find_element_by_xpath('//*[@id="appMain"]/div/div[5]/div/div/ul/li[{}]'.format(k)).click()
                    break
                except:
                    print("点击下一页失败")
                    time.sleep(random.uniform(3, 5))
        print("这是第" + str(getActiveNum(browser)) + "页")
        a = getnum(browser) % 10
        # 获取最后一页
        if a == 0 and getnum(browser)>0:
            sumDf = process_page(browser, pname, cname, countyname)
        else:
            sumDf = process_last_page(browser, pname, cname, countyname, a)
    return sumDf
    
# 获取大于8页的数据
def chooseNum2(browser, pname, cname, countyname):
    global sumDf
    if getSumNum(browser) > 8:
        # 获取1-6页数据
        if getActiveNum(browser) <=7:
            sumDf = process_pages(browser, pname, cname, countyname, getActiveNum(browser), 7)

        # 获取7-(getSumNum(browser)-2)页数据
        sumDf = process_pages1(browser, pname, cname, countyname, getActiveNum(browser), getSumNum(browser) - 1)

        # 点击倒数第二页
        if getActiveNum(browser) == (getSumNum(browser) - 2):
            while True:
                try:
                    browser.find_element_by_xpath('//*[@id="appMain"]/div/div[5]/div/div/ul/li[7]').click()
                    break
                except:
                    print("点击下一页失败")
                    time.sleep(random.uniform(2, 4))
            print("这是第" + str(getActiveNum(browser)) + "页")
            sumDf = process_page(browser, pname, cname, countyname)

        # 点击最后一页
        if getActiveNum(browser) == (getSumNum(browser) - 1):
            while True:
                try:
                    browser.find_element_by_xpath('//*[@id="appMain"]/div/div[5]/div/div/ul/li[8]').click()
                    break
                except:
                    print("点击下一页失败")
                    time.sleep(random.uniform(3, 5))
        print("这是第" + str(getActiveNum(browser)) + "页")
        a = getnum(browser) % 10
        # 获取最后一页
        if a == 0 and getnum(browser)>0:
            sumDf = process_page(browser, pname, cname, countyname)
        else:
            sumDf = process_last_page(browser, pname, cname, countyname, a)

    return sumDf


# In[8]:


# 城市点击
def click_element_safe(element):
    while True:
        try:
            element.click()
            break
        except (ElementClickInterceptedException, ElementNotInteractableException):
            print("City Element click was intercepted or not interactable.")
            time.sleep(random.uniform(3,5))
            browser.execute_script("arguments[0].scrollIntoView();", element)
        except NoSuchElementException:
            print("No such element")
            time.sleep(random.uniform(3,5))
            browser.execute_script("arguments[0].scrollIntoView();", element)  
        except:
            print("Clicking element failed")
            time.sleep(3)
# 区县点击
def click_element_county(element):
    while (1):
        try:
            # 选择一个县级元素，并使用其 text 属性构建 XPath
            browser.execute_script("arguments[0].click();",element)
            print("成功点击一次区县")
            time.sleep(random.uniform(3,5))
            break
        except IndexError:
            print("No county elements found or index out of range.")
            time.sleep(random.uniform(3,5))
        except (ElementClickInterceptedException,ElementNotInteractableException ):
            print("County Element click was intercepted or not interactable.")
            time.sleep(random.uniform(3,5))
        except  StaleElementReferenceException:
            print("County stale element reference: stale element not found")
            time.sleep(random.uniform(3,5))
            cancel_button = browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[3]/form[1]/div[1]/div/div/div/span/span/i')
            click_element_safe(cancel_button)
            time.sleep(random.uniform(3, 5))
            chooseProvince(browser, "辽宁省")  # Change to your province
            click_element_safe(i)
            print("成功点击一次城市")
            time.sleep(random.uniform(3, 5))
            countyname = (browser.find_elements_by_xpath('//*[@class="el-cascader-node__label"][1]'))[35 + a:]
            countylabel = (browser.find_elements_by_class_name('el-radio__input'))[35 + a:]
        except NoSuchElementException:
            print("No such County element")
            time.sleep(random.uniform(3,5))


# In[ ]:


''' # 隐藏浏览器
    #浏览器启动选项
    option=webdriver.ChromeOptions()
    #指定为无界面模式
    option.add_argument('--headless')
    # option.headless=True  或者将上面的语句换成这条亦可
    #创建Chrome驱动程序的实例
    browser=webdriver.Chrome(options=option)'''

# 创建 ChromeOptions 并添加无头模式和其他选项
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # 添加无头模式选项
chrome_options.add_argument("--disable-gpu")  # 禁用 GPU
chrome_options.add_argument("--disable-software-rasterizer")  # 禁用软件光栅化器

# 创建 Chrome 浏览器实例并传入选项
browser = webdriver.Chrome(options=chrome_options)


if __name__ == "__main__":
    startTime = time.time()
    browser.get('https://landchina.com/#/givingNotice')
    # Click the search button
    search_button = browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[3]/form[2]/div[3]/div/button[2]')
    #search_button = browser.find_element(By.XPATH,'//*[@id="appMain"]/div/div[3]/div[3]/form[2]/div[3]/div/button[2]')
    search_button.click()
    time.sleep(random.uniform(2, 4))
    
    sumDf=pd.DataFrame()
    total_num = 0
    error = 0
    
    # Loop through all cities and counties
    cityname, a = getCity(browser, "辽宁省")  # Change to your province，更改六次
    for i in cityname[1:2]:   
        click_element_safe(i)
        print("成功点击一次城市")
        time.sleep(random.uniform(3, 5))
        cit = i.text
        countylabel = (browser.find_elements(By.CLASS_NAME,'el-radio__input'))[35 + a:]
        countyname = (browser.find_elements(By.XPATH,'//*[@class="el-cascader-node__label"][1]'))[35 + a:]
        num2 = list(range(len(countyname)))
        
        for t in num2[1:2]: #-6开始
            count = countyname[t].text
            click_element_county(countylabel[t])
            
            if getnum(browser) > 0:
                if getSumNum(browser) < 9:
                    if getActiveNum(browser) != 1:
                        click_element_safe(browser.find_element_by_xpath('//*[@id="appMain"]/div/div[5]/div/div/ul/li[1]'))
                    chooseNum1(browser, "辽宁省", cit, count)  # Change to your province
                #获取页码数大于8 的
                if getSumNum(browser) > 8:
                    #if getActiveNum(browser) != 1:
                        #click_element_safe(browser.find_element_by_xpath('//*[@id="appMain"]/div/div[5]/div/div/ul/li[1]'))
                    chooseNum2(browser, "辽宁省", cit, count)  # Change to your province
                time.sleep(3)
                if getActiveNum(browser) != 1:
                    click_element_safe(browser.find_element_by_xpath('//*[@id="appMain"]/div/div[5]/div/div/ul/li[1]'))
            # Reset province, city, county selection
            if len(sumDf) > 0:
                sumDf.to_csv(r'F:\Users\zhang\Desktop\土地爬取\辽宁省.csv', index=False, mode='a', header=False,encoding="utf_8_sig")
                print(count+"爬取完毕")
                sumDf = pd.DataFrame()
            while 1:
                try:
                    cancel_button = browser.find_element_by_xpath('//*[@id="appMain"]/div/div[3]/div[3]/form[1]/div[1]/div/div/div/span/span/i')
                    #click_element_safe(cancel_button)
                    cancel_button.click()
                    time.sleep(random.uniform(3, 5))
                    chooseProvince(browser, "辽宁省")  # Change to your province
                    click_element_safe(i)
                    print("成功点击一次城市")
                    time.sleep(random.uniform(3, 5))
                    countyname = (browser.find_elements_by_xpath('//*[@class="el-cascader-node__label"][1]'))[35 + a:]
                    countylabel = (browser.find_elements_by_class_name('el-radio__input'))[35 + a:]
                    break
                except:
                    print("Clicking province or city failed")
                    time.sleep(3)
    
 
    # 检查是否还有剩余数据未存入文件
    if len(sumDf) > 0:
        sumDf.to_csv(r'F:\Users\zhang\Desktop\土地爬取\辽宁省.csv', index=False, mode='a', header=False,encoding="utf_8_sig")
    #爬虫统计
    print("Total records:", total_num, "Errors:", error)
    endtime = time.time()
    dtime = endtime - startTime
    print("Program runtime: %.8s s" % dtime)
    browser.quit()

#16页开始
# In[ ]:









