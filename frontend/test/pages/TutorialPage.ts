import { By, Locator, WebElement, until } from 'selenium-webdriver'
import { BasePage } from './BasePage'

export class TutorialPage extends BasePage {
  override baseurl = 'http://localhost:8080/simulator/contracts'
  override visibleLocator: Locator = By.xpath("//h3[contains(text(), 'Your Contracts')]")

  async getStepElement(target: string): Promise<WebElement> {
    const stepElement = await this.driver.wait(
      until.elementLocated(By.xpath(`//div[@data-testid='tutorial-step-${target}']`))
    )
    return stepElement
  }

  async getStepItems(
    stepElement: WebElement
  ): Promise<{ header: WebElement; content: WebElement }> {
    const headerElement = await stepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__header')]/div")
    )

    const contentElement = await stepElement.findElement(
      By.xpath("//div[contains(@class, 'v-step__content')]/div")
    )

    return {
      header: headerElement,
      content: contentElement
    }
  }

  async getNextButton(stepElement: WebElement): Promise<WebElement> {
    const nextButton = await stepElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-next')]"
      )
    )

    return nextButton
  }

  async getFinishButton(stepElement: WebElement): Promise<WebElement> {
    const finishButton = await stepElement.findElement(
      By.xpath(
        "//div[contains(@class, 'v-step__buttons')]/button[contains(@class, 'v-step__button-stop')]"
      )
    )

    return finishButton
  }
}
