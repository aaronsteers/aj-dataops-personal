# Evidence Template Project

Thank you for checking out Evidence. This is the project template that you should use to get started.

## Getting Started

Check out the [documentation](https://docs.evidence.dev) for a complete walk through.

```bash
npx degit evidence-dev/template my-project
cd my-project
npm install
npm run dev
```

Don't clone this repo, just download the code using the steps above.

## Using with Meltano

```
meltano invoke --container evidence:pull_image  # Get the latest docker image
meltano invoke --container evidence:help        # Show help from Evidence
meltano invoke --container evidence:install     # Install the latest dependencies and update the package-lock.json file.
meltano invoke --container evidence:dev         # Run the Evidence in dev mode 
meltano invoke --container evidence:build       # Build project artifacts for production
```

## Learning More

- [Getting Started Walkthrough](https://docs.evidence.dev/getting-started/get-started)
- [Project Home Page](https://www.evidence.dev)
- [Github](https://github.com/evidence-dev/evidence)
