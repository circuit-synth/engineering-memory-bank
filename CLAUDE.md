# CLAUDE.md - engineering-memory-bank

This file provides guidance to Claude Code when working on the engineering-memory-bank project.

## Project Overview

engineering-memory-bank is an AI-powered engineering decision documentation system that automatically captures and analyzes design decisions with git integration.

## Architecture

```
engineering-memory-bank/
├── python/                          # Core Python library
│   ├── memory_bank/                # Main package
│   │   ├── core/                   # Core decision management
│   │   ├── ai/                     # AI analysis and insights
│   │   ├── git/                    # Git integration and hooks
│   │   ├── templates/              # Documentation templates
│   │   ├── analysis/               # Decision analysis tools
│   │   ├── mcp/                    # MCP server interface
│   │   └── utils/                  # Utilities and exceptions
│   └── tests/                      # Comprehensive test suite
├── mcp-server/                     # TypeScript MCP server
├── templates/                      # Project templates
└── examples/                       # Usage examples
```

## Key Commands

### Development
```bash
# Install in development mode
cd python
uv pip install -e .

# Run tests
uv run pytest tests/ -v

# Format code
uv run black memory_bank/ tests/
uv run isort memory_bank/ tests/
```

### Memory Bank Usage
```bash
# Initialize in project
engineering-memory-bank init

# Setup git hooks
engineering-memory-bank setup-hooks

# Generate report
engineering-memory-bank report

# Export decisions
engineering-memory-bank export decisions.json
```

## Core API Usage

```python
import engineering_memory_bank as emb

# Initialize memory bank
bank = emb.init_project('/path/to/project')

# Log decisions
bank.log_decision(
    category='component_selection',
    decision='Selected STM32F407 over STM32F405',
    rationale='Need USB OTG and Ethernet for full connectivity',
    alternatives=['STM32F405', 'STM32H7 series'],
    impact='high'
)

# AI analysis
insights = bank.analyze_decisions()
recommendations = bank.get_ai_recommendations()

# Search and timeline
power_decisions = bank.search_decisions('power supply')
timeline = bank.get_decision_timeline()
```

## MCP Integration

The memory-bank includes a native MCP server for AI agent integration:

### MCP Tools Available
- `init_memory_bank` - Initialize memory bank in project
- `log_decision` - Record engineering decisions
- `search_decisions` - Find relevant decisions
- `analyze_decisions` - AI-powered decision analysis
- `get_recommendations` - AI recommendations based on history
- `get_timeline` - Project decision timeline
- `export_decisions` - Export decision data

### Agent Workflow Example
```
User: "Document why we chose the buck converter for power supply"

Claude: I'll help document this power supply decision in your memory bank.

[Agent uses MCP tools to:]
1. log_decision with category='power_supply'
2. Record rationale about efficiency and size
3. Note alternatives considered (linear regulator)
4. Add relevant tags and context
5. Update project timeline

Your power supply decision has been documented and will be available for future reference and AI analysis.
```

## Testing Strategy

### Test Categories
- **Unit tests**: Core decision logic and data structures
- **Integration tests**: Git hooks and file operations
- **AI tests**: Decision analysis and recommendation generation
- **CLI tests**: Command-line interface functionality
- **MCP tests**: AI agent integration

### Test Data
- Sample engineering projects with decision histories
- Git repositories with commit histories for testing
- Reference decision templates and examples

## Key Principles

1. **Domain Agnostic**: Works for electronics, software, mechanical, etc.
2. **AI-Powered**: Claude integration for insights and recommendations
3. **Git Native**: Seamless integration with development workflows
4. **Professional Quality**: Suitable for enterprise engineering teams
5. **Knowledge Building**: Cross-project learning and improvement

## Dependencies

- **GitPython**: Git repository integration
- **click**: Command-line interface
- **pydantic**: Data validation and serialization
- **jinja2**: Template rendering
- **anthropic/openai**: AI integration (optional)

## Memory Bank System - REQUIRED WORKFLOW

This repository uses a **Code Memory Bank** system for persistent development context. **ALL DEVELOPMENT WORK MUST FOLLOW THIS WORKFLOW.**

### 🚨 MANDATORY WORKFLOW FOR ALL AI DEVELOPMENT

#### 1. BEFORE Starting Any Work:
```bash
# ALWAYS start by reading existing context
1. Read .memory_bank/activeContext.md (current state)
2. Read .memory_bank/decisionLog.md (past decisions) 
3. Read .memory_bank/progress.md (current milestones)
4. Check .memory_bank/productContext.md (project scope)
```

#### 2. FOR New Features (REQUIRED):
```bash
# Create PRD BEFORE coding
1. Write PRD in .memory_bank/features/[feature-name].md
2. Document requirements, design approach, success criteria
3. Get alignment on approach before implementation
```

#### 3. DURING Development:
```bash
# Keep context current
1. Update .memory_bank/activeContext.md with current work
2. Document decisions in .memory_bank/decisionLog.md (ADR format)
3. Track progress in .memory_bank/progress.md
```

#### 4. AFTER Completing Work:
```bash
# ALWAYS update memory bank
/umb
```

### Memory Bank Structure

- **activeContext.md**: Current session state, focus areas, files being worked on
- **decisionLog.md**: All architectural decisions in ADR format with rationale
- **productContext.md**: Project overview, value proposition, target users  
- **progress.md**: Milestones, current tasks, success metrics
- **features/**: PRDs for all planned features (REQUIRED before coding)

### 🔍 Query Memory Bank

Ask natural language questions about past decisions:
- "What AI analysis approaches were chosen and why?"
- "How does git integration capture engineering decisions?"
- "What are the current cross-project knowledge priorities?"

### ⚠️ CRITICAL: No Development Without Memory Bank

1. **Never start coding** without reading existing memory bank context
2. **Always write PRDs** for new features before implementation
3. **Document all decisions** in ADR format with rationale
4. **Use /umb command** before ending development sessions

## Related Projects

- **kicad-sch-api**: Can use memory-bank for schematic design decisions
- **kicad-pcb-api**: Can use memory-bank for PCB design decisions
- **circuit-synth**: Parent project and source of extracted logic

---

*This project transforms scattered engineering documentation into structured knowledge that improves with every decision.*