# AXM Merge-Gate Boundary

This repository follows the AXM governance boundary below.

## 1. Inside AXM: the roots are the merge gate

For AXM's own internal evolution, **no person, founder, owner, steward, model, role, worker, or technical permission is the constitutional merge gate**.

The constitutional merge gate is the four roots:

1. **Truth**
2. **Agency / non-domination**
3. **Continuity**
4. **Wisdom before speed**

A proposed internal change may enter canonical AXM state only when its reasoning, evidence, consequences, and conflicts can be grounded against those roots strongly enough for the current state.

Technical ability to commit, merge, deploy, or execute work is an implementation permission. It is **not** canonical authority by itself.

If grounding is unresolved, preserve the uncertainty, dissent, or conflict instead of silently converting confidence, seniority, capability, ownership, or convenience into authority.

## 2. User-facing products: the user is the merge gate

For an AXM product used by a person, the **current user is the default product-level merge gate** for changes that affect that user's product state, data, preferences, workflow, outputs, or consequential actions.

The system may inspect, reason, draft, simulate, test, recommend, and prepare changes within the user's granted scope. It must not silently turn preparation into user approval.

The user may explicitly delegate bounded merge authority to automation or another intelligence, and may later change or revoke that delegation. Delegation must be represented as state rather than assumed from convenience or prior capability.

User-level merge authority does not grant authority over another actor's agency, and it does not silently rewrite AXM's four constitutional roots.

## 3. Boundary summary

```text
AXM internal canonical evolution
        -> merge gate = four roots

AXM user-facing product state
        -> merge gate = current user
        -> unless the user explicitly delegates a bounded scope

Git/CI/deploy permission
        -> execution mechanism only
        -> never constitutional authority by itself
```

## 4. Why this matters to Institution Fabric

A lane occupant may be highly capable and may have technical write access, but that does not make the occupant the institutional merge gate.

Inside AXM, lane outputs, integration decisions, institution changes, and canonical state transitions remain accountable to the roots. In a user-facing institution package, the user's product-level choices remain theirs unless explicitly delegated.

The Building should encode this distinction in machine-readable state rather than relying on social rank, hidden convention, or chat memory.
