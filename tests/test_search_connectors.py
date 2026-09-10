import unittest
from market_research.search_connectors import (
    DuckDuckGoConnector,
    SerpAPIConnector,
    TavilyConnector,
    estimate_monthly_budget,
)


class TestSearchConnectors(unittest.TestCase):

    def test_duckduckgo_fallback(self):
        ddg = DuckDuckGoConnector()
        res = ddg.search("synthetic biology market size")
        self.assertGreaterEqual(len(res), 1)
        self.assertEqual(res[0].provider, "DuckDuckGo")
        self.assertEqual(ddg.cost_per_query(), 0.0)

    def test_serpapi_mock(self):
        serp = SerpAPIConnector()
        res = serp.search("agentic workflows")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].provider, "SerpAPI")
        self.assertEqual(serp.cost_per_query(), 0.01)

    def test_tavily_mock(self):
        tavily = TavilyConnector()
        res = tavily.search("ai voice interfaces")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].provider, "Tavily")
        self.assertEqual(tavily.cost_per_query(), 0.005)

    def test_estimate_monthly_budget(self):
        # 100 queries/day = 3000 queries/month
        budget = estimate_monthly_budget(100)
        self.assertEqual(budget["monthly_queries"], 3000)
        tavily_cost = budget["providers"]["Tavily"]["estimated_monthly_cost_usd"]
        # 3000 - 1000 free = 2000 * 0.005 = $10.00
        self.assertEqual(tavily_cost, 10.0)

        serp_cost = budget["providers"]["SerpAPI"]["estimated_monthly_cost_usd"]
        # 3000 - 100 free = 2900 * 0.01 = $29.00
        self.assertEqual(serp_cost, 29.0)


if __name__ == "__main__":
    unittest.main()
