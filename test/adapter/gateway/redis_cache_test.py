import pytest
from unittest.mock import patch, MagicMock
from redis.exceptions import RedisError
from adapter.gateways.cache import RedisCacheRepository, RedisAdapter
from domain.entities import Character

@pytest.fixture
def character():
    return Character(
        character_id = '',
        name = 'Marlowe Fairwind',
        community = 'Loreborne',
        ancestry = 'Elf',
        class_ = 'Sorcerer',
        subclass = 'Primal Origin',
        level = 1,
        agility = -1,
        strength = -1,
        finesse = +1,
        instinct = +2,
        presence = +1,
        knowledge = 0,
        evasion = 9,
        armor = 3,
        minor_th = 1,
        major_th = 6,
        severe_th = 12,
        armor_slots = 6,
        hp_slots = 6,
        stress_slots = 6,
        hope_slots = 6,
        thumbnail='',
        user_id = -1,
        game_id = -1
    )

@pytest.fixture
def redis_cache_repository():
    with patch('redis.Redis') as mock:
        yield RedisCacheRepository()

class TestRedisAdapter:
    def test_to_json(self, character):
        """ Testear la conversión de una entidad a JSON. """
        entity = character
        result = RedisAdapter.to_json(entity)
        assert result == '{"character_id": "", "name": "Marlowe Fairwind", "community": "Loreborne", "ancestry": "Elf", "class_": "Sorcerer", "subclass": "Primal Origin", "level": 1, "agility": -1, "strength": -1, "finesse": 1, "instinct": 2, "presence": 1, "knowledge": 0, "evasion": 9, "armor": 3, "minor_th": 1, "major_th": 6, "severe_th": 12, "armor_slots": 6, "hp_slots": 6, "stress_slots": 6, "hope_slots": 6, "thumbnail": "", "user_id": -1, "game_id": -1}'

    def test_from_json(self):
        """ Testear la conversión de JSON a entidad. """
        json_data = '{"character_id": "", "name": "Marlowe Fairwind", "community": "Loreborne", "ancestry": "Elf", "class_": "Sorcerer", "subclass": "Primal Origin", "level": 1, "agility": -1, "strength": -1, "finesse": 1, "instinct": 2, "presence": 1, "knowledge": 0, "evasion": 9, "armor": 3, "minor_th": 1, "major_th": 6, "severe_th": 12, "armor_slots": 6, "hp_slots": 6, "stress_slots": 6, "hope_slots": 6, "thumbnail": "", "user_id": -1, "game_id": -1}'
        result = RedisAdapter.from_json(json_data, Character)
        assert isinstance(result, Character)
        assert result.name == "Marlowe Fairwind"

class TestRedisCacheRepository:
    def test_get(self, redis_cache_repository: RedisCacheRepository, character: Character):
        """ Testear la obtención de un valor desde Redis. """
        with patch.object(RedisAdapter, 'from_json', return_value=character) as mock_json:
            mock_client = redis_cache_repository.client
            mock_client.get.return_value = '{"character_id": "", "name": "Marlowe Fairwind", "community": "Loreborne", "ancestry": "Elf", "class_": "Sorcerer", "subclass": "Primal Origin", "level": 1, "agility": -1, "strength": -1, "finesse": 1, "instinct": 2, "presence": 1, "knowledge": 0, "evasion": 9, "armor": 3, "minor_th": 1, "major_th": 6, "severe_th": 12, "armor_slots": 6, "hp_slots": 6, "stress_slots": 6, "hope_slots": 6, "thumbnail": "", "user_id": -1, "game_id": -1}'
            
            result = redis_cache_repository.get("character:123", Character)
            mock_json.assert_called_once()
            assert isinstance(result, Character)
            assert result.name == "Marlowe Fairwind"

    def test_set(self, redis_cache_repository: RedisCacheRepository, character):
        """ Testear el almacenamiento de un valor en Redis. """
        with patch.object(RedisAdapter, 'to_json', return_value='{"name": "Marlowe Fairwind"}') as mock_json:
            mock_client = redis_cache_repository.client
            redis_cache_repository.set("character:123", character)
            mock_client.set.assert_called_once_with("character:123", '{"name": "Marlowe Fairwind"}')
            mock_json.assert_called_once_with(character)
