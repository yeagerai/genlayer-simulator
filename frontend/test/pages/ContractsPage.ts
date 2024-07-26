import { By, Locator, until } from 'selenium-webdriver'
import { BasePage } from './BasePage'

export class ContractsPage extends BasePage {
  override baseurl = 'http://localhost:8080/simulator/contracts'
  override visibleLocator: Locator = By.xpath(
    "//*[@data-testid='contracts-page-title']",
  )

  async openContract(name: string) {
    const locator = By.xpath(`//div[contains(text(), '${name}')]`)
    return this.driver.wait(until.elementLocated(locator), 2000).click()
  }
}
