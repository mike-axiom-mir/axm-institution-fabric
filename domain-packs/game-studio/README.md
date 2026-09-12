# Game Studio Domain Package

This is the first proving domain for **AXM Institution Fabric — The Building**.

It is intentionally a package *inside* the institution rather than the definition of the institution.

## Purpose

Translate real game-development professions into persistent lane contracts that can be occupied by different intelligences without losing role continuity.

The package should eventually carry:

- role/lane definitions;
- professional reference knowledge;
- deterministic specialist tools;
- artifact types;
- quality gates;
- evidence requirements;
- handoff conventions;
- domain tests;
- integration dependencies.

## Source experiment

AXM Ghost Studio is the main current evidence source for role behavior and coordination needs.

Use it to discover what each lane actually requires. Do not assume every prompt, temporary scheduling rule, or current studio convention belongs permanently in this package.

## Candidate lanes

The current experiment suggests at least:

```text
Game Director
Integration Steward
Gameplay Engineer
Systems Designer
World / Encounter Designer
Experience / Art / Audio Director
QA / Playtest Specialist
```

Additional lanes may be added when evidence shows a persistent professional responsibility is missing.

## Extraction rule

When converting an existing specialist role into a lane, separate:

```text
PERMANENT ROLE CONTRACT
purpose
responsibilities
exclusions
inputs
outputs
knowledge
tools
evidence
quality gates
handoff

FROM

TEMPORARY EXPERIMENT DETAIL
current chat wording
specific schedule
current worker identity
one-off branch names
temporary coordination hacks
historical accidents
```

The first category belongs here. The second belongs in experiment state or not at all.

## First implementation target

Start with only three lanes:

1. Gameplay Engineer
2. Systems Designer
3. QA / Playtest

Use them to prove an implementation -> rule-system -> verification loop.

Do not expand to the whole studio until those lanes can exchange typed artifacts and return packets through the Institution Fabric kernel.

## Success condition

A different occupant should be able to enter each lane and continue from explicit institutional state without needing the previous occupant's private conversation.
