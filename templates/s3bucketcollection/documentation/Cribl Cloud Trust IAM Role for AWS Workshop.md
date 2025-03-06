<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# Cribl Cloud Trust IAM Role for AWS Workshop

This CloudFormation template creates an IAM role and associated resources to enable Cribl Cloud Search and Stream to access S3 buckets for the AWS Workshop (https://cribl.awsworkshop.io/). It sets up the necessary permissions and infrastructure for secure, efficient log storage and processing.

## Template Overview

The template performs the following actions:

1. Creates two S3 buckets for testing purposes
2. Establishes an IAM role with a trust relationship to Cribl Cloud
3. Configures permissions for S3 access
4. Outputs relevant information for Cribl Cloud integration

## Parameters

- `CriblCloudAccountID`: Cribl Cloud's AWS account ID for trust relationship (default: '012345678910')

## Resources Created

### S3 Buckets

1. `s3DefaultSecurityLake`: For testing Amazon Security Lake Destination
2. `s3DefaultSIEM`: For testing SIEM Destination

Both buckets are configured with public access blocked for security.

### IAM Role (`CriblTrustCloud`)

#### Trust Relationship

Allows two specific roles from the Cribl Cloud account to assume this role:

- `arn:aws:iam::{CriblCloudAccountID}:role/search-exec-main`
- `arn:aws:iam::{CriblCloudAccountID}:role/main-default`


#### Permissions

The role has an inline policy granting S3 access to both created buckets:

- List bucket
- Get and put objects
- Get bucket location


## Security Features

- Uses an external ID derived from the stack ID for additional security when assuming the role
- Limits S3 access to only the specified buckets
- Blocks public access to the S3 buckets


## Outputs

- `SecurityLakeBucket`: ARN of the S3 bucket for testing Amazon Security Lake Destination
- `SIEMBucket`: ARN of the S3 bucket for testing SIEM Destination
- `RoleName`: Name of the created IAM role
- `RoleArn`: ARN of the created IAM role
- `ExternalId`: The external ID for role assumption


## Usage

1. Deploy this template in your AWS account
2. Use the outputted information to configure Cribl Cloud for the AWS Workshop
3. Utilize the created S3 buckets for testing Security Lake and SIEM destinations

This setup enables Cribl Cloud to securely access and process data in the created S3 buckets, facilitating the AWS Workshop exercises and demonstrations.

<div style="text-align: center">⁂</div>

[^1]: https://cribl.io/blog/securely-connecting-aws-s3-destination-to-cribl-cloud-and-hybrid-workers/

[^2]: https://docs.cribl.io/search/aws-access

[^3]: https://aws.amazon.com/partners/success/cribl/

[^4]: https://docs.cribl.io/stream/usecase-aws-x-account/

[^5]: https://docs.cribl.io/search/set-up-aws/

[^6]: https://workshops.aws/categories/IAM

[^7]: https://docs.cribl.io/suite/usecase-s3/

[^8]: https://aws.amazon.com/blogs/awsmarketplace/cribl-stream-observability-aws-control-tower-account-factory-customization/

