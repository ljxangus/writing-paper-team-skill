# Lessons Learned

This directory captures structured lessons from each research project for cross-project learning.

## Format

Each lesson file follows this structure:

```markdown
# Lesson: [Title]
- Date: YYYY-MM-DD
- Project: [project name]
- Stage: [which pipeline stage]
- Category: [search | writing | experiment | review | audit | general]

## Context
[What was happening when this lesson was learned]

## Lesson
[The key takeaway]

## Hermes Skill Factory Alignment
- approaches_used: [list]
- edge_cases: [list]
- domain_knowledge: [list]
- failures_and_fixes: [list]
```

## Hermes Agent Integration

Lessons are formatted to align with Hermes Agent's skill factory output:
- `approaches_used` maps directly to Hermes approach capture
- `edge_cases` maps to Hermes edge case learning
- `domain_knowledge` maps to Hermes knowledge reconstruction
- `failures_and_fixes` maps to Hermes failure learning

When using Hermes Agent, lessons can be automatically converted into reusable skills.
