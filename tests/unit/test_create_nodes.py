import asyncio
from typing import Callable, List, Optional
import pytest
from backend.domain.types import LLMProvider
from backend.node.create_nodes.create_nodes import random_validator_config
from backend.node.genvm.llms import Plugin


def plugin_mock(available: bool, available_models: List[str]) -> Plugin:
    class PluginMock(Plugin):
        def __init__(self, plugin_config: dict):
            pass

        async def call(
            self,
            node_config: dict,
            prompt: str,
            regex: Optional[str],
            return_streaming_channel: Optional[asyncio.Queue],
        ) -> str:
            pass

        def is_available(self):
            return available

        def is_model_available(self, model: str) -> bool:
            return model in available_models

    return PluginMock({})


@pytest.mark.parametrize(
    "stored_providers,plugins,limit_providers,limit_models,amount,expected",
    [
        pytest.param(
            [
                LLMProvider(
                    provider="ollama",
                    model="llama3",
                    config={},
                    plugin="ollama",
                    plugin_config={},
                )
            ],
            {"ollama": plugin_mock(True, ["llama3"])},
            None,
            None,
            10,
            [
                LLMProvider(
                    provider="ollama",
                    model="llama3",
                    config={},
                    plugin="ollama",
                    plugin_config={},
                )
            ],
            id="only ollama",
        ),
        # pytest.param(
        #     ["llama3", "llama3.1"],
        #     [
        #         LLMProvider(
        #             provider="ollama",
        #             model="llama3.1",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4o",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #     ],
        #     None,
        #     None,
        #     10,
        #     {"OPENAI_API_KEY": ""},
        #     [
        #         LLMProvider(
        #             provider="ollama",
        #             model="llama3.1",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         )
        #     ],
        #     id="only ollama available",
        # ),
        # pytest.param(
        #     ["llama3", "llama3.1"],
        #     [
        #         LLMProvider(
        #             provider="ollama",
        #             model="llama3",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4o",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="a",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="b",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #     ],
        #     ["openai"],
        #     None,
        #     10,
        #     {"OPENAIKEY": "filled"},
        #     [
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4o",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #     ],
        #     id="only openai",
        # ),
        # pytest.param(
        #     ["llama3", "llama3.1"],
        #     [
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4o",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="a",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="b",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #     ],
        #     ["heuristai"],
        #     ["a"],
        #     10,
        #     {"OPENAI_API_KEY": "filled", "HEURISTAI_API_KEY": "filled"},
        #     [
        #         LLMProvider(
        #             provider="heuristai",
        #             model="a",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #     ],
        #     id="only heuristai",
        # ),
        # pytest.param(
        #     ["llama3", "llama3.1"],
        #     [
        #         LLMProvider(
        #             provider="ollama",
        #             model="llama3.1",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4o",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="a",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="b",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #     ],
        #     None,
        #     None,
        #     10,
        #     {"OPENAI_API_KEY": "filled", "HEURISTAI_API_KEY": "filled"},
        #     [
        #         LLMProvider(
        #             provider="ollama",
        #             model="llama3.1",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="openai",
        #             model="gpt-4o",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="a",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #         LLMProvider(
        #             provider="heuristai",
        #             model="b",
        #             config={},
        #             plugin="",
        #             plugin_config={},
        #         ),
        #     ],
        #     id="all available",
        # ),
    ],
)
def test_random_validator_config(
    stored_providers,
    plugins,
    limit_providers,
    limit_models,
    amount,
    expected,
):
    result = random_validator_config(
        lambda: stored_providers,
        lambda plugin, config: plugins[plugin],
        limit_providers,
        limit_models,
        amount,
    )

    assert set(result).issubset(set(expected))


# @pytest.mark.parametrize(
#     "available_ollama_models,stored_providers,limit_providers,limit_models,amount,environ,exception",
#     [
#         pytest.param(
#             [],
#             [
#                 LLMProvider(
#                     provider="ollama",
#                     model="llama3",
#                     config={},
#                     plugin="",
#                     plugin_config={},
#                 )
#             ],
#             ["heuristai", "openai"],
#             None,
#             10,
#             {},
#             ValueError,
#             id="no match",
#         ),
#         pytest.param(
#             [],
#             [
#                 LLMProvider(
#                     provider="ollama",
#                     model="llama3",
#                     config={},
#                     plugin="",
#                     plugin_config={},
#                 )
#             ],
#             ["ollama"],
#             None,
#             10,
#             {"OPENAI_API_KEY": "filled", "HEURISTAI_API_KEY": "filled"},
#             Exception,
#             id="no intersection",
#         ),
#     ],
# )
# def test_random_validator_config_fail(
#     available_ollama_models,
#     stored_providers,
#     limit_providers,
#     limit_models,
#     amount,
#     environ,
#     exception,
# ):
#     with pytest.raises(exception):
#         random_validator_config(
#             result=random_validator_config(
#                 lambda: available_ollama_models,
#                 lambda: stored_providers,
#                 limit_providers,
#                 limit_models,
#                 amount,
#                 environ,
#             )
#         )
