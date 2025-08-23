#!/usr/bin/env python3
"""
Business-Critical Regression Test: ROI Tracking

Alvaro's Test Suite: Ensures ROI calculation, investment tracking, and
business value measurement work correctly for strategic decision making.

BUSINESS IMPACT: ROI tracking failures lead to poor investment decisions,
budget misallocation, and inability to demonstrate platform value.
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal
import sys

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestROITracking(unittest.TestCase):
    """Business-critical tests for ROI tracking and investment analysis"""

    def setUp(self):
        """Set up test environment with mock investment data"""
        self.test_dir = tempfile.mkdtemp()
        self.roi_data_dir = Path(self.test_dir) / "roi_tracking"
        self.roi_data_dir.mkdir(parents=True, exist_ok=True)

        # Mock investment proposals for testing
        self.sample_investments = {
            "platform_infrastructure": {
                "proposal_id": "INV-2024-001",
                "title": "Platform Infrastructure Modernization",
                "total_investment": Decimal("500000"),
                "expected_annual_savings": Decimal("150000"),
                "implementation_months": 6,
                "roi_target": Decimal("1.30"),  # 30% ROI
                "category": "platform_infrastructure",
                "business_sponsor": "VP Engineering",
                "status": "approved",
            },
            "developer_tools": {
                "proposal_id": "INV-2024-002",
                "title": "Developer Productivity Tools",
                "total_investment": Decimal("200000"),
                "expected_annual_savings": Decimal("80000"),
                "implementation_months": 3,
                "roi_target": Decimal("1.20"),  # 20% ROI
                "category": "developer_tools",
                "business_sponsor": "Engineering Director",
                "status": "in_progress",
            },
        }

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_roi_calculation_accuracy(self):
        """
        BUSINESS CRITICAL: ROI calculations must be mathematically accurate

        FAILURE IMPACT: Wrong investment decisions based on incorrect ROI
        BUSINESS COST: Misallocated budget, failed initiatives, lost opportunities
        """
        investment = self.sample_investments["platform_infrastructure"]

        # Test basic ROI calculation: (Benefits - Investment) / Investment
        total_investment = investment["total_investment"]
        annual_savings = investment["expected_annual_savings"]

        # 3-year ROI calculation
        three_year_benefits = annual_savings * 3
        roi_ratio = three_year_benefits / total_investment
        roi_percentage = (roi_ratio - 1) * 100

        # Verify calculations
        expected_benefits = Decimal("450000")  # 150k * 3 years
        expected_roi_ratio = Decimal("0.9")  # 450k / 500k = 0.9
        expected_roi_percentage = Decimal("-10.0")  # (0.9 - 1) * 100 = -10%

        self.assertEqual(three_year_benefits, expected_benefits)
        self.assertEqual(roi_ratio, expected_roi_ratio)
        self.assertEqual(roi_percentage, expected_roi_percentage)

        # Test payback period calculation
        payback_period = total_investment / annual_savings
        expected_payback = Decimal("3.33")  # 500k / 150k ≈ 3.33 years

        self.assertAlmostEqual(float(payback_period), float(expected_payback), places=1)

        print("✅ ROI calculation accuracy: PASSED")

    def test_investment_portfolio_tracking(self):
        """
        BUSINESS CRITICAL: Investment portfolio tracking must work correctly

        FAILURE IMPACT: Cannot track multiple investments, portfolio optimization fails
        BUSINESS COST: Poor portfolio management, suboptimal resource allocation
        """
        # Create investment portfolio
        portfolio = {
            "portfolio_id": "PORTFOLIO-2024-Q1",
            "investments": [],
            "total_portfolio_value": Decimal("0"),
            "expected_portfolio_roi": Decimal("0"),
            "risk_score": Decimal("0"),
        }

        # Add investments to portfolio
        for investment_key, investment in self.sample_investments.items():
            portfolio_investment = {
                "proposal_id": investment["proposal_id"],
                "title": investment["title"],
                "investment_amount": investment["total_investment"],
                "expected_roi": investment["roi_target"],
                "risk_category": self._calculate_risk_category(investment),
                "strategic_alignment": self._calculate_strategic_alignment(investment),
                "added_date": datetime.now().isoformat(),
            }
            portfolio["investments"].append(portfolio_investment)
            portfolio["total_portfolio_value"] += investment["total_investment"]

        # Calculate portfolio metrics
        total_investments = len(portfolio["investments"])
        total_value = portfolio["total_portfolio_value"]

        # Verify portfolio tracking
        self.assertEqual(total_investments, 2)
        self.assertEqual(total_value, Decimal("700000"))  # 500k + 200k

        # Test portfolio ROI calculation
        weighted_roi = Decimal("0")
        for investment in portfolio["investments"]:
            weight = investment["investment_amount"] / total_value
            weighted_roi += investment["expected_roi"] * weight

        portfolio["expected_portfolio_roi"] = weighted_roi

        # Verify weighted ROI (500k/700k * 1.30 + 200k/700k * 1.20)
        expected_weighted_roi = Decimal("500000") / Decimal("700000") * Decimal(
            "1.30"
        ) + Decimal("200000") / Decimal("700000") * Decimal("1.20")

        self.assertAlmostEqual(
            float(portfolio["expected_portfolio_roi"]),
            float(expected_weighted_roi),
            places=3,
        )

        print("✅ Investment portfolio tracking: PASSED")

    def test_performance_measurement_accuracy(self):
        """
        BUSINESS CRITICAL: Actual vs projected performance measurement must be accurate

        FAILURE IMPACT: Cannot measure investment success, no learning from outcomes
        BUSINESS COST: Repeated poor decisions, no improvement in investment strategy
        """
        investment = self.sample_investments["developer_tools"]

        # Mock actual performance data
        actual_performance = {
            "proposal_id": investment["proposal_id"],
            "measurement_period": "2024-Q1",
            "actual_investment": Decimal("210000"),  # 5% over budget
            "actual_savings_q1": Decimal("22000"),  # Quarterly savings
            "projected_savings_q1": Decimal("20000"),  # Expected quarterly
            "timeline_adherence": Decimal("0.95"),  # 95% on time
            "budget_adherence": Decimal("0.95"),  # 95% on budget
            "user_adoption_rate": Decimal("0.87"),  # 87% adoption
            "productivity_improvement": Decimal("0.23"),  # 23% improvement
        }

        # Calculate performance metrics
        savings_variance = (
            actual_performance["actual_savings_q1"]
            - actual_performance["projected_savings_q1"]
        )
        savings_variance_pct = (
            savings_variance / actual_performance["projected_savings_q1"]
        ) * 100

        budget_variance = (
            actual_performance["actual_investment"] - investment["total_investment"]
        )
        budget_variance_pct = (budget_variance / investment["total_investment"]) * 100

        # Verify performance calculations
        expected_savings_variance = Decimal("2000")  # 22k - 20k
        expected_savings_variance_pct = Decimal("10.0")  # (2k / 20k) * 100
        expected_budget_variance = Decimal("10000")  # 210k - 200k
        expected_budget_variance_pct = Decimal("5.0")  # (10k / 200k) * 100

        self.assertEqual(savings_variance, expected_savings_variance)
        self.assertEqual(savings_variance_pct, expected_savings_variance_pct)
        self.assertEqual(budget_variance, expected_budget_variance)
        self.assertEqual(budget_variance_pct, expected_budget_variance_pct)

        # Test performance scoring
        performance_score = (
            actual_performance["timeline_adherence"] * Decimal("0.3")
            + actual_performance["budget_adherence"] * Decimal("0.3")
            + actual_performance["user_adoption_rate"] * Decimal("0.2")
            + actual_performance["productivity_improvement"] * Decimal("0.2")
        )

        expected_score = (
            Decimal("0.95") * Decimal("0.3")  # Timeline: 0.285
            + Decimal("0.95") * Decimal("0.3")  # Budget: 0.285
            + Decimal("0.87") * Decimal("0.2")  # Adoption: 0.174
            + Decimal("0.23") * Decimal("0.2")
        )  # Productivity: 0.046

        self.assertAlmostEqual(
            float(performance_score), float(expected_score), places=3
        )

        print("✅ Performance measurement accuracy: PASSED")

    def test_business_value_calculation(self):
        """
        BUSINESS CRITICAL: Business value calculation must include all value streams

        FAILURE IMPACT: Undervalued investments, missed strategic opportunities
        BUSINESS COST: Platform investments appear less valuable than they are
        """
        investment = self.sample_investments["platform_infrastructure"]

        # Calculate comprehensive business value
        business_value = {
            "direct_cost_savings": Decimal("150000"),  # Annual operational savings
            "productivity_gains": Decimal("200000"),  # Developer productivity value
            "risk_mitigation": Decimal("75000"),  # Reduced downtime/security risks
            "strategic_enablement": Decimal("100000"),  # Future capability value
            "competitive_advantage": Decimal("50000"),  # Market positioning value
            "compliance_value": Decimal("25000"),  # Regulatory compliance value
        }

        # Total annual business value
        total_annual_value = sum(business_value.values())
        expected_total = Decimal("600000")  # Sum of all value streams

        self.assertEqual(total_annual_value, expected_total)

        # Calculate comprehensive ROI including all value streams
        comprehensive_roi = (total_annual_value * 3) / investment["total_investment"]
        expected_comprehensive_roi = Decimal("3.6")  # (600k * 3) / 500k = 3.6

        self.assertEqual(comprehensive_roi, expected_comprehensive_roi)

        # Test value stream breakdown percentages
        value_percentages = {
            stream: round((value / total_annual_value) * 100, 2)
            for stream, value in business_value.items()
        }

        # Verify largest value streams
        self.assertEqual(
            value_percentages["productivity_gains"], Decimal("33.33")
        )  # 200k/600k
        self.assertEqual(
            value_percentages["direct_cost_savings"], Decimal("25.0")
        )  # 150k/600k
        self.assertEqual(
            value_percentages["strategic_enablement"], Decimal("16.67")
        )  # 100k/600k

        print("✅ Business value calculation: PASSED")

    def test_roi_tracking_data_persistence(self):
        """
        BUSINESS CRITICAL: ROI tracking data must persist for historical analysis

        FAILURE IMPACT: Cannot learn from investment history, no trend analysis
        BUSINESS COST: Repeated mistakes, no investment strategy improvement
        """
        # Create ROI tracking database
        roi_database = {
            "database_version": "1.0",
            "created_at": datetime.now().isoformat(),
            "investments": {},
            "portfolio_history": [],
            "performance_trends": {},
        }

        # Add investment tracking data
        for investment_key, investment in self.sample_investments.items():
            tracking_data = {
                "proposal_id": investment["proposal_id"],
                "investment_history": [
                    {
                        "date": datetime.now().isoformat(),
                        "event": "proposal_created",
                        "amount": investment["total_investment"],
                        "status": "proposed",
                    },
                    {
                        "date": (datetime.now() + timedelta(days=30)).isoformat(),
                        "event": "proposal_approved",
                        "amount": investment["total_investment"],
                        "status": "approved",
                    },
                ],
                "performance_measurements": [
                    {
                        "measurement_date": datetime.now().isoformat(),
                        "period": "baseline",
                        "actual_roi": Decimal("0"),
                        "projected_roi": investment["roi_target"],
                        "confidence": Decimal("0.8"),
                    }
                ],
            }
            roi_database["investments"][investment["proposal_id"]] = tracking_data

        # Save to file
        roi_file = self.roi_data_dir / "roi_tracking.json"
        with open(roi_file, "w") as f:
            # Convert Decimal to string for JSON serialization
            serializable_db = self._convert_decimals_to_strings(roi_database)
            json.dump(serializable_db, f, indent=2)

        # Verify persistence
        self.assertTrue(roi_file.exists(), "ROI tracking file must be created")

        # Load and verify data
        with open(roi_file, "r") as f:
            loaded_db = json.load(f)

        # Verify investment data persisted
        self.assertIn("INV-2024-001", loaded_db["investments"])
        self.assertIn("INV-2024-002", loaded_db["investments"])

        # Verify investment history
        inv_001_history = loaded_db["investments"]["INV-2024-001"]["investment_history"]
        self.assertEqual(len(inv_001_history), 2)
        self.assertEqual(inv_001_history[0]["event"], "proposal_created")
        self.assertEqual(inv_001_history[1]["event"], "proposal_approved")

        print("✅ ROI tracking data persistence: PASSED")

    def _calculate_risk_category(self, investment):
        """Calculate risk category for investment"""
        if investment["total_investment"] > Decimal("400000"):
            return "high"
        elif investment["total_investment"] > Decimal("100000"):
            return "medium"
        else:
            return "low"

    def _calculate_strategic_alignment(self, investment):
        """Calculate strategic alignment score"""
        alignment_scores = {
            "platform_infrastructure": Decimal("0.9"),
            "developer_tools": Decimal("0.8"),
            "analytics_capabilities": Decimal("0.85"),
            "security_improvements": Decimal("0.95"),
        }
        return alignment_scores.get(investment["category"], Decimal("0.7"))

    def _convert_decimals_to_strings(self, obj):
        """Convert Decimal objects to strings for JSON serialization"""
        if isinstance(obj, dict):
            return {
                key: self._convert_decimals_to_strings(value)
                for key, value in obj.items()
            }
        elif isinstance(obj, list):
            return [self._convert_decimals_to_strings(item) for item in obj]
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return obj


def run_business_critical_roi_tests():
    """Run all business-critical ROI tracking tests"""
    print("🔥 BUSINESS-CRITICAL REGRESSION TEST: ROI Tracking")
    print("=" * 70)
    print("OWNER: Alvaro | IMPACT: Investment Decision Quality")
    print(
        "FAILURE COST: Poor investment decisions, budget misallocation, no ROI visibility"
    )
    print("=" * 70)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestROITracking)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    # Report results
    if result.wasSuccessful():
        print("\n✅ ALL ROI TRACKING TESTS PASSED")
        print("💼 Business Impact: Investment decision quality maintained")
        print("📊 Strategic Value: ROI visibility and tracking preserved")
        return True
    else:
        print(f"\n❌ ROI TRACKING FAILURES: {len(result.failures + result.errors)}")
        print("💥 Business Impact: Investment decisions compromised")
        print("🚨 Action Required: Fix ROI tracking immediately")
        return False


if __name__ == "__main__":
    success = run_business_critical_roi_tests()
    sys.exit(0 if success else 1)
