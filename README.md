# Shadow Man Remastered — Archipelago World

An [Archipelago](https://archipelago.gg) multiworld implementation of
**Shadow Man Remastered** (Nightdive Studios, 2021). This is the AP
*world* — the plugin Archipelago's generator and client load to include
Shadow Man in a multiworld. It's a sibling project to, and shares its
byte-level patching engine with, the standalone single-player randomizer
(the `shadow-man-remastered-randomizer` repo) for the same game, but the
two are built for different audiences and have diverged in real ways —
see "How this differs from the standalone randomizer" below.

## Goal

Defeat Legion. Reaching him requires collecting enough Dark Souls to open
the coffin gates blocking Deadside progress and completing the five Engine
Blocks (or, if Piston Combo Randomizer is on, also finding and reading
Jack's Schematic to learn that seed's randomized piston combination). Your
client reports `goal complete` automatically the moment Legion is
confirmed dead.

## Setup

**Follow [the setup guide](guide_en.md), not this file, for install steps.**
Short version: generate a YAML (by hand, via the Archipelago website's
generator, or with the Shadow Man Remastered AP Companion tool in the
`shadow-man-remastered-randomizer` repo), get your `.apshadowman` file
from generation, then run `apply_ap_seed.py` (or the Companion tool's
"Apply AP Seed" tab) against your local game install to patch it. No
local game install is needed until that last step.

## What gets randomized

Progression items (Engineers Key, Poigne, Baton, Flambeau, Marteau,
Calabash, Eclipser parts, Retractors, Accumulators, Gad Powers, Prison Key
Card), plus whichever optional categories you enable: weapons, lore items,
the Light Soul bonus, enemy types, ambient creatures, music, voice lines,
and sound effects. Dark Souls, Govis, and Gad Powers are always shuffled
into the item pool and placed by AP's own fill — there's no option to keep
Gad Powers at their vanilla temple locations (an earlier "Shuffle Gad
Temples" toggle existed but its off-state was a real bug, since removed;
see the feature-gap section below). If you want Gad Powers guaranteed from
the start instead of found through play, use AP's own Start Inventory From
Pool for them in your YAML. Coffin gate soul requirements, in-game
soul-level thresholds, Deadside
portal connections, and Dark Engine piston combinations can all be
randomized too. Full option list and detailed behavior notes live in
`options.py` — this section just groups the highlights.

**Progression & logic**
- `gate_preset` — coffin gate soul requirements: story (all open) through
  chaos (fully unconstrained).
- `max_gate_sl` / `open_gates_n` — extra caps/overrides on top of the preset,
  mainly for multiworld reliability.
- `entrance_mode` — shuffle which Deadside hub portal leads where
  (`deadside_only`; `cross_hub` isn't ported from the standalone yet).
- `soul_threshold_mode` / `soul_logic_buffer` — randomize real in-game
  soul-level requirements and/or pad AP's own logic with extra slack.
- `progression_balancing` — how aggressively key items are pushed toward
  deeper locations.
- `piston_combos` — randomize the 6 Dark Engine piston combinations;
  makes Jack's Schematic required progression when on.
- `insanity` ("Cadeaux Key Items") / `cadeaux_bundle_size` /
  `cadeaux_gated_content` ("Fog Door Check") — whether Cadeaux locations
  exist as AP checks at all, whether they're bundled into grouped checks,
  and whether the Fogometers Light Soul is included.

**Cosmetic / optional shuffles**
`shuffle_weapons`, `shuffle_lore`, `shuffle_bonus`, `shuffle_enemies`
(+ `enemy_mode`, `enemy_mix_movement`, `enemy_uncap_counts`),
`shuffle_true_forms`, `shuffle_ambients` (+ `ambient_mode`),
`shuffle_music`, `shuffle_voices`, `shuffle_weapons_sfx`,
`shuffle_enemies_sfx`, `shuffle_sky`.

**Gameplay tweaks (EXE patch — applied by `apply_ap_seed.py`, not at
generation time)**
`deadside_guns`, `starting_health`, `altar_health_grant`,
`altar_cadeaux_required`, `fogometers_cadeaux_required`, `death_penalty`,
`sprint_multiplier`.

**Traps & Bonuses**
`trap_bonus_count` and friends add filler items that apply a random
temporary or permanent effect on receipt — cosmetic secrets, a health
poison/heal, a voodoo power drain/hold, or an ammo drain/hold. Fully
optional (0 by default) and each effect category can be toggled off
independently.

**Multiplayer**
`death_link` / `death_link_threshold` — standard Death Link, with an
optional throttle on how many of your own deaths it takes to send one.

## How this differs from the standalone randomizer

This world and the standalone tool share the same placement engine and
byte-patching modules, but they're genuinely different products, not just
two skins on one feature set:

- **No barrel/weapon/lore/bonus "insanity" scope.** The standalone's
  graded insanity tiers can also open weapon/lore/bonus/barrel slots as
  fill targets (barrels alone would add ~2,085 locations). This world's
  `insanity` option only covers Cadeaux locations — a deliberate, narrower
  scope, not a missing port.
- **`cross_hub` entrance mode and `shuffle_prisms` aren't ported.**
  `deadside_only` entrance shuffle and piston combo randomization are.
- **In-game tracker hints aren't available.** The standalone's
  `patch_tracker` option has no AP equivalent — it was removed after
  turning out to be a non-functional no-op on the AP side.
- **Gad Powers are always shuffled, with no "leave them at the temples"
  option.** The standalone's `--shuffle-gad-temples` flag genuinely works
  either way. This world used to expose the same choice, but its off-state
  turned out to silently discard whatever AP placed at a gad temple
  location (best case a lost filler check, worst case an unbeatable seed)
  — nothing here ever excluded those locations from AP's own fillable pool
  the way it needed to. Removed rather than patched around it; use Start
  Inventory From Pool if you want Gad Powers guaranteed from the start.
- **Traps & Bonuses and Death Link are AP-only additions** with no
  standalone equivalent — they only make sense in a multiworld/live-client
  context.
- **Because Archipelago's own fill algorithm places items** (rather than
  this project's own assumed-fill sequence), `access_rules.py` and
  `regions.py` carry substantially more logic here than their standalone
  counterparts — the two are not meant to be identical files, unlike most
  of the small patch/randomizer modules they're built alongside.

See `AP_FEATURE_GAP.md` for the full, detailed audit history behind these
gaps, including the real bugs found and fixed along the way.

## Credits

- Game by Nightdive Studios
- Randomizer and AP world by the Shadow Man modding community
