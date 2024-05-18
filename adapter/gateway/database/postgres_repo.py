import psycopg
from psycopg import sql
from domain.entities.character import Character

class PostgresRepository:
    def __init__(self, dsn):
        self.dsn = dsn
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = psycopg.connect(self.dsn)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def insert_character(self, character: Character):
        insert_query = sql.SQL("""
            INSERT INTO characters (
                user_id, name, community, ancestry, class, subclass, level,
                agility, strength, finesse, instinct, presence, knowledge,
                evasion, armor, minor_th, major_th, severe_th, armor_slots,
                hp_slots, stress_slots, hope_slots
            ) VALUES (
                {user_id}, {name}, {community}, {ancestry}, {class_}, {subclass}, {level},
                {agility}, {strength}, {finesse}, {instinct}, {presence}, {knowledge},
                {evasion}, {armor}, {minor_th}, {major_th}, {severe_th}, {armor_slots},
                {hp_slots}, {stress_slots}, {hope_slots}
            ) RETURNING id
        """).format(
            user_id=sql.Placeholder('user_id'),
            name=sql.Placeholder('name'),
            community=sql.Placeholder('community'),
            ancestry=sql.Placeholder('ancestry'),
            class_=sql.Placeholder('class'),
            subclass=sql.Placeholder('subclass'),
            level=sql.Placeholder('level'),
            agility=sql.Placeholder('agility'),
            strength=sql.Placeholder('strength'),
            finesse=sql.Placeholder('finesse'),
            instinct=sql.Placeholder('instinct'),
            presence=sql.Placeholder('presence'),
            knowledge=sql.Placeholder('knowledge'),
            evasion=sql.Placeholder('evasion'),
            armor=sql.Placeholder('armor'),
            minor_th=sql.Placeholder('minor_th'),
            major_th=sql.Placeholder('major_th'),
            severe_th=sql.Placeholder('severe_th'),
            armor_slots=sql.Placeholder('armor_slots'),
            hp_slots=sql.Placeholder('hp_slots'),
            stress_slots=sql.Placeholder('stress_slots'),
            hope_slots=sql.Placeholder('hope_slots')
        )
        self.cursor.execute(insert_query, character.__dict__)
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def update_character(self, character_id, character: Character):
        update_query = sql.SQL("""
            UPDATE characters SET
                user_id = {user_id}, name = {name}, community = {community},
                ancestry = {ancestry}, class = {class_}, subclass = {subclass},
                level = {level}, agility = {agility}, strength = {strength},
                finesse = {finesse}, instinct = {instinct}, presence = {presence},
                knowledge = {knowledge}, evasion = {evasion}, armor = {armor},
                minor_th = {minor_th}, major_th = {major_th}, severe_th = {severe_th},
                armor_slots = {armor_slots}, hp_slots = {hp_slots},
                stress_slots = {stress_slots}, hope_slots = {hope_slots}
            WHERE id = {character_id}
        """).format(
            user_id=sql.Placeholder('user_id'),
            name=sql.Placeholder('name'),
            community=sql.Placeholder('community'),
            ancestry=sql.Placeholder('ancestry'),
            class_=sql.Placeholder('class'),
            subclass=sql.Placeholder('subclass'),
            level=sql.Placeholder('level'),
            agility=sql.Placeholder('agility'),
            strength=sql.Placeholder('strength'),
            finesse=sql.Placeholder('finesse'),
            instinct=sql.Placeholder('instinct'),
            presence=sql.Placeholder('presence'),
            knowledge=sql.Placeholder('knowledge'),
            evasion=sql.Placeholder('evasion'),
            armor=sql.Placeholder('armor'),
            minor_th=sql.Placeholder('minor_th'),
            major_th=sql.Placeholder('major_th'),
            severe_th=sql.Placeholder('severe_th'),
            armor_slots=sql.Placeholder('armor_slots'),
            hp_slots=sql.Placeholder('hp_slots'),
            stress_slots=sql.Placeholder('stress_slots'),
            hope_slots=sql.Placeholder('hope_slots'),
            character_id=sql.Placeholder('character_id')
        )
        params = {**character.__dict__, 'character_id': character_id}
        self.cursor.execute(update_query, params)
        self.conn.commit()

    def delete_character(self, character_id):
        delete_query = sql.SQL("DELETE FROM characters WHERE id = {character_id}").format(
            character_id=sql.Placeholder('character_id')
        )
        self.cursor.execute(delete_query, {'character_id': character_id})
        self.conn.commit()

    def get_character(self, character_id):
        select_query = sql.SQL("SELECT * FROM characters WHERE id = {character_id}").format(
            character_id=sql.Placeholder('character_id')
        )
        self.cursor.execute(select_query, {'character_id': character_id})
        row = self.cursor.fetchone()
        if row:
            return Character(
                user_id=row[1], name=row[2], community=row[3], ancestry=row[4],
                character_class=row[5], subclass=row[6], level=row[7], agility=row[8],
                strength=row[9], finesse=row[10], instinct=row[11], presence=row[12],
                knowledge=row[13], evasion=row[14], armor=row[15], minor_th=row[16],
                major_th=row[17], severe_th=row[18], armor_slots=row[19], hp_slots=row[20],
                stress_slots=row[21], hope_slots=row[22]
            )
        return None