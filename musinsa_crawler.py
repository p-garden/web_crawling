from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# ✅ ChromeDriver 경로 확인 후 설정
chrome_driver_path = "/Users/pg/Downloads/chromedriver-mac-arm64/chromedriver"
service = Service(chrome_driver_path)

try:
    # ✅ Chrome 실행
    driver = webdriver.Chrome(service=service)

    # ✅ Google 페이지 열기
    driver.get("https://www.google.com")

    # ✅ 3초 대기 후 종료
    time.sleep(3)
    driver.quit()

    print("✅ Selenium과 ChromeDriver 연결 성공!")

except Exception as e:
    print(f"❌ 오류 발생: {e}")