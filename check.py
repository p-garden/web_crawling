from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# ✅ ChromeDriver 실행 경로 설정
chrome_driver_path = "/Users/pg/Desktop/작업PRO/chromedriver-mac-arm64/chromedriver"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# ✅ 무신사 랭킹 페이지 이동
url = "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=104000&contentsId="
driver.get(url)

# ✅ 페이지 로딩 대기
time.sleep(3)

# ✅ HTML 코드 일부 가져오기 (상품 리스트 구조 확인)
html_source = driver.page_source

# ✅ 파일로 저장 (VS Code에서 직접 확인 가능)
with open("musinsa_ranking_source.html", "w", encoding="utf-8") as f:
    f.write(html_source)

print("✅ HTML 소스 코드가 'musinsa_ranking_source.html' 파일로 저장되었습니다!")

# ✅ 브라우저 종료
driver.quit()