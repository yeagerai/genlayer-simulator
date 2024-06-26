import { By, Locator, until } from 'selenium-webdriver'
import { BasePage } from './BasePage'

export class RunDebugPage extends BasePage {
  override baseurl = 'http://localhost:8080/simulator/run-debug'
  override visibleLocator: Locator = By.xpath("//h3[contains(text(), 'Run and Debug')]")

}
