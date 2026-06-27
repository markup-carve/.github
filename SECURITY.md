# Security Policy

## Supported Versions

Only the latest released version of each Carve implementation receives security fixes.

| Version | Supported |
|---------|-----------|
| 0.1.x (latest) | Yes |
| Earlier | No |

## What Is in Scope

Carve's normative security model is defined in grammar **PART 9 §25** (URL-scheme hardening, attribute-name filtering) and **§26** (Trojan-Source / bidi-control / zero-width-character handling). Reports covering the following are treated as security issues:

- **Parser DoS / panic** - inputs that cause a crash, stack overflow, excessive memory use, or unbounded CPU time in any conformant parser (carve-js, carve-rs, carve-php, or bindings).
- **XSS via rendered HTML** - any input that causes a conformant renderer to emit executable script in its default or safe-mode output, including via raw-HTML pass-through, round-trip converters (`DjotToCarve`, `MarkdownToCarve`, `HtmlToCarve`), or attribute injection.
- **URL scheme-denylist bypass** - inputs that smuggle a `javascript:`, `data:`, `vbscript:`, or other non-safelisted scheme past the §25 URL filter into an `href` or `src` attribute.
- **Trojan-Source / homoglyph attacks** - inputs containing bidi-control characters or zero-width characters in identifiers, link targets, or visible text that a §26-conformant implementation should strip or reject but does not.
- **Safe-mode bypass** - any technique that defeats the `safe: true` / `--no-raw-html` flag to emit raw HTML or execute script.

**Out of scope:** issues that require the caller to have explicitly disabled safe-mode and passed attacker-controlled input without sanitization (this is documented as the caller's responsibility), rendering bugs with no security impact, and theoretical issues without a concrete proof-of-concept input.

## How to Report

**Do not open a public issue for a security vulnerability.**

1. Go to the GitHub repository where you found the issue (e.g., `markup-carve/carve-js`, `markup-carve/carve-php`, `markup-carve/carve-rs`).
2. Click **Security** -> **Advisories** -> **Report a vulnerability** to open a private GitHub Security Advisory (GHSA). This keeps details confidential until a fix is ready.
3. If you are unsure which repo to target, open the GHSA on [`markup-carve/carve`](https://github.com/markup-carve/carve/security/advisories/new) (the spec repo) and describe which implementation is affected.

Alternatively, email the maintainer directly: **dereuromark@gmail.com** - include "Carve Security" in the subject line.

## What to Expect

- **Acknowledgment** within 48 hours of receipt.
- **Triage and initial assessment** within 7 days.
- **Fix or mitigation** coordinated privately; all affected implementations are patched together before public disclosure.
- Credit in the release notes (unless you prefer to remain anonymous).

## Notes on Raw HTML and Safe Mode

Carve implementations expose a `safe` / `--no-raw-html` flag. When this flag is off (the default in most library integrations), raw HTML in the source document passes through to the output. Passing attacker-controlled Carve source through a renderer with `safe: false` is the caller's responsibility - it is equivalent to serving user HTML directly. The spec's security defaults are designed so that **safe-mode-on is the safe default for untrusted input**, and no XSS should be possible even with raw HTML off when the §25/§26 rules are enforced.
