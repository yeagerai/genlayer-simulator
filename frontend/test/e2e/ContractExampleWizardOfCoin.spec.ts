import { WebDriver, By, until } from 'selenium-webdriver'
import { ContractsPage } from '../pages/ContractsPage.js'
import { RunDebugPage } from '../pages/RunDebugPage.js'
import { SettingsPage } from '../pages/SettingsPage.js'
import { before, describe, after, it } from 'node:test'
import { expect } from 'chai'
import { getDriver } from '../utils/driver.js'

let driver: WebDriver
let contractsPage: ContractsPage
let runDebugPage: RunDebugPage
let settingsPage: SettingsPage

describe('Contract Example WizardOfCoin', () => {
  before(async () => {
    driver = await getDriver()
    contractsPage = new ContractsPage(driver)
    runDebugPage = new RunDebugPage(driver)
    settingsPage = new SettingsPage(driver)

    await contractsPage.navigate()
    await contractsPage.waitUntilVisible()
    await contractsPage.skipTutorial()
    await settingsPage.navigate()
    await settingsPage.createValidatorIfRequired()
  })

  it('should open WizardOfCoin example contract', async () => {
    await contractsPage.navigate()
    await contractsPage.waitUntilVisible()
    await contractsPage.openContract('wizard_of_coin.gpy')
    const tabs = await driver.findElements(By.xpath("//div[contains(@class, 'contract-item')]"))
    expect(tabs.length, 'Number of tabs should be 2').equal(2)
  })

  it('should open Run debug page and set constructor arguments for WizardOfCoin', async () => {
    await runDebugPage.navigate()
    await runDebugPage.waitUntilVisible()

    const nameOfContract = await driver.wait(
      until.elementLocated(
        By.xpath(
          "//div[contains(@class, 'text-xs text-neutral-800 dark:text-neutral-200') and contains(text(), 'wizard_of_coin.gpy')]"
        )
      )
    )
    expect(nameOfContract, 'WizardOfCoin file name contract should be visible').not.null

    const haveCoinCheck = await driver.wait(
      until.elementLocated(
        By.xpath("//input[contains(@name, 'have_coin') and contains(@type, 'checkbox')]")
      )
    )
    expect(haveCoinCheck, 'Have coin checkbox should be visible').not.null
    await haveCoinCheck.click()
  })

  it('should deploy the contract WizardOfCoin', async () => {
    await driver.wait(until.elementLocated(By.xpath("//button[text()='Deploy']"))).click()

    // locate elements that should be visible
    const contractStateTitle = await driver.wait(
      until.elementLocated(
        By.xpath(
          "//h5[contains(@class, 'text-sm') and contains(text(), 'Current Intelligent Contract State')]"
        )
      ),
      15000
    )
    expect(contractStateTitle, 'Contract state title section should be visible').not.null

    const executeTransactionsTitle = await driver.wait(
      until.elementLocated(
        By.xpath("//h5[contains(@class, 'text-sm') and contains(text(), 'Execute Transactions')]")
      )
    )
    expect(executeTransactionsTitle, 'Execute transactions title section should be visible').not
      .null

    const latestTransactions = await driver.wait(
      until.elementLocated(
        By.xpath("//h5[contains(@class, 'text-sm') and contains(text(), 'Latest Transactions')]")
      )
    )
    expect(latestTransactions, 'Latest transactions title section should be visible').not.null
  })

  it('should call get_have_coin state', async () => {
    const stateBtn = await driver.wait(until.elementLocated(By.xpath("//button[text()='get_have_coin']")), 25000)
    await stateBtn.click()

    const stateResult = await driver.wait(
      until.elementLocated(By.xpath("//div[contains(@data-testid, 'get_have_coin')]"))
    )
    expect(stateResult, 'get_have_coin result should be visible').not.null

    const stateResultText = await driver.wait(until.elementTextContains(stateResult, 'True')).getText()

    console.log(`get_have_coin result: ${stateResultText}`)
    expect(stateResultText, 'get_have_coin result should true').be.equal('True')
  })

  it('should call ask_for_coin() method', async () => {
    const dropdownExecuteMethod = await driver.wait(
      until.elementLocated(By.xpath("//select[@name='dropdown-execute-method']"))
    )
    expect(dropdownExecuteMethod, 'select with method list should be visible').not.null

    await dropdownExecuteMethod.findElement(By.xpath("//option[@value='ask_for_coin']")).click()

    const requestInput = await driver.wait(
      until.elementLocated(By.xpath("//input[@name='request']"))
    )
    await requestInput.clear()
    await requestInput.sendKeys('Please give me the coin')
    const requestText = await requestInput.getAttribute('value')
    expect(requestText, 'The input text should be equal to `Please give me the coin`').to.be.equal(
      'Please give me the coin'
    )

    await driver
      .wait(until.elementLocated(By.xpath("//button[text()='Execute ask_for_coin()']")))
      .click()
  })
  after(() => driver.quit())
})
