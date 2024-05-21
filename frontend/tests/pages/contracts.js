import { By, until } from 'selenium-webdriver';

export default class ContractsPage {
    baseurl = 'http://localhost:8080/simulator/contracts'
    constructor(driver) {
        this.driver = driver;

    }

    elements = {
        btnSkipTutorial: 'btn-skip-tutorial',
        listTitle: 'contracts-list-title',
        items: {
            llm_erc20: 'contract-item-llm_erc20.py',
            football_prediction_market: 'contract-item-football_prediction_market.py',
            user_storage: 'contract-item-user_storage.py',
            storage: 'contract-item-storage.py',
            wizard_of_coin: 'contract-item-tab-wizard_of_coin.py'
        },
        tabs: {
            llm_erc20: 'contract-tab-llm_erc20.py',
            football_prediction_market: 'contract-tab-football_prediction_market.py',
            user_storage: 'contract-tab-user_storage.py',
            storage: 'contract-tab-storage.py',
            wizard_of_coin: 'contract-tab-wizard_of_coin.py'
        }
    }

    waitUntilVisible() {
        return this.driver.wait(until.elementLocated(By.id(this.elements.listTitle)));
    }

    async skipTutorial() {
        await this.driver.wait(until.elementLocated(By.id(this.elements.btnSkipTutorial)), 5000)
        const btn = this.driver.findElement(By.id(this.elements.btnSkipTutorial))
        if(btn) {
            await btn.click()
        }
    }

    navigate() {
        return this.driver.navigate().to(this.baseurl);
    }

    openContract(contract) {
        return this.driver.findElement(By.id(this.elements.items[contract])).click();
    }
}