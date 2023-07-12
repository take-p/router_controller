from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys

username = os.getenv("ROUTER_USERNAME")
password = os.getenv("ROUTER_PASSWORD")
url = "http://192.168.3.2"

# ユーザー名とパスワードをURLに埋め込む
auth_url = f"http://{username}:{password}@192.168.3.2"

driver = webdriver.Firefox()
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
    if sys.argv[1] == 'off' and checkbox.is_selected():
        checkbox.click()
        driver.execute_script("goToApply()") # 設定を反映
        print("フィルタリングをoffにしました")

# ドライバーを終了する
driver.quit()
