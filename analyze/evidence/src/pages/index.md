# AJ's [Evidence](https://evidence.dev)-based BI Portal

This site is a BI portal built on top of the [Meltano](https://meltano.com) DataOps OS and the Evidence.dev BI tool.

## Contributing guide

Visit [docs.evidence.dev](https://docs.evidence.dev) to read the Evidence documentation.

Within the project, you can edit this page at `analyze/evidence/src/pages/index.md`.

## Building and Testing

Locally in your project, you can build and refresh the report with the following command:

`meltano invoke --containers evidence:dev`

This command will spin up the server and will monitor the directory for file changes.
