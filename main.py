import time, datetime, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import URL_LIST, YOUTUBE_DIR, MAX_TOTAL_ITEMS
# encoding=utf8
import sys, re
reload(sys)
sys.setdefaultencoding('utf8')

max_total_items = MAX_TOTAL_ITEMS
default_loading_time = 3

browser = webdriver.Firefox()


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def load_page(website):
    browser.get(website)
    elem = None
    while elem is None:
        time.sleep(default_loading_time)
        elem = browser.find_element_by_tag_name("body")
        return elem


create_folder(YOUTUBE_DIR)
start_time = time.time()
today = datetime.date.today().strftime("%Y-%m-%d")
for url in open(URL_LIST):
    url = url.rstrip('\n')
    url_name = url.split('=')[1]
    log = open(YOUTUBE_DIR + url_name + '_' + today + '.csv', 'w')
    body = load_page(url)
    browser.execute_script('window.scrollTo(1, 500);') # without this code, comments can not be loaded
    time.sleep(default_loading_time)
    current_total_items = 0
    has_next_page = True
    comment_list  = []
    published_time_list = []
    while has_next_page and current_total_items < max_total_items:
        body.send_keys(Keys.COMMAND + Keys.ARROW_DOWN)
        time.sleep(default_loading_time)
        content=browser.find_element_by_xpath('//*[@id="contents"]')
        comments=content.find_elements_by_xpath('//*[@id="content-text"]')
        published_times=content.find_elements_by_xpath('//*[@id="published-time-text"]')

        for i in range(0, len(comments)):
            if comments[i].text not in comment_list:
                comment_list.append(comments[i].text)
                published_time_list.append(published_times[i].text)

        # check if ending page
        total_comments = len(comment_list)
        if total_comments == current_total_items:
            has_next_page = False
        current_total_items = total_comments
    # print 'number of comments: ', len(comment_list)

    num = 1
    for i in range(0, len(comment_list)):
        log.write(str(num) + ',')
        log.write(published_time_list[i] + ',')
        log.write(re.sub(r"\n+", "\n", comment_list[i]).replace('\n', ' '))
        log.write('\n')
        num += 1
    log.close()

    print '# input url: ' + url
    print 'number of comments: ', len(comment_list)
    print 'number of published times: ', len(published_time_list)

print 'finish in: ', time.time() - start_time
