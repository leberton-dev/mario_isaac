from mario_isaac.ecs.component import HealthComponent


def test_take_damage_reduces_current_hp():
    health = HealthComponent(max_hp=6)

    assert health.damage(1) is True
    assert health.hp == 5


def test_take_damage_does_not_go_below_zero():
    health = HealthComponent(max_hp=6)
    _ = health.damage(10)

    assert health.hp == 0


def test_take_damage_respects_invulnerability_window():
    health = HealthComponent(max_hp=6)
    _ = health.damage(1)

    assert health.damage(1) is False
    assert health.hp == 5


def test_invulnerability_expires_after_ticking():
    health = HealthComponent(max_hp=6, invulnerability_duration=3)
    _ = health.damage(1)

    for _ in range(3):
        health.tick_invulnerability()

    assert health.damage(1) is True
    assert health.hp == 4


def test_alive():
    health = HealthComponent(max_hp=6)
    assert health.alive

    _ = health.damage(6)

    assert not health.alive


def test_zero_invulnerability_duration_allows_immediate_repeat_hits():
    health = HealthComponent(max_hp=3, invulnerability_duration=0)

    assert health.damage(1) is True
    assert health.damage(1) is True
    assert health.damage(1) is True
    assert health.hp == 0
    assert not health.alive

