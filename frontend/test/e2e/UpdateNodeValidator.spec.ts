import { WebDriver, By, until } from 'selenium-webdriver';
import { Select } from 'selenium-webdriver/lib/select';
import { SettingsPage } from '../pages/SettingsPage.js';
import { ContractsPage } from '../pages/ContractsPage.js';
import { before, describe, after, it } from 'node:test';
import { expect } from 'chai';
import { getDriver } from '../utils/driver.js';

let driver: WebDriver;
let settingsPage: SettingsPage;
let contractsPage: ContractsPage;

describe('Settings - Update Node Validator', () => {
  before(async () => {
    driver = await getDriver();
    settingsPage = new SettingsPage(driver);
    contractsPage = new ContractsPage(driver);
  });

  it('should update an existing validator', async () => {
    await contractsPage.navigate();
    await contractsPage.waitUntilVisible();
    await contractsPage.skipTutorial();

    await settingsPage.navigate();
    await settingsPage.waitUntilVisible();

    await settingsPage.createValidator({
      provider: 'heuristai',
      model: 'mistralai/mixtral-8x7b-instruct',
      stake: 7,
    });
    const existingValidators = await settingsPage.getValidatorsElements();
    expect(
      existingValidators.length,
      'number of validators should be greather than 0',
    ).be.greaterThan(0);

    const validator = await existingValidators[0].findElement(
      By.xpath("//div[@data-testid = 'validator-item']"),
    );
    await validator.click();

    // provider select
    const selectProviderElement = await driver.wait(
      until.elementLocated(
        By.xpath("//select[contains(@data-testid, 'dropdown-provider')]"),
      ),
      2000,
    );
    const selectProvider = new Select(selectProviderElement);
    await selectProvider.selectByValue('ollama');

    // model select
    const selectModelElement = await driver.wait(
      until.elementLocated(
        By.xpath("//select[contains(@data-testid, 'dropdown-model')]"),
      ),
      2000,
    );
    const selectModel = new Select(selectModelElement);
    await selectModel.selectByValue('llama2');

    const stakeInput = await driver.wait(
      until.elementLocated(By.xpath("//input[@data-testid='input-stake']")),
      2000,
    );
    await stakeInput.clear();
    await stakeInput.sendKeys(8);

    const updateValidatorBtn = await driver.wait(
      until.elementLocated(
        By.xpath("//button[@data-testid='btn-update-validator']"),
      ),
      2000,
    );
    // call save validator button
    await updateValidatorBtn.click();

    driver.sleep(10000);
    const validators = await settingsPage.getValidatorsElements();
    const provider = await validators[0].findElement(
      By.xpath("//span[@data-testid = 'validator-item-provider']"),
    );
    const model = await validators[0].findElement(
      By.xpath("//span[@data-testid = 'validator-item-model']"),
    );
    const providerText = await provider.getText();
    const modelText = await model.getText();
    expect(providerText, 'provider should be ollama').be.equal('ollama');
    expect(modelText, 'model should be llama2').be.equal('llama2');
  });

  after(() => driver.quit());
});
