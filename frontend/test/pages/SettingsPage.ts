import { By, Locator, WebElement, until, Select } from 'selenium-webdriver'
import { BasePage } from './BasePage'

export class SettingsPage extends BasePage {
  override baseurl = 'http://localhost:8080/simulator/settings'
  override visibleLocator: Locator = By.xpath("//h3[contains(text(), 'Settings')]")

  async openNewValidatorModal() {
    const locator = By.xpath(`//button[contains(text(), 'New Validator')]`)
    return this.driver.wait(until.elementLocated(locator), 5000).click()
  }
  async getValidatorsElements(): Promise<WebElement[]> {
    return this.driver.findElements(By.xpath("//div[@data-testid = 'validator-item-container']"))
  }

  async createValidator() {
     // get the list of validators
   
     await this.openNewValidatorModal()
     // provider select
     const selectProviderElement = await this.driver.wait(
       until.elementLocated(By.xpath("//select[contains(@data-testid, 'dropdown-provider-create')]"))
     )
     const selectProvider = new Select(selectProviderElement)
     await selectProvider.selectByValue('heuristai')
 
     // model select
     const selectModelElement = await this.driver.wait(
       until.elementLocated(By.xpath("//select[contains(@data-testid, 'dropdown-model-create')]"))
     )
     const selectModel = new Select(selectModelElement)
     await selectModel.selectByValue('mistralai/mixtral-8x7b-instruct')
 
     const stakeInput = await this.driver.wait(
       until.elementLocated(By.xpath("//input[@data-testid='input-stake-create']"))
     )
     await stakeInput.clear()
     await stakeInput.sendKeys(7)
  
 
     const createValidatorBtn = await this.driver.wait(
       until.elementLocated(By.xpath("//button[@data-testid='btn-create-validator']"))
     )
     // call create validator button
     await createValidatorBtn.click()
     await this.driver.navigate().refresh();
  
  }
}
