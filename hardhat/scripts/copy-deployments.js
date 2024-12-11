const fs = require('fs-extra');
const path = require('path');

async function copyDeployments() {
    const baseDir = process.cwd();
    const network = 'localhost';

    console.log('Starting deployment files backup process...');

    try {
        // Wait for the deployment files to be available
        await waitForDeployments(path.join(baseDir, 'deployments', 'localhost'));

        // Create backups
        const sourceDir = path.join(baseDir, 'deployments', network);
        const backupDir = path.join(baseDir, 'copy_deployments', network);

        // Check if the source directory exists and has files
        if (await fs.pathExists(sourceDir)) {
            // Ensure the backup directory exists
            await fs.ensureDir(backupDir);

            // Create backup
            await fs.copy(sourceDir, backupDir, { overwrite: true });
            console.log(`Backup created successfully`);
        } else {
            console.log(`No deployments found, skipping backup`);
        }


        console.log('All backups completed successfully!');
    } catch (error) {
        console.error('Error creating deployment backups:', error);
        process.exit(1);
    }
}

async function waitForDeployments(deploymentsPath) {
    const requiredFiles = [
        'ConsensusMain.json',
        'ConsensusManager.json',
        'GhostBlueprint.json',
        'GhostContract.json',
        'GhostFactory.json',
        'MockGenStaking.json',
        'Queues.json',
        'Transactions.json'
    ];

    console.log('Waiting for deployment files to be available...');

    let attempts = 0;
    const maxAttempts = 30; // 30 attempts * 2 seconds = 1 minute maximum wait

    while (attempts < maxAttempts) {
        try {
            const files = await fs.readdir(deploymentsPath);
            const allFilesExist = requiredFiles.every(file =>
                files.includes(file) &&
                fs.statSync(path.join(deploymentsPath, file)).size > 0
            );

            if (allFilesExist) {
                console.log('All deployment files found!');
                return;
            }
        } catch (error) {
            console.log('Error reading deployment files:', error);
        }

        await new Promise(resolve => setTimeout(resolve, 2000)); // wait 2 seconds
        attempts++;

        if (attempts % 5 === 0) { // Show message every 10 seconds
            console.log(`Still waiting for deployment files... (${attempts}/${maxAttempts})`);
        }
    }

    throw new Error('Timeout waiting for deployment files');
}

// Run if called directly
if (require.main === module) {
    copyDeployments()
        .then(() => process.exit(0))
        .catch(error => {
            console.error(error);
            process.exit(1);
        });
}

module.exports = copyDeployments;