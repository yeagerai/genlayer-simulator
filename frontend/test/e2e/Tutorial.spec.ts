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
    const headerElement = await welcomeStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Welcome step title should be visible').to.be.equal(
      'Welcome to GenLayer Simulator!'
    )

    const contentElement = await welcomeStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Welcome step content should be visible').to.be.equal(
      'This tutorial will guide you through the basics. Click “Next” to begin!'
    )
    const nextButton = await welcomeStepElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the contract example step and navigate to the next', async () => {
    const contractExampleStepElement = await driver.wait(
      until.elementLocated(
        By.xpath("//div[@data-testid='tutorial-step-#tutorial-contract-example']")
      )
    )
    expect(contractExampleStepElement, 'Contract example step should be visible').not.null
    const headerElement = await contractExampleStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Contract example step title should be visible').to.be.equal('Code Editor')

    const contentElement = await contractExampleStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Contract example step content should be visible').to.be.equal(
      "Write and edit your Intelligent Contracts here. The example contract 'ExampleContract.py' is preloaded for you."
    )
    const nextButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the Run and Debug step and navigate to the next to Deploy', async () => {
    const howToDeployStepElement = await driver.wait(
      until.elementLocated(By.xpath("//div[@data-testid='tutorial-step-#tutorial-how-to-deploy']"))
    )
    expect(howToDeployStepElement, 'Deploying Contracts step should be visible').not.null
    const headerElement = await howToDeployStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Deploying Contracts step title should be visible').to.be.equal(
      'Deploying Contracts'
    )

    const contentElement = await howToDeployStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Deploying Contracts step content should be visible').to.be.equal(
      'Click “Next” to automatically deploy your Intelligent Contract to the GenLayer network.'
    )
    const nextButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the Contract Transactions step and navigate to the next to step', async () => {
    const contractTransactionsStepElement = await driver.wait(
      until.elementLocated(
        By.xpath("//div[@data-testid='tutorial-step-#tutorial-creating-transactions']")
      )
    )
    expect(contractTransactionsStepElement, 'Contract Transactions step should be visible').not.null
    const headerElement = await contractTransactionsStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Contract Transactions step title should be visible').to.be.equal(
      'Creating Transactions'
    )

    const contentElement = await contractTransactionsStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Contract Transactions step content should be visible').to.be.equal(
      'This is where you can interact with the deployed contract. You can select a method you want to use from the dropdown, and provide the parameters. Click “Next” to automatically create a transaction and interact with your deployed contract.'
    )
    const nextButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the Node Output step and navigate to the next to step', async () => {
    const nodeOutputStepElement = await driver.wait(
      until.elementLocated(By.xpath("//div[@data-testid='tutorial-step-#tutorial-node-output']"))
    )
    expect(nodeOutputStepElement, 'Node Output step should be visible').not.null
    const headerElement = await nodeOutputStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Node Output step title should be visible').to.be.equal('Node Output')

    const contentElement = await nodeOutputStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Node Output step content should be visible').to.be.equal(
      'View real-time feedback as your transaction execution and debug any issues.'
    )
    const nextButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the Contract State step and navigate to the next to step', async () => {
    const contractStateStepElement = await driver.wait(
      until.elementLocated(By.xpath("//div[@data-testid='tutorial-step-#tutorial-contract-state']"))
    )
    expect(contractStateStepElement, 'Contract State step should be visible').not.null
    const headerElement = await contractStateStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Contract State step title should be visible').to.be.equal('Contract State')

    const contentElement = await contractStateStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Contract State step content should be visible').to.be.equal(
      "This panel shows the contract's data after executing transactions."
    )
    const nextButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the Transaction Response step and navigate to the next to step', async () => {
    const transactionResponseStepElement = await driver.wait(
      until.elementLocated(By.xpath("//div[@data-testid='tutorial-step-#tutorial-tx-response']"))
    )
    expect(transactionResponseStepElement, 'Transaction Response step should be visible').not.null
    const headerElement = await transactionResponseStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Transaction Response step title should be visible').to.be.equal(
      'Transaction Response'
    )

    const contentElement = await transactionResponseStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Transaction Response step content should be visible').to.be.equal(
      'See the results of your transaction interaction with the contract in this area.'
    )
    const nextButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the Switching Examples step and navigate to the next to step', async () => {
    const transactionResponseStepElement = await driver.wait(
      until.elementLocated(
        By.xpath("//div[@data-testid='tutorial-step-#tutorial-how-to-change-example']")
      )
    )
    expect(transactionResponseStepElement, 'Switching Examples step should be visible').not.null
    const headerElement = await transactionResponseStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Switching Examples step title should be visible').to.be.equal(
      'Switching Examples'
    )

    const contentElement = await transactionResponseStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Transaction Response step content should be visible').to.be.equal(
      'Switch between different example contracts to explore various features and functionalities.'
    )
    const nextButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the Validators step and navigate to the next to step', async () => {
    const transactionResponseStepElement = await driver.wait(
      until.elementLocated(By.xpath("//div[@data-testid='tutorial-step-#tutorial-validators']"))
    )
    expect(transactionResponseStepElement, 'Validators step should be visible').not.null
    const headerElement = await transactionResponseStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Validators step title should be visible').to.be.equal('Validators')

    const contentElement = await transactionResponseStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Transaction Response step content should be visible').to.be.equal(
      'Configure the number of validators and set up their parameters here.'
    )
    const nextButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )
    expect(nextButton, 'Next button should be visible').not.null
    const nextButtonText = await nextButton.getText()
    expect(nextButtonText, 'Next button text should be equal to "Next"').to.be.equal('Next')
    await nextButton.click()
  })

  it('Should show the Final Step step and close the tutorial', async () => {
    const tutorialEndStepElement = await driver.wait(
      until.elementLocated(By.xpath("//div[@data-testid='tutorial-step-#tutorial-end']"))
    )
    expect(tutorialEndStepElement, 'Final step should be visible').not.null
    const headerElement = await tutorialEndStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )
    const headerText = await headerElement.getText()
    expect(headerText, 'Final step title should be visible').to.be.equal('Congratulations!')

    const contentElement = await tutorialEndStepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )
    const contentText = await contentElement.getText()
    expect(contentText, 'Final step content should be visible').to.be.equal(
      "You've completed the GenLayer Simulator tutorial. Feel free to revisit any step or start experimenting with your own contracts. Happy coding!"
    )
    const finishButton = await contentElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-stop')]"
      )
    )
    expect(finishButton, 'Finish button should be visible').not.null
    const finishButtonText = await finishButton.getText()
    expect(finishButtonText, 'Finish button text should be equal to "Finish"').to.be.equal('Finish')
    await finishButton.click()
  })

  after(() => driver.quit())
})
