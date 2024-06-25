import { By, Locator, until } from 'selenium-webdriver'
import { BasePage } from './BasePage'

export class SettingsPage extends BasePage {
  override baseurl = 'http://localhost:8080/simulator/settings'
  override visibleLocator: Locator = By.xpath("//h3[contains(text(), 'Settings')]")

  async openNewValidatorModal() {
    const locator = By.xpath(`//button[contains(text(), 'New Validator')]`)
    return this.driver.wait(until.elementLocated(locator), 5000).click()
  }
}
