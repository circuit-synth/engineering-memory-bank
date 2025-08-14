# Context Portal Integration - engineering-memory-bank

## Setup

```bash
# Install Context Portal
cd tools/context-portal && pip install -e .

# Start server for this repository
uvx context-portal --workspace engineering-memory-bank --port 8004
```

## Repository Context

**engineering-memory-bank** provides AI-powered engineering decision documentation and knowledge management.

### Key Development Areas

- **Decision Capture**: Automatic documentation of engineering choices
- **Git Integration**: Commit-triggered decision analysis
- **AI Analysis**: Machine learning insight generation from decisions
- **Memory Templates**: Structured formats for engineering documentation
- **Cross-Project Insights**: Knowledge sharing between engineering projects

### Context Categories

- `decision-capture`: Automatic documentation strategies
- `git-integration`: Hook and trigger implementation patterns
- `ai-analysis`: Decision analysis algorithm approaches
- `data-models`: Engineering decision data structure design
- `templates`: Documentation template design decisions
- `cross-project`: Knowledge sharing architecture

### Usage Examples

```bash
# Add context about decision capture strategies
uvx context-portal add --category decision-capture "Git hooks capture commits automatically"

# Query AI analysis approaches
uvx context-portal query "decision analysis with Claude API"

# Search template design decisions
uvx context-portal query "engineering documentation templates"
```

This provides AI assistants with context about how the memory-bank system itself is designed and developed.