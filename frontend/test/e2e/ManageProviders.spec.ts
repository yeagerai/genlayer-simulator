import { By, until, WebDriver } from 'selenium-webdriver';

import { SettingsPage } from '../pages/SettingsPage.js';
import { ContractsPage } from '../pages/ContractsPage.js';
import { before, describe, after, it } from 'node:test';
import { expect } from 'chai';
import { getDriver } from '../utils/driver.js';

let driver: WebDriver;
let settingsPage: SettingsPage;
let contractsPage: ContractsPage;

const providerParams = {
  provider: '0-custom-provider',
  model: '0-custom-model',
  plugin: 'openai',
};

describe('Settings - Manage Providers', () => {
  before(async () => {
    driver = await getDriver();
    settingsPage = new SettingsPage(driver);
    contractsPage = new ContractsPage(driver);
  });

  it('should create, update and delete a custom provider', async () => {
    await contractsPage.navigate();
    await contractsPage.waitUntilVisible();
    await contractsPage.skipTutorial();

    await settingsPage.navigate();
    await settingsPage.waitUntilVisible();

    const initialProviders = await settingsPage.getProvidersElements();

    // Create
    await settingsPage.createCustomProvider(providerParams);

    const newProviders = await settingsPage.getProvidersElements();

    expect(
      newProviders.length,
      'number of providers should be greather than old providers list',
    ).be.greaterThan(initialProviders.length);

    const newProvider = await settingsPage.getFirstProviderWithModelText(
      providerParams.model,
    );

    expect(newProvider, 'newProvider should be found').to.exist;

    if (!newProvider) {
      throw new Error('newProvider not found');
    }

    // Update

    await newProvider.click();
    await driver.sleep(500);

    const updateProviderBtn = await driver.wait(
      until.elementLocated(
        By.xpath("//button[@data-testid='btn-update-provider']"),
      ),
    );

    await updateProviderBtn.click();
    await driver.sleep(500);
  });

  it('should delete the custom provider', async () => {
    const existingProviders = await settingsPage.getProvidersElements();

    const existingProvidersLength = existingProviders.length;
    expect(
      existingProvidersLength,
      'number of providers should be greather than 0',
    ).be.greaterThan(0);

    const customProvider = existingProviders[0];

    if (!customProvider) {
      throw new Error('customProvider not found');
    }

    await driver.actions().move({ origin: customProvider }).perform();
    await driver.sleep(1000);

    const deleteProviderBtn = await customProvider.findElement(
      By.xpath("//button[@data-testid='provider-item-delete']"),
    );

    await deleteProviderBtn.click();
    await driver.sleep(1000);

    const confirmDeleteProviderBtn = await customProvider.findElement(
      By.xpath("//button[@data-testid='provider-item-confirm-delete']"),
    );
    // call delete validator button
    await confirmDeleteProviderBtn.click();

    const providers = await driver.findElements(
      By.xpath("//button[@data-testid = 'provider-item']"),
    );

    expect(
      providers.length,
      'providers length should be less than initial providers length',
    ).be.lessThan(existingProvidersLength);
  });

  after(() => driver.quit());
});
