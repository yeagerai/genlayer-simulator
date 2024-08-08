import { Builder, Browser, WebDriver } from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome';

export async function getDriver(): Promise<WebDriver> {
  const options = new chrome.Options();
  options.addArguments('--disable-search-engine-choice-screen');

  const driver = await new Builder()
    .forBrowser(Browser.CHROME)
    .setChromeOptions(options)
    .build();

  await driver.manage().setTimeouts({ implicit: 2000 });

  return driver;
}
