# Temporal holdout release protocol · ARIS4C013

## Purpose

The 1997–2005 temporal holdout must remain inaccessible to the analysis pipeline until discovery is frozen.

The repository enforces this with a two-step release.

## Default state

HOLDOUT_RELEASE.json has released = false.

HOLDOUT_RELEASE_DECISION.json has authorized = false.

The holdout runner validates the gate before opening any data archive. In the default repository state it exits before reading holdout bytes.

## Step 1 · freeze discovery

Run only the locked 1988–1996 Pilot 1 v2.

Commit:

- discovery JSON result;
- discovery Markdown report;
- any frozen, clearly labeled discovery-only diagnostics.

Do not inspect 1997–2005.

Record:

- discovery result repository path;
- Git blob SHA of the JSON result;
- discovery commit SHA;
- current Pilot 1 lock blob SHA.

## Step 2 · separate release-decision commit

In a later commit, change HOLDOUT_RELEASE_DECISION.json to:

- authorized = true;
- pilot1_lock_version = v2;
- exact lock blob SHA;
- exact discovery-result blob SHA;
- discovery years = [1988, 1996];
- holdout years = [1997, 2005].

This commit is the explicit scientific decision that discovery is finished.

The gate requires the discovery commit to be an ancestor of this release-decision commit.

## Step 3 · release manifest commit

Only after Step 2, update HOLDOUT_RELEASE.json:

- released = true;
- discovery_result_path;
- discovery_result_blob_sha;
- discovery_commit_sha;
- release_decision_commit_sha.

This is a separate later commit because a commit cannot reliably contain its own SHA.

## Mechanical checks before data access

The gate refuses release unless all are true:

- spec version is v2;
- years remain 1988–1996 / 1997–2005;
- current Pilot 1 lock blob equals the frozen blob;
- discovery result is a tracked file;
- discovery result blob equals the manifest;
- discovery commit contains that exact result blob;
- discovery commit is an ancestor of release-decision commit;
- both commits are ancestors of current HEAD;
- release-decision record at that commit says authorized = true;
- decision record binds the same lock and discovery blobs.

Only then may the holdout script open the NUMIDENT zip files.

## Outcome discipline

After release:

- run the holdout once under the frozen primary specification;
- commit the complete output;
- do not replace the primary result with a sensitivity analysis;
- additional analyses are labeled post-holdout exploratory.
