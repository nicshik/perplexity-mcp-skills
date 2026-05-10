# Releasing

This package is intended to be published to npm through GitHub Actions Trusted Publishing, so routine releases do not require an `NPM_TOKEN` repository secret.

## One-Time npm Setup

After the package exists on npm, configure a trusted publisher with these values:

```text
Provider: GitHub Actions
Organization or user: nicshik
Repository: perplexity-mcp-skills
Workflow file: release.yml
```

The workflow path is `.github/workflows/release.yml`.

## First Publish Bootstrap

If `https://www.npmjs.com/package/perplexity-mcp-skills` does not exist yet, publish the first version locally from a logged-in npm account:

```bash
npm login
npm ci
npm run typecheck
npm test
npm run check
npm publish --dry-run
npm publish --access public
```

Then configure Trusted Publishing in the npm package settings. Future versions should be published from GitHub Releases.

## Publish a Release

1. Confirm `package.json` and `CHANGELOG.md` describe the version.
2. Confirm CI is green on `main`.
3. Create a GitHub Release:

```bash
gh release create "$(node -p "'v' + require('./package.json').version")" \
  --repo nicshik/perplexity-mcp-skills \
  --target main \
  --title "$(node -p "'v' + require('./package.json').version")" \
  --notes "Release $(node -p "'v' + require('./package.json').version")"
```

The release workflow validates the package, skips publishing if the version already exists, and publishes with provenance through Trusted Publishing.

## Verify

```bash
npm view perplexity-mcp-skills version
npx perplexity-mcp-skills --help
npx perplexity-mcp-skills doctor --offline
```
