from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_alliance_summary(hgnc_id):
    url = f"https://www.alliancegenome.org/gene/{hgnc_id}"
    
    options = Options()
    options.add_argument("--headless")  # убрать если хочешь видеть браузер
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=Service(), options=options)
    
    try:
        driver.get(url)

        # Ждём появления нужного блока
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "col-md-9"))
        )
        
        all_dd = driver.find_elements(By.CLASS_NAME, "col-md-9")
        for dd in all_dd:
            text = dd.text
            if "Enables several functions" in text:
                return text

        return None  # не найдено

    except Exception as e:
        print(f"[Alliance] Ошибка Selenium: {e}")
        return None

    finally:
        driver.quit()
