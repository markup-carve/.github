# Repository baseline

Every repository in this organization is expected to carry the same merge
behavior, the same branch protection on `main`, and the same label taxonomy.
GitHub applies none of this at repository creation, so a new repository can
take its first merge unconfigured and leave a branch behind.

This page is the contract. `.github/scripts/check-repo-baseline.sh` reads it
back from the API and reports anything that does not match.

## The settings

| Setting | Value | Why |
|---|---|---|
| `delete_branch_on_merge` | `true` | A merged branch is finished work. Without this, every merge leaves debris behind. |
| `allow_squash_merge` | `true` | One commit per pull request keeps `main` readable and keeps the changelog derivable from it. |
| `allow_merge_commit` | `false` | A merge commit on `main` breaks the one-commit-per-pull-request shape. |
| `allow_rebase_merge` | `false` | Same reason. |
| `allow_auto_merge` | `true` | Arming auto-merge is how a pull request lands on its own checks rather than on someone watching them. |
| `allow_update_branch` | `true` | Lets a behind branch take the base without a local round trip. |
| `has_projects` | `false` | Tickets are tracked in issues; a per-repository project board is a second place to look. |
| `web_commit_signoff_required` | `false` | No DCO flow in this organization. |

`has_wiki` is deliberately absent: it is on in most repositories and off in a
few, and nothing depends on either state.

## Branch protection on `main`

Required status checks, and nothing else: no required reviews, and
administrators are not included. A single maintainer cannot satisfy a review
requirement, and including administrators would block the admin merge that
clears a behind-but-green pull request.

## Labels

Every repository carries the full kind and area taxonomy, because a ticket is
labeled at creation and an area label that does not exist cannot be applied.
The taxonomy and its colors live in the autopilot skill, which creates any
missing label:

```bash
~/.claude/skills/autopilot/scripts/autopilot-gh.sh labels-sync markup-carve/<repo>
```

It is idempotent, so running it on a configured repository changes nothing.

## Applying it to a new repository

Run both of these as the last step of creating a repository, before the first
pull request:

```bash
repo=markup-carve/<repo>

gh api "repos/$repo" -X PATCH \
  -F delete_branch_on_merge=true \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=false \
  -F allow_auto_merge=true \
  -F allow_update_branch=true \
  -F has_projects=false \
  -F web_commit_signoff_required=false

~/.claude/skills/autopilot/scripts/autopilot-gh.sh labels-sync "$repo"
```

Branch protection needs the repository to have a `main` with at least one
commit, and the required check names differ per repository, so it is set once
the first workflow exists rather than from a template.

## Verifying

```bash
.github/scripts/check-repo-baseline.sh             # every repository
.github/scripts/check-repo-baseline.sh carve-js    # one repository
```

It writes one line per deviation and exits non-zero when it finds any. It
changes nothing: applying a correction is a maintainer action, with the
commands above.

## What this does not cover

Environment protection rules and their reviewers are per repository and are
set by the maintainer. Release workflows gate on an environment approval, and
an organization-wide default would either weaken a gate that matters or add
one where no release exists.

`automation/bump-spec` is a persistent shared branch that the bump bot
force-pushes for each new pull request. It survives on purpose. A branch sweep
must skip it.
