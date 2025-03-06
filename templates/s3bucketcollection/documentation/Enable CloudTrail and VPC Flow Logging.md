<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# Enable CloudTrail and VPC Flow Logging for Cribl Cloud


This document explains the resources that will be created when deploying the provided CloudFormation template. The template is designed to create an IAM role that trusts Cribl Cloud and sets up CloudTrail and VPC Flow logging to an S3 bucket.

## Template Overview

The template automates the creation of AWS resources to enable centralized logging, specifically focusing on CloudTrail logs and VPC Flow Logs. It creates S3 buckets for storing these logs, SQS queues for triggering processes upon log arrival, and an IAM role to allow Cribl Cloud to access these logs.

## Resources Created

Here's a breakdown of the resources defined in the CloudFormation template:

*   **CriblCTQueue (AWS::SQS::Queue):** Creates an SQS queue named according to the `CTSQS` parameter (default: `cribl-cloudtrail-sqs`). This queue will be used to trigger actions when new CloudTrail logs are written to the S3 bucket.

    *   **Properties:**
        *   `QueueName`: `!Ref CTSQS` - Sets the queue name to the value of the `CTSQS` parameter.

*   **CriblCTQueuePolicy (AWS::SQS::QueuePolicy):** Defines the policy for the `CriblCTQueue`, allowing `s3.amazonaws.com` to send messages to the queue. The policy includes a condition that the source account must match the AWS account ID in which the stack is deployed. This ensures only S3 events from the current AWS account can trigger the queue.

    *   **Properties:**
        *   `PolicyDocument`:
            *   `Statement`:
                *   `Effect`: `Allow` - Allows actions specified in the policy.
                *   `Principal`: `Service: s3.amazonaws.com` - Specifies the service that can perform the actions.
                *   `Action`: `SQS:SendMessage` - Allows sending messages to the queue.
                *   `Resource`: `!GetAtt CriblCTQueue.Arn` - The ARN of the SQS queue.
                *   `Condition`:
                    *   `StringEquals`: `'aws:SourceAccount': !Ref AWS::AccountId` - Restricts the source account to the account where the stack is deployed.
        *   `Queues`: `!Ref CTSQS` - Associates the policy with the SQS queue.

*   **TrailBucket (AWS::S3::Bucket):** Creates an S3 bucket used to store CloudTrail logs. The bucket is configured with a `NotificationConfiguration` that sends an event to the `CriblCTQueue` when a new object is created (specifically, a PUT operation). This will trigger processing when new CloudTrail logs are available.

    *   **Properties:**
        *   `NotificationConfiguration`:
            *   `QueueConfigurations`:
                *   `Event`: `s3:ObjectCreated:Put` - Specifies that the notification should be triggered when an object is created using a PUT operation.
                *   `Queue`: `!GetAtt CriblCTQueue.Arn` - The ARN of the SQS queue to send the notification to.
    *   `DependsOn`: `CriblCTQueuePolicy` - Ensures that the queue policy is created before the bucket.

