module.exports = {
    branches: ['main', '485-do-trunk-based-development'],
    plugins: [
        '@semantic-release/commit-analyzer',
        '@semantic-release/release-notes-generator',
        '@semantic-release/github'
    ]
};
