<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>


# Cribl Stream Worker Deployment (amd64)

This CloudFormation template deploys Cribl Stream workers in AWS. It automates the deployment and configuration of worker nodes that connect to a Cribl Cloud leader for centralized management and configuration. This template is designed for amd64 architecture.

## Template Overview

The template automates the deployment of Cribl Stream workers by:

1. Creating a Security Group for network access.
2. Setting up an IAM Role with necessary permissions for worker nodes.
3. Configuring an Auto Scaling Group (ASG) to manage the worker nodes.
4. Defining a Launch Template to configure worker nodes upon creation.
5. Creating an SQS queue and a Lambda function to gracefully shut down Cribl Stream worker nodes when the ASG scales down.
6. Creating a secret in Secrets Manager to store the Cribl cluster authentication token.

## Parameters

The template requires the following parameters:

* **criblCloudLeader**: (Required) The hostname of your Cribl Cloud leader node (e.g., `my-cribl-leader.cribl.cloud`). Do not include `https://`.
* **criblclusterAuthToken**: (Required) The authentication token from your Cribl Cloud leader. This is a sensitive parameter and is marked `NoEcho`.
* **workerGroup**: The Cribl Stream worker group to assign the worker nodes to (defaults to `default`).
* **workerCount**: (Required) Enter the number of worker nodes desired.
* **vpcId**: (Required) The ID of your existing VPC where the worker nodes will be deployed.
* **subnetIds**: (Required) Select 2 subnet IDs in different Availability Zones within the specified VPC.
* **ImageId**: (Required) The AMI ID for the EC2 instance being used for your Cribl Deployment. This AMI should be pre-configured with the necessary Cribl dependencies.
* **workerInstanceType**: The EC2 instance type for the worker nodes (defaults to `c5a.xlarge`). A list of allowed instance types is provided in the template.
* **AdditionalPolicies**: A comma-separated list of IAM policy ARNs to attach to the worker nodes' IAM role. Defaults to `arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore,arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy`. These policies are required to allow the SSM agent and Cloudwatch agent to run. Ensure that the provided policies are comma-separated.


## Resources Created

* **ec2WorkerSecurityGroup**: A security group for the worker nodes, allowing egress traffic.
* **s3DefaultDestinationBucket**: An S3 bucket used as the default destination for Cribl Stream. Public access is blocked.
* **StreamRole**: An IAM role for the worker nodes, granting permissions to:
    * Assume the role by EC2 instances.
    * Put, get, and list objects in the `s3DefaultDestinationBucket`.
    * Get Kinesis records and shard iterators.
    * Get secrets from AWS Secrets Manager.
* **StreamInstanceProfile**: An IAM instance profile associated with the `StreamRole`.
* **clusterAuthToken**: A Secrets Manager Secret for storing the Cribl Stream cluster authentication token.
* **ec2WorkersAutoScalingGroup**: An Auto Scaling Group to manage the Cribl Stream worker nodes.
* **ec2WorkersAutoScalingGroupLifecycleHook**: Lifecycle hook to stop worker nodes gracefully before termination
* **ec2WorkerslaunchTemplate**: A launch template defining the configuration for the worker nodes, including:
    * Instance type.
    * AMI ID.
    * IAM instance profile.
    * Security group.
    * User data to configure Cribl Stream on startup.
* **functionWorkerShutdown**: A Lambda function that gracefully shuts down Cribl Stream worker nodes.
* **workerShutdownEventRule**: Cloudwatch event rule to trigger `functionWorkerShutdown` upon EC2 termination.
* **lamdbaPermissionWorkerShutdownEventRule**: Lambda permissions for WorkerShutdownEventRule.


## Security Considerations

* The template uses Secrets Manager to store the Cribl Stream authentication token.
* The security group allows egress traffic. Restrict this further based on your security requirements.
* The IAM role is granted access to S3 buckets and Kinesis streams.  Consider limiting these permissions to specific resources.
* Ensure that the AMI specified in the `ImageId` parameter is from a trusted source and properly secured.


## User Data Script

The launch template includes a user data script that configures the Cribl Stream worker nodes on startup. This script:

* Sets the AWS region.
* Configures Cribl Stream as a worker node, connecting to the Cribl Cloud leader.
* Assigns the worker node to the specified worker group.


## Lambda Function for Graceful Shutdown

The template includes a Lambda function (`functionWorkerShutdown`) that is triggered when an EC2 instance in the Auto Scaling Group is terminating. This function gracefully shuts down the Cribl Stream worker node by:

1. Disabling and stopping the Cribl service using SSM.
2. Completing the lifecycle action to allow the instance to terminate.

This ensures that data in flight is properly processed before the instance is terminated.

## Outputs

* **StreamWebUrlPublic**: The URL for the Cribl Cloud Stream login page (`https://cribl.cloud`).
* **stackName**: The name of the CloudFormation stack.


## Usage

1. Populate the required parameters: `criblCloudLeader`, `criblclusterAuthToken`, `workerCount`, `vpcId`, `subnetIds`, and `ImageId`.
2. Optionally customize the `workerGroup`, `workerInstanceType`, and `AdditionalPolicies`.
3. Launch the CloudFormation stack with the configured parameters.
4. Verify that the appropriate number of worker nodes have joined your Cribl Cloud environment.

## Pre-requisites

* An existing Cribl Cloud account.
* A configured VPC with at least two subnets in different Availability Zones.
* An AMI with Cribl pre-installed and configured.
* Appropriate security policies and IAM roles to allow the CloudFormation template to create and manage resources in your AWS account.

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/11857645/fd6318c7-152b-4de9-a67b-97846c6a8917/free_x86_64_template.yaml

