import { ContractsPage } from '../pages/ContractsPage.js'
import { RunDebugPage } from '../pages/RunDebugPage.js'
import { SettingsPage } from '../pages/SettingsPage.js'
import { TutorialPage } from '../pages/TutorialPage.js'
import { WebDriver } from 'selenium-webdriver'


export class PageFactory {
  private _driver: WebDriver

  constructor(driver: WebDriver) {
    this._driver = driver
  }

  getContractsPage() {
    return new ContractsPage(this._driver)
  }
  getRunDebugPage() {
    return new RunDebugPage(this._driver)
  }
  getSettingsPage() {
    return new SettingsPage(this._driver)
  }

  getTutorialPage() {
    return new TutorialPage(this._driver)
  }
}
