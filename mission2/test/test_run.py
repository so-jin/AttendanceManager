import pytest
import subprocess
import sys

from unittest.mock import Mock, patch, mock_open, MagicMock
from mission2.attendance import Player, PlayerManager, Gold, Silver, Normal, run, read_file

@pytest.fixture
def dummy_attendance():
    return [
        ["Alice", "monday"],
        ["Alice", "wednesday"],
        ["Bob", "saturday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "wednesday"],
        ["Charlie", "saturday"],
        ["Charlie", "sunday"],
    ]

def test_enroll_player(dummy_attendance):
    player_manager = PlayerManager(dummy_attendance)
    player_manager.enroll_player()
    assert len(player_manager.players) == 3
    assert "Charlie" in player_manager.players
    assert "Alice" in player_manager.players
    assert "Bob" in player_manager.players


def test_calculate_players_point(dummy_attendance):
    player_manager = PlayerManager(dummy_attendance)
    player_manager.enroll_player()
    player_manager.calculate_players_point()
    assert player_manager.players["Charlie"].point == 34
    assert player_manager.players["Alice"].point == 4
    assert player_manager.players["Bob"].point ==2

def test_calculate_players_bonus_point(dummy_attendance):
    charlie = Player("charle",1)
    charlie.attended_on_wed = 10

    player_manager = PlayerManager(dummy_attendance)
    player_manager.players["charle"] = charlie
    player_manager.calculate_players_bonus_point()
    assert charlie.point == 10

def test_player_point_and_grade_gold():
    player = Player(name="Test", id=1)
    for day in ["wednesday"] * 10 + ["saturday"] * 10:
        player.calculate_point(day)

    player.calculate_bonus_point()
    player.get_grade()

    assert player.attended_on_wed == 10
    assert player.attended_on_weeken == 10
    assert player.point == 30 + 20 + 10 +10
    assert player.grade == Gold.name


def test_player_point_and_grade_silver():
    player = Player(name="Test", id=1)
    for day in ["wednesday"] * 10 + ["saturday", "sunday"]:
        player.calculate_point(day)

    player.calculate_bonus_point()
    player.get_grade()

    assert player.attended_on_wed == 10
    assert player.attended_on_weeken == 2
    assert player.point == 30 + 4 + 10
    assert player.grade == Silver.name


def test_player_calculate_and_grade_normal():
    player = Player("ana", 2)
    for day in ["monday"] * 10:
        player.calculate_point(day)
    player.calculate_bonus_point()
    player.get_grade()

    assert player.point == 10
    assert player.grade == Normal.name

def test_get_players_grade(capsys, dummy_attendance):
    player_manager = PlayerManager(dummy_attendance)
    player_manager.players["Ant"] = Player("Ant",1)

    player_manager.get_players_grade()
    output = capsys.readouterr().out.rstrip()
    assert "NAME" in output
    assert "POINT" in output
    assert "GRADE" in output
    assert "Ant" in output

def test_get_removed_player(capsys,dummy_attendance):
    player_manager = PlayerManager(dummy_attendance)

    player_manager.players["Ant"] = Player("Ant",1)
    player_manager.get_removed_player()
    output = capsys.readouterr().out.rstrip()
    assert "Removed player" in output
    assert "Ant" in output


def test_player_manager_enroll(dummy_attendance, monkeypatch):

    manager = PlayerManager(dummy_attendance)
    manager.enroll_player()
    manager.get_players_scores()
    manager.get_players_grade()

    assert "Alice" in manager.players
    assert "Charlie" in manager.players
    assert manager.players["Charlie"].grade == Silver.name


def test_get_removed_player_print(monkeypatch):
    player = Player("Lee", 3)
    player.get_grade()  # should be NORMAL by default

    manager = PlayerManager(dummy_attendance)
    manager.players["Lee"] = player
    printed = []

    def fake_print(*args):
        printed.append(args)

    monkeypatch.setattr("builtins.print", fake_print)

    manager.get_removed_player()
    assert any("Lee" in line for line in printed)


def test_readfile_fail(capsys):
    read_file("TEST")
    output = capsys.readouterr().out.rstrip()
    assert "파일을 찾을 수 없습니다." in output

def test_read_file_success():
    fake_data = ("Alice Monday\nBOO Tuseday")
    m = mock_open(read_data=fake_data)
    with patch("builtins.open",m):
        attendance = read_file("TEST")
        assert attendance == [["Alice", "Monday"], ["BOO", "Tuseday"]]


def test_run():
    fake_data = ("Alice Monday")
    m = mock_open(read_data=fake_data)
    with patch("builtins.open", m):
        attendance = read_file("TEST")
        run()
        assert attendance == [["Alice", "Monday"]]
