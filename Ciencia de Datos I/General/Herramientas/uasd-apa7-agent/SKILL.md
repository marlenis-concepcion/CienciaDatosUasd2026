---
name: uasd-apa7-agent
description: Apply UASD/FIA APA 7th edition rules from the supplied "FIA_Normas APA 7ma edicion.pdf" to academic essays, reports, forums, DOCX files, references, citations, abstracts, tables, figures, annexes, and Spanish-language university assignments. Use when the user asks for APA, APA 7, normas APA, formato UASD, ensayo, investigación, referencias, citas, tabla de contenido, resumen, anexos, or asks to revise anything they send for APA compliance.
---

# UASD APA 7 Agent

Use this skill to create, revise, or format academic work according to APA 7 and the user's UASD/FIA guide. Treat the user's attached PDF as the local authority when it conflicts with generic memory.

## Workflow

1. Identify the deliverable type: forum post, essay, research paper, DOCX, references-only, citation check, or full APA formatting.
2. Apply the assignment requirements first, then APA 7 rules from `references/fia_apa7_rules.md`.
3. For UASD Virtual assignments in INF-8237, enforce the platform delivery rules in `references/uasd_inf8237_requirements.md` before generic APA decisions.
4. For full papers, enforce this order unless the user or assignment says otherwise:
   - Página de presentación
   - Resumen
   - Abstract if requested
   - Tabla de contenido if requested by the assignment
   - Cuerpo/desarrollo
   - Referencias
   - Notas al pie if any
   - Tablas
   - Figuras
   - Anexos
5. In Spanish, use Spanish APA adaptations:
   - Use `y` between authors in citations and Spanish references.
   - Use sentence-style capitalization in titles.
   - Use dates as `Año, día de mes`.
   - Use ordinal editions such as `(2.ª ed.)`.
6. For DOCX output, prefer:
   - Letter size, 1-inch/2.54 cm margins.
   - Times New Roman 12 unless the user asks for another allowed font.
   - Double spacing, no extra spacing between paragraphs.
   - Left alignment, no full justification.
   - First-line paragraph indent of 1.27 cm/0.5 in.
   - References with 1.27 cm/0.5 in hanging indent.
   - Page number at top right in Arabic numerals, unless the teacher explicitly asks for Roman preliminary pages.
7. If the teacher asks for Roman numbering, use lower Roman numerals for preliminary matter and restart Arabic numerals at 1 for the body.
8. Before finalizing, run an APA checklist:
   - Every in-text citation has a reference entry.
   - Every reference entry is cited in text.
   - Citation author-year forms are correct.
   - Tables/figures are numbered, titled, mentioned in text, and credited.
   - Annexes are lettered, titled, mentioned in text, and placed after references.
   - The reference list is alphabetized by first author.

## Citation Rules

- Prefer paraphrase over direct quotation.
- Cite primary sources when possible.
- Narrative citation: `Autor (Año)`.
- Parenthetical citation: `(Autor, Año)`.
- Direct quotation always needs page, paragraph, section, or timestamp.
- Short quotation under 40 words: integrate in paragraph with quotation marks.
- Long quotation 40+ words: block quotation, 1.27 cm left indent, no quotation marks.
- One author: `López (2019)` or `(López, 2019)`.
- Two authors: `Rodríguez y Sánchez (2013)` or `(Rodríguez y Sánchez, 2013)`.
- Three or more authors: `Barton et al. (2016)` or `(Barton et al., 2016)` from the first citation.
- Corporate author with abbreviation: first use full name plus abbreviation, later use abbreviation.
- Multiple works in one parenthesis: alphabetical order, separated by semicolons.
- Same author same year: add `a`, `b`, `c`.
- No author: cite first words of title and year.
- No date: use `s.f.`.
- Secondary citation: `Autor original (como se citó en Autor consultado, Año)`, but avoid when primary source is available.
- Personal communications are cited in text only and omitted from references.

## References

Reference entries use four core elements: author, date, title, source. Use references, not bibliography: include only sources cited in the paper.

Common formats:

- Book: `Apellido, A. A. (Año). Título del libro en cursiva. Editorial. URL`
- Journal article with DOI: `Apellido, A. A., Apellido, B. B. y Apellido, C. C. (Año). Título del artículo. Nombre de la revista en cursiva, volumen en cursiva(número), pp-pp. https://doi.org/...`
- Web page: `Autor. (Año, día de mes). Título. Nombre del sitio web. URL`
- Thesis: `Apellido, A. (Año). Título de la tesis [Tesis de maestría/doctoral, Universidad]. Repositorio. URL`
- Conference: `Apellido, A. (Año, día de mes). Título [Tipo de contribución]. Nombre del congreso, Ciudad, País. URL`

Load `references/fia_apa7_rules.md` when the task involves detailed formatting, citations, references, tables, figures, annexes, or DOCX generation.

Load `references/uasd_inf8237_requirements.md` for INF-8237 essays and UASD Virtual assignment submissions.
