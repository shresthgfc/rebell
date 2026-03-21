# Review Checklist

Used to verify sub-agent outputs meet quality standards.

---

## Agent definition quality

- [ ] Has YAML frontmatter (name, description, tools, model, effort)
- [ ] Has Role section defining specialist boundaries
- [ ] Has Primary objectives (numbered list)
- [ ] Has Non-negotiable rules with sub-sections
- [ ] Has Entity taxonomy or classification system
- [ ] Has Standard output structure with exact markdown template
- [ ] Has Quality gates as checkbox list
- [ ] Has Absolute prohibitions as "Never:" list
- [ ] Description is specific enough for Claude to auto-delegate

---

## Agent output quality

- [ ] Written to the correct output file path
- [ ] Follows the agent's standard output structure exactly
- [ ] All quality gates in the agent definition are satisfied
- [ ] No information was invented (only extracted or logically implied)
- [ ] Assumptions are documented
- [ ] Open questions are listed with blocking status
- [ ] Upstream context was read before producing output

---

## Pipeline quality

- [ ] All phases ran in sequence
- [ ] Each phase has a synthesis document
- [ ] Risk register is consolidated across phases
- [ ] Final report exists with all sections
- [ ] Open questions from all phases are collected
