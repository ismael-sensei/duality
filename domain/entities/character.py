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
    hp_slots: int
    stress_slots: int
    hope_slots: int
    thumbnail: str
    user_id: int
    game_id: int