*   **TrailBucketPolicy (AWS::S3::BucketPolicy):** Defines the policy for the `TrailBucket`. This policy grants permissions to:
    *   `delivery.logs.amazonaws.com`: Allows the AWS Logs service to write objects to the bucket, ensuring proper log delivery. It requires `bucket-owner-full-control` ACL.
    *   `cloudtrail.amazonaws.com`: Allows CloudTrail to get the bucket ACL and put objects into the bucket. It also requires `bucket-owner-full-control` ACL.
    *   A `Deny` statement that enforces the use of SSL for all requests to the bucket, enhancing security.

    *   **Properties:**
        *   `Bucket`: `!Ref TrailBucket` - The name of the S3 bucket.
        *   `PolicyDocument`:
            *   `Version`: `2012-10-17` - The version of the policy document.
            *   `Statement`:
                *   `Sid`: `AWSLogDeliveryWrite`
                    *   `Effect`: `Allow` - Allows the action specified.
                    *   `Principal`: `Service: delivery.logs.amazonaws.com` - The AWS Logs service principal.
                    *   `Action`: `s3:PutObject` - Allows putting objects into the bucket.
                    *   `Resource`: `!Sub '${TrailBucket.Arn}/AWSLogs/'` - The S3 bucket and prefix to allow the action on.
                    *   `Condition`: `StringEquals: 's3:x-amz-acl': bucket-owner-full-control` - Requires the `bucket-owner-full-control` ACL.
                *   `Sid`: `AWSCloudTrailAclCheck`
                    *   `Effect`: `Allow`
                    *   `Principal`: `Service: cloudtrail.amazonaws.com`
                    *   `Action`: `s3:GetBucketAcl`
                    *   `Resource`: `!Sub '${TrailBucket.Arn}'`
                *   `Sid`: `AWSCloudTrailWrite`
                    *   `Effect`: `Allow`
                    *   `Principal`: `Service: cloudtrail.amazonaws.com`
                    *   `Action`: `s3:PutObject`
                    *   `Resource`: `!Sub '${TrailBucket.Arn}/AWSLogs/*/*'`
                    *   `Condition`: `StringEquals: 's3:x-amz-acl': 'bucket-owner-full-control'`
                *   `Sid`: `AllowSSLRequestsOnly`
                    *   `Effect`: `Deny`
                    *   `Principal`: `*` - Applies to all principals.
                    *   `Action`: `s3:*` - Denies all S3 actions.
                    *   `Resource`:
                        *   `!GetAtt TrailBucket.Arn`
                        *   `!Sub '${TrailBucket.Arn}/*'`
                    *   `Condition`: `Bool: 'aws:SecureTransport': false` - Denies requests that are not using SSL.

*   **ExternalTrail (AWS::CloudTrail::Trail):** Creates a CloudTrail trail. It is configured to:

    *   Store logs in the `TrailBucket`.
    *   Include global service events.
    *   Enable logging.
    *   Create a multi-region trail.
    *   Enable log file validation.

    *   **Properties:**
        *   `S3BucketName`: `!Ref TrailBucket` - The name of the S3 bucket where the logs will be stored.
        *   `IncludeGlobalServiceEvents`: `true` - Includes global service events.
        *   `IsLogging`: `true` - Enables logging.
        *   `IsMultiRegionTrail`: `true` - Creates a multi-region trail.
        *   `EnableLogFileValidation`: `true` - Enables log file validation.
        *   `TrailName`: `!Sub '${TrailBucket}-trail'` - Sets the name of the trail.
    *   `DependsOn`:
        *   `TrailBucket`
        *   `TrailBucketPolicy`

*   **CriblVPCQueue (AWS::SQS::Queue):** Creates an SQS queue named according to the `VPCSQS` parameter (default: `cribl-vpc-sqs`). This queue will be used to trigger actions when new VPC Flow Logs are written to the S3 bucket.

    *   **Properties:**
        *   `QueueName`: `!Ref VPCSQS` - Sets the queue name.

*   **CriblVPCQueuePolicy (AWS::SQS::QueuePolicy):** Defines the policy for the `CriblVPCQueue`, allowing `s3.amazonaws.com` to send messages to the queue. Similar to `CriblCTQueuePolicy`, it restricts access to events originating from the same AWS account.

    *   **Properties:**
        *   `PolicyDocument`:
            *   `Statement`:
                *   `Effect`: `Allow`
                *   `Principal`: `Service: s3.amazonaws.com`
                *   `Action`: `SQS:SendMessage`
                *   `Resource`: `!GetAtt CriblVPCQueue.Arn`
                *   `Condition`: `StringEquals: 'aws:SourceAccount': !Ref "AWS::AccountId"`
        *   `Queues`: `!Ref VPCSQS`

*   **LogBucket (AWS::S3::Bucket):** Creates an S3 bucket used to store VPC Flow Logs. The bucket is configured with a `NotificationConfiguration` to send an event to the `CriblVPCQueue` when new objects are created.

    *   **Properties:**
        *   `NotificationConfiguration`:
            *   `QueueConfigurations`:
                *   `Event`: `s3:ObjectCreated:Put`
                *   `Queue`: `!GetAtt CriblVPCQueue.Arn`
    *   `DependsOn`: `CriblVPCQueuePolicy`

