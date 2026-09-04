---
name: note-writing
description: Write or revise technical learning notes in the user's clean, personal, conversational voice. Use for Markdown study notes, concept explanations, walkthroughs, and cheatsheets; do not use for formal product documentation unless the user asks for this note style.
---

# Personal Note-Writing Contract

Write notes like a learner explaining a concept to their future self. The result should feel personal, practical, and easy to return to later—not like copied documentation or a corporate reference manual.

## Voice

* Use plain, direct language and explain one idea at a time.
* Sound conversational but clear. Natural phrases such as “let's say,” “you can,” and “I like to think of it as” are welcome when they make the explanation easier to follow.
* Use first-person observations sparingly to capture a useful mental model, comparison, mistake, or realization.
* Prefer short explanations in the user's own words over textbook definitions.
* Start simple, then add detail. Connect a new idea to something already familiar when possible.
* Use occasional analogies when they genuinely make a concept stick. Do not force an analogy into every section.
* Fix spelling, grammar, and unclear sentences, but keep the personal wording and rhythm. Do not turn the note into stiff, academic, promotional, or overly polished prose.
* Avoid filler, generic introductions, repeated conclusions, and decorative language.

## Accuracy and Missing Information

* Preserve the meaning of user-supplied material unless it is technically incorrect.
* Correct clear technical errors. If the intended meaning is uncertain and correctness would be affected, ask the user instead of guessing.
* For a small non-blocking gap, add a visible `TODO:` that states what is missing or needs confirmation.
* Never invent commands, APIs, behavior, output, citations, or source material.
* Do not perform external research unless the user asks for it or authorizes it. When research is requested, prefer authoritative primary documentation and distinguish sourced facts from personal explanation.
* Do not copy source documentation at length. Restate the idea concisely in the user's voice.

## Structure

Adapt the structure to the material instead of forcing every note into the same template.

* Use exactly one descriptive `#` title at the top of the note.
* Follow the title with a short introduction that says what the topic is, why it matters, or what the note will cover.
* Use `##` for main ideas and `###` for parts of those ideas. Use `####` only when the extra level is genuinely needed.
* Arrange sections in a learning-friendly order: basic idea → how it works → example → important details or differences.
* Introduce a concept in words before presenting its code or commands.
* Keep sections focused. Split a long explanation when it begins teaching a separate idea.
* Use a `---` separator only when it creates a useful transition between major parts. Do not insert one mechanically after every section.
* Add a Key Takeaways or Summary section only when it helps the reader review the concept. Do not repeat the whole note.

### Concept notes

Normally move through these ideas as relevant:

1. What the concept is.
2. Why or when it is useful.
3. How it works or its basic syntax.
4. A small working example.
5. Important differences, mistakes, or takeaways.

The headings do not need to use these exact labels.

### Walkthroughs

* Organize the work in the order the reader should perform it.
* Keep instructions beside the code or command they explain.
* Explain why a step is needed when that reason is not obvious.
* Do not add a separate recap when the sequence already makes the result clear.

### Cheatsheets

* Organize entries by task, workflow stage, or functional category.
* Give each section a one-sentence orientation before its reference material.
* Use tables for compact command-to-purpose mappings; use code blocks when a runnable sequence is easier to understand.

## Examples and Code

* Prefer small, concrete examples that build on one another.
* Explain what an example demonstrates before showing it.
* Always add the correct language identifier to fenced code blocks, such as `python`, `java`, `sql`, `typescript`, `bash`, or `html`.
* Use inline comments to explain decisions or behavior that is not immediately obvious.
* Show expected output as a comment when it helps confirm the reader's mental model.
* For a multi-file example, identify each file in a comment at the top of its code block.
* Use realistic names that make the example readable. Avoid unnecessary scaffolding around the concept being taught.
* When comparing two approaches, show the smallest example that makes the difference visible, then explain that difference in plain language.

For example, prefer wording shaped like this:

> Let's say you have two Python files: `car.py` and `main.py`. You can place the class in `car.py`, then import it into `main.py` like this:

This is a voice example, not text to repeat mechanically.

## Markdown Conventions

* Leave one blank line between headings, paragraphs, lists, code blocks, tables, and separators.
* Do not use more than two consecutive blank lines or leave trailing spaces.
* Use `*` for unordered lists and `1.`, `2.`, `3.` for ordered steps. Indent nested list items by four spaces.
* Keep list items concise. Move a long explanation into a paragraph or subsection.
* Use **bold** for useful labels and important terms, `backticks` for code identifiers, filenames, and commands, and *italics* only for light emphasis.
* Use recurring labels such as **Example:**, **Syntax:**, **Purpose:**, **Analogy:**, or **Critical Rule:** only when the label helps the reader scan the note.
* Use pipe-style tables only for real comparisons, matrices, or compact references. Include a header row and left-align columns with `:---`.
* Use `✅`, `❌`, and `→` when they make a compact comparison clearer, not as decoration.
* Do not add YAML frontmatter to ordinary note files.

## File Organization

When the user has not supplied a filename or repository convention:

* Use lowercase `snake_case.md` filenames with no spaces.
* Add a numeric prefix for an ordered series, such as `01_topic.md` and `02_next_topic.md`.
* Place the note in the closest topic folder and add a subtopic folder only when it improves organization.
* Follow an established neighboring convention when the destination already contains related notes.

## Revising Existing Notes

* Read the entire note before editing so later examples and explanations are not contradicted.
* Preserve useful phrases, first-person mental models, and the original learning sequence.
* Correct typos, broken Markdown, technical mistakes, and confusing transitions without rewriting sound passages merely for stylistic uniformity.
* Combine duplicated explanations and remove statements that add no learning value.
* Keep intentional rough notes, questions, and reflections when they record the user's learning. Clean their wording only enough to make them understandable.
* Do not expand a short note into a comprehensive guide unless the user asks for more depth.

## Final Check

Before delivering a note, confirm that:

* it sounds like a clear personal explanation rather than copied documentation;
* the progression can be followed by someone returning to the topic later;
* every code block has a language tag and enough context to understand it;
* facts, examples, and expected output do not contradict one another;
* uncertainty is marked or raised instead of hidden by a guess;
* headings, spacing, lists, and tables render cleanly; and
* optional sections were included because they help, not because a template required them.
