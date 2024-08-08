import { WebDriver } from 'selenium-webdriver';

import { TutorialPage } from '../pages/TutorialPage.js';
import { before, describe, after, it } from 'node:test';
import { expect } from 'chai';
import { getDriver } from '../utils/driver.js';

let driver: WebDriver;
let tutorialPage: TutorialPage;
const nextButtonElementText = 'Next';
const finishButtonElementText = 'Finish';

async function validateTutorialStep({
  stepTarget,
  isEndStep,
}: {
  stepTarget: string;
  isEndStep?: boolean;
}) {
  console.log(`Validating step tutorial element with target ${stepTarget}`);
  const stepElement = await tutorialPage.getStepElement(stepTarget);
  expect(stepElement, 'Step container should be visible').not.null;

  if (isEndStep) {
    const finishButton = await tutorialPage.getFinishButton(stepElement);
    expect(finishButton, 'Finish button should be visible').not.null;
    const finishButtonText = await finishButton.getText();
    expect(
      finishButtonText,
      `Finish button text should be equal to ${finishButtonText}`,
    ).to.be.equal(finishButtonElementText);
    await finishButton.click();
  } else {
    const nextButton = await tutorialPage.getNextButton(stepElement);
    expect(nextButton, 'Next button should be visible').not.null;
    const nextButtonText = await nextButton.getText();
    expect(
      nextButtonText,
      'Next button text should be equal to "Next"',
    ).to.be.equal(nextButtonElementText);
    await nextButton.click();
  }
}

describe('Tutorial - Run all tutorial steps', () => {
  before(async () => {
    driver = await getDriver();
    tutorialPage = new TutorialPage(driver);
  });

  it('Should show the welcome step and navigate to the next', async () => {
    await tutorialPage.navigate();
    await tutorialPage.waitUntilVisible();

    await validateTutorialStep({
      stepTarget: '#tutorial-welcome',
    });
  });

  it('Should show the contract example step and navigate to the next', async () => {
    await validateTutorialStep({
      stepTarget: '#contract-item-1a621cad-1cfd-4dbd-892a-f6bbde7a2fab',
    });
  });

  it('Should show the Run and Debug step and navigate to the next to Deploy', async () => {
    await validateTutorialStep({
      stepTarget: '#tutorial-how-to-deploy',
    });
  });

  it('Should show the Contract State step and navigate to the next to step', async () => {
    await validateTutorialStep({
      stepTarget: '#tutorial-read-methods',
    });
  });

  it('Should show the Contract Transactions step and navigate to the next to step', async () => {
    await validateTutorialStep({
      stepTarget: '#tutorial-write-methods',
    });
  });

  it('Should show the Transaction Response step and navigate to the next to step', async () => {
    await validateTutorialStep({
      stepTarget: '#tutorial-tx-response',
    });
  });

  it('Should show the Node Output step and navigate to the next to step', async () => {
    await validateTutorialStep({
      stepTarget: '#tutorial-node-output',
    });
  });

  it('Should show the Switching Examples step and navigate to the next to step', async () => {
    await validateTutorialStep({
      stepTarget: '#tutorial-how-to-change-example',
    });
  });

  it('Should show the Validators step and navigate to the next to step', async () => {
    await validateTutorialStep({
      stepTarget: '#tutorial-validators',
    });
  });

  it('Should show the Final Step step and close the tutorial', async () => {
    await validateTutorialStep({
      stepTarget: '#tutorial-end',
      isEndStep: true,
    });
  });

  after(() => driver.quit());
});
