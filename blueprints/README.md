# Blueprints

Automation blueprints for units running this integration, contributed by people
who use them on their own systems.

## What is in here

- **[MHI multi-split mode lockout resolver](automation/smdev0925/mhi-multi-split-mode-lockout.yaml)**
  by [smdev0925](https://github.com/smdev0925) — one outdoor unit serves one
  mode at a time, and MHI's AUTO latches its heat/cool choice, so a head that
  went quiet hours ago can still be locking everyone else out. This stands the
  side that just had its turn down to fan-only for a few minutes, which drops
  the latch and lets the waiting side take the system. It decides nothing about
  what a room needs: the vote is the unit's own Cool/Heat Status, and priority
  is its Compressor Demand. Running on a four-head SCM80.
  ([discussion](https://github.com/blues-sechseck/Mitsubishi-WF-RAC-Integration/discussions/328))

## Why they live here and not in the integration

The integration reports what a unit says and sends what you ask it to. It does
not decide anything on your behalf — no thermostat logic, no inference about
what a room needs, no coordination between units. That belongs in automations,
where you can read it, trace it and change it without waiting for a release.

A blueprint is the packaged form of exactly that: someone's working automation,
with the parts you have to fill in turned into a form.

## Installing one

Blueprints are **not** part of the integration download. HACS installs
`custom_components/mitsubishi_wf_rac/` and nothing else, so a file in here never
reaches your configuration on its own. Import it yourself:

**Settings → Automations & scenes → Blueprints → Import blueprint**, then paste
the GitHub URL of the `.yaml` file.

Home Assistant fetches it, checks it, and stores it under
`blueprints/automation/<author>/` in your configuration directory. It then shows
up under "Create automation → Use a blueprint". Re-importing the same URL later
picks up changes.

Each blueprint's header says which entities it needs. Several of the useful ones
are diagnostic entities that are **disabled by default** — you turn those on
under Settings → Devices & services → the device → "+N entities not shown".

## Contributing one

Send a pull request. Blueprints stay under their author's name, in the file and
in the pull request history.

What a blueprint needs before it can go in:

- **It has to run.** Say on what — how many indoor units, single-split or
  multi-split, and roughly how long it has been in service. "Untested but should
  work" is a gist, not a blueprint.
- **A header that says what it does and what it assumes**, including every
  entity it needs and whether that entity is on by default.
- **No hidden single-split assumptions.** On a multi-split several readings
  belong to the shared outdoor unit rather than to the head you asked, and
  compressor frequency is the obvious trap — it does not tell you what one
  indoor unit is doing. If a blueprint only makes sense on one architecture, its
  header should say so.
- **Helpers are the user's to create.** A blueprint cannot create an
  `input_text` or an `input_number`. If yours needs one, take it as an entity
  input and document it.
- **Write sparingly.** Every command to a unit takes a short exclusive lease on
  it, so an automation that writes on a tight loop will collide with the app and
  with this integration. Check the current state before sending a command that
  would not change anything.
