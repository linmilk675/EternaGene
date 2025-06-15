from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_genecards_summary(gene_symbol="FOXO3"):
    url = f"https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene_symbol}"

    options = Options()
    # options.add_argument("--headless")  # Без окна
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)

        # Ждём появления секции GeneCards Summary
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "summaries"))
        )

        time.sleep(2)  # подстраховка на подгрузку контента

        # Ищем div с описанием
        summary_div = driver.find_element(By.XPATH, '//*[@id="summaries"]//div[contains(@class, "gc-subsection-content")]')
        print("📘 GeneCards Summary:\n")
        print(summary_div.text)

    except Exception as e:
        print("❌ Ошибка:", e)
    finally:
        driver.quit()

# Пример вызова
if __name__ == "__main__":
    fetch_genecards_summary("FOXO3")
