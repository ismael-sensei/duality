import discord
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sqlite3
import d20



TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Habilitar la intención de contenido del mensaje
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    print('Bot está listo y escuchando comandos!')

@client.event
async def on_message(message):
    print(f'Recibido mensaje: {message.content}')
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        command = message.content[1:].split()
        if command[0] == 'ping':
            await message.channel.send('pong!')
        elif command[0] == 'import' and len(command) == 2:
            character_id = command[1]
            url = f'https://app.demiplane.com/nexus/daggerheart/character-sheet/{character_id}'
            character_data = fetch_character_data(url)
            if character_data:
                save_character(message.author.id, character_data)
                await message.author.send(f'''```
    Personaje asignado: 

    **{character_data["name"]}**
    {character_data["class"]}, level {character_data["level"]}
```''')
            else:
                await message.channel.send('Error al importar los datos del personaje.')
        elif command[0] == 'show':
            character_data = load_character(message.author.id)
            if character_data:
                await message.channel.send(f'Tu personaje: Nombre: {character_data["name"]}, Nivel: {character_data["level"]}, Clase: {character_data["class"]}')
            else:
                await message.channel.send('No tienes un personaje asignado.')
        elif command[0] == 'agility':
            character_data = load_character(message.author.id)
            if character_data:
                mod = character_data['agility']
                result, hope, fear, _ = roll_dh(character_data['agility'])
                await message.channel.send(f'Roll 2d12+{mod}: **{result}** (Hope: {hope}, Fear: {fear})')
            else:
                await message.channel.send('No tienes un personaje asignado.')
        else:
            await message.channel.send(f'Comando `{command}` no reconocido.')

def roll_dh(mod = 0, adv = False, dis = False):
    hope = d20.roll('1d12')
    fear = d20.roll('1d12')
    result = hope + fear

    adv_dis = d20.roll('1d6')
    if adv:
        result = result + adv_dis
    elif dis:
        result = result - adv_dis

    result = result + mod

    return result, hope, fear, adv_dis


def fetch_character_data(url):
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
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'level-value'))
        )

        character_data = {}
        character_data['name'] = driver.find_element(By.CLASS_NAME, 'css-1dyfylb').text.strip()
        character_data['community'] = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-community').text.strip()
        character_data['ancestry'] = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-ancestry').text.strip()
        character_data['class'] = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-class').text.strip()
        character_data['subclass'] = driver.find_element(By.CLASS_NAME, 'header-name-subtitle-subclass').text.strip()
        character_data['level'] = driver.find_element(By.CLASS_NAME, 'level-value').text.strip()
        character_data['agility'] = driver.find_elements(By.CLASS_NAME, 'trait-value')[0].text.strip()
        character_data['strength'] = driver.find_elements(By.CLASS_NAME, 'trait-value')[1].text.strip()
        character_data['finesse'] = driver.find_elements(By.CLASS_NAME, 'trait-value')[2].text.strip()
        character_data['instinct'] = driver.find_elements(By.CLASS_NAME, 'trait-value')[3].text.strip()
        character_data['presence'] = driver.find_elements(By.CLASS_NAME, 'trait-value')[4].text.strip()
        character_data['knowledge'] = driver.find_elements(By.CLASS_NAME, 'trait-value')[5].text.strip()
        character_data['evasion'] = driver.find_element(By.CLASS_NAME, 'evasion-value').text.strip()
        character_data['armor'] = driver.find_element(By.CLASS_NAME, 'armor-value').text.strip()
        character_data['minor_th'] = driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[0].text.strip()
        character_data['major_th'] = driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[1].text.strip()
        character_data['severe_th'] = driver.find_elements(By.CLASS_NAME, 'threshold-value-text')[2].text.strip()
        character_data['armor_slots'] = driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()
        character_data['hp_slots'] = driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()
        character_data['stress_slots'] = driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()
        character_data['hope_slots'] = driver.find_elements(By.CLASS_NAME, 'tracker-max')[1].text.strip()
        

        print(character_data)

        driver.quit()
        return character_data
    except Exception as e:
        print(f'Error al parsear la hoja de personaje: {e}')
        return None
    


def create_table():
    conn = sqlite3.connect('characters.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            community TEXT,
            ancestry TEXT,
            class TEXT,
            subclass TEXT,
            level INTEGER,
            agility INTEGER,
            strength INTEGER,
            finesse INTEGER,
            instinct INTEGER,
            presence INTEGER,
            knowledge INTEGER,
            evasion INTEGER,
            armor INTEGER,
            minor_th INTEGER,
            major_th INTEGER,
            severe_th INTEGER,
            armor_slots INTEGER,
            hp_slots INTEGER,
            stress_slots INTEGER,
            hope_slots INTEGER
        );
    ''')
    conn.commit()
    conn.close()



def save_character(user_id, character_data):
    conn = sqlite3.connect('characters.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO characters (
            user_id, name, community, ancestry, class, subclass, level, 
            agility, strength, finesse, instinct, presence, knowledge, 
            evasion, armor, minor_th, major_th, severe_th, armor_slots, 
            hp_slots, stress_slots, hope_slots
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, character_data['name'], character_data['community'], character_data['ancestry'], 
        character_data['class'], character_data['subclass'], character_data['level'], 
        character_data['agility'], character_data['strength'], character_data['finesse'], 
        character_data['instinct'], character_data['presence'], character_data['knowledge'], 
        character_data['evasion'], character_data['armor'], character_data['minor_th'], 
        character_data['major_th'], character_data['severe_th'], character_data['armor_slots'], 
        character_data['hp_slots'], character_data['stress_slots'], character_data['hope_slots']
    ))
    conn.commit()
    conn.close()


def load_character(user_id):
    conn = sqlite3.connect('characters.db')
    c = conn.cursor()
    c.execute('''
        SELECT name, community, ancestry, class, subclass, level, agility, strength, finesse, 
               instinct, presence, knowledge, evasion, armor, minor_th, major_th, severe_th, 
               armor_slots, hp_slots, stress_slots, hope_slots 
        FROM characters 
        WHERE user_id = ?
    ''', (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return {
            'name': result[0],
            'community': result[1],
            'ancestry': result[2],
            'class': result[3],
            'subclass': result[4],
            'level': result[5],
            'agility': result[6],
            'strength': result[7],
            'finesse': result[8],
            'instinct': result[9],
            'presence': result[10],
            'knowledge': result[11],
            'evasion': result[12],
            'armor': result[13],
            'minor_th': result[14],
            'major_th': result[15],
            'severe_th': result[16],
            'armor_slots': result[17],
            'hp_slots': result[18],
            'stress_slots': result[19],
            'hope_slots': result[20]
        }
    else:
        return None

create_table()
client.run(TOKEN)