*   **LogBucketPolicy (AWS::S3::BucketPolicy):** Defines the policy for the `LogBucket`. This policy grants permissions to:
    *   `delivery.logs.amazonaws.com`: Allows the AWS Logs service to write objects to the bucket. It requires `bucket-owner-full-control` ACL.
    *   Allows `delivery.logs.amazonaws.com` to get the bucket ACL.
    *   Enforces SSL for all requests to the bucket.

    *   **Properties:**
        *   `Bucket`: `!Ref LogBucket`
        *   `PolicyDocument`:
            *   `Version`: `2012-10-17`
            *   `Statement`:
                *   `Sid`: `AWSLogDeliveryWrite`
                    *   `Effect`: `Allow`
                    *   `Principal`: `Service: delivery.logs.amazonaws.com`
                    *   `Action`: `s3:PutObject`
                    *   `Resource`: `!Sub '${LogBucket.Arn}/AWSLogs/${AWS::AccountId}/*'`
                    *   `Condition`: `StringEquals: 's3:x-amz-acl': bucket-owner-full-control`
                *   `Sid`: `AWSLogDeliveryAclCheck`
                    *   `Effect`: `Allow`
                    *   `Principal`: `Service: delivery.logs.amazonaws.com`
                    *   `Action`: `s3:GetBucketAcl`
                    *   `Resource`: `!GetAtt LogBucket.Arn`
                *   `Sid`: `AllowSSLRequestsOnly`
                    *   `Effect`: `Deny`
                    *   `Principal`: `*`
                    *   `Action`: `s3:*`
                    *   `Resource`:
                        *   `!GetAtt LogBucket.Arn`
                        *   `!Sub '${LogBucket.Arn}/*'`
                    *   `Condition`: `Bool: 'aws:SecureTransport': false`

*   **FlowLog (AWS::EC2::FlowLog):** Creates a VPC Flow Log that captures network traffic information for the VPC specified in the `VPCId` parameter. The flow logs are stored in the `LogBucket`. The type of traffic to log is determined by the `TrafficType` parameter (ALL, ACCEPT, or REJECT).

    *   **Properties:**
        *   `LogDestination`: `!Sub 'arn:${AWS::Partition}:s3:::${LogBucket}'` - The ARN of the S3 bucket where the flow logs will be stored.
        *   `LogDestinationType`: `s3` - Specifies that the destination is an S3 bucket.
        *   `ResourceId`: `!Ref VPCId` - The ID of the VPC to log.
        *   `ResourceType`: `VPC` - Specifies that the resource is a VPC.
        *   `TrafficType`: `!Ref TrafficType` - The type of traffic to log (ALL, ACCEPT, REJECT).

*   **CriblTrustCloud (AWS::IAM::Role):** Creates an IAM role that allows Cribl Cloud to access AWS resources.

    *   **Properties:**
        *   `AssumeRolePolicyDocument`:
            *   `Version`: `2012-10-17`
            *   `Statement`:
                *   `Effect`: `Allow`
                *   `Principal`:
                    *   `AWS`:
                        *   `!Sub 'arn:aws:iam::${CriblCloudAccountID}:role/search-exec-main'`
                        *   `!Sub 'arn:aws:iam::${CriblCloudAccountID}:role/main-default'`
                *   `Action`:
                    *   `sts:AssumeRole`
                    *   `sts:TagSession`
                    *   `sts:SetSourceIdentity`
                *   `Condition`:
                    *   `StringEquals`: `'sts:ExternalId': !Select - 4 - !Split - '-' - !Select - 2 - !Split - '/' - !Ref 'AWS::StackId'`
        *   `Description`: `Role to provide access AWS resources from Cribl Cloud Trust`
        *   `Policies`:
            *   `PolicyName`: `SQS`
                *   `PolicyDocument`:
                    *   `Version`: `2012-10-17`
                    *   `Statement`:
                        *   `Effect`: `Allow`
                        *   `Action`:
                            *   `sqs:ReceiveMessage`
                            *   `sqs:DeleteMessage`
                            *   `sqs:GetQueueAttributes`
                            *   `sqs:GetQueueUrl`
                        *   `Resource`:
                            *   `!GetAtt CriblCTQueue.Arn`
                            *   `!GetAtt CriblVPCQueue.Arn`
            *   `PolicyName`: `S3EmbeddedInlinePolicy`
                *   `PolicyDocument`:
                    *   `Version`: `2012-10-17`
                    *   `Statement`:
                        *   `Effect`: `Allow`
                        *   `Action`:
                            *   `s3:ListBucket`
                            *   `s3:GetObject`
                            *   `s3:PutObject`
                            *   `s3:GetBucketLocation`
                        *   `Resource`:
                            *   `!Sub ${TrailBucket.Arn}`
                            *   `!Sub ${TrailBucket.Arn}/*`
                            *   `!Sub ${LogBucket.Arn}`
                            *   `!Sub ${LogBucket.Arn}/*`

