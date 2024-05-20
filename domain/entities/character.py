from dataclasses import dataclass

@dataclass
class Character:
    character_id: str
    name: str
    community: str
    ancestry: str
    class_: str
    subclass: str
    level: int
    agility: int
    strength: int
    finesse: int
    instinct: int
    presence: int
    knowledge: int
    evasion: int
    armor: int
    minor_th: int
    major_th: int
    severe_th: int
    armor_slots: int
    armor_slots_max: int
    hp: int
    hp_max: int
    stress: int
    stress_max: int
    hope: int
    hope_max: int
    thumbnail: str
    user_id: int
    game_id: int