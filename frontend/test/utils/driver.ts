import { Builder, Browser, WebDriver } from 'selenium-webdriver';

export async function getDriver():Promise<WebDriver> {
    return new Builder().forBrowser(Browser.CHROME).build();
}