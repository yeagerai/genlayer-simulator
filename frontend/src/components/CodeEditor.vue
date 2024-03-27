<script setup lang="ts">
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api';
import { onUnmounted } from 'vue';
import { onMounted, ref, shallowRef, watchEffect } from 'vue'

const editorElement = ref(null)
const editor = shallowRef<monaco.editor.IStandaloneCodeEditor | null>(null)
const props = defineProps<{
  content?: string
}>()
let unwatch: () => void | null
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
onMounted(() => {
  // the instance has already been loaded
  if (editor.value) return
  unwatch = watchEffect(() => {
    editor.value = monaco.editor.create(editorElement.value!, {
      value: contract,
      language: 'python',
      theme: 'vs-dark',
      automaticLayout: true,
      formatOnPaste: true,
      formatOnType: true
    });
  })
})



onUnmounted(() => {
  if (unwatch) {
    unwatch()
  }
})

watchEffect(() => {
  if (props.content) {
    editor.value?.setValue(props.content);
  }
})
</script>
<template>
  <v-card>
    <v-toolbar density="compact">
      <v-spacer></v-spacer>


      <v-tooltip text="New File">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon>
            <v-icon>mdi-file</v-icon>
          </v-btn>
        </template>
      </v-tooltip>
      <v-tooltip text="Upload">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon>
            <v-icon>mdi-upload</v-icon>
          </v-btn>
        </template>
      </v-tooltip>

      <v-tooltip text="Compile">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon>
            <v-icon>mdi-play</v-icon>
          </v-btn>
        </template>
      </v-tooltip>

      <v-tooltip text="Deploy">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" icon>
            <v-icon>mdi-cog-play</v-icon>
          </v-btn>
        </template>
      </v-tooltip>
    </v-toolbar>
    <div class="editor" ref="editorElement"> </div>
  </v-card>
</template>
<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
