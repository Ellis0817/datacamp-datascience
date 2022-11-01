from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import pandas as pd
from collections import defaultdict

url = 'https://www.nba.com/'
driver = webdriver.Chrome()
driver.get(url)

# select stats
states_btn = driver.find_element(By.CSS_SELECTOR, '#nav-ul > li:nth-child(5) > a > span')
states_btn.click()

# select player index 將滑鼠移動到標籤後，向下選擇player_index
players = driver.find_element(By.CSS_SELECTOR, '#__next > div.Layout_base__6IeUC.Layout_withSubNav__ByKRF.Layout_justNav__2H4H0 > div.Layout_fixedContent__kWFtM > div.SubNav_snMain__Y5P_b > nav > ul > li:nth-child(3) > button > span > svg > polyline')
player_index = driver.find_element(By.CSS_SELECTOR, '#__next > div.Layout_base__6IeUC.Layout_withSubNav__ByKRF.Layout_justNav__2H4H0 > div.Layout_fixedContent__kWFtM > div.SubNav_snMain__Y5P_b > nav > ul > li:nth-child(3) > div > ul > li:nth-child(2) > a') 
ActionChains(driver).move_to_element(players).click(player_index).perform()

# select all player 用Select選擇下拉選單
dropdown = driver.find_element(By.CSS_SELECTOR, '#__next > div.Layout_base__6IeUC.Layout_withSubNav__ByKRF.Layout_justNav__2H4H0 > div.Layout_mainContent__jXliI > main > div.MaxWidthContainer_mwc__ID5AG > section > div > div.PlayerList_content__kwT7z > div.PlayerList_filters__n_6IL > div.PlayerList_pagination__c5ijE > div > div.Pagination_pageDropdown__KgjBU > div > label > div > select')
all_info = Select(dropdown).select_by_index(0)

title= ['Player', 'Team', 'Numbers', 'Position', 'Height', 'Weight', 'Last attended', 'Country']
info = []
# player, team, numbers, position, height, weight, last attended, country
player_info = driver.find_elements(By.TAG_NAME, 'td')
for a in player_info:
    a = a.text.replace('\n',' ')
    info.append(a)

num = len(info)
title_total = title * int((num / 8))
player_dict = dict(zip(title_total, info))

# zip title_total and info to a dictionary by using 
# from collections import defaultdict
my_dict = defaultdict(list)
for k, v in zip(title_total, info):
    my_dict[k].append(v)

df = pd.DataFrame(my_dict, index=range(1,501))
print(df)

# save in excel
df.to_excel('player_stats.xlsx')
driver.close()