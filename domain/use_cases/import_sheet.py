from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from domain.interfaces.input import ImportSheetInput
from domain.entities.character import Character

class ImportSheet(ImportSheetInput):
    def logic(self, sheet_id: str, user_id: str) -> Character:
        character = ImportSheet.__fetch_data(f'https://app.demiplane.com/nexus/daggerheart/character-sheet/{sheet_id}')
        character.user_id = user_id

        return character


    def __fetch_data(url):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--remote-debugging-port=9222')
            options.binary_location = os.getenv('GOOGLE_CHROME_BIN')

            driver = webdriver.Chrome(service=ChromeService(executable_path=os.getenv('CHROMEDRIVER_PATH')), options=options)
            driver.get(url)

            # Esperar hasta que el div con class level-value sea visible
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'level-value'))
            )

            character = Character(
                user_id = '',
                name = driver.find_element(By.CLASS_NAME, 'css-1dyfylb').text.strip(),
                community = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-community').text.strip(),
                ancestry = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-ancestry').text.strip(),
                class_ = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-class').text.strip(),
                subclass = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-subclass').text.strip(),
                level = int(driver.find_element(By.CLASS_NAME, 'level-value').text.strip()),
                agility = int(driver.find_elements(By.CLASS_NAME, 'trait-value')[0].text.strip()),
                strength = int(driver.find_elements(By.CLASS_NAME, 'trait-value')[1].text.strip()),
                finesse = int(driver.find_elements(By.CLASS_NAME, 'trait-value')[2].text.strip()),
                instinct = int(driver.find_elements(By.CLASS_NAME, 'trait-value')[3].text.strip()),
                presence = int(driver.find_elements(By.CLASS_NAME, 'trait-value')[4].text.strip()),
                knowledge = int(driver.find_elements(By.CLASS_NAME, 'trait-value')[5].text.strip()),
                evasion = int(driver.find_element(By.CLASS_NAME, 'evasion-value').text.strip()),
                armor = int(driver.find_element(By.CLASS_NAME, 'armor-value').text.strip()),
                minor_th = int(driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[0].text.strip()),
                major_th = int(driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[1].text.strip()),
                severe_th = int(driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[2].text.strip()),
                armor_slots = int(driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()),
                hp_slots = int(driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()),
                stress_slots = int(driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()),
                hope_slots = int(driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip())
            )

            driver.quit()
            return character
        except Exception as e:
            print(f'Error al parsear la hoja de personaje: {e}')
            return None