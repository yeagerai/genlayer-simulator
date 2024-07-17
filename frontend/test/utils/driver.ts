import { Builder, Browser, WebDriver } from 'selenium-webdriver'

export async function getDriver(): Promise<WebDriver> {
  const driver = await new Builder().forBrowser(Browser.CHROME).build()
  await driver.manage().setTimeouts({ implicit: 10000 })
  return driver
}
