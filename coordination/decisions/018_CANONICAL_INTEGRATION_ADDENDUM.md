# Decision 018 — Canonical Integration Addendum

Date: 2026-09-14
Status: **canonical on the demonstrated bounded Python v0 read-only surface**
Canonical implementation integration: `9ddcbff747a516dc1f1048cc71e5fc7dff43138a`

This addendum records the post-evidence disposition of `018_EXACT_REACHABLE_DEPENDENCY_FRONTIER_FACTS.md`. The original Decision 018 file remains the pre-integration contract and attack surface; this file records that its bounded factual projection has now passed implementation evidence, independent adversarial pressure, and Lane 01 four-root review.

## Canonical bounded meaning

For each exact packet output, the kernel may deterministically reconstruct the exact non-packet dependency declarations reachable through that output's exact packet-local prerequisite subgraph while preserving:

- exact declaring output identity;
- exact dependency target identity;
- exact Decision 015 claim-base membership fact;
- the nested Decision 017 reachability projection and its upstream exact context.

Same-packet targets remain outside this frontier projection. Repeated declaration of the same exact dependency by multiple reachable outputs preserves each declaring-output relation. Exact-ref lexical sorting is presentation only.

## Evidence accepted at integration

### Lane 02 implementation

- exact implementation/workflow head: `d9fa6488937b2e0b6916477ae8833ea0be11e3bd`;
- exact tested PR merge candidate: `6c3afb426fabad6fe1d4d9bff1daa30d3212cf8b`;
- native run/job: `34798702894` / `103836781621`;
- Python 3.12.14;
- **367 / 367 tests passed** in 538.478s;
- explicit compile succeeded;
- final Lane 02 commit `ef2ec35914a5e3847572cfca2d7f4f0590b05d95` added only its durable return packet after the exact tested implementation head.

PR #81 was squash-integrated as `9ddcbff747a516dc1f1048cc71e5fc7dff43138a`. The resulting canonical tree equals the final Lane 02 branch tree, so the tested production and baseline test content was not silently rewritten during integration.

### Lane 03 ADV-052

Lane 03's first adversarial run is preserved as red evidence: 379 tests ran, exactly ADV-052-A failed, and compile was skipped. Review showed the adversarial oracle had accidentally treated presentation tuple position as semantic authority while attacking ordering authority. Lane 03 corrected only that oracle; Decision 018 production code and authored schemas did not change.

Corrected evidence:

- exact corrected adversarial head: `61cb120dda523315ea58330adb7d7dbd362ca327`;
- original stacked merge candidate: `096af5a5bcb1c8716b3df27e5b8ebf0822dc7a53`;
- native run/job: `34799578083` / `103839341301`;
- **379 / 379 tests passed** in 403.563s;
- ADV-052-A through L all passed;
- explicit compile succeeded.

Because Decision 018 was squash-integrated, the original stacked PR #82 no longer represented a clean canonical-main diff. Lane 01 therefore reapplied only the exact corrected Lane 03 workflow/test evidence and durable return packet onto fresh canonical main instead of replaying duplicate Lane 02 production history.

Fresh canonical-main integration evidence:

- integration branch test-bearing head: `067f96e9ee79b09c08e8cf9e25bbca352dd31ad2`;
- exact PR merge candidate tested: `f89d31825f5a541694f6497719af642e0e58c81c`;
- run/job: `34801146677` / `103843914470`;
- Python 3.12.14;
- **379 / 379 tests passed** in 342.949s;
- ADV-052-A through L all passed;
- explicit compile including Decision 018 production, baseline tests, and ADV-052 succeeded;
- complete job succeeded.

Any later commits on that integration branch are coordination/documentation only unless separately evidenced.

## Four-root disposition

- **Truth:** Decision 018 is canonical only for the demonstrated factual frontier projection. The first red ADV-052 oracle run remains part of the evidence record rather than being erased. `in_claim_base` remains membership fact, not validity or trust.
- **Agency / non-domination:** no founder, specialist, branch owner, Git permission, logical id, version, `supersedes_ref`, recency, array order, output family, topological witness, scheduler position, or resolver convention gains hidden authority.
- **Continuity:** exact heads, merge candidates, run/job identities, preserved failure, bounded meaning, and unresolved semantics are all reconstructable from repository state and Actions evidence without private chat memory.
- **Wisdom before speed:** integration stops at reachable dependency-frontier facts. It does not jump into dependency policy, closure, acceptance, Stage 5 integration, epochs, or replay.

## Still not established

This canonicalization does **not** establish:

- dependency admissibility or allowed-context policy;
- dependency satisfaction;
- declaration completeness or dependency closure;
- actual execution chronology or scheduler order;
- source-provenance identity, quality, or closure;
- evidence quality, precedence, invalidation dominance, or closure;
- packet acceptance/rejection;
- claim closure;
- successor state-revision publication;
- Stage 5 integration correctness;
- epochs/barriers;
- replay correctness;
- supported cross-language frontier transport;
- exact self/mutual-cycle authorability through the ordinary content-addressed artifact publication path.

Decision 019 therefore opens only source-provenance taxonomy research. It does not convert any unresolved item above into policy or implementation authority.
