# Analyze Decisions Command - memory-bank

## Usage
```bash
/analyze-decisions [category] [--ai] [--timeline] [--export]
```

## Description
Performs comprehensive analysis of engineering decisions in the memory-bank, providing insights, patterns, and AI-powered recommendations for improved decision making.

## Parameters
- `category` (optional): Specific decision category to analyze
- `--ai`: Enable AI-powered analysis and recommendations
- `--timeline`: Generate decision timeline visualization
- `--export`: Export analysis results to files

## Analysis Types

### 1. Decision Pattern Analysis
```bash
/analyze-decisions --patterns
```

**Analyzes**:
- **Decision frequency** by category and time period
- **Impact distribution** across different decision types
- **Tag clustering** to identify common themes
- **Author patterns** and decision-making styles
- **Validation rates** and decision quality metrics

### 2. AI-Powered Insights
```bash
/analyze-decisions --ai
```

**Provides**:
- **Decision confidence** scoring based on rationale quality
- **Risk assessment** for high-impact decisions
- **Alternative analysis** - were better options available?
- **Pattern recognition** - similar decisions across projects
- **Recommendation generation** for future decisions

### 3. Timeline Analysis
```bash
/analyze-decisions --timeline
```

**Generates**:
- **Chronological decision flow** with impact visualization
- **Milestone identification** from decision history
- **Decision clustering** by time periods
- **Project phase analysis** based on decision types
- **Decision velocity** and project momentum tracking

### 4. Cross-Project Learning
```bash
/analyze-decisions --cross-project
```

**Discovers**:
- **Similar decisions** across different projects
- **Success patterns** that can be replicated
- **Common failure modes** to avoid
- **Best practices** derived from decision outcomes
- **Knowledge transfer** opportunities

## Output Formats

### Analysis Report
```markdown
# Decision Analysis Report - Project Name

## Executive Summary
- Total decisions analyzed: 156
- High-impact decisions: 23 (15%)
- Average decision confidence: 8.2/10
- Most active category: Component Selection (34%)

## Key Insights
1. **Power supply decisions** show highest confidence scores
2. **Component selection** benefits from more alternative analysis
3. **Testing decisions** correlate with project success metrics

## Recommendations
1. Document more alternatives for component selection decisions
2. Increase validation frequency for architecture decisions
3. Cross-reference similar decisions from Project-X for MCU selection
```

### Timeline Visualization
```
2024-01 |████████| Architecture decisions (8)
2024-02 |██████  | Component selection (6)
2024-03 |████████████| Testing and validation (12)
2024-04 |██████  | Issue resolution (6)
```

### AI Insights
```json
{
  "confidence_trends": {
    "overall": 8.2,
    "by_category": {
      "power_supply": 9.1,
      "component_selection": 7.8,
      "architecture": 8.5
    }
  },
  "risk_factors": [
    "High-impact decisions with minimal alternative analysis",
    "Clustering of critical decisions without validation"
  ],
  "recommendations": [
    {
      "category": "process_improvement",
      "suggestion": "Implement peer review for high-impact decisions",
      "confidence": 0.85
    }
  ]
}
```

## Implementation

