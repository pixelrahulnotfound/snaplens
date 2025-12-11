import base64
import time
from io import BytesIO
from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def screenshot_fullpage_base64(url: str, timeout=10):

    chrome_options = Options()
    chrome_options.add_argument("--headless")   # FIXED
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-javascript")


    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.get(url)

        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            pass

        time.sleep(1)

        total_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")

        if not total_height or not viewport_height:
            raise Exception("Page returned zero height. Headless mode issue.")

        images = []
        offset = 0

        while offset < total_height:
            driver.execute_script(f"window.scrollTo(0, {offset});")
            time.sleep(0.4)

            png_bytes = driver.get_screenshot_as_png()
            img = Image.open(BytesIO(png_bytes))
            images.append(img)

            offset += viewport_height

        driver.quit()

        total_width = images[0].width
        total_stitched_height = sum(i.height for i in images)

        stitched = Image.new("RGB", (total_width, total_stitched_height))

        y = 0
        for img in images:
            stitched.paste(img, (0, y))
            y += img.height

        buffer = BytesIO()
        stitched.save(buffer, format="PNG")
        b64 = base64.b64encode(buffer.getvalue()).decode()

        return b64

    except Exception as e:
        print(f"[!] Fullpage screenshot failed for {url}: {e}")
        try:
            driver.quit()
        except:
            pass
        return None
