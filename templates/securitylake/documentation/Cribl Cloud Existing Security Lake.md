<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# IAM Role and SQS Configuration for Cribl Integration with Amazon Security Lake

## Description
This CloudFormation template sets up the necessary resources to grant access to your Cribl tenant for collecting data from existing Amazon Security Lake S3 buckets. It includes an SQS queue and a corresponding policy to enable secure communication between Amazon Security Lake and Cribl Cloud.

---

## Features
### Resources Created
1. **SQS Queue (`CriblASLSQS`)**
   - Creates an Amazon SQS queue named according to the `AmazonSecurityLakeSQS` parameter.
   - Facilitates message exchange for Amazon Security Lake.

2. **SQS Queue Policy (`CriblASLQueuePolicy`)**
   - Grants permissions for:
     - **Amazon EventBridge**: Sending messages to the SQS queue.
     - **Cribl Cloud Trust ARN**: Receiving, deleting messages, and accessing queue attributes.

### Outputs
1. **CriblCloudTrustARN**: The ARN of the existing IAM role used by Cribl Cloud.
2. **AmazonSecurityLakeSQS**: The ARN of the created SQS queue.

---

## Parameters
- **CriblCloudTrustARN**: The ARN of the Cribl Cloud Trust role, found in the Cribl Cloud UI under the Trust section.
- **AmazonSecurityLakeSQS**: The name of the Amazon Security Lake SQS queue. Default value is `cribl-sqs-asl`.

---

## Usage
This template is designed to integrate Cribl with your Amazon Security Lake environment, enabling seamless data collection and routing. It ensures secure access for Cribl Cloud services while maintaining control over permissions.

### Permissions
The SQS Queue Policy ensures:
- EventBridge can send messages to the queue.
- Cribl Cloud Trust ARN can interact with the queue for message processing.

---

## How to Deploy
1. Retrieve the `CriblCloudTrustARN` from your Cribl Cloud UI under the Trust section.
2. Update the `AmazonSecurityLakeSQS` parameter if a custom queue name is required.
3. Deploy the template using AWS CloudFormation in your preferred region.

---

## Notes
- Ensure that `CriblCloudTrustARN` matches the ARN provided by Cribl Cloud for proper integration.
- Modify the policy if additional permissions are needed for your use case.
