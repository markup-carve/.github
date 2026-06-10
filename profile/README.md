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
| [**carve-php**](https://github.com/markup-carve/carve-php) | PHP parser and HTML renderer, with converters from Markdown, HTML, BBCode, and Djot. |
| [**carve-wasm**](https://github.com/markup-carve/carve-wasm) | WASM bindings for carve-rs. *Early.* |

**Editor support**

| Project | Description |
|---|---|
| [**intellij-carve**](https://github.com/markup-carve/intellij-carve) | JetBrains IDEs (IntelliJ, PhpStorm, WebStorm, ...): highlighting, live preview, HTML export. |
| [**vscode-carve**](https://github.com/markup-carve/vscode-carve) | VS Code extension — syntax highlighting, snippets, live preview. |
| [**zed-carve**](https://github.com/markup-carve/zed-carve) | Zed editor support. |
| [**tree-sitter-carve**](https://github.com/markup-carve/tree-sitter-carve) | Tree-sitter grammar (highlighting, structural editing). |
| [**carve-lsp**](https://github.com/markup-carve/carve-lsp) | Language server: diagnostics, completion, hover, rename, folding, formatting, and semantic tokens. |

These provide **source-mode** editing: you write Carve markup and get highlighting,
snippets, and a rendered preview side by side.

**Integrations**

| Project | Description |
|---|---|
| [**carve-grammars**](https://github.com/markup-carve/carve-grammars) | **WYSIWYG** rich-text editing via Tiptap / ProseMirror, with a Carve serializer for **roundtripping** (Carve &harr; rich text &harr; Carve). Also ships **Prism** and **highlight.js** grammars for web syntax highlighting. |
| [**wp-carve**](https://github.com/markup-carve/wp-carve) | WordPress plugin (carve-php engine) — live preview, paste, REST API. |
| [**vite-plugin-carve**](https://github.com/markup-carve/vite-plugin-carve) | Vite plugin — import `.carve` documents as rendered HTML. *Early.* |

**WYSIWYG vs source editing:** the editor plugins above edit Carve *source* with a
read-only preview. For *WYSIWYG* (edit the rendered document directly), use
[**carve-grammars**](https://github.com/markup-carve/carve-grammars) — its Tiptap
kit edits rich text and its serializer **roundtrips** that content back to Carve
source. (carve-js also ships Markdown/Djot → Carve migration helpers for one-way
conversion.)

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
