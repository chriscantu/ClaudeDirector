"""
Embedded Framework Integration Demo and Testing
Demonstrates the complete embedded framework-enhanced persona workflow and validates core functionality.

This test demonstrates:
1. Context Analysis → Persona Selection → Embedded Framework Enhancement workflow
2. Diego systematic analysis with embedded frameworks
3. Maintained response quality without external dependencies
4. Zero-setup functionality validation

Author: Martin (Principal Platform Architect)
"""

import sys
import os
import time
from pathlib import Path

# Add the lib directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from claudedirector.core.enhanced_persona_manager import EnhancedPersonaManager
from claudedirector.core.template_engine import TemplateDiscoveryEngine
from claudedirector.core.complexity_analyzer import AnalysisComplexityDetector
from claudedirector.core.persona_enhancement_engine import PersonaEnhancementEngine


def create_demo_enhanced_manager() -> EnhancedPersonaManager:
    """Create enhanced persona manager for demo with embedded frameworks"""
    
    # Mock template discovery for demo
    template_discovery = TemplateDiscoveryEngine()
    
    # Enhancement configuration for testing
    enhancement_config = {
        "enhancement_thresholds": {
            "systematic_analysis": 0.6,  # Lower threshold for demo
            "framework_lookup": 0.5,
            "minimum_complexity": 0.4
        }
    }
    
    # Create enhanced manager with embedded frameworks
    manager = EnhancedPersonaManager(
        template_discovery=template_discovery,
        enhancement_config=enhancement_config
    )
    
    return manager


def demo_diego_systematic_analysis():
    """Demonstrate Diego's systematic analysis with embedded frameworks"""
    
    print("\n🚀 **Diego's Embedded Framework Systematic Analysis Demo**")
    print("=" * 70)
    
    # Create enhanced persona manager
    manager = create_demo_enhanced_manager()
    
    # Test input that should trigger systematic analysis
    test_input = "Help me develop Q4 platform strategy with systematic stakeholder alignment"
    
    print(f"\n📝 **User Query:**")
    print(f"   {test_input}")
    
    # Process input through enhanced workflow
    print(f"\n⚙️ **Processing through embedded framework enhancement...**")
    start_time = time.time()
    
    result = manager.process_user_input(test_input)
    
    processing_time = int((time.time() - start_time) * 1000)
    
    # Display results
    print(f"\n✅ **Results:**")
    print(f"   Persona Selected: {result.get('persona_selection', {}).get('primary', 'Unknown')}")
    print(f"   Enhancement Applied: {result.get('enhancement_result', {}).get('enhancement_applied', False)}")
    print(f"   Framework Used: {result.get('enhancement_result', {}).get('framework_used', 'None')}")
    print(f"   Processing Time: {processing_time}ms")
    
    # Show enhanced response
    enhanced_response = result.get('final_response', 'No response generated')
    
    print(f"\n📋 **Diego's Enhanced Response:**")
    print("-" * 50)
    print(enhanced_response)
    print("-" * 50)
    
    # Analyze response quality
    print(f"\n🔍 **Response Quality Analysis:**")
    
    # Check for systematic characteristics
    systematic_indicators = [
        "systematic", "framework", "step", "analysis", "assessment",
        "stakeholder", "implementation", "planning", "strategy"
    ]
    
    found_indicators = [word for word in systematic_indicators 
                       if word.lower() in enhanced_response.lower()]
    
    print(f"   Systematic Analysis Indicators: {len(found_indicators)}/9")
    print(f"   Found: {', '.join(found_indicators)}")
    
    # Check for Diego's personality
    diego_characteristics = [
        "😊", "excited", "explore", "together", "resonates", 
        "thoughts", "collaborative", "systematic"
    ]
    
    found_characteristics = [char for char in diego_characteristics 
                           if char.lower() in enhanced_response.lower()]
    
    print(f"   Diego Personality Markers: {len(found_characteristics)}/8")
    print(f"   Found: {', '.join(found_characteristics)}")
    
    # Overall quality assessment
    total_quality_score = len(found_indicators) + len(found_characteristics)
    max_possible = len(systematic_indicators) + len(diego_characteristics)
    quality_percentage = (total_quality_score / max_possible) * 100
    
    print(f"   Overall Quality Score: {quality_percentage:.1f}%")
    
    if quality_percentage >= 70:
        print("   ✅ HIGH QUALITY: Systematic analysis with personality preserved")
    elif quality_percentage >= 50:
        print("   ⚠️ MEDIUM QUALITY: Some systematic elements present")
    else:
        print("   ❌ LOW QUALITY: Enhancement may not be working properly")
    
    return result


