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
  headerElementText,
  contentElementText,
  isEndStep,
}: {
  stepTarget: string;
  headerElementText: string;
  contentElementText: string;
  isEndStep?: boolean;
}) {
  console.log(`Validating step tutorial element with target ${stepTarget}`);
  const stepElement = await tutorialPage.getStepElement(stepTarget);
  expect(stepElement, 'Step container should be visible').not.null;

  const { header, content } = await tutorialPage.getStepItems(stepElement);
  const headerText = await header.getText();
  console.log(`Step title: ${headerText}`);

  expect(headerText, 'Step title should be visible').to.be.equal(
    headerElementText,
  );
  const contentText = await content.getText();
  console.log(`Step content: ${contentText}`);

  expect(contentText, 'Step content should be visible').to.be.equal(
    contentElementText,
  );
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

    const headerElementText = 'Welcome to GenLayer Simulator!';
    const contentElementText =
      'This tutorial will guide you through the basics. Click “Next” to begin!';
    await validateTutorialStep({
      stepTarget: '#tutorial-welcome',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the contract example step and navigate to the next', async () => {
    const headerElementText = 'Code Editor';
    const contentElementText = `Write and edit your Intelligent Contracts here. This example contract is preloaded for you.`;
    await validateTutorialStep({
      stepTarget: '.contract-item',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the Run and Debug step and navigate to the next to Deploy', async () => {
    const headerElementText = 'Deploying Contracts';
    const contentElementText = `Click “Next” to automatically deploy your Intelligent Contract to the GenLayer network.`;
    await validateTutorialStep({
      stepTarget: '#tutorial-how-to-deploy',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the Contract Transactions step and navigate to the next to step', async () => {
    const headerElementText = 'Creating Transactions';
    const contentElementText =
      'This is where you can interact with the deployed contract. You can select a method you want to use from the dropdown, and provide the parameters. Click “Next” to automatically create a transaction and interact with your deployed contract.';
    await validateTutorialStep({
      stepTarget: '#tutorial-creating-transactions',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the Node Output step and navigate to the next to step', async () => {
    const headerElementText = 'Node Output';
    const contentElementText =
      'View real-time feedback as your transaction execution and debug any issues.';
    await validateTutorialStep({
      stepTarget: '#tutorial-node-output',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the Contract State step and navigate to the next to step', async () => {
    const headerElementText = 'Contract State';
    const contentElementText = `This panel shows the contract's data after executing transactions.`;
    await validateTutorialStep({
      stepTarget: '#tutorial-contract-state',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the Transaction Response step and navigate to the next to step', async () => {
    const headerElementText = 'Transaction Response';
    const contentElementText =
      'See the results of your transaction interaction with the contract in this area.';
    await validateTutorialStep({
      stepTarget: '#tutorial-tx-response',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the Switching Examples step and navigate to the next to step', async () => {
    const headerElementText = 'Switching Examples';
    const contentElementText =
      'Switch between different example contracts to explore various features and functionalities.';
    await validateTutorialStep({
      stepTarget: '#tutorial-how-to-change-example',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the Validators step and navigate to the next to step', async () => {
    const headerElementText = 'Validators';
    const contentElementText =
      'Configure the number of validators and set up their parameters here.';
    await validateTutorialStep({
      stepTarget: '#tutorial-validators',
      headerElementText,
      contentElementText,
    });
  });

  it('Should show the Final Step step and close the tutorial', async () => {
    const headerElementText = 'Congratulations!';
    const contentElementText = `You've completed the GenLayer Simulator tutorial. Feel free to revisit any step or start experimenting with your own contracts. Happy coding!`;
    await validateTutorialStep({
      stepTarget: '#tutorial-end',
      headerElementText,
      contentElementText,
      isEndStep: true,
    });
  });

  after(() => driver.quit());
});
