# Contributing to GenLayer Simulator

We're thrilled that you're interested in contributing to the GenLayer Simulator! This document will guide you through the contribution process.

## What is the GenLayer Simulator?

The GenLayer Simulator is an interactive sandbox designed for developers to explore the potential of GenLayer's Intelligent Contracts. It replicates the GenLayer network's execution environment and consensus algorithm, providing a controlled and local environment to test different ideas and behaviors.

## How You Can Contribute?

Contributions to the GenLayer Simulator are welcome in several forms:

### Testing the Simulator and Providing Feedback

Help us make the simulator better by testing and giving feedback:

- First, install the simulator using the GenLayer [CLI](https://github.com/yeagerai/genlayer-simulator?tab=readme-ov-file#quick-install).
- Try out the Simulator features and tell us what you think through our [feedback form](https://docs.google.com/forms/d/1IVNsZwm936kSNCiXmlAP8bgJnbik7Bqaoc3I6UYhr-o/viewform) or on our [Discord Channel](https://discord.gg/8Jm4v89VAu).
- If you find any issues, please report them on our [GitHub issues page](https://github.com/yeagerai/genlayer-simulator/issues).

### Sharing New Ideas and Use Cases

Have ideas for new features or usecases? We're eager to hear them! But first:

- Ensure you have the [Simulator installed](https://github.com/yeagerai/genlayer-simulator?tab=readme-ov-file#quick-install) first to explore existing use cases.
- After you've familiarized yourself with the simulator, contribute your unique use case and share your ideas in our [Discord channel](https://discord.gg/8Jm4v89VAu).

### Writing Code

To contribute to feature development or bug fixes. Check our [issue tracker](https://github.com/yeagerai/genlayer-simulator/issues) for tasks labeled `help wanted`.

#### Setup Simulator manually

##### Window One

```
$ cp .env.example .env
$ docker compose up
```

##### Window Two

1. Installing the Ollama model

   ```
   $ docker exec ollama ollama pull llama3
   ```

2. Setup your environment

   - Linux / MacOS

     ```
     $ virtualenv .venv
     $ source .venv/bin/activate
     (.venv) $ pip install -r requirements.txt
     (.venv) $ export PYTHONPATH="$(pwd)"
     ```

   - Windows (cmd)

     ```
     $ virtualenv .venv
     $  .\.venv\Scripts\activate
     (.venv) $ pip install -r requirements.txt
     (.venv) $ set PYTHONPATH=%cd%
     ```

   - Windows (PowerShell)

     ```
     $ virtualenv .venv
     $  .\.venv\Scripts\activate
     (.venv) $ pip install -r requirements.txt
     (.venv) $ $env:PYTHONPATH = (Get-Location).Path
     ```

3. Execute the Demo

   ```
   (.venv) $ python scripts/debug_simulator.py
   ```

### Improving Documentation

To contribute to our docs, start by visiting our [Documentation Repository](https://github.com/yeagerai/genlayer-docs) to create new issues or contribute to existing issues.

## Review Process

We strive to maintain high-quality code and ensure that all contributions align with our goals. Here’s our process:

- **Black Formatter on Save File**: Configure IDE extensions to format your code with [Black](https://github.com/psf/black) before submitting it.
- **Pull Request**: Submit your changes through a pull request (PR).
- **Automated Tests**: Your PR will automatically be tested. Ensure all tests pass to proceed.
- **Peer Review**: One or more core contributors will review your PR. They may suggest changes or improvements.
- **Approval and Merge**: After approval from the reviewers, your PR will be merged into the project.

### PR Checks

On PRs we have the following checks:

- Backend end-to-end tests
- Frontend unit tests

These will be run automatically when you open a PR (and would need an approval from a maintainer if you are not a maintainer). If you modify your PR afterwards, you'll need to manually run the checks again by commenting `/test` on the PR.

## Community

Connect with the GenLayer community to discuss, collaborate, and share insights:

- **[Discord Channel](https://discord.gg/8Jm4v89VAu)**: Our primary hub for discussions, support, and announcements.
- **[Telegram Group](https://t.me/genlayer)**: For more informal chats and quick updates.

Your continuous feedback drives better product development. Engage with us regularly to test, discuss, and improve the GenLayer Simulator.
