<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# Cribl Stream Hybrid Worker Deployment (arm64)

This CloudFormation template deploys Cribl Stream workers in AWS. It's designed to provision and configure worker nodes that connect to a Cribl Cloud leader for centralized management and configuration.

## Template Overview

The template automates the deployment of Cribl Stream workers by:

1. Setting up required infrastructure components like security groups and IAM roles.
2. Configuring an Auto Scaling Group (ASG) to manage the worker nodes.
3. Using a launch template to define worker node configuration.
4. Creating an SQS queue to configure worker node shutdown
5. Creating a Lambda function that gracefully shuts down Cribl Stream worker nodes when the ASG scales down.

## Parameters

The template requires several parameters to be configured:

* **criblCloudLeader**: The hostname of your Cribl Cloud leader node.
* **criblclusterAuthToken**: The authentication token from your Cribl Cloud leader. This is a sensitive parameter and is marked `NoEcho`.
* **workerGroup**: The Cribl Stream worker group to assign the worker nodes to (defaults to `default`).
* **workerCount**: The desired number of worker nodes in the ASG.
* **vpcId**: The ID of your existing VPC where the worker nodes will be deployed.
* **subnetIds**: A list of two subnet IDs in different Availability Zones within the specified VPC.
* **ImageId**: The AMI ID for the EC2 instances to be used as Cribl Stream workers.
* **workerInstanceType**: The EC2 instance type for the worker nodes (defaults to `c6g.xlarge`). A variety of `t4g`, `m6g`, `m7g`, `m8g`, `c6g`, and `c7g` instance types are supported.
* **AdditionalPolicies**: A comma-separated list of IAM policy ARNs to attach to the worker nodes' IAM role. Defaults to `arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore,arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy`.


## Resources Created

* **ec2WorkerSecurityGroup**: A security group for the worker nodes, allowing egress traffic.
* **s3DefaultDestinationBucket**: An S3 bucket used as the default destination for Cribl Stream. Public access is blocked.
* **StreamRole**: An IAM role for the worker nodes, granting permissions to:
    * Assume the role by EC2 instances.
    * Put, get, and list objects in the `s3DefaultDestinationBucket`.
    * Get Kinesis records and shard iterators.
    * Get secrets from AWS Secrets Manager.
* **StreamInstanceProfile**: An IAM instance profile associated with the `StreamRole`.
* **clusterAuthToken**:  A Secrets Manager Secret for storing the Cribl Stream cluster authentication token.
* **ec2WorkersAutoScalingGroup**: An Auto Scaling Group to manage the Cribl Stream worker nodes.
* **ec2WorkersAutoScalingGroupLifecycleHook**:  Lifecycle hook to stop worker nodes gracefully before termination
* **ec2WorkerslaunchTemplate**: A launch template defining the configuration for the worker nodes, including:
    * Instance type.
    * AMI ID.
    * IAM instance profile.
    * Security group.
    * User data to configure Cribl Stream on startup.
* **functionWorkerShutdown**: A Lambda function that gracefully shuts down Cribl Stream worker nodes
* **workerShutdownEventRule**: Cloudwatch event rule to trigger functionWorkerShutdown upon ec2 termination
* **lamdbaPermissionWorkerShutdownEventRule**: Lambda permissions for WorkerShutdownEventRule


## Security Considerations

* The template uses Secrets Manager to store the Cribl Stream authentication token.
* The security group allows egress traffic. You may want to restrict this further based on your security requirements.
* The IAM role is granted access to S3 buckets and Kinesis streams. Consider limiting these permissions to specific resources.


## User Data Script

The launch template includes a user data script that configures the Cribl Stream worker nodes on startup. This script:

* Sets the AWS region.
* Configures Cribl Stream as a worker node, connecting to the Cribl Cloud leader.
* Assigns the worker node to the specified worker group.


## Outputs

* **StreamWebUrlPublic**: The URL for the Cribl Cloud Stream login page.
* **stackName**: The name of the CloudFormation stack.


## Usage

1. Fill out all required parameters, including Cribl Cloud Leader Node, Token, Instance Count, and VPC/Subnet Ids
2. Launch the CloudFormation stack with the populated parameter
3. Validate the appropriate number of nodes have joined your Cribl.Cloud environment.

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/11857645/26e6b129-8491-4260-bd5f-3f2ab879f85b/paste.txt

