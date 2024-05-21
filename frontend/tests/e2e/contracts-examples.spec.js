import { Builder, Browser } from 'selenium-webdriver';
import ContractsPage from '../pages/contracts.js';
import { beforeEach, before, describe, afterEach, it } from 'node:test';
import { expect } from 'chai';
let driver;
let contractsPage;

describe('Contract examples', () => {
    before(async () => {
        driver = await new Builder().forBrowser(Browser.CHROME).build();
        contractsPage = new ContractsPage(driver)
    })

    beforeEach(async () => {
        await contractsPage.navigate();
        await contractsPage.skipTutorial();
    })

    it('should load contract examples', async () => {
        let title = await driver.getTitle();

        expect(title).equal("GenLayer - The Intelligence Layer of the Internet");
    })
    afterEach(() => driver.quit());

})