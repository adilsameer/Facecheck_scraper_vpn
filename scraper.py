import base64
import time
import requests
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


print("Welcome to the FaceCheck ID Scraper! This tool uses a VPN to bypass captchas and retrieve results. To run, "
      "provide the absolute path to an image. The script will make up to 15 attempts to get the results. If it "
      "exceeds the limit, please rerun the script after some time.\n\n")
class Scraper:

    def start(self):

        options = webdriver.ChromeOptions()
        options.add_extension(r"C:\Users\mdadi\Downloads\Internship-OCR-project\VPN-extension.crx")
        self.driver = webdriver.Chrome(options=options)
        self.extension_url = "chrome-extension://majdfhpaihoncoakbjgbdhglocklcgno/html/foreground.html"
        self.first_execution = True
        self.extracted_urls = []

    def setup_vpn(self):
        try:
            time.sleep(1)
            self.driver.get(self.extension_url)
            time.sleep(3)
            self.driver.switch_to.window(self.driver.window_handles[0])
            start = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#screen-tooltips-template > div.navigation > div > div:nth-child(3) > div > div > button")))
            start.click()
            continue_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#screen-tooltips-template > div.navigation > div > div:nth-child(3) > div > div > button")))
            continue_btn.click()
            select_region = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#content > div.current-region > div > div.current-region-upper-block > span")))
            select_region.click()
            select_france = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#region-list > div:nth-child(2) > div.region-name-fav-wrapper > div > span.region-area")))
            select_france.click()
        except TimeoutException:
            print("Timeout while setting up VPN")

    def toggle_vpn(self, target_state, max_attempts=2):
        attempts = 0
        while attempts < max_attempts:
            try:
                vpn_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainBtn > span")))
                vpn_button.click()
                WebDriverWait(self.driver, 15).until(
                    EC.text_to_be_present_in_element((By.XPATH, '//*[@id="mainBtn"]/div'), f"VPN is {target_state}"))
                time.sleep(2)
                return True
            except TimeoutException:
                print(f"Timeout while turning VPN {target_state.lower()}, attempt {attempts + 1}")
                attempts += 1
        print(f"Failed to turn VPN {target_state.lower()} after {max_attempts} attempts")
        return False

    def turn_on_vpn(self):
        return self.toggle_vpn("ON")

    def turn_off_vpn(self):
        return self.toggle_vpn("OFF")

    def upload_pic(self, image_path):
        try:
            self.driver.get('https://facecheck.id/')
            wait = WebDriverWait(self.driver, 10)
            file_input = self.driver.find_element(By.CSS_SELECTOR, "#fileElem")
            file_input.send_keys(image_path)
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#searchButton")))
            time.sleep(0.543)
            search_button.click()
            if self.first_execution:
                check_mark = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#iagree")))
                check_mark.click()
                time.sleep(1)
                view_report_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]")))
                view_report_button.click()
                self.first_execution = False
        except (TimeoutException, NoSuchElementException):
            print("Timeout or element not found during picture upload")

    def main(self, image_path):
        try:
            self.start()
            self.setup_vpn()
            if not self.turn_on_vpn():
                print("Failed to turn on VPN during initial setup")
                return
            max_captcha_attempts = 15
            attempts = 0
            while attempts < max_captcha_attempts:
                self.upload_pic(image_path)
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "captcha")))
                    print(f"Captcha detected. Reconnecting VPN... (Attempt {attempts + 1}/{max_captcha_attempts})")
                    time.sleep(1)
                    self.driver.get(self.extension_url)
                    time.sleep(1)
                    self.driver.get(self.extension_url)
                    self.turn_off_vpn()
                    if not self.turn_on_vpn():
                        print("Failed to turn on VPN during captcha handling")
                        return
                except TimeoutException:
                    print("Captcha Not Detected")
                    # print(self.driver.current_url)
                    id_search_value = self.driver.current_url.split('#')[-1]
                    self.driver.quit()
                    # print(id_search_value)
                    api_url = "https://facecheck.id/api/search"
                    payload = (
                        "{{\"id_search\":\"{id_search1}\",\"with_progress\":true,"
                        "\"id_captcha\":\"65d72428-0a87-406d-b4a4-78a40d05edc4\",\"status_only\":false,\"demo\":false}}"
                    ).format(id_search1=id_search_value)
                    headers = {
                        'accept': 'application/json, text/javascript, */*; q=0.01',
                        'accept-language': 'en-US,en;q=0.5',
                        'content-type': 'application/json; charset=UTF-8',
                        'origin': 'https://facecheck.id',
                        'priority': 'u=1, i',
                        'referer': 'https://facecheck.id/',
                        'sec-ch-ua': '"Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'sec-gpc': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/125.0.0.0 Safari/537.36',
                        'x-requested-with': 'XMLHttpRequest'
                    }

                    api_attempts = 0
                    while api_attempts < 4:
                        response = requests.post(api_url, headers=headers, data=payload)
                        if response.status_code == 200:
                            data = response.json()
                            if data and data.get("code") == "TEMP_BAN":
                                print("Too many attempts. Temporary ban in effect.")
                                break
                            if data and data.get("message") == "Search Completed":
                                print("Search Completed")
                                if 'output' in data and 'items' in data['output']:
                                    os.makedirs("images", exist_ok=True)
                                    self.extracted_urls = []
                                    for item in data['output']['items']:
                                        base64_image = item['base64'].split(",")[1]
                                        binary_image = base64.b64decode(base64_image)
                                        with open(f"images/{item['guid']}.jpg", "wb") as f:
                                            f.write(binary_image)
                                        url = item['url']
                                        self.extracted_urls.append(url)
                                    print("Image appeared in below websites (URLs):")
                                    for url in self.extracted_urls:
                                        clean_url = url.replace("*****", "")
                                        print(clean_url)
                                else:
                                    print("No items found in the response")
                                break
                            else:
                                print("Search In Progress...")
                                time.sleep(3)  # Wait before making the next request
                        else:
                            print("Error:", response.status_code)
                            break
                        api_attempts += 1
                attempts += 1
        except WebDriverException as e:
            print(f"WebDriverException occurred: {e}")
        finally:
            try:
                self.driver.quit()
            except:
                pass

# image_path = r"absolute path"
# scraper = Scraper()
# scraper.main(image_path)
