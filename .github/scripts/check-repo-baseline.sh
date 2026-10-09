#!/usr/bin/env bash
# Reports repositories whose settings do not match REPOSITORY_BASELINE.md.
#
# Read-only on purpose: GitHub applies nothing at repository creation, so the
# gap this closes is "nobody noticed", not "nobody could fix it". Applying a
# correction is a maintainer action, with the commands the baseline page gives.
#
# Usage: check-repo-baseline.sh [repo ...]   (no argument: every repository)
# Exit 0 everything matches, 1 a deviation was found, 2 the check could not run.

set -uo pipefail

ORG=${ORG:-markup-carve}

command -v gh >/dev/null || { echo "gh is not on PATH" >&2; exit 2; }

# The settings the baseline page pins, as field:expected.
EXPECTED=(
  default_branch:main
  delete_branch_on_merge:true
  allow_squash_merge:true
  allow_merge_commit:false
  allow_rebase_merge:false
  allow_auto_merge:true
  allow_update_branch:true
  has_projects:false
  web_commit_signoff_required:false
)

# The kind and area labels every repository carries. Keep in step with the
# autopilot skill's taxonomy, which is what creates them.
LABELS=(
  bug enhancement chore documentation
  area:parser area:renderer area:importer area:ast area:cli area:grammar
  area:lsp area:editor area:corpus area:spec area:docs area:tooling
)

deviations=0

note() {
  printf '%s: %s\n' "$1" "$2"
  deviations=$((deviations + 1))
}

check_repo() {
  local repo=$1 settings pair field want got branch labels label

  # One request for every pinned field, as `field<TAB>value` lines.
  settings=$(gh api "repos/$ORG/$repo" \
    --jq 'to_entries[] | select(.value != null) | "\(.key)\t\(.value)"' 2>/dev/null) || {
    note "$repo" 'could not be read'
    return
  }

  for pair in "${EXPECTED[@]}"; do
    field=${pair%%:*}
    want=${pair#*:}
    got=$(printf '%s\n' "$settings" | awk -F'\t' -v f="$field" '$1 == f { print $2; exit }')
    [ -n "$got" ] || got='(absent)'
    [ "$got" = "$want" ] || note "$repo" "$field is $got, baseline is $want"
  done

  branch=$(printf '%s\n' "$settings" | awk -F'\t' '$1 == "default_branch" { print $2; exit }')
  branch=${branch:-main}

  if ! gh api "repos/$ORG/$repo/branches/$branch/protection" \
    --jq 'if .required_status_checks == null then "unchecked" else "ok" end' 2>/dev/null |
    grep -qx ok; then
    note "$repo" "$branch protection is missing or requires no status checks"
  fi

  labels=$(gh api "repos/$ORG/$repo/labels?per_page=100" --paginate --jq '.[].name' 2>/dev/null)
  for label in "${LABELS[@]}"; do
    printf '%s\n' "$labels" | grep -qxF -- "$label" || note "$repo" "label $label is missing"
  done
}

repos=("$@")
if [ ${#repos[@]} -eq 0 ]; then
  mapfile -t repos < <(gh api "orgs/$ORG/repos?per_page=100&type=all" --paginate --jq '.[].name' | sort)
  [ ${#repos[@]} -gt 0 ] || { echo "no repositories returned for $ORG" >&2; exit 2; }
fi

for repo in "${repos[@]}"; do
  check_repo "$repo"
done

if [ "$deviations" -eq 0 ]; then
  printf 'baseline: all %d checked repositories match\n' "${#repos[@]}"
  exit 0
fi

printf '\n%d deviation(s). REPOSITORY_BASELINE.md has the commands that correct them.\n' "$deviations"
exit 1
