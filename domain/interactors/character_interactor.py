from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from domain.interfaces import CharacterRepository
from domain.entities import Character, ActionRoll
import d20

class CharacterInteractor():
    repo: CharacterRepository
    user_id: str
    game_id: str
    character: Character

    def __init__(self, repo: CharacterRepository, user_id: str, game_id: str):
        self.repo = repo
        self.user_id = user_id
        self.game_id = game_id
        self.character = repo.get_character(user_id, game_id)

    def action_roll(self, attribute: str, mod: str = 0):
        if self.character is not None:
            mod = f"{mod}+{getattr(self.character, attribute)}"

        return ActionRoll(hope = d20.roll("1d12").total, fear = d20.roll("1d12").total, mod = d20.roll(mod))

    def agility(self, mod: str = 0):
        return self.action_roll("agility", mod)
    
    def strength(self, mod: str = 0):
        return self.action_roll("strength", mod)
    
    def finesse(self, mod: str = 0):
        return self.action_roll("finesse", mod)
    
    def instinct(self, mod: str = 0):
        return self.action_roll("instinct", mod)
    
    def presence(self, mod: str = 0):
        return self.action_roll("presence", mod)
    
    def knowledge(self, mod: str = 0):
        return self.action_roll("knowledge", mod)
    
    def import_sheet(self, sheet_url: str) -> Character:
        character = self.__fetch_data(sheet_url)
        self.character = character

        self.repo.add_character(character)
        return character

    def __fetch_data(self, sheet_url: str):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--remote-debugging-port=9222')
            options.binary_location = os.getenv('GOOGLE_CHROME_BIN')

            service=ChromeService(executable_path=os.getenv('CHROMEDRIVER_PATH'))
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(sheet_url)

            # Esperar hasta que el div con class level-value sea visible
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'level-value'))
            )

            character = Character(
                character_id = sheet_url.split('/')[-1],
                name = driver.find_element(By.CLASS_NAME, 'css-1dyfylb').text.strip(),
                community = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-community').text.strip(),
                ancestry = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-ancestry').text.strip(),
                class_ = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-class').text.strip(),
                subclass = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-subclass').text.strip(),
                level = int(driver.find_element(By.CLASS_NAME, 'level-value').text.strip()),
                agility = int(driver.find_elements(By.CSS_SELECTOR, 'div.trait-value.css-0')[0].text.strip()),
                strength = int(driver.find_elements(By.CSS_SELECTOR, 'div.trait-value.css-0')[1].text.strip()),
                finesse = int(driver.find_elements(By.CSS_SELECTOR, 'div.trait-value.css-0')[2].text.strip()),
                instinct = int(driver.find_elements(By.CSS_SELECTOR, 'div.trait-value.css-0')[3].text.strip()),
                presence = int(driver.find_elements(By.CSS_SELECTOR, 'div.trait-value.css-0')[4].text.strip()),
                knowledge = int(driver.find_elements(By.CSS_SELECTOR, 'div.trait-value.css-0')[5].text.strip()),
                evasion = int(driver.find_element(By.CLASS_NAME, 'evasion-value').text.strip()),
                armor = int(driver.find_element(By.CLASS_NAME, 'armor-value').text.strip()),
                minor_th = int(driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[0].text.strip()),
                major_th = int(driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[1].text.strip()),
                severe_th = int(driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[2].text.strip()),
                armor_slots = 0,
                armor_slots_max = int(driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()),
                hp = 0,
                hp_max = int(driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()),
                stress = 0,
                stress_max = int(driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()),
                hope = 0,
                hope_max = int(driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()),
                thumbnail = driver.find_element(By.CLASS_NAME, 'avatar__image').get_attribute('src'),
                user_id = self.user_id,
                game_id = self.game_id
            )

            driver.quit()
            service.stop()

            return character
        except Exception as e:
            print(f'Error al parsear la hoja de personaje: {e}')
            return None
        
    def update_attribute(self, attribute: str, mod: str):
        if self.character is not None:
            mod_value = d20.roll(mod).total
            current_value = getattr(self.character, attribute, 0)
            new_value = min(getattr(self.character, f'{attribute}_max'), max(0, current_value + mod_value))
            setattr(self.character, attribute, new_value)

            self.repo.add_character(self.character)
            return self.character
        return None
    
    def update_hope(self, mod: str):
        self.update_attribute("hope", mod)

    def update_hp(self, mod: str):
        self.update_attribute("hp", mod)

    def update_armor_slots(self, mod: str):
        self.update_attribute("armor_slots", mod)

    def update_stress(self, mod: str):
        self.update_attribute("stress", mod)

    def set_attribute(self, attribute: str, mod: str):
        if self.character is not None:
            mod_value = d20.roll(mod).total
            new_value = min(getattr(self.character, f'{attribute}_max'), max(0, mod_value))
            setattr(self.character, attribute, new_value)

            self.repo.add_character(self.character)
            return self.character
        return None

    def set_hope(self, mod: str):
        self.set_attribute("hope", mod)

    def set_hp(self, mod: str):
        self.set_attribute("hp", mod)

    def set_armor_slots(self, mod: str):
        self.set_attribute("armor_slots", mod)

    def set_stress(self, mod: str):
        self.set_attribute("stress", mod)