import { WebDriver, Select } from 'selenium-webdriver'

import { SettingsPage } from '../pages/SettingsPage.js'
import { ContractsPage } from '../pages/ContractsPage.js'
import { before, describe, after, it } from 'node:test'
import { expect } from 'chai'
import { getDriver } from '../utils/driver.js'

let driver: WebDriver
let settingsPage: SettingsPage
let contractsPage: ContractsPage

describe('Settings - Create Node Validator', () => {
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

    const initialValidators = await settingsPage.getValidatorsElements()
    await settingsPage.createValidator({
      provider: 'heuristai',
      model: 'mistralai/mixtral-8x7b-instruct',
      stake: 7
    })
    const existingValidators = await settingsPage.getValidatorsElements()
    expect(
      existingValidators.length,
      'number of validators should be greather than old validators list'
    ).be.greaterThan(initialValidators.length)
  })

  after(() => driver.quit())
})
