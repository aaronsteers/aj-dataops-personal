# Infra Deployments

This readme describes the process of deploying resources to AWS.

## Prereqs

### Pulumi

```bash
brew install pulumi
```

Copy the contents of `infra/.env.template` to `/infra/.env`. Then update the file to
match the correct values for your environment.

Until we establish a separate state storage location, you will also need to log into Pulumi by running `pulumi login`.

### AWS

You'll need an AWS credential pair with access to create resources in your account.

Specify those credentials using the `/infra/.env` file mentioned above.

### Sourcing environment variables from `.env`

To source environment variables from your .env file, run this command from your terminal:

```bash
export $(grep -v '^#' .env | xargs)
```

## Design

### `pulumi-meltano` IAC Module

This module has definitions for the entire infrastructure.

There are four main deployment layers as of now:

1. **MeltanoData Service Fabric** (Layer 1)
   - This is the foundational services and network resources for the MeltanoData Service.
   - The Service Fabric establishes monitoring, alerting and other capabilities which are shared across all instances.
2. **Site Instances** (Layer 2)
   - Aka "Organizational Account".
   - This is an instance of MeltanoData specific to an organization.
   - Site Instances cannot access resources from other Site Instances.
   - Site Instances contains user and group mappings, as well as ACL.
   - A Site Instance may optionally have one or more Hosted Projects.
3. **Hosted Projects** (Layer 3)
   - A Hosted Project maps to a single git repo and a single `meltano.yml` resource.
   - A Hosted Project understands Meltano concepts such as environments.
   - Not all Meltano environments are automatically activated with services and other cloud resources.
   - A Hosted Project allows users to define rules on which branches should map to which environments, which environments should be activated, and which services should be activated in each environment.
4. **Activated Environments** (Layer 4)
   - An Activated Environment maps to a single Git repo, a single Git ref (such as a branch or tag), an environment name, and a set of rules for which services should be enabled within the environment.
   - Activated Environments are the primary driver of cloud costs, due to the reliance on compute resources.
   - Activated Environments should have an option to archive environment artifacts (logs, data files, etc.) when being disposed.

### Library Design

Module capabilities are organized as follows:

- `pulumi_meltano.service_fabric` - The functions and design of `Layer 1`, as described above.
- `pulumi_meltano.site_instances` - The functions and design of `Layer 2`, as described above.
- `pulumi_meltano.projects` - The functions and design of `Layer 3`, as described above.
- `pulumi_meltano.meltano_environments` - The functions and design of `Layer 4`, as described above.
- `pulumi_meltano.components` - Shared components across modules, for instance common code related to managing EKS, K8, and other AWS resources.

### Cost Profile

1. **MeltanoData Service Fabric**
   - This service benefits from efficiency of scale, and cost per project scales better than linear as number of sites and projects increase.
   - MeltanoData Web UI hosting and associated backend API costs live here.
2. **Site Instances**
   - Primary driver of cost is shared compute services.
   - If we avoid always-on compute resources in this layer, cloud cost of hosting for each site will be low.
3. **Hosted Projects**
   - Cloud cost of hosting each site is relatively low.
   - Primary driver of cost is shared services and we should minimize compute resources in this category if we can.
   - Total costs are expected to scale linearly along with the number of projects.
4. **Activated Environments**
   - Most cloud costs wil likely come from this category (likely 80-90%).
   - Compute from this layer will be charged back to the user, and the user will be incentivized to be mindful of resource usage.

## Manual Deployment

There are four Pulumi projects within the `deployments`, one for each of the layers described above.

To perform a deployment:

1. Switch to the desired directory, e.g.: `cd deployments/01_service_fabric`.
2. Make sure you have completed the [prereqs](#prereqs) described above.
3. From the directory, run `pulumi preview` and then `pulumi up`.
4. If config parameters are needed, those can be set via `Pulumi.yaml`, `Pulumi.dev.yaml`, or similar.
