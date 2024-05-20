import pytest
from unittest.mock import MagicMock, patch
from domain.entities import Character, ActionRoll
from domain.interactors.character_interactor import CharacterInteractor
import d20

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    return repo

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
        armor_slots = 0,
        armor_slots_max= 6,
        hp = 0,
        hp_max = 6,
        stress = 0,
        stress_max = 6,
        hope = 2,
        hope_max = 6,
        thumbnail='',
        user_id = '1',
        game_id = '1'
    )

@pytest.fixture
def interactor(mock_repo, character):
    mock_repo.get_character.return_value = character
    return CharacterInteractor(repo=mock_repo, user_id="1", game_id="1")

def test_import_sheet(interactor, mock_repo):
    with patch.object(interactor, '_CharacterInteractor__fetch_data') as mock_fetch:
        mock_fetch.return_value = interactor.character
        character = interactor.import_sheet("http://example.com/sheet")
        assert character == interactor.character
        mock_repo.add_character.assert_called_once_with(character)

def test_update_attribute(interactor, mock_repo):
    with patch('d20.roll') as mock_roll:
        mock_roll.side_effect = [MagicMock(total=5)]
        interactor.update_attribute("hope", "1d6")
        assert interactor.character.hope == 6  # min(6, max(0, 2+5)) = 6
        mock_repo.add_character.assert_called_once_with(interactor.character)

def test_update_hope(interactor, mock_repo):
    with patch('d20.roll') as mock_roll:
        mock_roll.side_effect = [MagicMock(total=5)]
        interactor.update_hope("1d6")
        assert interactor.character.hope == 6  # min(6, max(0, 2+5)) = 6
        mock_repo.add_character.assert_called_once_with(interactor.character)

def test_update_hp(interactor, mock_repo):
    with patch('d20.roll') as mock_roll:
        mock_roll.side_effect = [MagicMock(total=5)]
        interactor.update_hp("1d6")
        assert interactor.character.hp == 5  # 0 + 5
        mock_repo.add_character.assert_called_once_with(interactor.character)

def test_update_armor_slots(interactor, mock_repo):
    with patch('d20.roll') as mock_roll:
        mock_roll.side_effect = [MagicMock(total=-2)]
        interactor.update_armor_slots("-1d6")
        assert interactor.character.armor_slots == 0  # min(6, max(0, 0 -2)) = 0
        mock_repo.add_character.assert_called_once_with(interactor.character)

def test_update_stress(interactor, mock_repo):
    with patch('d20.roll') as mock_roll:
        mock_roll.side_effect = [MagicMock(total=3)]
        interactor.update_stress("1d6")
        assert interactor.character.stress == 3  # 0 + 3
        mock_repo.add_character.assert_called_once_with(interactor.character)

def test_action_roll(interactor):
    action_roll = interactor.action_roll("agility", "+1")
    assert action_roll.mod.total == 0

def test_agility(interactor):
    action_roll = interactor.agility("+1")
    assert action_roll.mod.total == 0

def test_strength(interactor):
    action_roll = interactor.strength("+2")
    assert action_roll.mod.total == 1

def test_finesse(interactor):
    action_roll = interactor.finesse()
    assert action_roll.mod.total == 1

def test_instinct(interactor):
    action_roll = interactor.instinct("-1")
    assert action_roll.mod.total == 1

def test_presence(interactor):
    action_roll = interactor.presence("-1")
    assert action_roll.mod.total == 0

def test_knowledge(interactor):
    action_roll = interactor.knowledge("-1")
    assert action_roll.mod.total == -1