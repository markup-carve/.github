<h1 align="center">markup-carve</h1>

<p align="center">
  <em>Markup that respects humans and parsers.</em>
</p>

---

### Why

- **Visual mnemonics** — syntax resembles its output (`/italic/`, `*bold*`, `_underline_`, `~strike~`)
- **One way to do things** — no ambiguity, no redundant syntax
- **Learnable in 5 seconds, memorable after 5 days** — designed around how non-technical users actually mark up text
- **No expressive blind spots** — every output is achievable without workarounds
- **Linear parsing** — no backtracking, no forward references

### Projects

**Language**

| Project | Description |
|---|---|
| [**carve**](https://github.com/markup-carve/carve) | Language definition, design rationale, and quick reference. [Docs →](https://markup-carve.github.io/carve/) |

**Implementations**

| Project | Description |
|---|---|
| [**carve-js**](https://github.com/markup-carve/carve-js) | Reference TypeScript implementation. |
| [**carve-rs**](https://github.com/markup-carve/carve-rs) | Rust parser and HTML renderer with a `carve` CLI; passes the spec corpus. |
| [**carve-php**](https://github.com/markup-carve/carve-php) | PHP parser, forked from djot-php — syntax migration in progress. *Alpha.* |
| [**carve-wasm**](https://github.com/markup-carve/carve-wasm) | WASM bindings for carve-rs. *Early.* |

**Editor support**

| Project | Description |
|---|---|
| [**vscode-carve**](https://github.com/markup-carve/vscode-carve) | VS Code extension — syntax highlighting, snippets, live preview. |
| [**zed-carve**](https://github.com/markup-carve/zed-carve) | Zed editor support. |
| [**tree-sitter-carve**](https://github.com/markup-carve/tree-sitter-carve) | Tree-sitter grammar (highlighting, structural editing). |
| [**carve-lsp**](https://github.com/markup-carve/carve-lsp) | Language server — syntax diagnostics. *Early.* |

**Integrations**

| Project | Description |
|---|---|
| [**wp-carve**](https://github.com/markup-carve/wp-carve) | WordPress plugin (carve-php engine) — live preview, paste, REST API. |
| [**carve-grammars**](https://github.com/markup-carve/carve-grammars) | Tiptap editor kit and Carve serializer. |
| [**vite-plugin-carve**](https://github.com/markup-carve/vite-plugin-carve) | Vite plugin — import `.carve` documents as rendered HTML. *Early.* |

**Resources**

| Project | Description |
|---|---|
| [**awesome-carve**](https://github.com/markup-carve/awesome-carve) | Curated list of Carve tools, libraries, and resources. |

### A taste

```
# Heading

/italic/  *bold*  _underline_  ~strike~  ==highlight==

![Photo](img.jpg)
^ Figure 1: caption attaches to the image above

|= Name  |= Role     |
| Ada    | Author    |
| Linus  | Reviewer  |
^ Table caption
```

### Get involved

Issues, ideas, and PRs welcome on any project repo.
Browse [awesome-carve](https://github.com/markup-carve/awesome-carve) for tools and integrations.
