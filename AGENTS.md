# AGENTS.md — Documents Hub

## Repository Structure

```
documents_hub/
├── opencode/              # OpenCode documentation
├── backend/               # Backend patterns (NestJS)
├── frontend/              # Frontend patterns (React/TypeScript)
└── testing/               # Testing rules and TDD
```

## Commands

```bash
# Markdown validation
npx markdownlint-cli "*.md"
npx markdown-link-check "*.md"
```

## Documentation Conventions

### Format
- **Language**: Russian or English (consistent within document)
- **Format**: Markdown with mermaid diagrams
- **TOC**: Required for documents >50 lines
- **Examples**: Real code examples preferred

### Structure
```markdown
# Title

## Содержание
1. [Section](#section)

---

## Section
```

### Code Blocks
Always specify language:
```typescript
const example = "code";
```

## Content Guidelines

### Adding to `opencode/`
- Add .md files as needed
- Update existing files when OpenCode changes

### Adding to `backend/` / `frontend/`
- Create subdirectories by topic: `backend/nestjs/`, `frontend/react/`
- Structure: README.md + code examples

### Adding to `testing/`
- Update TESTING_RULES.md for TDD principles
- Reference specific framework guides in backend/frontend

## Agent Rules

1. **Read existing docs** before adding content
2. **Follow structure** of existing .md files
3. **Update TOC** when changing document structure
4. **Don't duplicate** — reference existing sections
5. **Use examples** from real projects when possible
6. **Be concise** — prefer linking over duplicating

## Key References

| File | Content |
|------|---------|
| `testing/TESTING_RULES.md` | TDD, red-green-refactor |
| `backend/BACKEND_TESTING.md` | NestJS testing |
| `frontend/TESTING.md` | React testing patterns |
| `frontend/TYPESCRIPT.md` | TypeScript conventions |
| `backend/nestjs/*.md` | NestJS patterns |