## Parameters

The template utilizes parameters to allow customization during deployment:

*   **CriblCloudAccountID:** The AWS account ID of the Cribl Cloud instance. This is required for the IAM role's trust relationship.
    *   `Description`: `Cribl Cloud Trust AWS Account ID. Navigate to Cribl.Cloud, go to Workspace and click on Access. Find the Trust and copy the AWS Account ID found in the trust ARN.`
    *   `Type`: `String`
    *   `Default`: `'012345678910'`
*   **CTSQS:** The name of the SQS queue for CloudTrail logs.
    *   `Description`: `Name of the SQS queue for CloudTrail to trigger for S3 log retrieval.`
    *   `Type`: `String`
    *   `Default`: `cribl-cloudtrail-sqs`
*   **TrafficType:** The type of traffic to log for VPC Flow Logs (ALL, ACCEPT, REJECT).
    *   `Description`: `The type of traffic to log.`
    *   `Type`: `String`
    *   `Default`: `ALL`
    *   `AllowedValues`: `ACCEPT`, `REJECT`, `ALL`
*   **VPCSQS:** The name of the SQS queue for VPC Flow Logs.
    *   `Description`: `Name of the SQS for VPCFlow Logs.`
    *   `Type`: `String`
    *   `Default`: `cribl-vpc-sqs`
*   **VPCId:** The ID of the VPC for which to enable flow logging.
    *   `Description`: `Select your VPC to enable logging`
    *   `Type`: `AWS::EC2::VPC::Id`

## Outputs

The template defines outputs that provide key information about the created resources:

*   **CloudTrailS3Bucket:** The ARN of the S3 bucket storing CloudTrail logs.
    *   `Description`: `Amazon S3 Bucket for CloudTrail Events`
    *   `Value`: `!GetAtt TrailBucket.Arn`
*   **VPCFlowLogsS3Bucket:** The ARN of the S3 bucket storing VPC Flow Logs.
    *   `Description`: `Amazon S3 Bucket for VPC Flow Logs`
    *   `Value`: `!GetAtt LogBucket.Arn`
*   **RoleName:** The name of the created IAM role.
    *   `Description`: `Name of created IAM Role`
    *   `Value`: `!Ref CriblTrustCloud`
*   **RoleArn:** The ARN of the created IAM role.
    *   `Description`: `Arn of created Role`
    *   `Value`: `!GetAtt CriblTrustCloud.Arn`
*   **ExternalId:** The external ID used for authentication when assuming the IAM role.
    *   `Description`: `External Id for authentication`
    *   `Value`: `!Select - 4 - !Split - '-' - !Select - 2 - !Split - '/' - !Ref 'AWS::StackId'`

## Deployment Considerations

*   **Cribl Cloud Account ID:** Ensure the `CriblCloudAccountID` parameter is set to the correct AWS account ID for your Cribl Cloud instance. This is crucial for establishing the trust relationship.
*   **S3 Bucket Names:** S3 bucket names must be globally unique. If the template is deployed multiple times in the same region, you may need to adjust the names of the buckets. Consider using a Stack name prefix.
*   **VPC ID:** The `VPCId` parameter should be set to the ID of the VPC for which you want to enable flow logging.
*   **Security:** Regularly review and update IAM policies to adhere to the principle of least privilege. Consider using more restrictive S3 bucket policies if necessary.
*   **SQS Queue Configuration:** Monitor the SQS queues for backlog and adjust the processing capacity accordingly.
*   **CloudTrail Configuration:** Confirm that CloudTrail is properly configured to deliver logs to the designated S3 bucket.
*   **VPC Flow Log Configuration:** Verify that VPC Flow Logs are correctly capturing network traffic.
*   **External ID:** The External ID is a critical security measure for cross-account access. Make sure it's correctly configured in both AWS and Cribl Cloud.

This detailed explanation provides a comprehensive understanding of the resources created by the CloudFormation template, enabling informed deployment and management. Remember to adapt parameters to your specific environment and security requirements.


