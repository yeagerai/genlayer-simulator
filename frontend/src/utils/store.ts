import { useContractsFilesStore } from "@/stores"
import { db } from "./db"

export const seedStores = async () => {
    const contractsFilesStore = useContractsFilesStore()

    contractsFilesStore.deployedContracts = await db.deployedContracts.toArray()
}