<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# Cribl Cloud Trust IAM Role for VPC Flow Logs Access

This CloudFormation template creates an IAM role and associated resources to enable Cribl Cloud Search and Stream to access an existing VPC Flow S3 bucket. It sets up the necessary permissions and infrastructure for secure, efficient log retrieval and processing.

## Template Overview

The template performs the following actions:

1. Creates an SQS queue for VPC Flow log notifications
2. Establishes an IAM role with a trust relationship to Cribl Cloud
3. Configures permissions for S3 and SQS access
4. Outputs relevant information for Cribl Cloud integration

## Parameters

- `VPCFlowS3`: The existing S3 bucket containing VPC Flow logs
- `VPCSQS`: Name of the SQS queue for VPC Flow log notifications (default: cribl-vpc-sqs)
- `CriblCloudAccountID`: Cribl Cloud's AWS account ID for trust relationship


## Resources Created

### SQS Queue (`CriblVPCQueue`)

An SQS queue named according to the `VPCSQS` parameter, used for VPC Flow S3 event notifications.

### SQS Queue Policy (`CriblVPCQueuePolicy`)

Allows the S3 service to send messages to the SQS queue, restricted to the account owning the CloudFormation stack.

### IAM Role (`CriblTrustCloud`)

#### Trust Relationship

Allows two specific roles from the Cribl Cloud account to assume this role:

- `arn:aws:iam::{CriblCloudAccountID}:role/search-exec-main`
- `arn:aws:iam::{CriblCloudAccountID}:role/main-default`


#### Permissions

The role has an inline policy granting:

1. S3 access to the specified VPC Flow bucket:
    - List bucket
    - Get and put objects
    - Get bucket location
2. SQS access to the created queue:
    - Receive and delete messages
    - Change message visibility
    - Get queue attributes and URL

## Security Features

- Uses an external ID derived from the stack ID for additional security when assuming the role
- Limits S3 access to only the specified VPC Flow bucket
- Restricts SQS access to only the created queue


## Outputs

- `VPCFlowS3`: The S3 bucket containing VPC Flow logs
- `VPCSQS`: ARN of the created SQS queue
- `RoleName`: Name of the created IAM role
- `RoleArn`: ARN of the created IAM role
- `ExternalId`: The external ID for role assumption


## Usage

1. Deploy this template in your AWS account
2. Provide the resulting role ARN, SQS queue ARN, and external ID to Cribl Cloud
3. Configure Cribl Cloud to use these credentials for accessing your VPC Flow logs

This setup enables Cribl Cloud to securely access and process your VPC Flow logs, facilitating advanced log analysis and management capabilities.

<div style="text-align: center">⁂</div>

[^1]: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-iam-role.html

[^2]: https://community.cribl.io/discussion/67/how-do-i-create-a-trust-between-my-aws-account-and-a-cribl-cloud-instance

[^3]: https://cribl.io/blog/manage-data-collection-across-aws-accounts/

[^4]: https://docs.cribl.io/stream/4.5/cloud-portal/

[^5]: https://serverfault.com/questions/721538/how-to-set-up-iam-role-permissions-for-vpc-cloudwatch-logs

[^6]: https://cribl.io/blog/securely-connecting-aws-s3-destination-to-cribl-cloud-and-hybrid-workers/

[^7]: https://docs.cribl.io/stream/usecase-firewall-logs/

[^8]: https://github.com/criblio/cribl-aws-cloudformation-templates

[^9]: https://docs.cribl.io/stream/usecase-aws-x-account/

[^10]: https://docs.cribl.io/search/aws-access

