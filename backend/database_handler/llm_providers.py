from backend.domain.types import LLMProvider
from backend.node.create_nodes.providers import get_default_providers
from .models import LLMProviderDBModel
from sqlalchemy.orm import Session


class LLMProviderRegistry:
    def __init__(self, session: Session):
        self.session = session

    def reset_defaults(self):
        """Reset all providers to their default values."""
        self.session.query(LLMProviderDBModel).delete()

        providers = get_default_providers()
        for provider in providers:
            self.session.add(_to_db_model(provider))

        self.session.commit()

    def get_all(self) -> list[LLMProvider]:
        return [
            _to_domain(provider)
            for provider in self.session.query(LLMProviderDBModel).all()
        ]


def _to_domain(db_model: LLMProvider) -> LLMProvider:
    return LLMProvider(
        provider=db_model.provider,
        model=db_model.model,
        config=db_model.config,
    )


def _to_db_model(domain: LLMProvider) -> LLMProviderDBModel:
    return LLMProviderDBModel(
        provider=domain.provider,
        model=domain.model,
        config=domain.config,
    )
