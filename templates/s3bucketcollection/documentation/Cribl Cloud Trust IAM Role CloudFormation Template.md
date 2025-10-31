<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# Cribl Cloud Trust IAM Role CloudFormation Template

This CloudFormation template creates an IAM role that allows Cribl Cloud to access specific AWS resources in your account. The role is designed to provide Cribl Cloud with the necessary permissions to interact with S3 buckets and SQS queues.

## Template Overview

The template does the following:

1. Creates an IAM role named `CriblTrustCloud`
2. Configures a trust relationship with Cribl Cloud's AWS account
3. Attaches a policy that grants access to S3 and SQS resources
4. Outputs the role name, ARN, and an external ID for authentication

## Parameters

- `CriblCloudAccountID`: The AWS account ID of Cribl Cloud (default: '012345678910')


## IAM Role Details

### Trust Relationship

The role trusts two specific roles in the Cribl Cloud account:

- `arn:aws:iam::{CriblCloudAccountID}:role/search-exec-main`
- `arn:aws:iam::{CriblCloudAccountID}:role/main-default`

These roles can assume the `CriblTrustCloud` role using the `sts:AssumeRole`, `sts:TagSession`, and `sts:SetSourceIdentity` actions.

### Permissions

The role has a policy named `CriblCloudS3SQSPolicy` that grants the following permissions:

1. S3 access:
    - List buckets
    - Get and put objects
    - Get bucket location
2. SQS access:
    - Receive and delete messages
    - Change message visibility
    - Get queue attributes and URL

These permissions apply to all S3 buckets and SQS queues in the account.

## Security Feature

The template includes a security feature that requires an external ID for authentication. This external ID is derived from the CloudFormation stack ID, providing an additional layer of security when assuming the role.

## Outputs

The template provides three outputs:

1. `RoleName`: The name of the created IAM role
2. `RoleArn`: The ARN of the created role
3. `ExternalId`: The external ID required for authentication when assuming the role

## Usage

To use this template:

1. Deploy it in your AWS account using CloudFormation
2. Provide the resulting role ARN and external ID to Cribl Cloud
3. Cribl Cloud can then assume this role to access your S3 and SQS resources

Remember to review and adjust the permissions as necessary to align with your security requirements and the specific needs of your Cribl Cloud integration [^1][^2][^4].

<div style="text-align: center">⁂</div>

[^1]: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html

[^2]: https://github.com/criblio/cribl-aws-cloudformation-templates

[^3]: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/format-version-structure.html

[^4]: https://awsfundamentals.com/blog/aws-iam-roles-with-aws-cloudformation

[^5]: https://d1.awsstatic.com/Marketplace/solutions-center/downloads/AWSMP-CT-Cribl-Implementation-Guide.pdf

[^6]: https://github.com/awslabs/aws-cloudformation-template-builder/blob/master/README.md

[^7]: https://cloudkatha.com/how-to-create-iam-role-using-cloudformation/

[^8]: https://aws-ia.github.io/cfn-ps-cribl-cloudtrail/

[^9]: https://docs.cribl.io/stream/usecase-aws-x-account/

[^10]: https://docs.cribl.io/search/set-up-aws#permission-requirements-for-aws-api/