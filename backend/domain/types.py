# Types from our domain
# Trying to follow [hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) or layered architecture.
# These types should not depend on any other layer.

from dataclasses import dataclass


@dataclass()
class LLMProvider:
    provider: str
    model: str
    config: dict

    def __hash__(self):
        return hash((self.provider, self.model, frozenset(self.config.items())))
