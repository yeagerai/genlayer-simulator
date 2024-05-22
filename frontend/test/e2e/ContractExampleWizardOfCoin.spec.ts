import { WebDriver, By, until} from 'selenium-webdriver';
import { ContractsPage } from '../pages/ContractsPage.js';
import { RunDebugPage } from '../pages/RunDebugPage.js';
import { beforeEach, before, describe, after, it } from 'node:test';
import { expect } from 'chai';
import { getDriver } from '../utils/driver.js';

let driver: WebDriver;
let contractsPage: ContractsPage;
let runDebugPage: RunDebugPage;

describe('Contract Example WizardOfCoin', () => {
    before(async () => {
        driver = await getDriver();
        await driver.manage().setTimeouts({ implicit: 2000 });
        contractsPage = new ContractsPage(driver)
        runDebugPage = new RunDebugPage(driver)
    })

    beforeEach(async () => {
    })

    it('should open WizardOfCoin example contract', async () => {
        await contractsPage.navigate();
        await contractsPage.waitUntilVisible();
        await contractsPage.skipTutorial();
        await contractsPage.openContract('wizard_of_coin.gpy')
        const tabs = await driver.findElements(By.xpath("//div[contains(@class, 'contract-item')]"))
        expect(tabs.length, 'Number of tabs should be 2').equal(2)
    })

    it('should open Run debug page and set constructor arguments for WizardOfCoin', async () => {
        await runDebugPage.navigate() 
        await runDebugPage.waitUntilVisible();

        const nameOfContract = await driver.wait(until.elementLocated(By.xpath("//div[contains(@class, 'text-xs text-neutral-800 dark:text-neutral-200') and contains(text(), 'wizard_of_coin.gpy')]",)), 5000)
        expect(nameOfContract, 'WizardOfCoin file name contract should be visible').not.null

        const haveCoinCheck = await driver.wait(until.elementLocated(By.xpath("//input[contains(@name, 'have_coin') and contains(@type, 'checkbox')]")), 5000)
        expect(haveCoinCheck, 'Have coin checkbox should be visible').not.null
        await haveCoinCheck.click()
    })

    it('should deploy the contract WizardOfCoin', async () => {
        await driver.wait(until.elementLocated(By.xpath("//button[text()='Deploy']")), 5000).click()
 
        // locate elements that should be visible
        const contractStateTitle = await driver.wait(until.elementLocated(By.xpath("//h5[contains(@class, 'text-sm') and contains(text(), 'Current Intelligent Contract State')]")), 5000)
        expect(contractStateTitle, 'Contract state title section should be visible').not.null

        const executeTransactionsTitle = await driver.wait(until.elementLocated(By.xpath("//h5[contains(@class, 'text-sm') and contains(text(), 'Execute Transactions')]")), 5000)
        expect(executeTransactionsTitle, 'Execute transactions title section should be visible').not.null

        const latestTransactions = await driver.wait(until.elementLocated(By.xpath("//h5[contains(@class, 'text-sm') and contains(text(), 'Latest Transactions')]")), 5000)
        expect(latestTransactions, 'Latest transactions title section should be visible').not.null
    })

    it('should call get_have_coin', async () => {
        await driver.wait(until.elementLocated(By.xpath("//button[text()='get_have_coin']")), 5000).click();
 
        const stateResult = await driver.wait(until.elementLocated(By.xpath("//div[@data-test-id='contract-state-item-get_have_coin']")), 5000);
        
        expect(stateResult, 'get_have_coin result should be visible').not.null;
        
        //TODO:  validate result content
    })
    after(() => driver.quit());

})