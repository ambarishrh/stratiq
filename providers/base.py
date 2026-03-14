"""
Base provider interface — all providers must implement scan() and generate()
"""

from abc import ABC, abstractmethod


class ProviderError(Exception):
    """Raised when a provider API call fails."""
    pass


class BaseProvider(ABC):

    @abstractmethod
    def scan(self, url: str, api_key: str) -> dict:
        """
        Scan a company URL and return structured intelligence signals.

        Returns:
            {
                "company": { name, industry, region, size, growth_stage, growth_signal },
                "sources": [ { icon, label, url, signals: [{id, cat, text}] } ]
            }
        """
        pass

    @abstractmethod
    def generate(self, context: dict, api_key: str) -> dict:
        """
        Generate full strategy from wizard context.

        Context keys:
            company_name, industry, region, size, growth, url,
            audience, frameworks (list), signals_text, inventory,
            gaps, org_context (list)

        Returns:
            {
                "dashboard": { vision, risk_domains, pillars, kpis, framework_alignment },
                "roadmap":   { phases, risk_without_roadmap, roi_note },
                "document":  { doc_ref, period, executive_summary, strategic_context,
                               vision_statement, pillars, governance, success_metrics, attribution }
            }
        """
        pass
