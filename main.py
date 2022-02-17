import datetime
import json

import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver as web
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

bot_username = 'saad_swaad'
bot_password = 'saidracgrich'

profiles = ['wecodeinpython']
amount = 30

# 'usernames' or 'links'
result = 'usernames'

us = ''


class InstgrameProfile_Scrapper():
    def __init__(self):
        options = Options()
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-notifications")
        # options.add_argument('--headless')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.browser = web.Chrome("chromedriver", options=options)
        self.browser.set_window_size(400, 900)
        self.browser.minimize_window();

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self, username, password):
        browser = self.browser
        try:
            browser.get('https://www.instagram.com')
            time.sleep(random.randrange(3, 5))
            # Enter username:
            username_input = browser.find_element_by_name('username')
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(random.randrange(2, 4))
            # Enter password:
            password_input = browser.find_element_by_name('password')
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(random.randrange(1, 2))
            password_input.send_keys(Keys.ENTER)
            time.sleep(random.randrange(3, 5))
            print(f'[{username}] Successfully logged on!')
            return 1;
        except Exception as ex:
            print(f'[{username}] Authorization fail')
            self.close_browser()
            return -1;

    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def get_followers(self, users, amount):
        account_list = [];
        time.sleep(10)
        browser = self.browser
        followers_list = []
        for user in users:
            browser.get('https://instagram.com/' + user)
            time.sleep(random.randrange(3, 5))
            followers_button = browser.find_elements(By.CSS_SELECTOR, 'li.LH36I')
            followers_button = followers_button[1]
            count = followers_button.find_element(By.TAG_NAME, 'span').text
            if ',' in count:
                count = int(''.join(count.split(',')))
            elif 'k' in count:
                count = int(count.replace('k', '000'))
            else:
                count = int(count)
            print(count);

            if amount > count:
                print(f'You set amount = {amount} but there are {count} followers, then amount = {count}')
                amount = count
            followers_button.click()
            loops_count = int(amount / 12)
            print(f'Scraping. Total: {amount} usernames. Wait {loops_count} iterations')
            time.sleep(random.randrange(8, 10))
            followers_ul = browser.find_element(By.XPATH, "//div[@class='isgrP']")
            time.sleep(random.randrange(5, 7))
            try:
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(8, 10))
                    all_div = followers_ul.find_elements_by_tag_name("li")
                    for us in all_div:
                        us = us.find_element_by_tag_name("a").get_attribute("href")
                        if result == 'usernames':
                            us1 = us.replace("https://www.instagram.com/", "")
                            us = us1.replace("/", "")
                        followers_list.append(us)
                    time.sleep(1)
                    f3 = open('userlist.txt', 'w')
                    for list in followers_list:
                        f3.write(list + '\n')
                    print(f'Got: {len(followers_list)} usernames of {amount}. Saved to file.')
                time.sleep(random.randrange(3, 5))
                print("followers-list");
                print(followers_list)
                for user in followers_list:
                    acount_info = self.profile_scraaper(user)
                    print(acount_info)
                    account_list.append(acount_info)
                df = pd.DataFrame(account_list)
                tmp = datetime.datetime.now()
                tmp = str(tmp);
                tmp = tmp.replace(' ', '_')
                tmp = tmp.replace('.', '_')
                tmp = tmp.replace(':', '_')
                df.to_csv('Data/followers' + user + str(tmp) + '.csv')
                print(account_list)
                return 1;
            except Exception as ex:
                print(ex)
                self.close_browser()
                return -1;

    def profile_scraaper(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/?__a=1')
        soup = BeautifulSoup(self.browser.page_source, "html.parser").get_text()
        jsondata = json.loads(soup)

        id = jsondata["graphql"]['user']['id']
        fullname = jsondata["graphql"]['user']['full_name'];
        username = username;
        email = jsondata["graphql"]['user']['business_email'];
        phone_number = jsondata["graphql"]['user']["business_phone_number"];
        profile_photo = jsondata["graphql"]['user']['profile_pic_url_hd']
        followers = jsondata["graphql"]['user']['edge_followed_by']['count'];
        follow_Count = jsondata["graphql"]['user']['edge_follow']['count']
        return {'id': id, 'fullname': fullname, 'followed_by': followers, 'follow': follow_Count, 'username': username,
                'phone_number': phone_number, 'email': email, 'profile_photo': profile_photo}

    def listToString(s):

        # initialize an empty string
        str1 = " "

        # return string
        return (str1.join(s))

    def load_post(self, link, data):
        try:
            df = pd.read_csv(data);
            usernames = df['username'].tolist();
            print(usernames)
            tmp = len(usernames) / 5;
            tmp = tmp + 1;
            splice_usernames = np.array_split(usernames, tmp)
            self.browser.get(link);
            for users in splice_usernames:
                time.sleep(10)
                comment_button = self.browser.find_element(By.XPATH,
                                                           '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[3]/div/div/section[1]/span[2]/button')
                comment_button.click();
                time.sleep(3)
                form = self.browser.find_element(By.CSS_SELECTOR, 'form.X7cDz');
                textarea = form.find_element(By.CSS_SELECTOR, 'textarea.Ypffh');
                textarea.click()
                textarea2 = form.find_element(By.CSS_SELECTOR, 'textarea.Ypffh');
                text_list = []
                for user in users:
                    text_list.append('@' + user)
                listToStr = ' '.join([str(elem) for elem in text_list])
                textarea2.send_keys(listToStr)
                time.sleep(5)
                form.submit();
                time.sleep(10)
            print('done')
            return 1
        except Exception as e:
            print(e)
            return -1;

    def post_mesg_to_group(self, data):
        time.sleep(10)
        self.browser.get('https://www.instagram.com/direct/inbox/')
        print(self.browser.current_url)
        try:
            notif = self.browser.find_element(By.CSS_SELECTOR, 'button.aOOlW.HoLwm')
            notif.click();
        except:
            print('pas de notification')

        time.sleep(5)
        time.sleep(5)
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.MWDvN")));
        df = pd.read_csv(data);
        usernames = df['username'].tolist();
        lent = len(usernames);
        am = lent / 28;
        splice_usernames = np.array_split(usernames, am)
        print(splice_usernames);
        print('-----------------------------------')
        for users in splice_usernames:
            message_button = self.browser.find_element(By.XPATH,
                                                       '//*[@id="react-root"]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button')
            message_button.click();

            print(users)
            print('----------------')
            print(len(users));

            for user in users:
                input_users = self.browser.find_element(By.CSS_SELECTOR, 'input.j_2Hd.uMkC7.M5V28');
                input_users.clear()

                print(user)
                try:
                    input_users.send_keys(user);
                    time.sleep(5)
                    self.browser.execute_script("arguments[0].click();", WebDriverWait(self.browser, 60).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "/html/body/div[5]/div/div/div[2]/div[2]/div[2]/div/div[3]/button"))))
                    for i in user:
                        input_users.send_keys(Keys.BACKSPACE)

                except Exception as e:
                    input_users.clear();
                    continue;

        time.sleep(5)
        next_button = self.browser.find_element(By.CSS_SELECTOR, 'button.sqdOP.yWX7d.y3zKF.cB_4K');
        next_button.click()
        time.sleep(20);
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.qF0y9.Igw0E.IwRSH.eGOV_.vwCYk.ItkAi")));
        form = self.browser.find_element(By.CSS_SELECTOR, 'div.qF0y9.Igw0E.IwRSH.eGOV_.vwCYk.ItkAi')
        text_input = form.find_element(By.TAG_NAME, 'textarea');
        text_input.click();
        text_input = form.find_element(By.TAG_NAME, 'textarea');
        data = ''
        with open('message.txt', 'r') as file:
            data = file.read().rstrip()
            text_input.send_keys(data)
        time.sleep(5)
        send_btn = form.find_element(By.XPATH,
                                     '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button')
        send_btn.click()

        print('Messaging Don')
        return 1;


if __name__ == '__main__':
    bot = InstgrameProfile_Scrapper();
    bot.login('grich.test', 'check8tobesafe');
    # followers = bot.get_followers(profiles, amount);
    bot.post_mesg_to_group(
        r'C:\Users\grich\PycharmProjects\instagram\Data\followerscem__emre2022-02-17_21_57_10_400189.csv')
