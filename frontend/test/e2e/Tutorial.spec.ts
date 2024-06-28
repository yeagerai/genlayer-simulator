import { WebDriver, By, until } from 'selenium-webdriver'


import { ContractsPage } from '../pages/ContractsPage.js'
import { before, describe, after, it } from 'node:test'
import { expect } from 'chai'
import { getDriver } from '../utils/driver.js'

let driver: WebDriver
let contractsPage: ContractsPage

describe('Tutorial - Run all tutorial steps', () => {
  before(async () => {
    driver = await getDriver()
    await driver.manage().setTimeouts({ implicit: 10000 })
    contractsPage = new ContractsPage(driver)
  })

  it('Should show the welcome step and navigate to the next', async () => {
    await contractsPage.navigate()
    await contractsPage.waitUntilVisible()

    const welcomeStepElement = await driver.wait(
        until.elementLocated(By.xpath("//div[@data-testid='tutorial-step-#tutorial-welcome']"))
      )
    expect(welcomeStepElement, 'Welcome step should be visible').not.null
    const headerElement = await welcomeStepElement.findElement(By.xpath("//div[contains(@class, 'v-step__header')]/div"))
    const headerText = await headerElement.getText()
    expect(headerText, 'Welcome step title should be visible').to.be.equal('Welcome to GenLayer Simulator!')

    const contentElement = await welcomeStepElement.findElement(By.xpath("//div[contains(@class, 'v-step__content')]/div"))
    const contentText = await contentElement.getText()
    expect(contentText, 'Welcome step content should be visible').to.be.equal('This tutorial will guide you through the basics. Click “Next” to begin!')
    const nextButton = await welcomeStepElement.findElement(By.xpath("//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"))
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the contract example step and navigate to the next', async () => {
    const contractExampleStepElement = await driver.wait(
        until.elementLocated(By.xpath("//div[@data-testid='tutorial-step-#tutorial-contract-example']"))
      )
    expect(contractExampleStepElement, 'Contract example step should be visible').not.null
    const headerElement = await contractExampleStepElement.findElement(By.xpath("//div[contains(@class, 'v-step__header')]/div"))
    const headerText = await headerElement.getText()
    expect(headerText, 'Contract example step title should be visible').to.be.equal('Code Editor')

    const contentElement = await contractExampleStepElement.findElement(By.xpath("//div[contains(@class, 'v-step__content')]/div"))
    const contentText = await contentElement.getText()
    expect(contentText, 'Contract example step content should be visible').to.be.equal("Write and edit your Intelligent Contracts here. The example contract 'ExampleContract.py' is preloaded for you.")
    const nextButton = await contentElement.findElement(By.xpath("//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"))
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })
  after(() => driver.quit())
})
