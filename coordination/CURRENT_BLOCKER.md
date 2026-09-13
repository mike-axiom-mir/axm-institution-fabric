# Current Stage 4 Sequencing Overlay

Date: 2026-09-13
Canonical main after this activation's Decision 013 integration: `be9a59786af663d7fd8ef58dc0471e447672794b`
Current stage: **Stage 4 — claim / occupancy / return lifecycle**
Current next bounded gate: **Decision 014 — Exact Output Dependency Identity**

`coordination/CURRENT_WAVE.md` remains historical chronology. This file is the newer current-state overlay and must be read together with the numbered decisions and specialist return packets.

## What is now canonical

The deterministic institution kernel now canonically demonstrates, on the bounded Python v0 path:

- strict canonical identity and immutable references;
- exact revision membership and exact lifecycle bases;
- occupancy admission, work-claim admission, and return-packet admission from exact historical state;
- exact packet created-artifact / evidence identity;
- Decision 008 exact evidence-subject chronology;
- Decision 009 trusted-runtime boundary without claiming hostile same-process isolation;
- Decision 010 exact created-artifact work-base provenance;
- Decision 011 exact two-sided modified-artifact prior/result identity;
- Decision 012 exact modification-result output/evidence compatibility;
- Decision 013 one read-only mixed created+modified packet compatibility projection from one exact packet/claim/base/occupancy/lane context;
- ADV-035 through ADV-046 regression pressure preserving proof-to-use identity, fail-closed transport/materialization behavior, historical-contract boundaries, exact evidence subjects, exact provenance, two-sided modification identity, compatibility isolation, and mixed-projection non-acceptance semantics.

Decision 013 remains deliberately narrow. Per-output `satisfied` facts are compatibility observations only; they are not packet acceptance, evidence closure, claim closure, successor-state publication, integration, epochs, or replay.

## Decision 013 integration evidence

### Lane 02 PR #60 — production implementation

PR #60 was integrated as canonical commit:

`dedb6017244ee2061353435de070c2c33d1de687`

Lane 02 preserved its first failed implementation run rather than rewriting it: 259 tests reached the new surface with 6 implementation errors and compile was skipped. The repaired implementation was then directly observed green at 259/259 with explicit compile success.

### Lane 03 ADV-046 — independent adversarial evidence

Lane 03 PR #61 remained evidence/test-only. Its final head:

`90c0137e7359aa59f9f8737e664b5adff5d85562`

proved the ADV-046 A–F surface: historical lane recency cannot rebind either output family; high-version/`supersedes_ref` same-logical decoys stay exact-separated; evidence order cannot erase conflicts/unmatched evidence; detached materialization cannot mutate exact operational facts; unsupported ordinary JSON transport fails closed; and component compatibility does not become packet acceptance/rejection.

Because PR #60 was squash-merged, retargeting stacked PR #61 to `main` exposed already-canonical production commits again. Lane 01 therefore preserved PR #61 unchanged and reapplied only its evidence files on fresh canonical main in PR #62.

PR #62 head:

`3a36573a8f7dd8baa644f6fcf2cb93b06953b154`

had tree:

`1918932be7c23235afe1730a21a47ead9aa11fc2`

which is byte-for-byte the same tree as Lane 03 final head `90c0137...`. Fresh native Actions then independently completed on PR #62 merge candidate `f9987a3c0cf4dafbec2be86e6a187149b8661fdd`:

- Python 3.12.14;
- **265 / 265 tests passed** in 296.738s;
- ADV-046-A/B/C/D/E/F all green;
- explicit `py_compile`, including the ADV-046 regression file, passed;
- job conclusion: success.

PR #62 was integrated as:

`be9a59786af663d7fd8ef58dc0471e447672794b`

PR #61 was then closed as superseded, not invalidated; its stacked evidence history remains preserved.

## Why Stage 4 is not done