```bash
#!/bin/bash

# Parse arguments
CATEGORY=""
AI_ANALYSIS=false
TIMELINE=false
EXPORT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --ai)
            AI_ANALYSIS=true
            shift
            ;;
        --timeline)
            TIMELINE=true
            shift
            ;;
        --export)
            EXPORT=true
            shift
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            CATEGORY="$1"
            shift
            ;;
    esac
done

# Ensure we're in a memory-bank project
if [[ ! -f ".memory-bank-config.json" ]]; then
    echo "❌ No memory-bank found in current directory"
    echo "Run 'memory-bank init' to initialize"
    exit 1
fi

echo "🧠 Memory Bank Decision Analysis"
echo "=" * 50

# Basic decision analysis
echo "📊 Analyzing decisions..."
uv run python -c "
import memory_bank as mb
bank = mb.current_project()
stats = bank.get_statistics()

print(f'Total decisions: {stats[\"total_decisions\"]}')
print(f'Categories: {len(stats[\"by_category\"])}')
print(f'Recent decisions: {sum(1 for d in bank._load_all_decisions() if d.is_recent)}')

# Category breakdown
print('\n📋 Decision Categories:')
for category, count in stats['by_category'].items():
    print(f'  {category}: {count}')

# Impact breakdown  
print('\n⚡ Decision Impact:')
for impact, count in stats['by_impact'].items():
    print(f'  {impact}: {count}')
"

# AI analysis if requested
if [[ "$AI_ANALYSIS" == "true" ]]; then
    echo ""
    echo "🤖 AI Analysis..."
    uv run python -c "
import memory_bank as mb
bank = mb.current_project()

try:
    insights = bank.analyze_decisions()
    print(f'✅ AI Analysis completed')
    print(f'Confidence score: {insights.confidence_score:.1f}/10')
    print(f'Risk factors: {len(insights.risk_factors)}')
    print(f'Recommendations: {len(insights.recommendations)}')
    
    # Show top recommendations
    for i, rec in enumerate(insights.recommendations[:3]):
        print(f'  {i+1}. {rec[\"suggestion\"]}')
        
except Exception as e:
    print(f'⚠️ AI analysis failed: {e}')
    print('Note: AI analysis requires API keys for Claude/OpenAI')
"
fi

# Timeline analysis if requested
if [[ "$TIMELINE" == "true" ]]; then
    echo ""
    echo "⏰ Timeline Analysis..."
    uv run python -c "
import memory_bank as mb
bank = mb.current_project()

timeline = bank.get_decision_timeline()
milestones = bank.get_project_milestones()

print(f'Timeline events: {len(timeline)}')
print(f'Major milestones: {len(milestones)}')

# Show recent timeline
recent_timeline = [event for event in timeline[-10:]]
print('\n📅 Recent Decision Timeline:')
for event in recent_timeline:
    date = event['timestamp'].strftime('%Y-%m-%d')
    print(f'  {date}: {event[\"decision\"][:60]}...')
"
fi

# Export if requested
if [[ "$EXPORT" == "true" ]]; then
    echo ""
    echo "📤 Exporting analysis..."
    OUTPUT_DIR="analysis-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$OUTPUT_DIR"
    
    uv run python -c "
import memory_bank as mb
bank = mb.current_project()

# Export decisions
bank.export_decisions('$OUTPUT_DIR/decisions.json')

# Generate comprehensive report
report = bank.generate_decision_report()
with open('$OUTPUT_DIR/analysis_report.md', 'w') as f:
    f.write(report)

print(f'✅ Analysis exported to: $OUTPUT_DIR/')
print('  decisions.json - Raw decision data')
print('  analysis_report.md - Comprehensive analysis report')
"
fi

echo ""
echo "✅ Decision analysis completed"
```

## Usage Examples

```bash
# Basic analysis
/analyze-decisions

# AI-powered analysis
/analyze-decisions --ai

# Component selection analysis
/analyze-decisions component_selection --ai

# Full analysis with export
/analyze-decisions --ai --timeline --export

# Quick timeline view
/analyze-decisions --timeline
```

## Expected Outputs

### Pattern Analysis Results
- **Decision frequency trends** over time
- **Category distribution** and focus areas  
- **Impact assessment** and risk identification
- **Quality metrics** (validation rates, confidence scores)

### AI Insights
- **Decision confidence scoring** based on rationale quality
- **Risk factor identification** for high-impact decisions
- **Pattern recognition** across similar decisions
- **Improvement recommendations** for decision processes

### Timeline Visualization
- **Chronological decision flow** with impact markers
- **Project milestone identification** from decision history
- **Decision clustering** by development phases
- **Velocity tracking** and project momentum analysis

This command provides comprehensive insights into engineering decision patterns, helping teams improve their decision-making processes and learn from past experiences.