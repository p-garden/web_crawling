from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import re  # 가격 숫자 추출을 위한 정규식 사용

# ✅ ChromeDriver 실행 경로 설정
chrome_driver_path = "/Users/pg/Desktop/작업PRO/chromedriver-mac-arm64/chromedriver"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# ✅ 카테고리별 URL 설정
category_urls = {
    "뷰티": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=104000&contentsId=",
    "전체": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=020000&contentsId=",
    "신발": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=103000&contentsId=",
    "상의": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=001000&contentsId=",
    "아우터": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=002000&contentsId=",
    "바지": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=003000&contentsId=",
    "원피스/스커트": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=100000&contentsId=",
    "가방": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=004000&contentsId=",
    "패션소품": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=101000&contentsId=",
    "속옷/홈웨어": "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=026000&contentsId=",

}

# ✅ 카테고리별 데이터 저장 딕셔너리
category_data = {}

for category, url in category_urls.items():
    try:
        print(f"📌 카테고리: {category} 크롤링 시작...")

        # ✅ 해당 카테고리 URL 이동
        driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        # ✅ 첫 번째 `div.sc-1y072n9-0` 찾기 (카테고리별 3개 상품을 포함)
        category_blocks = driver.find_elements(By.CLASS_NAME, "sc-1y072n9-0")  # 모든 카테고리 그룹 찾기
        if not category_blocks:
            print(f"❌ {category} 카테고리에서 상품 그룹을 찾을 수 없음")
            continue
        
        first_category_block = category_blocks[0]  # 첫 번째 카테고리 그룹 선택
        product_elements = first_category_block.find_elements(By.CLASS_NAME, "sc-1m4cyao-0")[:3]  # 상위 3개 상품

        top_3_products = []

        for product in product_elements:
            try:
                # ✅ 순위 가져오기 (data-item-list-index)
                rank = product.get_attribute("data-item-list-index")
                rank = int(rank) if rank else "순위 없음"

                # ✅ 상품명 가져오기
                product_name = product.find_element(By.CLASS_NAME, "text-body_13px_reg").text.strip()

                # ✅ 브랜드 가져오기 (data-item-brand)
                brand_name = product.get_attribute("data-item-brand") or "브랜드 없음"

                # ✅ 가격 가져오기 (data-price)
                price = product.get_attribute("data-price")
                price = f"{int(price):,}원" if price else "가격 없음"

                # ✅ 할인율 가져오기 (data-discount-rate)
                discount_rate = product.get_attribute("data-discount-rate")
                discount_rate = f"{discount_rate}%" if discount_rate and discount_rate != "0" else "할인 없음"

                # ✅ 상품 URL 가져오기
                product_url = product.find_element(By.CLASS_NAME, "sc-1m4cyao-9").get_attribute("href")

                # ✅ 데이터 저장
                top_3_products.append({
                    "순위": rank,
                    "상품명": product_name,
                    "브랜드": brand_name,
                    "가격": price,
                    "할인율": discount_rate,
                    "브랜드 URL": product_url
                })

            except NoSuchElementException:
                print(f"❌ {category} 카테고리에서 일부 상품 데이터를 찾을 수 없음")

        # ✅ 데이터 저장
        category_data[category] = top_3_products
        print(f"✅ {category} 완료!")

    except NoSuchElementException:
        print(f"❌ {category} 페이지에서 데이터를 찾을 수 없음")

# ✅ 브라우저 종료
driver.quit()

# ✅ 데이터 출력
for category, items in category_data.items():
    print(f"\n📌 {category} TOP 3:")
    for rank, name in enumerate(items, start=1):
        print(f"  {rank}위: {name}")

# ✅ CSV 파일로 저장
df = pd.DataFrame.from_dict(category_data, orient="index").transpose()
df.to_csv("musinsa_category_top3.csv", index=False, encoding="utf-8-sig")

print("\n✅ 크롤링한 데이터가 'musinsa_category_top3.csv' 파일로 저장되었습니다!")