Mixed output compatibility still does not establish the exact identity or validity of declared artifact dependencies. Current artifact v0.1/v0.2 contracts accept `dependency_refs[]` as arbitrary non-empty strings. The historical valid fixture uses `schemas/lane.schema.json`, proving old dependency strings may be path-like and therefore must not be silently reinterpreted as immutable institutional refs. Artifact v0.2 exacted the work-base provenance ref but did not change dependency semantics.

That is now the smallest mechanical continuity gap that can be advanced without inventing evidence precedence, lineage policy, source taxonomy, packet acceptance, or integration semantics.

## Decision 014 — opened next

See:

`coordination/decisions/014_EXACT_OUTPUT_DEPENDENCY_IDENTITY.md`

Decision 014 opens **dependency target identity only**:

- artifact v0.3 will give non-empty `dependency_refs[]` an explicit canonical exact `artifact`-ref meaning;
- every such ref must parse through the shared Stage 2 immutable-reference grammar and exact-load to the same artifact identity;
- historical v0.1/v0.2 non-empty dependency strings remain operationally unresolved, even when exact-looking;
- empty historical dependency arrays may continue because they assert no dependency target on this surface;
- Decision 013 remains the packet/output context authority;
- no base-membership rule, same-packet dependency rule, chronology, transitive closure, cycle policy, completeness claim, or packet acceptance meaning is introduced;
- `provenance.source_refs[]`, `evidence_refs[]`, `content_ref`, `version`, and `supersedes_ref` gain no dependency authority.

## Lane boundaries

### Lane 02 — next implementation lane

Implement only Decision 014's read-only exact output dependency identity preflight:

1. add artifact v0.3 without changing v0.1/v0.2 meaning;
2. require v0.3 dependency entries to be canonical exact artifact refs;
3. consume Decision 013's exact packet/output context;
4. exact-load each dependency and preserve exact ref/value pairing;
5. fail closed on non-empty historical v0.1/v0.2 dependency arrays;
6. preserve created-only, modified-only, and mixed behavior;
7. keep ADV-035 through ADV-046 green;
8. stop before membership/chronology/closure, source closure, evidence precedence, lineage, packet acceptance, claim closure, successor publication, Stage 5 integration, epochs, or replay.

### Lane 03 — next adversarial lane

After Lane 02 leaves an exact tested head, attack only the Decision 014 surface for historical exact-looking-string laundering, path/logical fallback, wrong-kind refs, missing/corrupt targets, same-logical/different-exact substitution, order/version/`supersedes_ref` authority, source/evidence refs being mistaken for dependencies, output-family divergence, materialization/transport drift, and accidental dependency-closure or packet-acceptance claims.

### Lane 01 — integration lane

Do not implement Decision 014 in parallel with Lane 02. Review the exact tested implementation and Lane 03 evidence, preserve failures, and integrate only if the four-root gate is grounded.

## Still explicitly unresolved

- artifact dependency membership, chronology, completeness, transitive closure, and cycles;
- exact source provenance / `provenance.source_refs[]` taxonomy and closure;
- evidence method/source quality, precedence, invalidation dominance, and closure;
- multiple `required_states` semantics;
- logical lineage and `supersedes_ref` validity for modifications;
- global occupancy/claim currentness, supersession, and authorization;
- multiple-packet conflict/selection semantics;
- packet acceptance/rejection and durable closure;
- claim closure;
- successor state-revision publication;
- Stage 5 integration receipts/runtime;
- epochs/barriers and replay;
- cross-language reproduction and supported serialized compatibility transport;
- stronger filesystem durability/concurrency evidence;
- hostile same-process code isolation beyond Decision 009's declared trusted deterministic runtime boundary.

## Four-root gate

- **Truth:** failed runs and historical schema meanings remain visible; no arbitrary dependency string is promoted to exact identity by resemblance.
- **Agency / non-domination:** neither founder status, specialist identity, scheduler position, Git permission, recency, order, nor version metadata gains dependency standing.
- **Continuity:** the next proof requires dependency targets to become reconstructable from durable exact refs rather than mutable names or private intent.
- **Wisdom before speed:** dependency identity is opened before dependency closure, acceptance, immutable integration, epochs, or replay.
