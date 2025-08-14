# Update and Commit Command - memory-bank

## Usage
```bash
/update-and-commit "Brief description of changes"
```

## Description
Comprehensive workflow for documenting progress, updating documentation, and committing changes to memory-bank with professional quality standards.

## Process

### 1. Update Documentation (Only if Needed)
- IF new CLI commands: Update README.md usage section
- IF new AI features: Update AI integration examples
- IF new MCP tools: Update MCP tool documentation
- NO documentation changes for internal fixes or refactoring

### 2. Format Code Before Committing
**IMPORTANT: Always format code before committing**
```bash
# Format Python code
uv run black memory_bank/ tests/ examples/ --quiet
uv run isort memory_bank/ tests/ examples/ --quiet

# Format TypeScript (MCP server)
cd mcp-server && npm run format --silent 2>/dev/null || echo "TypeScript formatting skipped"
cd ..

# Format configuration files
prettier --write "*.{json,yml,yaml}" --ignore-path .gitignore 2>/dev/null || echo "Config formatting skipped"
```

### 3. Quality Checks Before Committing
**IMPORTANT: Run basic quality checks**
```bash
# Syntax validation
find memory_bank/ tests/ examples/ -name "*.py" -exec python -m py_compile {} \; 2>/dev/null || echo "⚠️ Syntax errors found"

# Quick test run
uv run pytest tests/test_core/ tests/test_git/ -q || echo "⚠️ Core tests failing"

# Import validation
uv run python -c "import memory_bank; print('✅ Import successful')" || echo "⚠️ Import failed"
```

### 4. Commit Changes (Selective and Clean)
**IMPORTANT: Keep commit message under 3 lines**
```bash
# Check status and review changes
git status

# Add specific files (be selective)
git add memory_bank/ tests/ README.md pyproject.toml

# Remove unwanted files if any
git rm unwanted-file.py 2>/dev/null || true

# Commit with professional message
git commit -m "Brief description of change

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 5. File Management Strategy
**IMPORTANT: Be selective about what gets committed**

```bash
# Always include
git add memory_bank/                # Core library code
git add tests/                      # Test files (when relevant)
git add examples/                   # Usage examples
git add README.md CLAUDE.md         # Documentation

# Include when relevant  
git add mcp-server/                 # MCP server changes
git add templates/                  # Template updates
git add .claude/commands/           # Command updates

# Never include
git rm htmlcov/ .pytest_cache/ 2>/dev/null || true
git rm '*.log' '*.tmp' 2>/dev/null || true
git rm -r test_outputs/ 2>/dev/null || true
```

## Guidelines for memory-bank

- **Be concise**: Focus on user-visible decision management improvements
- **Document features**: New decision categories, AI capabilities, git integration
- **Skip internals**: Don't document refactoring unless it affects users
- **Professional quality**: Ensure tests pass and code is formatted

## Examples

### New Feature
```bash
/update-and-commit "Add AI-powered decision confidence scoring"
```

### Bug Fix
```bash
/update-and-commit "Fix git hook installation on Windows platforms"
```

### Integration Enhancement
```bash
/update-and-commit "Add Claude API integration for decision analysis"
```

### CLI Improvement
```bash
/update-and-commit "Add decision search with fuzzy matching"
```

## Quality Standards

Before committing, ensure:
- ✅ **Tests pass**: Core functionality validated
- ✅ **Code formatted**: Black and isort applied
- ✅ **Imports work**: Basic import validation passes
- ✅ **Git hooks work**: If testing git integration
- ✅ **Clean git status**: Only intended files committed

This command ensures professional quality commits for the memory-bank system while maintaining development velocity.