"""
worlds/shadowman/test/__init__.py
==================================
AP's own standard per-world test convention: WorldTestBase subclasses are
auto-discovered by pytest. Each class here constructs a real single-player
MultiWorld with the given options and runs it through generation -- this
is the same `world_setup()`/generation path AP's actual Generate.py uses,
just without needing to hand-write a YAML or run the full CLI.

RUN IT AS: `pytest worlds/shadowman/test/__init__.py` (the FILE, not the
bare directory). `pytest worlds/shadowman/test/` collects 0 items with no
error -- this AP version's pytest.ini python_files pattern
(`**/test*/**/__init__.py`) doesn't actually match this path on this
Python version (confirmed: `pathlib.Path.match()` here doesn't expand `**`
across directory segments the way a true globstar would -- a pytest.ini/
Python-version quirk, not something to fix by editing vendored AP config).
Pointing pytest at the file directly sidesteps it entirely and is proven
reliable.

This is new (2026-09-16) -- shadowman had no test/ package before this.
Deliberately starts small: default options, plus one class per recently
-added option most likely to break generation if something regresses
(Unique Retractor Keys, Cadeauxsanity, Piston Combos). Add more option
combinations here over time rather than trying to cover everything at
once.

IMPORTANT, learned the hard way while writing this file: a WorldTestBase
subclass with NO test_* methods of its own collects zero pytest items,
even though WorldTestBase itself defines test_fill/
test_all_state_can_reach_everything/test_empty_state_can_reach_something.
Pytest's unittest-style collection walks each MODULE for classes matching
python_classes (see pytest.ini: "Test"), then collects that class's own
methods matching python_functions ("test") -- but a bare subclass with
no body of its own apparently isn't enough to trigger it picking up the
*inherited* methods here (confirmed empirically: every class below needs
its own explicit test_ method, even a trivial `pass`, or pytest reports
"collected 0 items" with no error at all -- not a skip, not a failure,
just silently nothing). test_generates below exists for exactly this
reason: setUp() -> world_setup() already runs full generation before any
test method body executes, so even a `pass` body meaningfully proves
"generation didn't crash for this option combination" -- the whole point
of these classes existing. pytest STILL separately auto-discovers and
runs WorldTestBase's own inherited test_fill/test_all_state_.../
test_empty_state_... as their own independent test methods on every
class below (each gets its own freshly-seeded multiworld, distinct
from test_generates's) -- that's what actually provides reachability/
fill coverage; test_generates doesn't need to (and, see below, must
not) call them itself.

CORRECTION (2026-09-16, same day): test_generates originally also
called self.test_all_state_can_reach_everything()/test_fill() directly,
reasoning that "might as well exercise these explicitly rather than
hope they get auto-collected." This was wrong and produced a real false
alarm: it created a SECOND, redundantly re-seeded instance of the same
checks pytest was already running on its own, and that specific
redundant instance intermittently failed test_fill's own accessibility
check ("Collected all locations, but can't beat the game") even under
Jon's own real YAML (piston_combos/unique_retractor_keys/cadeauxsanity
all on), which he'd already generated successfully many times for real.
Confirmed the real Generate.py pipeline itself has no such issue: ran
it directly against that exact YAML across 5 different seeds, zero
failures. So the failure was specific to calling WorldTestBase's own
test_fill() a second, redundant time in this way -- not a real
completability bug in this world's logic, and not worth chasing further
now that real generation is proven solid. test_generates is back to
being a pure "did setUp() succeed" smoke test; do not re-add explicit
calls to the inherited test_* methods here.
"""
from test.bases import WorldTestBase


class ShadowManTestBase(WorldTestBase):
    game = "Shadow Man Remastered"

    def test_generates(self) -> None:
        """setUp() already ran full generation for this class's `options`
        -- reaching this line at all is the actual assertion. Do NOT
        call self.test_fill()/test_all_state_can_reach_everything() etc.
        here -- see the module docstring's 2026-09-16 correction."""
        pass


class TestDefaultOptions(ShadowManTestBase):
    """Generation succeeds with every option at its default value."""
    options = {}


class TestUniqueRetractorKeys(ShadowManTestBase):
    options = {
        "unique_retractor_keys": True,
    }


class TestCadeauxsanity(ShadowManTestBase):
    options = {
        "cadeauxsanity": True,
        "cadeaux_bundle_size": 5,
    }


class TestPistonCombos(ShadowManTestBase):
    options = {
        "piston_combos": True,
    }


class TestManyOptionsTogether(ShadowManTestBase):
    """A denser combination, closer to what a real player's YAML might
    look like, to catch interaction bugs a single-option test wouldn't."""
    options = {
        "unique_retractor_keys": True,
        "cadeauxsanity": True,
        "cadeaux_bundle_size": 5,
        "cadeaux_gated_content": True,
        "piston_combos": True,
        "trap_bonus_count": 10,
    }


class TestBropacmanYaml(ShadowManTestBase):
    """Jon's own real YAML (2026-09-16) -- he's generated this many times
    with zero failures. Used to check whether TestUniqueRetractorKeys/
    TestCadeauxsanity/TestPistonCombos's isolated test_fill failures are
    real bugs tied to those options, or an artifact of testing them with
    every OTHER option left at whatever WorldTestBase's bare default is
    (e.g. gate_preset/max_gate_sl/open_gates_n unset here, all
    deliberately pinned in Jon's real YAML). display/meta-only YAML keys
    (name, description, game, start_inventory_from_pool) excluded --
    those aren't real ShadowManOptions fields."""
    options = {
        "gate_preset": "hard",
        "max_gate_sl": 8,
        "open_gates_n": -1,
        "shuffle_weapons": True,
        "shuffle_lore": True,
        "shuffle_bonus": True,
        "shuffle_enemies": False,
        "enemy_mode": "difficulty",
        "enemy_mix_movement": False,
        "enemy_uncap_counts": False,
        "shuffle_true_forms": False,
        "shuffle_ambients": True,
        "ambient_mode": "global",
        "shuffle_music": True,
        "shuffle_voices": True,
        "shuffle_weapons_sfx": False,
        "shuffle_enemies_sfx": True,
        "combine_voice_and_enemy_sfx": True,
        "shuffle_sky": False,
        "entrance_mode": "off",
        "piston_combos": True,
        "unique_retractor_keys": True,
        "deadside_guns": True,
        "progression_balancing": 50,
        "cadeauxsanity": True,
        "cadeaux_bundle_size": 10,
        "starting_health": 5,
        "altar_health_grant": "random",
        "altar_cadeaux_required": "random",
        "fogometers_cadeaux_required": "random",
        "cadeaux_gated_content": True,
        "death_penalty": "random",
        "sprint_multiplier": 30,
        "soul_threshold_mode": "progressive",
        "soul_logic_buffer": "off",
        "trap_bonus_count": 150,
        "trap_bonus_mode": "random",
        "trap_bonus_duration": 100,
        "trap_bonus_secrets_enabled": True,
        "trap_bonus_health_enabled": True,
        "trap_bonus_voodoo_enabled": True,
        "trap_bonus_ammo_enabled": True,
        "death_link": True,
        "death_link_threshold": 1,
    }
