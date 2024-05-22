import { By, Locator, until } from 'selenium-webdriver'
import { BasePage } from './BasePage'

export class ContractsPage extends BasePage {
  override baseurl = 'http://localhost:8080/simulator/contracts'
  override visibleLocator: Locator = By.xpath("//h3[contains(text(), 'Your Contracts')]")

  elements = {
    contracts: ['storage', 'wizard_of_coin']
  }

  async openContract(name: string) {
    const locator = By.xpath(`//div[contains(@class, 'truncate ... cursor-pointer') and contains(text(), '${name}')]`)
    return this.driver.wait(until.elementLocated(locator), 5000).click();
  }
}