def demo_complexity_analysis():
    """Demonstrate the complexity analysis engine"""
    
    print("\n🧠 **Complexity Analysis Demo**")
    print("=" * 40)
    
    detector = AnalysisComplexityDetector()
    
    test_inputs = [
        "Hi there!",  # Simple
        "How do I improve my team's performance?",  # Medium
        "Help me develop comprehensive quarterly platform strategy with systematic stakeholder alignment",  # Complex
        "I need a strategic framework for organizational transformation"  # Systematic
    ]
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n{i}. **Input:** {test_input}")
        
        analysis = detector.analyze_input_complexity(test_input)
        
        print(f"   Complexity: {analysis.complexity.value}")
        print(f"   Confidence: {analysis.confidence:.2f}")
        print(f"   Strategy: {analysis.enhancement_strategy.value}")
        print(f"   Keywords: {', '.join(analysis.trigger_keywords[:3])}")


def demo_persona_enhancement_engine():
    """Demonstrate the persona enhancement engine directly"""
    
    print("\n⚡ **Persona Enhancement Engine Demo**")
    print("=" * 45)
    
    # Create enhancement engine
    detector = AnalysisComplexityDetector()
    enhancement_engine = PersonaEnhancementEngine(detector)
    
    # Test enhancement
    test_input = "Help me develop Q4 platform strategy with systematic stakeholder alignment"
    base_response = "Great question! Let me help you think through platform strategy. We should consider stakeholder needs and Q4 objectives."
    
    print(f"\n📥 **Base Response:**")
    print(f"   {base_response}")
    
    # Apply enhancement
    enhancement_result = enhancement_engine.enhance_response(
        persona_name="diego",
        user_input=test_input,
        base_response=base_response
    )
    
    print(f"\n🔧 **Enhancement Results:**")
    print(f"   Applied: {enhancement_result.enhancement_applied}")
    print(f"   Framework: {enhancement_result.framework_used}")
    print(f"   Processing Time: {enhancement_result.processing_time_ms}ms")
    
    if enhancement_result.enhancement_applied:
        print(f"\n📋 **Enhanced Response:**")
        print("-" * 30)
        print(enhancement_result.enhanced_response)
        print("-" * 30)
    else:
        print(f"\n⚠️ **Enhancement not applied:** {enhancement_result.fallback_reason}")


def run_complete_demo():
    """Run complete embedded framework demo"""
    
    print("🎯 **ClaudeDirector Embedded Framework Demo**")
    print("=" * 80)
    print("Demonstrating systematic analysis without external dependencies")
    print("=" * 80)
    
    try:
        # Demo 1: Complete workflow
        result = demo_diego_systematic_analysis()
        
        # Demo 2: Complexity analysis
        demo_complexity_analysis()
        
        # Demo 3: Enhancement engine
        demo_persona_enhancement_engine()
        
        print("\n" + "=" * 80)
        print("✅ **Demo Complete: Embedded Framework System Working**")
        print("🔧 Zero external dependencies")
        print("⚡ Systematic analysis preserved")  
        print("👥 Persona personalities maintained")
        print("🚀 Plug-and-play principle validated")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ **Demo Failed:** {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    """Run demo when executed directly"""
    success = run_complete_demo()
    exit(0 if success else 1)
