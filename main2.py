import os
import sys
import schedule
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime

def task(arg):
    ip = os.getenv("ROUTER_IP_ADDRESS")
    username = os.getenv("ROUTER_USERNAME")
    password = os.getenv("ROUTER_PASSWORD")

    # ユーザー名とパスワードをURLに埋め込む
    auth_url = f"http://{username}:{password}@{ip}"

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(auth_url + "/cgi-bin/luci/content/net_filtering/url_filter?nocache")

    # 認証後の動作を追加する
    checkbox = driver.find_element(By.ID, "enable_url_filter")
    
    # チェックボックスが既にチェックされているかどうかを確認
    #if not checkbox.is_selected():
        # チェックボックスが選択されていない場合、クリックしてチェックをつける
    #    checkbox.click()

        # 設定を反映
    #    driver.execute_script("goToApply()")

    dt_now = datetime.datetime.now()
    print(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'), end=" ")

    if arg == 0 and checkbox.is_selected():
        checkbox.click()
        driver.execute_script("goToApply()") # 設定を反映
        print("フィルタリングOFF")
    elif arg == 1 and not checkbox.is_selected():
        checkbox.click()
        driver.execute_script("goToApply()") # 設定を反映
        print("フィルタリングON")
    else:
        print("ルーター設定の変更に失敗しました。")

# スケジュール登録
schedule.every().days.at("09:00").do(task, 1)
schedule.every().days.at("18:00").do(task, 0)
#schedule.every().days.at("00:24").do(task, 1)

print("自動フィルタリング制御プログラム起動")

while True:
    schedule.run_pending()
    sleep(1)