# Decision 009 — Runtime Integrity Trust Boundary for v0 Proof-to-Use

Status: accepted Stage 4 scope boundary

## Context

The Stage 4 packet-output/evidence work intentionally hardened ordinary proof-to-use drift after exact durable verification. ADV-035 through ADV-040 demonstrated concrete ways returned Python values or relation wrappers could drift through ordinary mutation surfaces, builtin container mutators, transport/materialization behavior, or direct instance reassignment. Those failures were repaired while preserving the durable exact-ref model.

Lane 03 then demonstrated ADV-041 against Lane 02's repaired `NamedTuple` relation/result records. In one Python process, code can replace the user-defined class descriptors for `.reference`, `.value`, or `.evidence_records`. Existing tuple storage and durable objects remain unchanged, but public attribute reads can be made to report different meaning.

Native evidence on PR #48, exact tested merge candidate `b2c17a7bf462085b15e6bb0dc9a3412c2d72f800`, run `34765914599`, job `103746723073`, directly observed 192 tests with 189 passing and exactly ADV-041-A/B/C failing. ADV-040, ADV-039, normal subject binding, and ADV-035/036/037/038 remained green. Compile was not reached after the failing unittest gate.

## Boundary discovered

ADV-041 is a real observation, but it crosses from **data/result immutability** into **arbitrary same-process code/interpreter mutation**.

If an actor can freely rewrite class descriptors in the trusted kernel process, the same authority can also rewrite module globals, resolver functions, store methods, parsers, or verification code. No local substitution of one Python record/container type for another can truthfully establish general tamper resistance against arbitrary code mutation in that same interpreter.

The v0 institution proof does not claim a hostile-code sandbox. Its current target is deterministic institutional continuity from explicit durable state under the repository's kernel implementation and deterministic fixture occupants.

## Decision

### A. Canonical truth remains durable exact state

For v0, the authoritative continuity surface is:

- canonical immutable references;
- canonical bytes / content identity;
- exact object-store loading and validation;
- explicit lifecycle relationships reconstructed from durable state;
- deterministic kernel code executed within its declared runtime boundary.

Returned Python projections are operational read models. They must not silently drift through ordinary supported data mutation paths, but they are **not** claimed to be tamper-proof against arbitrary mutation of the Python program itself.

### B. ADV-041 is preserved, not erased

ADV-041 remains valid evidence that a long-lived Python process can be made to misreport an already-resolved relation if arbitrary code is allowed to mutate kernel class descriptors.

That evidence is classified as a **runtime-integrity / isolation obligation**, not as a blocker to the bounded exact evidence-subject resolver itself.

No claim is made that the current kernel is safe against malicious same-process code execution.

### C. Consequential consumers must keep the authority boundary explicit

Later compatibility/integration consumers must derive consequential decisions from durable exact refs and reconstructed canonical state, not from hidden recency, actor memory, or mutable ambient process state.

When a future deployment permits untrusted code or model-generated code to execute with arbitrary mutation authority inside the same process, the appropriate control is a grounded runtime boundary such as process isolation, capability restriction, or re-verification in a separately trusted kernel context. That concern must not be disguised as a stronger Python tuple/container guarantee.

### D. Scope of proof-to-use regressions

ADV-035 through ADV-040 remain permanent regression evidence for ordinary operational-value continuity because those attacks exercised returned data/object mutation and transport surfaces without redefining the kernel program itself.

ADV-041 remains a preserved adversarial witness for the future runtime-integrity/isolation layer. It is not promoted into a requirement that every v0 Python class, function, or module object resist arbitrary monkeypatching.

This boundary may be revisited if later evidence shows that same-process untrusted code is part of the intended execution model.

## Integration consequence

PR #45 may be integrated on its demonstrated bounded claims:

- exact evidence `subject_ref` parsing through the shared immutable-ref grammar;
- exact evidence-to-created-artifact binding;
- explicit unmatched evidence;
- wrong-kind exact subject fail-closed behavior;
- `artifact.evidence_refs` non-authority for Decision 008 chronology;
- `artifacts_modified` fail-closed behavior;
- preserved ADV-035 through ADV-040 regressions.

The integration must not be described as proof of hostile-interpreter tamper resistance.

## Smallest next gate

With exact subject binding canonical, the next Stage 4 step is a **read-only created-output compatibility preflight**, deliberately narrower than full packet acceptance.

Until the contract semantics are further grounded, the first implementation should fail closed when it encounters ambiguity rather than invent policy. In particular, it may support the demonstrated simple case where:

- one created artifact type resolves to exactly one declared lane output contract;
- that output resolves to exactly one evidence-requirement entry;
- that entry contains exactly one `required_states` value;
- at least one exact subject-bound evidence record has exactly that state.

It must not infer a hierarchy among evidence states, guess conjunctive/alternative meaning for multiple `required_states`, choose among duplicate output/evidence requirement entries by array order, or open modified-artifact, claim-closure, successor-revision, integration, epoch, or replay semantics.

## Root grounding

### Truth

Do not claim tamper resistance the implementation cannot provide. Preserve ADV-041 as evidence while keeping the actual Stage 4 guarantee bounded to exact durable state plus trusted deterministic kernel execution.

### Agency / non-domination

Process-level mutation authority must not silently become institutional truth authority. If untrusted occupants later receive such execution power, isolate or constrain it explicitly rather than pretending a container type removes that authority.

### Continuity

A replacement occupant can reconstruct exact subject relationships from durable refs and canonical storage without inheriting private chat or process-local monkeypatches. Durable reconstruction, not a particular Python wrapper, is the continuity anchor.

### Wisdom before speed

Stop the unbounded data-structure hardening loop at the point where the remaining attack requires rewriting trusted program semantics. Record the boundary honestly and continue the v0 institutional proof without silently claiming a security property outside its current scope.

## Still unresolved

This decision does not resolve evidence-state-set semantics, evidence quality, exact artifact provenance base semantics, modified-artifact prior/result identity, currentness/supersession/authorization, multiple-packet conflicts, historical schema reconstruction, durable closure, claim closure, successor revision publication, integration receipts/runtime, epochs/barriers, replay, cross-language reproduction, or hostile-runtime isolation.