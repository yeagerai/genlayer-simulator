import { WebDriver, By, until } from 'selenium-webdriver'

import { SettingsPage } from '../pages/SettingsPage.js'
import { ContractsPage } from '../pages/ContractsPage.js'
import { before, describe, after, it } from 'node:test'
import { expect } from 'chai'
import { getDriver } from '../utils/driver.js'

let driver: WebDriver
let settingsPage: SettingsPage
let contractsPage: ContractsPage

describe('Settings - Delete Node Validator', () => {
  before(async () => {
    driver = await getDriver()
    settingsPage = new SettingsPage(driver)
    contractsPage = new ContractsPage(driver)
  })

  it('should delete an existing validator', async () => {
    await contractsPage.navigate()
    await contractsPage.waitUntilVisible()
    await contractsPage.skipTutorial()

    await settingsPage.navigate()
    await settingsPage.waitUntilVisible()

    await settingsPage.createValidator({
      provider: 'heuristai',
      model: 'mistralai/mixtral-8x7b-instruct',
      stake: 7
    })
    const existingValidators = await settingsPage.getValidatorsElements()
    const existingValidatorsLength = existingValidators.length
    expect(
      existingValidatorsLength,
      'number of validators should be greather than 0'
    ).be.greaterThan(0)

    const deleteBtn = await existingValidators[0].findElement(
      By.xpath("//button[@data-testid = 'validator-item-delete']")
    )

    await driver.actions().move({ origin: existingValidators[0] }).perform();
    await driver.sleep(500); // Wait for hover effect
    await deleteBtn.click();

    const deleteValidatorBtn = await driver.wait(
      until.elementLocated(By.xpath("//button[@data-testid='btn-delete-validator']"))
    )
    // call delete validator button
    await deleteValidatorBtn.click()

    await driver.navigate().refresh()
    const validators = await driver.findElements(
      By.xpath("//button[@data-testid = 'validator-item']")
    )

    expect(
      validators.length,
      'validators length should be less than initial validators length'
    ).be.lessThan(existingValidatorsLength)
  })

  after(() => driver.quit())
})
