import time
import re
from datetime import datetime, timedelta
import random
import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import requests
from reposts_methods import Parsing, Queries
from selenium.common import exceptions
import pickle
import json
from gologin import GoLogin

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display


p = Parsing()
q = Queries()

display = Display(visible=0, size=(1920, 1080))
display.start()

token = q.get_GoToken2()[0][0]

profilePort = q.get_PofileIdPort()
for pr in profilePort:
    profile_id=str(pr[0])
    port =str(pr[1])
    name =str(pr[2])

gl = GoLogin({
    'token':token,
    'profile_id': profile_id,
    'port': port
    })


chrome_driver_path = 'chromedriver'

debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

driver.get("http://www.facebook.com")
driver.save_screenshot('login.png')

bx=0

while bx == 0:

    # get links of reposts

    time.sleep(random.randint(14,18))
    free_account = q.getTasks()

    for account in free_account:
        repost_id = account[0]
        link = account[1]
        user_id = account[2]
        project_id = account[3]


        try:
            print("link", link)
            if "groups/" in str(link):
                author = link.split("groups/")[1]
                author = author.split("/")[0]

            else:
                author = link.split("facebook.com/")[1]
                author = author.split("/")[0]

            time.sleep(5)

            driver.get(link)
            
            time.sleep(5)

            breaking = 0

            try:
                html0 = driver.page_source
                bs0 = BeautifulSoup(html0, 'html.parser')

                driver.save_screenshot('post.png')
                print("repost_id", repost_id)
                print("link", link)

                added_repost = []

                if ("Требуется подтверждение" in str(bs0)) or (
                        "Проверка безопасности" in str(bs0)):
                    print("Аккаунт забанен")
                    bx = 1
                    q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                elif "Для входа потребу" in str(bs0):
                    print("Аккаунт забанен")
                    bx = 1
                    q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                elif "Пожалуйста, войдите, чтобы продолжить" in str(bs0):
                    print("Аккаунт забанен")
                    bx = 1
                    q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                elif "Обновить контактную информацию" in str(bs0):
                    print("Аккаунт забанен")
                    bx = 1
                    q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                elif "a few more steps" in str(bs0):
                    print("Аккаунт забанен")
                    bx = 1
                    q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                scroll_count = 0

                q.updating(
                    """UPDATE add_post SET repost='2' WHERE id ={0}""".format(
                        repost_id))

                target2 = driver.find_element_by_xpath("//*[contains(text(), 'Поделились:')]")
                text_ = target2.get_attribute("innerHTML")
                scroll_count = str(text_).split("Поделились: ")[1].split("</")[0]

                scroll_count = str(scroll_count).replace("&nbsp;", '')
                scroll_count = str(scroll_count).replace(",", '')
                scroll_count = str(scroll_count).replace("тыс.", '00')
                scroll_count = int(scroll_count)

                target2.click()
                time.sleep(5)
                driver.save_screenshot('reposts.png')
                print('scroll_count',scroll_count)
                

                if scroll_count != 0:

                    scrolling = int((scroll_count / 2) + 1) + 1

                    print("scrolling", scrolling)
                    
                    for p in range(0, scrolling):
                        s_links = len(added_repost)

                        all_reposts = []

                        print("scroll", p)
                        
                        try: 
                            menu = driver.find_element_by_xpath("//*[contains(text(), 'Из-за настроек конфиденциальности здесь могут отображаться не все публикации')]")
                            ActionChains(driver).move_to_element(menu).perform()         
                        except:
                            pass

                        time.sleep(10)
                        driver.save_screenshot('link%s.png' % str(p))

                        html = driver.page_source
                        bs = BeautifulSoup(html, 'html.parser')

                        if ("Требуется подтверждение" in str(bs)) or (
                                "Проверка безопасности" in str(bs)):
                            print("Аккаунт забанен")
                            bx = 1
                            q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                        elif "Для входа потребу" in str(bs):
                            print("Аккаунт забанен")
                            bx = 1
                            q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                        elif "Пожалуйста, войдите, чтобы продолжить" in str(bs):
                            print("Аккаунт забанен")
                            bx = 1
                            q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                        elif "Обновить контактную информацию" in str(bs):
                            print("Аккаунт забанен")
                            bx = 1
                            q.updating("""UPDATE add_post SET repost='1' WHERE id ={0}""".format(repost_id))

                        reposts = bs.find_all("div", class_='jroqu855 nthtkgg5')

                        for repost_tag in reposts:

                            repost_ = repost_tag.find_all('a', class_='qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv rse6dlih s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq jxuftiz4 cxfqmxzd tes86rjd')

                            for repost in repost_:

                                if repost is not None:

                                    rep=str(repost.get('href'))

                                    rep = rep.split("?__cft__")[0]
                                    rep = rep.split("&__cft")[0]
                                    rep = rep.split("&__cft")[0]
                                    rep = rep.split("__xts__")[0]
                                    rep = rep.split("__tn__")[0]

                                    print("repost_link", rep)

                                    try:
                                        if len(rep) > 5:
                                            rep = rep.replace("?", "")
                                            rep = rep.replace("permalink.phpstory_fbid=",
                                                              "permalink.php?story_fbid=")

                                            if "www.facebook.com" not in str(rep):
                                                rep = "https://www.facebook.com" + str(rep)
                                
                                            if rep not in added_repost:
                                                added_repost.append(rep)
                                                if rep not in all_reposts:
                                                    if str(author) not in str(rep):
                                                        all_reposts.append(rep)
                                    except Exception as e:
                                        print("EX1", e)

                                        try:
                                            if len(rep) > 5:
                                                rep = rep.replace("?", "")
                                                rep = rep.replace("permalink.phpstory_fbid=",
                                                                  "permalink.php?story_fbid=")

                                                if "www.facebook.com" not in str(rep):
                                                    rep = "https://www.facebook.com" + str(rep)
                                    
                                                if rep not in added_repost:
                                                    added_repost.append(rep)
                                                    if rep not in all_reposts:
                                                        if str(author) not in str(rep):
                                                            all_reposts.append(rep)
                                        except Exception as e:
                                            print("EX2", e)
                        
                        
                        print("all_reposts", all_reposts)
                        for r in all_reposts:

                            try:
                                if r[-1:] == "&":
                                    r = r[:-1]
                                if r[-1:] == "/":
                                    r = r[:-1]
                        
                                r = r.replace("https://www.facebook.comhttps",
                                              "https")
                                r = r.replace("photo.phpfbid", "photo.php?fbid")
                                print(r)
                        
                                owner_id = 0
                                if "/groups/" in r and '/permalink/' in r:
                                    print(1)
                                    item_id = r.split("/permalink/")[1].replace(
                                        "/",
                                        "")
                                    owner_id = \
                                        r.split("/permalink/")[0].split(
                                            "/groups/")[1]
                                    try:
                                        owner_id = int(owner_id)
                                    except:
                                        owner_id = 0
                                if "https://www.facebook.com/permalink.php" in r:
                                    print(2)
                                    r = r.replace('&type=', '')
                                    owner_id = r.split("=")[-1]
                                    item_id = r.split("=")[1].split("&")[0]
                                if "/posts/" in r:
                                    print(3)
                                    item_id = r.split("/posts/")[1]
                                    owner_id = 0
                                if "/videos/" in r:
                                    print(4)
                                    item_id = r.split("/videos/")[1]
                                    owner_id = 0
                                if "photo.php?fbid=" in r:
                                    item_id = \
                                    r.split("photo.php?fbid=")[1].split("&")[
                                        0]
                        
                                print("r_link", r)
                                print("owner_id: ", owner_id)
                                print("item_id: ", item_id)
                                print("repost_id", repost_id)
                                print("link", link)
                                print("user_id", user_id)
                                print("project_id", project_id)
                                print("             ")
                        
                                if str(r)[-1:] == '/':
                                    r = str(r)[:-1]
                        
                                add_date = datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S")
                                q.updating(
                                    """INSERT add_post SET type=2, url='{0}', status='ready', owner_id='{1}', item_id='{2}', user_id='{3}', project_id='{4}', add_date='{5}', parent_id='{6}'""".format(
                                        r, owner_id, item_id, user_id, project_id,
                                        add_date, repost_id))
                        
                            except Exception as e:
                                print(e)

                else:
                    print("No Reposts For id", repost_id)


                if added_repost!=[]:
                    q.updating("""UPDATE add_post SET repost='3' WHERE id ={0}""".format(repost_id))

            except Exception as e:
                print("like_click_error1", e)

        except Exception as e:
            print("one_task", e)
            q.updating("""UPDATE add_post SET repost='2' WHERE id ={0}""".format(repost_id))