import { WebDriver, By, until } from 'selenium-webdriver'
import { ContractsPage } from '../pages/ContractsPage.js'
import { RunDebugPage } from '../pages/RunDebugPage.js'
import { expect, beforeAll, describe, afterAll, it } from 'vitest'
import { getDriver } from '../utils/driver.js'

let driver: WebDriver
let contractsPage: ContractsPage
let runDebugPage: RunDebugPage

describe('Contract Example WizardOfCoin', () => {
  beforeAll(async () => {
    driver = await getDriver()
    await driver.manage().setTimeouts({ implicit: 2000 })
    contractsPage = new ContractsPage(driver)
    runDebugPage = new RunDebugPage(driver)
  })


  it('should open WizardOfCoin example contract', async () => {
    await contractsPage.navigate()
    await contractsPage.waitUntilVisible()
    await contractsPage.skipTutorial()
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
      ),
      10000
    )
    expect(nameOfContract, 'WizardOfCoin file name contract should be visible').not.null

    const haveCoinCheck = await driver.wait(
      until.elementLocated(
        By.xpath("//input[contains(@name, 'have_coin') and contains(@type, 'checkbox')]")
      ),
      10000
    )
    expect(haveCoinCheck, 'Have coin checkbox should be visible').not.null
    await haveCoinCheck.click()
  })

  it('should deploy the contract WizardOfCoin', async () => {
    await driver.wait(until.elementLocated(By.xpath("//button[text()='Deploy']")), 5000).click()

    // locate elements that should be visible
    const contractStateTitle = await driver.wait(
      until.elementLocated(
        By.xpath(
          "//h5[contains(@class, 'text-sm') and contains(text(), 'Current Intelligent Contract State')]"
        )
      ),
      10000
    )
    expect(contractStateTitle, 'Contract state title section should be visible').not.null

    const executeTransactionsTitle = await driver.wait(
      until.elementLocated(
        By.xpath("//h5[contains(@class, 'text-sm') and contains(text(), 'Execute Transactions')]")
      ),
      10000
    )
    expect(executeTransactionsTitle, 'Execute transactions title section should be visible').not
      .null

    const latestTransactions = await driver.wait(
      until.elementLocated(
        By.xpath("//h5[contains(@class, 'text-sm') and contains(text(), 'Latest Transactions')]")
      ),
      5000
    )
    expect(latestTransactions, 'Latest transactions title section should be visible').not.null
  })

  it('should call get_have_coin state', async () => {
    await driver
      .wait(until.elementLocated(By.xpath("//button[text()='get_have_coin']")), 10000)
      .click()

    const stateResult = await driver.wait(
      until.elementLocated(By.xpath("//div[contains(@data-test-id, 'get_have_coin')]")),
      10000
    )
    expect(stateResult, 'get_have_coin result should be visible').not.null

    const stateResultText = await driver
      .wait(until.elementTextContains(stateResult, 'True'), 10000)
      .getText()
    expect(stateResultText, 'get_have_coin result should true').be.equal('True')
  })

  it('should call ask_for_coin() method', async () => {
    const dropdownExecuteMethod = await driver.wait(
      until.elementLocated(By.xpath("//select[@name='dropdown-execute-method']")),
      10000
    )
    expect(dropdownExecuteMethod, 'select with method list should be visible').not.null

    await dropdownExecuteMethod.findElement(By.xpath("//option[@value='ask_for_coin']")).click()

    const requestInput = await driver.wait(
      until.elementLocated(By.xpath("//input[@name='request']"))
    )
    await requestInput.clear()
    await requestInput.sendKeys('Please give me the coin')
    const requestText = await requestInput.getAttribute('value')
    expect(
      requestText,
      'The input text should be equal to `Please give me the coin`'
    ).to.be.equal('Please give me the coin')

    await driver
    .wait(until.elementLocated(By.xpath("//button[text()='Execute ask_for_coin()']")), 1000)
    .click()
  })
  afterAll(() => driver.quit())
})
