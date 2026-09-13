# CURRENT STATE OVERLAY — Stage 4 subject binding integrated

Status: **no active blocker on the bounded exact evidence-subject resolver**. The next open gate is a read-only created-output compatibility preflight. This file supersedes the older ADV-040 hold text and is a narrow current-state overlay on `coordination/CURRENT_WAVE.md`.

Canonical integration point:

`756c9cbd0820e08d1cf4f6d3c91bcff2e67a21e9`

PR #45 — `Lane 02: exact evidence subject binding` — is merged.

## What is now canonical

The Stage 4 runtime can now:

1. exact-load one return packet's created-artifact and packet-evidence relations through the already-canonical packet-output identity layer;
2. parse candidate `evidence.subject_ref` values through the shared Stage 2 immutable-ref grammar;
3. bind evidence only to the exact packet-created artifact ref it names;
4. preserve exact unrelated/non-exact subject evidence as unmatched rather than assigning it by type, array order, recency, logical id, or actor intent;
5. fail closed on wrong-kind exact subject refs for artifact compatibility use;
6. keep `artifact.evidence_refs` non-authoritative for the Decision 008 post-artifact chronology;
7. keep any non-empty `artifacts_modified[]` fail-closed;
8. preserve the ADV-035/036/037/038/039/040 regression spine.

This remains read-only proof-to-use groundwork. It does **not** close a claim, accept a packet, publish a successor revision, integrate outputs, open an epoch, or prove replay.

## Integration evidence

Lane 02 exact tested implementation/workflow head:

`e191271859000f709c5e5dd280e4eac8164968d5`

Current-main merge candidate tested before integration:

`f310ab670aeee3995e80bc70c0c8f4938856e891`

Native Actions run `34764989703`, job `103744260751`, Python 3.12.14 directly observed:

- **189 tests ran / 189 passed**;
- 0 failures / 0 errors;
- ADV-040-A/B/C unchanged and green;
- ADV-039-A/B/C/D green;
- all normal evidence-subject tests green;
- ADV-035/036/037/038 green;
- wider deterministic identity/store/lifecycle baseline green;
- explicit production/test `py_compile` succeeded.

The final PR head `6bf6eda0cfaa97f592f85b69d45d52f97ef8c89d` added only the Lane 02 return-packet documentation beyond the exact tested implementation/workflow head.

## ADV-041 — preserved runtime-integrity finding, not a Stage 4 subject-binding blocker

Lane 03 PR #48 attacked Lane 02's repaired `NamedTuple` relation/result types by replacing their **class descriptors** at runtime. Exact tested merge candidate:

`b2c17a7bf462085b15e6bb0dc9a3412c2d72f800`

Native run `34765914599`, job `103746723073`, directly observed:

- **192 tests ran**;
- **189 passed**;
- exactly ADV-041-A/B/C failed;
- ADV-040, ADV-039, normal subject binding, and ADV-035/036/037/038 remained green;
- compile was skipped because unittest failed first.

The observation is real: arbitrary same-process Python code can replace class-level read descriptors and make existing operational wrappers report meaning different from their physical tuple storage while durable objects remain unchanged.

Decision 009 classifies that as a **runtime-integrity / isolation obligation**, not a requirement that v0 Python record classes be tamper-proof against arbitrary program mutation. The same authority capable of rewriting class descriptors can also rewrite resolver functions, store methods, parsers, or module globals; local container substitution cannot honestly prove hostile-interpreter resistance.

Canonical decision:

`coordination/decisions/009_RUNTIME_INTEGRITY_TRUST_BOUNDARY.md`

Bounded claim only: current v0 continuity is grounded in canonical immutable refs, canonical bytes, exact durable loading/reconstruction, and trusted deterministic kernel execution. No hostile same-process code-execution safety claim is made.

## Smallest next implementation lane

**Lane 02** owns the next bounded runtime step: a read-only **created-output compatibility preflight**.

Do not implement full packet acceptance. Start only with the already-demonstrated unambiguous contract case and fail closed on unresolved semantics.

Required bounded behavior:

1. reconstruct the exact packet/lane context from durable lifecycle relationships rather than trusting actor memory or mutable current state;
2. consume the canonical exact subject-binding result for packet-created artifacts and evidence;
3. for one created artifact, require its `type` to resolve to exactly one declared lane output entry;
4. require that output type to resolve to exactly one lane `evidence_requirements[]` entry;
5. initially support only an evidence requirement whose `required_states` contains exactly one state;
6. satisfy that bounded requirement only when at least one exact subject-bound evidence record has exactly that state;
7. expose/fail closed on zero or multiple output-contract matches, zero or multiple evidence-requirement matches, or multiple `required_states` rather than inventing array-order, hierarchy, conjunctive, or alternative semantics;
8. remain read-only and keep `artifacts_modified[]` fail-closed.

Do not infer that `automated_tested` implies `implemented`, that `runtime_tested` outranks another state, or that multiple required states are AND/OR/ordered. Those semantics are not yet grounded.

## Lane 03 next adversarial pass

After Lane 02 has an exact tested head, attack only that bounded compatibility preflight:

- duplicate lane output entries for one artifact type;
- duplicate evidence-requirement entries for one output type;
- multiple `required_states` accidentally treated as AND/OR/rank;
- exact subject-bound evidence for the wrong artifact or wrong state;
- unmatched passing evidence accidentally satisfying the created output;
- same-logical-id/different-exact lane or artifact substitution;
- array order, recency, mutable current/HEAD, occupant identity, or schedule order entering selection;
- ADV-035 through ADV-040 remaining green.

ADV-041 should remain preserved as runtime-integrity evidence. Do not turn it into an endless requirement to make trusted Python program objects immune to arbitrary monkeypatching.

## Root grounding

- **Truth:** exact subject binding is integrated only on the claims directly demonstrated; hostile-interpreter resistance is explicitly not claimed.
- **Agency / non-domination:** actor/process mutation authority is not silently converted into institutional truth authority; a future untrusted-code runtime needs explicit isolation/capability boundaries.
- **Continuity:** consequential relations remain reconstructable from durable exact state rather than private chat, recency, or process-local mutation.
- **Wisdom before speed:** advance only to a fail-closed single-state compatibility preflight while multiple-state and later lifecycle semantics remain unresolved.

## Still unresolved

Multiple `required_states` semantics, evidence quality/closure, exact artifact provenance base semantics (`ADV-002-C`), modified-artifact prior/result identity (`ADV-002-I`), occupancy/claim currentness/supersession/authorization, multiple-packet conflict semantics, historical schema reconstruction, durable closure, claim closure, successor revision publication, integration receipts/runtime, epochs/barriers, replay, cross-language reproduction, stronger filesystem durability/concurrency evidence, and hostile same-process code isolation remain explicit obligations.