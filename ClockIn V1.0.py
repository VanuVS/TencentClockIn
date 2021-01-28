import time
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
#options.add_argument("headless") # 无头模式
#options.add_argument("sandbox")
driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe',options=options)
driver.get("https://docs.qq.com/desktop")  # 地址栏里输入健康打卡的网址
driver.implicitly_wait(2)  # 设置隐式等待时间

year = time.strftime("%Y", time.localtime())
month = time.strftime("%m", time.localtime())
day = time.strftime("%d", time.localtime())
if int(day) < 10:
    day = int(str(day))
date = year + "/" + month + "/" + str(day)
print("今天是" + date)
current_time = time.strftime("%H%M%S", time.localtime())  # 当前时间作为判断早上中午的依据

#  获取当天日期

time.sleep(1)
driver.switch_to.frame(driver.find_element_by_id('login_frame'))
try:
    driver.find_element_by_xpath('//*[@id="img_out"]').click()
    print("快速登录成功")
except:  # 非常用ip登录不可用 需要滑块验证
    driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
    driver.find_element_by_xpath('//*[@id="u"]').send_keys("") # 输入账号
    driver.find_element_by_xpath('//*[@id="p"]').send_keys("") # 输入密码
    driver.find_element_by_xpath('//*[@id="login_button"]').click()
    print("账密登录成功")
time.sleep(5)

# 点击进入文档页面

driver.find_element_by_xpath(
    '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[1]/div/div/div[2]/span[1]').click()  # 先点击进入星标界面
driver.find_element_by_xpath(
    '//*[@id="root"]/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div['
    '1]/div/div/div/div[1]/span[1]').click()  # 再点击进入文档界面 测试选用独立文档
print("成功进入文档")
time.sleep(5)

# 切换句柄至文档页面

handle = driver.current_window_handle  # 获取星标页面的句柄
handles = driver.window_handles  # 获取浏览器中所有页面的句柄
for i in handles:
    if handle != i:
        driver.switch_to.window(i)  # 切换页面句柄
time.sleep(5)


#  进行文档操作
#  以下为搜索日期阶段
def LocateDate():
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("f").perform()  # 同时按下ctrl+f,打开搜索栏
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="search-panel-input"]').send_keys(str(date))
    driver.find_element_by_xpath('//*[@id="search-panel-input"]').send_keys(str(date)) # 必须两次
    time.sleep(1)
    driver.execute_script("document.querySelector('body > div.dui-modal-mask.dui-modal-mask-visible > div > "
                          "div.dui-modal-close').click()")
    time.sleep(3)


#  以下为填写阶段


def LocatePerson(displacement):
    global textbox, flag, temperature
    flag = 0
    temperature = round(random.uniform(36.2, 36.8), 1) # 体温区间
    textbox = driver.find_element_by_id('alloy-simple-text-editor')
    for j in range(0, displacement):
        textbox.send_keys(Keys.ENTER)  # 对文字输入框输入Enter键进行下移操作
    if 130000 >= int(current_time) >= 120000:
        textbox.send_keys(Keys.TAB)  # 对文字输入框输入Tab键进行右移操作 右移1格 早上不移动中午移动一格
    textbox.click()
    if len(textbox.get_attribute("innerHTML")) > 33:
        flag = 1
        return flag
    for j in range(0, 6):
        textbox.click()
        textbox.send_keys(Keys.ARROW_RIGHT)
        textbox.send_keys(Keys.BACK_SPACE)  # 对文字输入框输入Delete键进行删除操作
    textbox.send_keys(str(temperature))  # 输入体温


def main():
    name = ["NONE"] # 输入姓名，保留"NONE"
    displacement = [0] # 输入位移量，保留"0"
    for j in range(0, len(name)):
        if j == len(name)-1:
            textbox.send_keys(Keys.ENTER)
            return
        LocateDate()
        LocatePerson(displacement[j])
        if flag == 0:
            print(name[j] + "输入成功" + " 体温为：" + str(temperature))
        else:
            print("文本框中已有内容")
            print(textbox.get_attribute("innerHTML"))


main()
driver.quit()
