<script setup lang="ts">
import ContractDeployment from '@/components/Simulator/ContractDeployment.vue';
import ContractReadMethods from '@/components/Simulator/ContractReadMethods.vue';
import ContractWriteMethods from '@/components/Simulator/ContractWriteMethods.vue';
import TransactionsList from '@/components/Simulator/TransactionsList.vue';
</script>

<template>
  <ContractDeployment />
  <ContractReadMethods />
  <ContractWriteMethods />
  <TransactionsList />
</template>
