# Infra Deployments

This readme describes the process of deploying resources to AWS.

## Prereqs

```
brew install pulumi
```

Copy the contents of `infra/.env.template` to `/infra/.env`. Then update the file to
match the correct values for your environment.

## AWS

You'll need an AWS credentail pair with access to create resources in your account.

Specify those credentials using the `/infra/.env` file mentioned above.

## Sourcing environment variables from `.env`

To source environment variables from your .env file, run this command from your terminal:

```
export $(grep -v '^#' .env | xargs)
```
