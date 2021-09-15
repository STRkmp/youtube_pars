import time,json
from selenium import webdriver
from bs4 import BeautifulSoup as BS

with open('channels_info.json', encoding="utf-8") as json_file:
    channels = json.load(json_file)

with open('last_videos.json', encoding="utf-8") as json_file_videos:
    last_video = json.load(json_file_videos)

data = {}
i=0
for channel in channels:
    i=i+1
    URL = channel["channel_url"] #Ваш урл
    data[channel["channel_name"]] = []
    driver = webdriver.Chrome()
    driver.get(URL)
   # time.sleep(5)  #Можно ждать до загрузки страницы, но проще подождать 10 секунд, их хвqатит с запасом
    html = driver.page_source

    soup = BS(html, "html.parser")
    videos = soup.find_all("ytd-grid-video-renderer",{"class":"style-scope ytd-grid-renderer"})
    flag = True
    for video in videos:
        a = video.find("a",{"id":"video-title"})
        if (a.get_text() == last_video[channel["channel_name"]][0]["title"] ):
            if flag:
                data[channel["channel_name"]].append({"title": a.get_text(), "url": "" })
            break
        flag = False
        data[channel["channel_name"]].append({"title": a.get_text(), "url": "https://www.youtube.com" + a.get("href"), "id": i })



with open("last_videos.json", "w", encoding='utf-8') as writeJSON:
    json.dump(data, writeJSON, ensure_ascii=False)