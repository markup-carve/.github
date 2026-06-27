# Contributing to Carve

Thanks for contributing. Carve is a multi-repo project - this page covers the common workflow across all repos.

## Where to File Issues

| Type | Target repo |
|------|-------------|
| Language spec, grammar, or design | [`markup-carve/carve`](https://github.com/markup-carve/carve) |
| Bug in the TypeScript parser / renderer | [`markup-carve/carve-js`](https://github.com/markup-carve/carve-js) |
| Bug in the Rust parser / renderer / CLI | [`markup-carve/carve-rs`](https://github.com/markup-carve/carve-rs) |
| Bug in the PHP parser / renderer | [`markup-carve/carve-php`](https://github.com/markup-carve/carve-php) |
| Bug in a binding (carve-py, carve-rb, carve-go, carve-wasm) | that binding's repo |
| Editor plugin | the relevant plugin repo |

When in doubt, open the issue in `markup-carve/carve` and it will be redirected.

## The Spec-First / Lockstep Workflow

Carve keeps all implementations in sync with the spec. Before a behavioral change lands anywhere:

1. **Spec first** - the grammar and conformance corpus in `markup-carve/carve` define the authoritative behavior. Changes to parser behavior that are not covered by the corpus need a corpus addition.
2. **Reference oracle** - `carve-js` is the reference implementation. Its output is what the corpus tests are verified against. If `carve-js` and the corpus disagree, the corpus wins.
3. **Lockstep** - after a spec change, the same behavior ships to `carve-rs` and `carve-php` in the same release cycle. PRs that change behavior in one impl without matching PRs (or at least issues) in the others are generally held until parity can be confirmed.

For pure bug fixes that are unambiguously wrong vs. the existing spec, you can fix directly in the relevant impl repo and note "spec already covers this" in the PR.

## Running Tests

### carve-js (TypeScript)
```sh
npm install
npm test
```
The conformance test runner is `tests/conformance.test.ts` and reads the corpus from the `tests/spec` submodule.

### carve-rs (Rust)
```sh
cargo test
cargo run -- --help
```
Conformance tests: `cargo test conformance`.

### carve-php (PHP)
```sh
composer install
vendor/bin/phpunit
```

### Bindings (carve-py, carve-rb, carve-go, carve-wasm)
See the individual repo README for build and test instructions - each binding wraps carve-rs and has its own build toolchain.

## Conformance Corpus

The `tests/spec` submodule in each implementation repo points to a commit of `markup-carve/carve` that contains the corpus at `tests/`. When you add or change behavior:

- Add a corpus case (or update the expected output) in a PR to `markup-carve/carve`.
- Bump the submodule pointer in the impl repo to include the new corpus case.
- PRs that change parser output without a matching corpus update will be asked to add one.

## Commit and PR Guidelines

- One logical change per commit. Descriptive subject line, imperative mood ("Fix fence-in-list parser edge case").
- No "Co-authored-by" or AI-tool signature lines.
- No issue/PR references in the commit message body - put those in the PR description.
- No `@mention` tokens outside fenced code blocks in PR titles, bodies, or commit messages (GitHub auto-notifies real users).
- American English in identifiers, comments, and documentation.

## Code Style

Each repo has its own linter/formatter config:

- **carve-js**: ESLint + Prettier (`npm run lint`, `npm run format`)
- **carve-rs**: `rustfmt` + Clippy (`cargo fmt`, `cargo clippy`)
- **carve-php**: PHP_CodeSniffer + PHPStan (`vendor/bin/phpcs`, `vendor/bin/phpstan analyse`)

Please run the appropriate formatter before opening a PR. CI will catch violations, but it is faster to fix locally.

## Security Issues

See [SECURITY.md](SECURITY.md). Do not open public issues for vulnerabilities.
