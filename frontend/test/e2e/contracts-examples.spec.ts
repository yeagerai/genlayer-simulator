import { WebDriver, By, until} from 'selenium-webdriver';
import { ContractsPage } from '../pages/ContractsPage.js';
import { RunDebugPage } from '../pages/RunDebugPage.js';
import { beforeEach, before, describe, after, it } from 'node:test';
import { expect } from 'chai';
import { getDriver } from '../utils/driver.js';

let driver: WebDriver;
let contractsPage: ContractsPage;
let runDebugPage: RunDebugPage;

describe('Contract examples', () => {
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

    it('should open Run debug page', async () => {
        await runDebugPage.navigate() 
        await runDebugPage.waitUntilVisible();

        const nameOfContract = await driver.wait(until.elementLocated(By.xpath("//div[contains(@class, 'text-xs text-neutral-800 dark:text-neutral-200') and contains(text(), 'wizard_of_coin.gpy')]",)), 5000)
        expect(nameOfContract, 'WizardOfCoin file name contract should be visible').not.null


        const haveCoinCheck = await driver.wait(until.elementLocated(By.xpath("//input[contains(@name, 'have_coin') and contains(@type, 'checkbox')]")), 5000)
        expect(haveCoinCheck, 'Have coin checkbox should be visible').not.null
        haveCoinCheck.click()
        

    })
    after(() => driver.quit());

})