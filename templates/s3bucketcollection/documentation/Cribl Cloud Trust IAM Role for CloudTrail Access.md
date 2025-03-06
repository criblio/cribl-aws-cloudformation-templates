<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# Cribl Cloud Trust IAM Role for CloudTrail Access

This CloudFormation template creates an IAM role and associated resources to enable Cribl Cloud Search and Stream to access an existing CloudTrail S3 bucket. It sets up the necessary permissions and infrastructure for secure, efficient log retrieval and processing.

## Template Overview

The template performs the following actions:

1. Creates an SQS queue for CloudTrail log notifications
2. Establishes an IAM role with a trust relationship to Cribl Cloud
3. Configures permissions for S3 and SQS access
4. Outputs relevant information for Cribl Cloud integration

## Parameters

- `CloudTrailsS3`: The existing S3 bucket containing CloudTrail logs
- `CTSQS`: Name of the SQS queue for CloudTrail notifications (default: cribl-cloudtrail-sqs)
- `CriblCloudAccountID`: Cribl Cloud's AWS account ID for trust relationship


## Resources Created

### SQS Queue (`CriblCTQueue`)

An SQS queue named according to the `CTSQS` parameter, used for CloudTrail S3 event notifications.

### SQS Queue Policy (`CriblCTQueuePolicy`)

Allows the S3 service to send messages to the SQS queue, restricted to the account owning the CloudFormation stack.

### IAM Role (`CriblTrustCloud`)

#### Trust Relationship

Allows two specific roles from the Cribl Cloud account to assume this role:

- `arn:aws:iam::{CriblCloudAccountID}:role/search-exec-main`
- `arn:aws:iam::{CriblCloudAccountID}:role/main-default`


#### Permissions

The role has an inline policy granting:

1. S3 access to the specified CloudTrail bucket:
    - List bucket
    - Get and put objects
    - Get bucket location
2. SQS access to the created queue:
    - Receive and delete messages
    - Change message visibility
    - Get queue attributes and URL

## Security Features

- Uses an external ID derived from the stack ID for additional security when assuming the role
- Limits S3 access to only the specified CloudTrail bucket
- Restricts SQS access to only the created queue


## Outputs

- `CloudTrailsS3`: The S3 bucket containing CloudTrail logs
- `CTSQS`: ARN of the created SQS queue
- `RoleName`: Name of the created IAM role
- `RoleArn`: ARN of the created IAM role
- `ExternalId`: The external ID for role assumption


## Usage

1. Deploy this template in your AWS account
2. Provide the resulting role ARN, SQS queue ARN, and external ID to Cribl Cloud
3. Configure Cribl Cloud to use these credentials for accessing your CloudTrail logs

This setup enables Cribl Cloud to securely access and process your CloudTrail logs, facilitating advanced log analysis and management capabilities.

<div style="text-align: center">⁂</div>

[^1]: https://d1.awsstatic.com/Marketplace/solutions-center/downloads/AWSMP-CT-Cribl-Implementation-Guide.pdf

[^2]: https://www.ibm.com/docs/nl/SS42VS_DSM/com.ibm.dsm.doc/t_dsm_guide_configuring_aws_cloudtrail_using_sqs.html

[^3]: https://github.com/criblio/cribl-aws-cloudformation-templates

[^4]: https://repost.aws/questions/QUKYkEoBGkSTu8-gwao4Tcbg/pushing-cloudtrail-logs-to-elasticsearch-via-sqs-and-lambda

[^5]: https://docs.cribl.io/search/aws-access

[^6]: http://docs.rapid7.com/insightidr/aws-cloudtrail-sqs

[^7]: https://community.cribl.io/discussion/67/how-do-i-create-a-trust-between-my-aws-account-and-a-cribl-cloud-instance

[^8]: https://www.googlecloudcommunity.com/gc/SecOps-SIEM/AWS-Cloud-trail-logs-ingestion/m-p/830935

[^9]: https://aws-ia.github.io/cfn-ps-cribl-cloudtrail/

