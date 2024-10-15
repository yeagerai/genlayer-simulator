import { By, type Locator } from 'selenium-webdriver';
import { BasePage } from './BasePage';

export class SettingsPage extends BasePage {
  override baseurl = 'http://localhost:8080/simulator/settings';
  override visibleLocator: Locator = By.xpath(
    "//*[@data-testid='settings-page-title']",
  );

  // TODO: Add / remove / update providers
  // TODO: reset providers
  // TODO: reset contracts
  // TODO: Add / remove / enable account
}
