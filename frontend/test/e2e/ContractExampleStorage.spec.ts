import { WebDriver, By, until } from 'selenium-webdriver'
import { ContractsPage } from '../pages/ContractsPage.js'
import { RunDebugPage } from '../pages/RunDebugPage.js'
import { beforeEach, before, describe, after, it } from 'node:test'
import { expect } from 'chai'
import { getDriver } from '../utils/driver.js'

let driver: WebDriver
let contractsPage: ContractsPage
let runDebugPage: RunDebugPage

describe('Contract Example Storage', () => {
  before(async () => {
    driver = await getDriver()
    await driver.manage().setTimeouts({ implicit: 2000 })
    contractsPage = new ContractsPage(driver)
    runDebugPage = new RunDebugPage(driver)
  })

  beforeEach(async () => {})

  it('should open Storage example contract', async () => {
    await contractsPage.navigate()
    await contractsPage.waitUntilVisible()
    await contractsPage.skipTutorial()
    await contractsPage.openContract('storage.gpy')
    const tabs = await driver.findElements(By.xpath("//div[contains(@class, 'contract-item')]"))
    expect(tabs.length, 'Number of tabs should be 2').equal(2)
  })

  it('should open Run debug page and set constructor arguments for WizardOfCoin', async () => {
    await runDebugPage.navigate()
    await runDebugPage.waitUntilVisible()

    const nameOfContract = await driver.wait(
      until.elementLocated(
        By.xpath(
          "//div[contains(@class, 'text-xs text-neutral-800 dark:text-neutral-200') and contains(text(), 'storage.gpy')]"
        )
      ),
      5000
    )
    expect(nameOfContract, 'Storage file name contract should be visible').not.null

    const initialStorageInput = await driver.wait(
      until.elementLocated(
        By.xpath("//input[contains(@name, 'initial_storage') and contains(@type, 'text')]")
      ),
      5000
    )
    expect(initialStorageInput, 'Initial Storage input should be visible').not.null
    await initialStorageInput.clear()
    await initialStorageInput.sendKeys('Test initial storage')
    const storageText = await initialStorageInput.getAttribute('value')
    expect(
      storageText,
      'The input text should be equal to `Test initial storage`'
    ).to.be.equal('Test initial storage')
  })

  it('should deploy the contract Storage', async () => {
    await driver.wait(until.elementLocated(By.xpath("//button[text()='Deploy']")), 5000).click()

    // locate elements that should be visible
    const contractStateTitle = await driver.wait(
      until.elementLocated(
        By.xpath(
          "//h5[contains(@class, 'text-sm') and contains(text(), 'Current Intelligent Contract State')]"
        )
      ),
      5000
    )
    expect(contractStateTitle, 'Contract state title section should be visible').not.null

    const executeTransactionsTitle = await driver.wait(
      until.elementLocated(
        By.xpath("//h5[contains(@class, 'text-sm') and contains(text(), 'Execute Transactions')]")
      ),
      5000
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

  it('should call get_storage state', async () => {
    await driver
      .wait(until.elementLocated(By.xpath("//button[text()='get_storage']")), 5000)
      .click()

    const stateResult = await driver.wait(
      until.elementLocated(By.xpath("//div[contains(@data-test-id, 'get_storage')]")),
      5000
    )
    expect(stateResult, 'get_storage result should be visible').not.null

    const stateResultText = await driver
      .wait(until.elementTextContains(stateResult, 'Test initial storage'), 5000)
      .getText()
    expect(stateResultText, 'get_storage result should be Test initial storage').be.equal('Test initial storage')
  })

  it('should call ask_for_coin() method', async () => {
    const dropdownExecuteMethod = await driver.wait(
      until.elementLocated(By.xpath("//select[@name='dropdown-execute-method']"))
    )
    expect(dropdownExecuteMethod, 'select with method list should be visible').not.null

    await dropdownExecuteMethod.findElement(By.xpath("//option[@value='update_storage']")).click()

    const newStorageInput = await driver.wait(
      until.elementLocated(By.xpath("//input[@name='new_storage']"))
    )
    await newStorageInput.clear()
    await newStorageInput.sendKeys('Updated storage text')
    const newStorageText = await newStorageInput.getAttribute('value')
    expect(
      newStorageText,
      'The input text should be equal to `Updated storage text`'
    ).to.be.equal('Updated storage text')

    await driver
    .wait(until.elementLocated(By.xpath("//button[text()='Execute update_storage()']")), 5000)
    .click()
  })
  after(() => driver.quit())
})
