<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# 

---

# write a readme.md markdown explanation as to what this cloudformation template does

```markdown
# Cribl Stream Single Instance Deployment (arm64)

This CloudFormation template deploys a single instance of Cribl Stream in AWS. It provides a simplified setup for proof-of-concept deployments, testing, or small-scale data processing. This template is designed for arm64 architecture.

## Template Overview

The template automates the deployment of Cribl Stream by:

1.  Creating a Security Group for controlled web access.
2.  Configuring an Elastic Load Balancer to provide access to the Cribl Stream web UI.
3.  Defining an EC2 Instance to run Cribl Stream.
4.  Creating an S3 bucket used as the default destination.
5.  Configuring an IAM Role with the necessary permissions for Cribl Stream.
6.  Setting up Lambda function to gracefully shutdown Cribl Stream instances

## Parameters

The template requires the following parameters:

*   **vpcId**: (Required) The ID of your existing VPC where the instance will be deployed.
*   **subnetIds**: (Required) Select two subnet IDs in different Availability Zones within the specified VPC.  These subnets must be in the same VPC as the VPC ID above.
*   **webAccessCidr**: (Required) The CIDR IP range permitted to access the Cribl Stream web console. Restricting this to a trusted IP range is highly recommended for security. The provided regular expression ensures a valid CIDR is entered.
*   **ImageId**: (Required) The AMI ID for the EC2 instance. This AMI should be configured for Cribl deployments.
*   **workerRootVolumeSize**:  (Optional) Root volume size on Cribl workers (default: 20 GB).
*   **LoadBalancerScheme**: (Optional) Type of load balancer (default: internet-facing). Allowed values: `internal`, `internet-facing`.
*   **instanceType**: (Optional) EC2 instance type for the Cribl Stream instance (default: `c5.xlarge`). A list of allowed instance types is provided in the template.
*   **AdditionalPolicies**: (Optional) A comma-separated list of IAM policy ARNs to attach to the IAM role used by Logstream instances. Append to defaults, DO NOT REMOVE! These provide additional permissions to the instances. Defaults to `"arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore,arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"`. These policies are required to allow the SSM agent and Cloudwatch agent to run. Ensure that the provided policies are comma-separated.

## Resources Created

*   **ec2SingleSecurityGroup**: A security group for the EC2 instance, allowing ingress on port 9000 (web UI) from the specified `webAccessCidr`, and unrestricted egress.
*   **LoadBalancer**: An Application Load Balancer (ALB) to provide access to the Cribl Stream web UI (port 9000).
*   **CriblTargetGroup**: A Target Group for the ALB, routing traffic to the EC2 instance on port 9000.
*   **CriblWebListener**: A listener for the ALB, forwarding traffic on port 9000 to the `CriblTargetGroup`.
*   **CriblWebListenerRule1**: A listener rule for the ALB, defining forwarding conditions.
*   **s3DefaultDestinationBucket**: An S3 bucket used as the default destination for Cribl Stream. Public access is blocked.
*   **LogstreamRole**: An IAM role for the EC2 instance, granting necessary permissions.
*   **iamDefaultInstanceProfile**: An instance profile for the EC2 instance, associating the `LogstreamRole` with the instance.
*   **ec2WorkersAutoScalingGroup**: An Auto Scaling Group to manage the Cribl Stream instances.
*   **ec2WorkersAutoScalingGroupLifecycleHook**: Lifecycle hook to stop worker nodes gracefully before termination
*   **ec2WorkerslaunchTemplate**: A launch template defining the configuration for the EC2 instance, including the AMI ID, instance type, and user data.
*   **workerShutdownEventRule**: Cloudwatch event rule to trigger functionWorkerShutdown upon ec2 termination
*   **lamdbaPermissionWorkerShutdownEventRule**: Lambda permissions for WorkerShutdownEventRule
*   **functionWorkerShutdown**: A Lambda function that gracefully shuts down Cribl Stream worker nodes

## Security Considerations

*   The `webAccessCidr` parameter is crucial for securing access to the Cribl Stream web console. It should be set to a trusted IP range.  The template enforces a valid CIDR format for this parameter.
*   The security group for the EC2 instance allows unrestricted egress traffic. You should review and restrict this further based on your security requirements.
*   The template relies on a pre-configured AMI. Ensure that the AMI is from a trusted source and is properly secured.

## User Data

The launch template includes a user data script that configures the Cribl Stream instance on startup. This script:

*   Configures Cribl Stream in single-instance mode.
*   Sets the default S3 destination bucket.
*   Applies basic configurations.

## Lambda Function for Graceful Shutdown

The `functionWorkerShutdown` Lambda function is triggered when the EC2 instance is terminating. It gracefully stops the Cribl Stream service to prevent data loss and ensures a clean shutdown.

## Outputs

*   **logstreamWebUrlPublic**: The URL for the Cribl Stream web UI.
*   **logstreamWebAccessCreds**: Default Web Access Credentials `admin / EC2 Instance ID`.

## Usage

1.  Populate the required parameters: `vpcId`, `subnetIds`, `webAccessCidr`, and `ImageId`.
2.  Optionally, customize `workerRootVolumeSize`, `LoadBalancerScheme`, `instanceType`, and `AdditionalPolicies`.
3.  Launch the CloudFormation stack with the configured parameters.
4.  After deployment, access the Cribl Stream web UI using the URL provided in the Outputs.

## Pre-requisites

*   An AWS account with sufficient permissions to create and manage the resources described above.
*   A configured VPC with at least two subnets in different Availability Zones.  The subnets must have internet access.
*   An AMI with Cribl Stream pre-installed and configured.
*   Appropriate security policies and IAM roles to allow the CloudFormation template to create and manage resources in your AWS account.

This template provides a streamlined approach to deploying a single instance of Cribl Stream in AWS, making it ideal for quick evaluations and smaller deployments.
```

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/11857645/0c67cb5d-fc85-46e7-bf99-0095e50a4c86/free_arm64_template.yaml

