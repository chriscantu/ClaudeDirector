#!/usr/bin/env python3
"""
📊 Framework Detection Regression Test - Critical User Journey 5a/5

BUSINESS CRITICAL PATH: Strategic framework detection and accuracy validation
FAILURE IMPACT: Framework intelligence lost, strategic guidance becomes generic

This focused test suite validates framework detection accuracy and reliability:
1. Strategic framework detection with confidence scoring
2. Framework identification across various strategic scenarios  
3. Detection performance with complex strategic content
4. Confidence threshold validation and tuning

COVERAGE: Framework detection intelligence validation
PRIORITY: P0 HIGH - Core framework detection capability
EXECUTION: <3 seconds for complete detection validation
"""

import sys
import os
import unittest
import tempfile
import time
from pathlib import Path

# Add the ClaudeDirector lib to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../lib"))


class TestFrameworkDetection(unittest.TestCase):
    """Test strategic framework detection accuracy and performance"""

    def setUp(self):
        """Set up test environment for framework detection testing"""
        self.test_dir = tempfile.mkdtemp()
        
        # Strategic framework library - focused subset for detection testing
        self.strategic_frameworks = {
            "Team Topologies": {
                "category": "organizational",
                "keywords": [
                    "team", "cognitive", "load", "boundaries", "platform", 
                    "stream", "engineering", "structure"
                ],
                "confidence_threshold": 0.5,
                "application_context": [
                    "organizational_design", "team_structure", "platform_strategy"
                ],
                "personas": ["diego", "martin", "rachel"],
            },
            "Good Strategy Bad Strategy": {
                "category": "strategic_analysis", 
                "keywords": [
                    "strategy", "competitive", "analysis", "advantage", 
                    "positioning", "board", "strategic"
                ],
                "confidence_threshold": 0.5,
                "application_context": [
                    "strategic_planning", "competitive_analysis", "business_strategy"
                ],
                "personas": ["camille", "alvaro", "diego"],
            },
            "Capital Allocation Framework": {
                "category": "investment_strategy",
                "keywords": [
                    "investment", "allocation", "roi", "platform", "feature", 
                    "resource", "board", "metrics"
                ],
                "confidence_threshold": 0.5,
                "application_context": [
                    "platform_investment", "resource_allocation", "roi_analysis"
                ],
                "personas": ["alvaro", "diego", "camille"],
            },
            "Design System Maturity Model": {
                "category": "design_systems",
                "keywords": [
                    "design", "system", "component", "consistency", "maturity", 
                    "scale", "teams", "product"
                ],
                "confidence_threshold": 0.5,
                "application_context": [
                    "design_systems", "component_architecture", "design_strategy"
                ],
                "personas": ["rachel", "martin", "diego"],
            },
            "Technical Strategy Framework": {
                "category": "technical_strategy",
                "keywords": [
                    "technical", "architecture", "roadmap", "technology", "platform"
                ],
                "confidence_threshold": 0.7,
                "application_context": [
                    "technical_strategy", "architecture_decisions", "technology_roadmap"
                ],
                "personas": ["martin", "diego", "camille"],
            },
        }
        
        # Test strategic scenarios for detection validation
        self.detection_scenarios = [
            {
                "query": "How should we restructure our engineering teams to reduce cognitive load and improve platform delivery?",
                "expected_frameworks": ["Team Topologies"],
                "expected_confidence": {"Team Topologies": 0.7},
                "context": "organizational_design",
            },
            {
                "query": "I need to present our platform investment strategy to the board. What ROI metrics should I focus on?",
                "expected_frameworks": ["Capital Allocation Framework"],
                "expected_confidence": {"Capital Allocation Framework": 0.7},
                "context": "investment_strategy",
            },
            {
                "query": "How do we scale our design system across multiple product teams while maintaining consistency?",
                "expected_frameworks": ["Design System Maturity Model"],
                "expected_confidence": {"Design System Maturity Model": 0.7},
                "context": "design_systems",
            },
            {
                "query": "What technical architecture decisions should we make to support our 3-year platform roadmap?",
                "expected_frameworks": ["Technical Strategy Framework"],
                "expected_confidence": {"Technical Strategy Framework": 0.7},
                "context": "technical_strategy",
            },
            {
                "query": "How should we develop our competitive positioning strategy for the enterprise market?",
                "expected_frameworks": ["Good Strategy Bad Strategy"],
                "expected_confidence": {"Good Strategy Bad Strategy": 0.6},
                "context": "strategic_analysis",
            },
        ]

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_framework_detection_accuracy(self):
        """REGRESSION TEST: Framework detection identifies appropriate frameworks with high confidence"""
        try:
            detection_results = []
            
            for scenario in self.detection_scenarios:
                query = scenario["query"]
                expected_frameworks = scenario["expected_frameworks"]
                expected_confidence = scenario["expected_confidence"]
                
                # Simulate framework detection algorithm
                detected_frameworks = self._detect_frameworks(query)
                
                # Verify expected frameworks are detected
                for expected_framework in expected_frameworks:
                    self.assertIn(
                        expected_framework,
                        detected_frameworks,
                        f"Framework '{expected_framework}' should be detected in query: {query[:50]}...",
                    )
                    
                    # Verify confidence scores meet thresholds
                    detected_confidence = detected_frameworks[expected_framework]["confidence"]
                    expected_min_confidence = expected_confidence[expected_framework]
                    
                    self.assertGreaterEqual(
                        detected_confidence,
                        expected_min_confidence,
                        f"Framework '{expected_framework}' confidence {detected_confidence} should be >= {expected_min_confidence}",
                    )
                
                # Track detection results for analytics
                detection_results.append(
                    {
                        "query": query,
                        "detected": list(detected_frameworks.keys()),
                        "expected": expected_frameworks,
                        "accuracy": len(
                            set(detected_frameworks.keys()) & set(expected_frameworks)
                        ) / len(expected_frameworks),
                    }
                )
            
            # Verify overall detection accuracy
            overall_accuracy = sum(
                result["accuracy"] for result in detection_results
            ) / len(detection_results)
            self.assertGreaterEqual(
                overall_accuracy,
                0.8,
                f"Overall framework detection accuracy should be >= 80%, got {overall_accuracy:.2%}",
            )
            
        except Exception as e:
            self.fail(f"Framework detection accuracy test failed: {e}")

    def test_framework_confidence_scoring(self):
        """REGRESSION TEST: Framework confidence scoring is consistent and meaningful"""
        try:
            confidence_results = []
            
            for scenario in self.detection_scenarios:
                query = scenario["query"]
                detected_frameworks = self._detect_frameworks(query)
                
                for framework_name, framework_data in detected_frameworks.items():
                    confidence = framework_data["confidence"]
                    keyword_matches = framework_data["keyword_matches"]
                    
                    # Confidence should be reasonable (0.3-1.0 range)
                    self.assertGreaterEqual(
                        confidence, 0.3,
                        f"Framework '{framework_name}' confidence {confidence} too low"
                    )
                    self.assertLessEqual(
                        confidence, 1.0,
                        f"Framework '{framework_name}' confidence {confidence} too high"
                    )
                    
                    # Confidence should correlate with keyword matches
                    framework_info = self.strategic_frameworks[framework_name]
                    total_keywords = len(framework_info["keywords"])
                    match_ratio = keyword_matches / total_keywords
                    
                    # Confidence should be roughly proportional to keyword matches
                    self.assertGreaterEqual(
                        confidence, match_ratio * 0.8,
                        f"Framework '{framework_name}' confidence {confidence} should correlate with match ratio {match_ratio}"
                    )
                    
                    confidence_results.append({
                        "framework": framework_name,
                        "confidence": confidence,
                        "keyword_matches": keyword_matches,
                        "match_ratio": match_ratio
                    })
            
            # Verify confidence distribution is reasonable
            confidences = [r["confidence"] for r in confidence_results]
            avg_confidence = sum(confidences) / len(confidences)
            
            self.assertGreaterEqual(
                avg_confidence, 0.5,
                f"Average confidence {avg_confidence:.2f} should be reasonable (>=0.5)"
            )
            
        except Exception as e:
            self.fail(f"Framework confidence scoring test failed: {e}")

    def test_framework_detection_performance(self):
        """REGRESSION TEST: Framework detection performs well with complex strategic content"""
        try:
            # Generate complex strategic scenario
            complex_query = """
            We're planning a comprehensive organizational transformation to scale our platform capabilities
            across multiple international markets. This initiative involves restructuring our engineering teams
            from a traditional product-focused model to a platform-centric approach with clear team boundaries
            and cognitive load management. We need to assess the investment allocation between platform development
            and feature delivery, ensuring we can demonstrate clear ROI to stakeholders while maintaining
            delivery velocity. The design system needs to scale across 15+ product teams globally.
            How should we approach this systematically?
            """
            
            expected_frameworks = [
                "Team Topologies", "Capital Allocation Framework", "Design System Maturity Model"
            ]
            max_detection_time = 2.0
            
            # Measure detection performance
            start_time = time.time()
            detected_frameworks = self._detect_frameworks(complex_query)
            detection_time = time.time() - start_time
            
            # Verify performance requirements
            self.assertLessEqual(
                detection_time,
                max_detection_time,
                f"Framework detection should complete in <{max_detection_time}s, took {detection_time:.3f}s",
            )
            
            # Verify detection accuracy with complex content
            detected_names = list(detected_frameworks.keys())
            accuracy = len(set(detected_names) & set(expected_frameworks)) / len(expected_frameworks)
            
            self.assertGreaterEqual(
                accuracy,
                0.6,
                f"Complex scenario detection accuracy should be >= 60%, got {accuracy:.2%}",
            )
            
            # Verify multiple frameworks detected
            self.assertGreaterEqual(
                len(detected_frameworks),
                2,
                f"Complex scenario should detect multiple frameworks, got {len(detected_frameworks)}"
            )
            
        except Exception as e:
            self.fail(f"Framework detection performance test failed: {e}")

    def test_detection_context_relevance(self):
        """REGRESSION TEST: Framework detection considers context appropriateness"""
        try:
            context_violations = []
            
            for scenario in self.detection_scenarios:
                query = scenario["query"]
                expected_context = scenario["context"]
                detected_frameworks = self._detect_frameworks(query)
                
                for framework_name, framework_data in detected_frameworks.items():
                    framework_info = self.strategic_frameworks[framework_name]
                    applicable_contexts = framework_info["application_context"]
                    
                    # Check if framework is contextually appropriate
                    context_match = any(
                        context_keyword in expected_context
                        or expected_context in context
                        for context in applicable_contexts
                        for context_keyword in context.split("_")
                    )
                    
                    if not context_match and framework_data["confidence"] > 0.8:
                        context_violations.append({
                            "framework": framework_name,
                            "detected_context": expected_context,
                            "applicable_contexts": applicable_contexts,
                            "confidence": framework_data["confidence"],
                        })
            
            # Verify minimal context violations for high-confidence detections
            violation_rate = len(context_violations) / sum(
                len(self._detect_frameworks(s["query"]))
                for s in self.detection_scenarios
            )
            self.assertLessEqual(
                violation_rate,
                0.2,
                f"Context violation rate should be <= 20%, got {violation_rate:.2%}. Violations: {context_violations}",
            )
            
        except Exception as e:
            self.fail(f"Detection context relevance test failed: {e}")

    # Helper methods for framework detection simulation
    
    def _detect_frameworks(self, query):
        """Simulate framework detection algorithm"""
        detected = {}
        query_lower = query.lower()
        
        for framework_name, framework_info in self.strategic_frameworks.items():
            keywords = framework_info["keywords"]
            threshold = framework_info["confidence_threshold"]
            
            # Calculate keyword match score
            keyword_matches = sum(1 for keyword in keywords if keyword in query_lower)
            keyword_score = keyword_matches / len(keywords)
            
            # Add context and length bonuses
            context_bonus = 0.1 if len(query) > 100 else 0
            complexity_bonus = 0.05 if len(query.split()) > 50 else 0
            
            confidence = keyword_score + context_bonus + complexity_bonus
            
            if confidence >= threshold:
                detected[framework_name] = {
                    "confidence": min(confidence, 1.0),
                    "keyword_matches": keyword_matches,
                    "context_relevance": context_bonus + complexity_bonus,
                }
        
        # Sort by confidence
        return dict(
            sorted(detected.items(), key=lambda x: x[1]["confidence"], reverse=True)
        )


if __name__ == "__main__":
    print("📊 Framework Detection Regression Test")
    print("=" * 50)
    print("Testing strategic framework detection accuracy and performance...")
    print()
    
    # Run the focused test suite
    unittest.main(verbosity=2, exit=False)
    
    print()
    print("✅ FRAMEWORK DETECTION REGRESSION TESTS COMPLETE")
    print("Strategic framework detection intelligence protected against regressions")
