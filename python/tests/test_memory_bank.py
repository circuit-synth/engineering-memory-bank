"""
Tests for memory-bank core functionality.
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from memory_bank.core.memory_bank import MemoryBank
from memory_bank.core.decision import Decision, DecisionCategory, DecisionImpact
from memory_bank.utils.exceptions import MemoryBankError


class TestMemoryBank:
    """Test memory-bank core functionality."""

    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir) / "test_project"
            project_path.mkdir()
            
            # Initialize git repository
            import subprocess
            subprocess.run(['git', 'init'], cwd=project_path, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=project_path)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=project_path)
            
            yield project_path

    def test_memory_bank_initialization(self, temp_project):
        """Test memory-bank initialization."""
        # Initialize memory-bank
        bank = MemoryBank.init_project(temp_project, "Test Project")
        
        # Verify initialization
        assert bank.is_initialized
        assert bank.project_name == "Test Project"
        assert bank.memory_bank_dir.exists()
        assert bank.config_file.exists()

    def test_decision_logging(self, temp_project):
        """Test manual decision logging."""
        bank = MemoryBank.init_project(temp_project, "Test Project")
        
        # Log a decision
        decision = bank.log_decision(
            category=DecisionCategory.COMPONENT_SELECTION,
            decision="Selected STM32F407 over STM32F405",
            rationale="Need USB OTG and Ethernet capabilities",
            alternatives=["STM32F405", "STM32H7 series"],
            impact=DecisionImpact.HIGH,
            tags=["mcu", "connectivity"]
        )
        
        # Verify decision
        assert decision.category == DecisionCategory.COMPONENT_SELECTION
        assert decision.decision == "Selected STM32F407 over STM32F405"
        assert decision.impact == DecisionImpact.HIGH
        assert "mcu" in decision.tags

    def test_decision_search(self, temp_project):
        """Test decision search functionality."""
        bank = MemoryBank.init_project(temp_project, "Test Project")
        
        # Log multiple decisions
        bank.log_decision(
            category=DecisionCategory.POWER_SUPPLY,
            decision="Buck converter for 5V to 3.3V",
            rationale="Better efficiency than linear regulator",
            tags=["power", "efficiency"]
        )
        
        bank.log_decision(
            category=DecisionCategory.COMPONENT_SELECTION,
            decision="0603 resistors for production",
            rationale="Good balance of size and hand soldering",
            tags=["resistor", "package"]
        )
        
        # Search decisions
        power_decisions = bank.search_decisions("power")
        resistor_decisions = bank.search_decisions("resistor")
        
        # Verify search results
        assert len(power_decisions) >= 1
        assert len(resistor_decisions) >= 1
        assert "Buck converter" in power_decisions[0].decision

    def test_test_result_logging(self, temp_project):
        """Test logging of test results."""
        bank = MemoryBank.init_project(temp_project, "Test Project")
        
        # Log test result
        test_decision = bank.log_test_result(
            test_name="Power consumption test",
            result={"idle": "50mA", "active": "120mA"},
            meets_spec=True,
            notes="Well under 150mA budget"
        )
        
        # Verify test result logging
        assert test_decision.category == DecisionCategory.TESTING
        assert "Power consumption test" in test_decision.decision
        assert test_decision.context["meets_spec"] is True

    def test_git_hook_setup(self, temp_project):
        """Test git hook setup."""
        bank = MemoryBank.init_project(temp_project, "Test Project")
        
        # Setup git hooks
        success = bank.setup_git_hooks()
        assert success
        
        # Verify hook file exists
        hook_file = temp_project / ".git" / "hooks" / "post-commit"
        assert hook_file.exists()
        
        # Verify hook content
        with open(hook_file, 'r') as f:
            content = f.read()
        assert "memory-bank system" in content

    def test_statistics(self, temp_project):
        """Test statistics generation."""
        bank = MemoryBank.init_project(temp_project, "Test Project")
        
        # Log some decisions
        for i in range(3):
            bank.log_decision(
                category=DecisionCategory.COMPONENT_SELECTION,
                decision=f"Selected component {i+1}",
                impact=DecisionImpact.MEDIUM
            )
        
        # Get statistics
        stats = bank.get_statistics()
        
        # Verify statistics
        assert stats['project_name'] == "Test Project"
        assert stats['total_decisions'] >= 3
        assert 'by_category' in stats
        assert 'by_impact' in stats

    def test_timeline_generation(self, temp_project):
        """Test decision timeline generation."""
        bank = MemoryBank.init_project(temp_project, "Test Project")
        
        # Log decisions with different impacts
        bank.log_decision(
            category=DecisionCategory.ARCHITECTURE,
            decision="Microcontroller architecture",
            impact=DecisionImpact.HIGH
        )
        
        bank.log_decision(
            category=DecisionCategory.TESTING,
            decision="Test plan approval",
            impact=DecisionImpact.MEDIUM
        )
        
        # Get timeline and milestones
        timeline = bank.get_decision_timeline()
        milestones = bank.get_project_milestones()
        
        # Verify timeline
        assert len(timeline) >= 2
        assert timeline[0]['type'] == 'decision'
        
        # Verify milestones (high impact decisions)
        assert len(milestones) >= 1  # Architecture decision is high impact

    def test_export_functionality(self, temp_project):
        """Test decision export functionality."""
        bank = MemoryBank.init_project(temp_project, "Test Project")
        
        # Log a decision
        bank.log_decision(
            category=DecisionCategory.COMPONENT_SELECTION,
            decision="Export test decision",
            rationale="Testing export functionality"
        )
        
        # Export decisions
        export_path = temp_project / "test_export.json"
        success = bank.export_decisions(export_path)
        
        assert success
        assert export_path.exists()
        
        # Verify export content
        import json
        with open(export_path, 'r') as f:
            data = json.load(f)
        
        assert 'project' in data
        assert 'decisions' in data
        assert len(data['decisions']) >= 1

    def test_error_handling(self):
        """Test error handling for invalid operations."""
        # Test current_project without initialization
        with pytest.raises(MemoryBankError, match="No memory-bank found"):
            MemoryBank.current_project()
        
        # Test invalid project path
        with pytest.raises(Exception):
            MemoryBank.init_project("/invalid/path/that/does/not/exist")


class TestDecisionAnalysis:
    """Test decision analysis and AI features."""

    @pytest.fixture
    def populated_memory_bank(self, temp_project):
        """Create memory-bank with sample decisions."""
        bank = MemoryBank.init_project(temp_project, "Analysis Test")
        
        # Add varied decisions for analysis
        decisions = [
            ("Component selection", "Selected STM32F407", "Need USB and Ethernet", ["high"]),
            ("Power supply", "Buck converter vs linear", "90% vs 60% efficiency", ["medium"]),
            ("Testing", "PCB prototype validation", "All tests passed", ["medium"]),
            ("Issue resolution", "Fixed power rail noise", "Added more decoupling caps", ["low"]),
        ]
        
        for i, (category, decision, rationale, impact) in enumerate(decisions):
            bank.log_decision(
                category=category,
                decision=decision, 
                rationale=rationale,
                impact=impact[0],
                tags=[f"test-{i}", "analysis"]
            )
        
        return bank

    def test_ai_analysis(self, populated_memory_bank):
        """Test AI decision analysis."""
        bank = populated_memory_bank
        
        # Get AI insights
        insights = bank.analyze_decisions()
        
        # Verify insights structure
        assert hasattr(insights, 'confidence_score')
        assert hasattr(insights, 'recommendations')
        assert hasattr(insights, 'risk_factors')
        
        # Should have some insights with multiple decisions
        assert insights.confidence_score > 0
        assert isinstance(insights.recommendations, list)

    def test_decision_patterns(self, populated_memory_bank):
        """Test decision pattern identification."""
        bank = populated_memory_bank
        
        # Analyze patterns
        insights = bank.analyze_decisions()
        
        # Should identify patterns in the test data
        assert isinstance(insights.patterns, list)
        
        # Timeline should show chronological order
        timeline = bank.get_decision_timeline()
        assert len(timeline) >= 4
        
        # Should be sorted by timestamp
        timestamps = [event['timestamp'] for event in timeline]
        assert timestamps == sorted(timestamps)

    def test_recommendation_generation(self, populated_memory_bank):
        """Test AI recommendation generation."""
        bank = populated_memory_bank
        
        recommendations = bank.get_ai_recommendations()
        
        # Should generate some recommendations
        assert isinstance(recommendations, list)
        
        # Each recommendation should have required fields
        for rec in recommendations:
            assert 'type' in rec
            assert 'suggestion' in rec
            assert 'confidence' in rec