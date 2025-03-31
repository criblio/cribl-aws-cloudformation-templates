<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# IAM Role for Cribl Cloud Search and Stream for Amazon Security Lake

## Description
This CloudFormation template creates an IAM role to facilitate secure access for Cribl Cloud services (Search and Stream) to interact with Amazon Security Lake and other AWS resources. The role includes a trust relationship with Cribl Cloud's AWS account and permissions to access specific AWS services.

---

## Features
### Resources Created
1. **IAM Role (`CriblTrustCloud`)**
   - Trust relationship allowing Cribl Cloud's roles (`search-exec-main` and `main-default`) to assume this role.
   - Inline policy granting permissions for:
     - **Amazon S3**: Listing buckets, retrieving objects, uploading objects, and accessing bucket locations.
     - **Amazon Security Lake**: Listing data lakes.
     - **Amazon SQS**: Receiving, deleting, changing visibility of messages, and accessing queue attributes.

### Outputs
1. **RoleName**: The name of the created IAM role.
2. **RoleArn**: The Amazon Resource Name (ARN) of the created IAM role.
3. **ExternalId**: A unique identifier used for authentication purposes.

---

## Parameters
- **CriblCloudAccountID**: The AWS account ID for Cribl Cloud Trust. Default value is `012345678910`.

---

## Usage
This IAM role is designed to integrate Cribl Cloud services with your AWS environment securely. It enables Cribl Cloud to access resources such as S3 buckets, Security Lake data lakes, and SQS queues required for its operations.

### Trust Relationship
The `AssumeRolePolicyDocument` specifies that only roles from the provided Cribl Cloud account ID can assume this role, ensuring secure cross-account access.

### Permissions
The inline policy grants the necessary permissions for Cribl Cloud services to interact with:
- Amazon S3 buckets for data storage and retrieval.
- Amazon Security Lake for managing data lakes.
- Amazon SQS queues for message processing.

---

## How to Deploy
1. Update the `CriblCloudAccountID` parameter with the correct AWS account ID provided by Cribl Cloud.
2. Deploy the template using AWS CloudFormation in your preferred region.

---

## Notes
- Ensure that the `CriblCloudAccountID` matches the account ID provided by Cribl Cloud to establish the trust relationship correctly.
- Modify the inline policy if additional permissions are required for your use case.
```

<div>⁂</div>

[^1]: https://awsfundamentals.com/blog/aws-iam-roles-with-aws-cloudformation

[^2]: https://docs.cribl.io/stream/usecase-aws-x-account/

[^3]: https://github.com/criblio/cribl-aws-cloudformation-templates

[^4]: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html

[^5]: https://cribl.io/blog/securely-connecting-aws-s3-destination-to-cribl-cloud-and-hybrid-workers/

[^6]: https://gist.github.com/t04glovern/b41057b1577d495027db83e3d6837bee

[^7]: https://cloudkatha.com/how-to-create-iam-role-using-cloudformation/

[^8]: https://docs.cribl.io/search/aws-access

