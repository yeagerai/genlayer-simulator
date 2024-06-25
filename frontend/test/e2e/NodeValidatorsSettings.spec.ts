import { WebDriver, By, until, Select } from 'selenium-webdriver'

import { SettingsPage } from '../pages/SettingsPage.js'
import { ContractsPage } from '../pages/ContractsPage.js'
import { before, describe, after, it } from 'node:test'
import { expect } from 'chai'
import { getDriver } from '../utils/driver.js'

let driver: WebDriver
let settingsPage: SettingsPage
let contractsPage: ContractsPage

describe('Node Validators Settings', () => {
  before(async () => {
    driver = await getDriver()
    await driver.manage().setTimeouts({ implicit: 10000 })
    settingsPage = new SettingsPage(driver)
    contractsPage = new ContractsPage(driver)
  })

  it('should create a new validator', async () => {
    await contractsPage.navigate()
    await contractsPage.waitUntilVisible()
    await contractsPage.skipTutorial()

    await settingsPage.navigate()
    await settingsPage.waitUntilVisible()
    await settingsPage.openNewValidatorModal()
    // provider select
    const selectProviderElement = await driver.wait(
      until.elementLocated(By.xpath("//select[contains(@data-testid, 'dropdown-provider-create')]"))
    )
    const selectProvider = new Select(selectProviderElement)
    await selectProvider.selectByValue('heuristai')
    
    // model select
    const selectModelElement = await driver.wait(
      until.elementLocated(By.xpath("//select[contains(@data-testid, 'dropdown-model-create')]"))
    )
    const selectModel = new Select(selectModelElement)
    await selectModel.selectByValue('mistralai/mixtral-8x7b-instruct')
    
    const createValidatorBtn = await driver.wait(
      until.elementLocated(By.xpath("//button[@data-testid='create-new-validator-btn']"))
    )

    // createValidatorBtn.click()
  })

  after(() => driver.quit())
})
