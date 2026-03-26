# Note Formatting Guide

This guide documents the formatting conventions used across this notes repository. Follow it when writing any new note.

---

## 1. Document Structure

- One `# H1` title at the top — the only H1 in the file.
- Immediately after the title, write the opening content (usually a **Definition:** block or a brief introductory sentence). No H2 between the title and the first content block.
- Use `---` to separate the opening block from the rest of the sections.
- Use `## H2` for main sections, `### H3` for subsections, `#### H4` for deeper nesting.
- Always leave a blank line before and after headings, `---` separators, code blocks, and tables.
- No YAML front matter.

**Example opening structure:**

```
# Topic Title

**Definition:**
Short explanation of the concept here.

---

## First Section
```

---

## 2. File Naming

- Use `snake_case.md` — all lowercase, underscores between words, no spaces.
- Use a numeric prefix when files are part of a sequence: `01_topic.md`, `02_topic.md`.
- Place files inside a topic folder: `java/`, `python/`, `sql/`, `git/`, etc.
- Add a subtopic folder when needed: `python/oop/notes/`, `python/general/`.

---

## 3. Section Flow by Note Type

### Concept Notes
Follow this progression:

1. **Definition** — What is it?
2. **Purpose** — Why use it?
3. **Syntax / How** — How does it work?
4. **Example** — Working code block(s)
5. **Key Takeaways** — Bullet summary at the end (optional but common)

### Cheatsheet Notes
- Organize by workflow stage or functional category using numbered `## H2` headings.
- Each section has a brief one-line description, then a table.
- Table format: `Command | Function` or `Command | Description | Example`.

### Walkthrough / Tutorial Notes
- Use numbered `## H2` or `### H3` sections for each step.
- Embed code blocks inline with the instructions.
- No standalone Key Takeaways section needed.

---

## 4. Code Blocks

- Always specify the language tag: ` ```python`, ` ```java`, ` ```sql`, ` ```bash`, ` ```html`, etc.
- Precede every code block with an explanatory sentence or a label like **Example:** or **Syntax:**.
- Use inline comments inside the code to explain what's happening.
- Show expected output as a comment when it adds clarity: `// Output: Hello World` or `# Output: [1, 2, 3]`.
- For multi-file examples, add a comment at the top of each block: `// Car.java` or `# models.py`.

---

## 5. Lists

- Unordered lists: use `*` (asterisk).
- Ordered lists: use `1.`, `2.`, `3.`.
- Nested lists: indent with 4 spaces.
- Keep list items concise. For longer explanations, break out into a paragraph or labeled section instead.

---

## 6. Emphasis

| Element | When to use |
| :--- | :--- |
| **Bold** | Section labels (`**Definition:**`, `**Purpose:**`, `**Example:**`), important terms, method names, keywords |
| `Backticks` | Inline code, variable names, function names, filenames, command names |
| *Italics* | Rarely used; only for light emphasis (e.g., `*defining*` vs `*calling*`) |

---

## 7. Section Labels (Recurring Patterns)

Use these bold labels consistently to introduce specific content types:

- **Definition:** — opens the whole note or a major concept block
- **Purpose:** — explains why something is used, before showing how
- **Syntax:** — shows the general form before a concrete example
- **Example:** — precedes a code block demonstrating usage
- **Use Case:** — short phrase describing when to apply this pattern
- **Analogy:** — a one-line real-world comparison to make a concept stick (written as a bullet: `* **Analogy:** The Bouncer...`)
- **Critical Rule:** — highlights a hard constraint the reader must not miss
- **Key Takeaways** — H2 or H3 section at the end of concept notes; bullet list of main points

---

## 8. Tables

- Use pipe-style markdown tables for comparisons, references, and feature matrices.
- Always include a header row and a separator row.
- Left-align columns with `:---`.
- Use `✅` and `❌` for yes/no comparison tables (e.g., access modifier tables).
- Use `→` to show transitions or relationships inline.

**Example:**

```
| Modifier    | Description                      | Accessible From     |
| :---------- | :------------------------------- | :------------------ |
| `public`    | Accessible from anywhere.        | All classes         |
| `private`   | Accessible only within the class.| Inside class only   |
```

---

## 9. Spacing

- One blank line between paragraphs, list blocks, and code blocks.
- One blank line before and after a `---` separator.
- No more than two consecutive blank lines anywhere in the file.
- No trailing spaces at end of lines.
