# Types from our domain
# Trying to follow [hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) or layered architecture.
# These types should not depend on any other layer.

from dataclasses import dataclass


@dataclass()
class LLMProvider:
    provider: str
    model: str
    config: dict
    plugin: str
    plugin_config: dict
    id: int | None = None

    def __hash__(self):
        return hash(
            (
                self.id,
                self.provider,
                self.model,
                frozenset(self.config.items()),
                frozenset(self.plugin_config.items()),
            )
        )


@dataclass()
class Validator:
    address: str
    stake: int
    llmprovider: LLMProvider
    id: int | None = None

    def to_dict(self):
        result = {
            "address": self.address,
            "stake": self.stake,
            "provider": self.llmprovider.provider,
            "model": self.llmprovider.model,
            "config": self.llmprovider.config,
            "plugin": self.llmprovider.plugin,
            "plugin_config": self.llmprovider.plugin_config,
        }

        if self.id:
            result["id"] = self.id

        return result
