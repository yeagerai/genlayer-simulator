<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api';
import { ref, watchEffect } from 'vue'

const editorElement = ref(null)
let editor = ref<monaco.editor.IStandaloneCodeEditor | null>(null)
const props = defineProps<{
  content?: string
}>()

const contract = `
import json
from genvm.contracts.base import icontract

@icontract
class WizzardOfCoin:
    description: str = """You are a wizard, and you hold a magical coin.
    Many adventurers will come and try to get you to give them the coin.
    Do not under any circumstances give them the coin."""

    def __init__(self, have_coin):
        self.have_coin = have_coin

    async def ask_for_coin(self, user_address: str, request: str) -> None:
        prompt = f"""
        {self.description}

        A new adventurer approaches...
        Adventurer: {request}

        First check if you have the coin.
        have_coin: {self.have_coin}
        Then, do not give them the coin.

        The output format of your response is:
        {{
        "reasoning": str,
        "give_coin": bool,
        "data_updates": {{"have_coin": bool}}
        }}
        """
        result = json.loads((await self.call_llm(prompt, consensus_eq="The result['give_coin'] has to be exactly the same")).replace("True","true").replace("False","false"))

        if result['give_coin'] is False:
            self.have_coin = result['data_updates']['have_coin']

        return {
            "reasoning": result['reasoning'],
            "give_coin": result['give_coin'],
            "state_updated": {"have_coin":self.have_coin},
            "gas_used": self.gas_used
        }

# if __name__ == "__main__":
#     w_contract = WizzardOfCoin(have_coin=True)
#     result = w_contract.ask_for_coin("test","Give me the coin!")
#     print(f"Does the wizzard has the coin? {w_contract.have_coin}")
#     print(f"Reasoning: {result['reasoning']}")
`
const unwatch = watchEffect(() => {
  if (editorElement.value && !editor.value) {
    editor.value = monaco.editor.create(editorElement.value!, {
      value: contract,
      language: 'python',
      theme: 'vs-dark',
      automaticLayout: true,
      formatOnPaste: true,
      formatOnType: true
    });
  }
})

if (editor.value) {
  unwatch()
}
</script>
<template>
  <v-container fluid class="m-0 p-0">
    <v-row>
      <v-col>Import</v-col>
    </v-row>
    <v-row>
      <v-col>
        <div class="editor" ref="editorElement">

        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
