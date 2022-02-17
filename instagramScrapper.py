import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class InstagramScrapper:
    def __init__(self):
        option=webdriver.ChromeOptions()
        self.my_username = "grich.test"
        self.my_password = "check8tobesafe"
        self.driver = webdriver.Chrome(options=option)
        self.driver.get("https://www.instagram.com/")
        self.driver.maximize_window()
    def login(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.rgFsT")));
        time.sleep(10)
        form=self.driver.find_element(By.ID,'loginForm');
        inputs=form.find_elements(By.TAG_NAME,'input')
        username_box=inputs[0];
        password_box=inputs[1];
        username_box.send_keys(self.my_username);
        password_box.send_keys(self.my_password);
        time.sleep(5);
        login_button=self.driver.find_element(By.CSS_SELECTOR,'button.sqdOP.L3NKy.y3zKF');
        time.sleep(5);
        login_button.click()
    def search_for_username(self,username):
        time.sleep(5)
        self.driver.get('https://www.instagram.com/'+username);
        folowers=self.driver.find_elements(By.CSS_SELECTOR,'li.Y8-fY');
        folowers=folowers[1]
        folowers.click()
        time.sleep(3)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.isgrP")));
        time.sleep(5)
        fBody = self.driver.find_element_by_xpath("//div[@class='isgrP']");
        number_of_folowers=self.driver.find_elements(By.CSS_SELECTOR,'span.g47SY')[1].text;
        print(number_of_folowers)
        scroll = 0
        while scroll < 10000:  # scroll 5 times
            print(scroll)
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            time.sleep(3)
            fList = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")
            print(len(fList))
            if int(len(fList))>=int(number_of_folowers):
                break;
            else:
                scroll += 1
        list_followers=[]
        for per in fList:
            print(per.find_element(By.TAG_NAME,'a').text)
            list_followers.append(per.find_element(By.TAG_NAME,'a').text)

if __name__=='__main__':
    ins =InstagramScrapper();
    ins.login()
    ins.search_for_username('grich.said')