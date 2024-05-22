import { WebDriver } from 'selenium-webdriver';
import { ContractsPage } from '../pages/ContractsPage.js';
import { beforeEach, before, describe, afterEach, it } from 'node:test';
import { expect } from 'chai';
import { getDriver } from '../utils/driver.js';

let driver: WebDriver;
let contractsPage: ContractsPage;

describe('Contract examples', () => {
    before(async () => {
        driver = await getDriver();
        await driver.manage().setTimeouts({ implicit: 2000 });
        contractsPage = new ContractsPage(driver)
    })

    beforeEach(async () => {
        await contractsPage.navigate();
        await contractsPage.waitUntilVisible();
        await contractsPage.skipTutorial();
    })

    it('should load contract examples', async () => {
        const title = await driver.getTitle();

        await contractsPage.openContract('wizard_of_coin.gpy') 

        expect(title).equal("GenLayer - The Intelligence Layer of the Internet");
    })
    afterEach(() => driver.quit());

})