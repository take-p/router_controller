import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service

ip = os.getenv("ROUTER_IP_ADDRESS")
username = os.getenv("ROUTER_USERNAME")
password = os.getenv("ROUTER_PASSWORD")

# ユーザー名とパスワードをURLに埋め込む
auth_url = f"http://{username}:{password}@{ip}"

driver="geckodriver"
service = Service(executable_path=driver)
options = Options()
options.headless = True
driver = webdriver.Firefox(service=service, options=options)
driver.get(auth_url + "/cgi-bin/luci/content/net_filtering/url_filter?nocache")

# 認証後の動作を追加する
checkbox = driver.find_element(By.ID, "enable_url_filter")
# チェックボックスが既にチェックされているかどうかを確認
if not checkbox.is_selected():
    # チェックボックスが選択されていない場合、クリックしてチェックをつける
    checkbox.click()

    # 設定を反映
    driver.execute_script("goToApply()")

if len(sys.argv) > 1:
    # 引数が 'on' で、チェックボックスが選択されていない場合、クリックしてチェックをつける
    if sys.argv[1] == 'on' and not checkbox.is_selected():
        checkbox.click()
        driver.execute_script("goToApply()") # 設定を反映
        print("フィルタリングをonにしました")
    # 引数が 'off' で、チェックボックスが選択されている場合、クリックしてチェックを外す
    elif sys.argv[1] == 'off' and checkbox.is_selected():
        checkbox.click()
        driver.execute_script("goToApply()") # 設定を反映
        print("フィルタリングをoffにしました")
    else:
        print("ルーター設定の変更はありません")

# ドライバーを終了する
driver.quit()
