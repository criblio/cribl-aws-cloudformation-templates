<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# write a readme.md markdown explanation as to what this cloudformation template does

```markdown
# Cribl Stream Free Distributed Deployment (arm64)

This CloudFormation template deploys a free, distributed instance of Cribl Stream in AWS. It provisions both a leader node and worker nodes, providing a fully functional Cribl Stream environment. This template is designed for arm64 architecture.

## Template Overview

The template automates the deployment of Cribl Stream by:

1.  Creating a Security Group for the leader node with controlled web access.
2.  Configuring Elastic Load Balancers (both external and internal) for the leader node.
3.  Setting up Target Groups for health checks and routing to the leader and worker instances.
4.  Defining EC2 Instances for the Cribl Leader.
5.  Configuring an Auto Scaling Group (ASG) to manage the worker nodes.
6.  Defining a Launch Template to configure worker nodes upon creation.
7.  Creating a Lambda function that gracefully shuts down Cribl Stream leader node when the ASG scales down.
8.  Creates secrets within the Secrets Manager for increased security

## Parameters

The template requires the following parameters:

*   **workerCount**: (Required) Enter the desired number of worker nodes.
*   **vpcId**: (Required) The ID of your existing VPC where the instances will be deployed.
*   **ImageId**: (Required) The AMI ID for the EC2 instances. This AMI should be configured for Cribl deployments.
*   **subnetIds**: (Required) Select two subnet IDs in different Availability Zones within the specified VPC.
*   **webAccessCidr**: (Required) The CIDR IP range permitted to access the Cribl Stream web console. Restricting this to a trusted IP range is highly recommended for security. The provided regular expression ensures a valid CIDR is entered.
*   **leaderInstanceType**: EC2 instance type for the Cribl Stream leader instance (defaults to `c6g.xlarge`).
*   **workerInstanceType**: EC2 instance type for the Cribl Stream worker instances (defaults to `c6g.xlarge`).
*   **AdditionalPolicies**: A comma-separated list of IAM policy ARNs to attach to the IAM role used by Logstream instances. Append to defaults, DO NOT REMOVE! These provide additional permissions to the instances.

## Resources Created

*   **ec2leaderSecurityGroup**: A security group for the leader node, allowing ingress on port 9000 (web UI) and 4200 (cluster communication) from the specified `webAccessCidr`, and unrestricted egress.
*   **LeaderLoadBalancerExternal**: An Application Load Balancer (ALB) for external access to the leader node's web UI (port 9000).  A WAF is associated to this LoadBalancer
*   **LeaderLoadBalancerInternal**: A Network Load Balancer (NLB) for internal cluster communication.
*   **LeaderCriblTargetGroup**: A Target Group for the ALB, routing traffic to the leader instance on port 9000.
*   **CriblLeaderWebListener**: A listener for the ALB, forwarding traffic on port 9000 to the `LeaderCriblTargetGroup`.
*   **WorkerCriblTargetGroup**: A Target Group for the NLB, routing traffic to the worker instances on port 4200.
*   **CriblWorkerAdminListener**: A listener for the NLB, forwarding traffic on port 4200 to the `WorkerCriblTargetGroup`.
*   **WorkerCriblTCPJSONTargetGroup**:  A Target Group for the NLB, routing traffic to the worker instances on port 10001, TCP JSON
*   **CriblWorkerTCPJSONListener**: A listener for the NLB, forwarding traffic on port 10001 to the `WorkerCriblTCPJSONTargetGroup`.
*   **WorkerCriblTCPRAWTargetGroup**: A Target Group for the NLB, routing traffic to the worker instances on port 7777, TCP RAW
*   **CriblWorkerTCPRAWListener**: A listener for the NLB, forwarding traffic on port 7777 to the `WorkerCriblTCPRAWTargetGroup`.
*   **ec2WorkersAutoScalingGroup**: An Auto Scaling Group to manage the Cribl Stream worker nodes.
*   **ec2WorkerslaunchTemplate**: A launch template defining the configuration for the worker nodes, including:
    *   Instance type.
    *   AMI ID.
    *   IAM instance profile.
    *   User data (for initial configuration).
*   **WAFWebACL**: A web access control list that is associated with the LeaderLoadBalancerExternal
*   **s3DefaultDestinationBucket**: An S3 bucket used as the default destination for Cribl Stream. Public access is blocked.
*   **LogstreamRole**: An IAM role for the worker nodes, granting necessary permissions.
*   **LogstreamInstanceProfile**: An instance profile for the worker nodes.
*   **clusterAuthToken**: A Secrets Manager Secret for storing the Cribl Stream cluster authentication token.
*   **ec2LeaderAutoScalingGroup**: An Auto Scaling Group to manage the leader node
*   **ec2LeaderAutoScalingGroupLifecycleHook**: Lifecycle hook to stop leader nodes gracefully before termination
*   **ec2leaderlaunchTemplate**: A launch template defining the configuration for the leader node
*   **leaderShutdownEventRule**: Cloudwatch event rule to trigger functionLeaderShutdown upon ec2 termination
*   **lamdbaPermissionLeaderShutdownEventRule**: Lambda permissions for LeaderShutdownEventRule
*   **functionLeaderShutdown**:  A Lambda function that gracefully shuts down Cribl Stream leader nodes

## Security Considerations

*   The `webAccessCidr` parameter is crucial for securing access to the Cribl Stream web console. It should be set to a trusted IP range.
*   The security group for the leader node allows unrestricted egress traffic. You should review and restrict this further based on your security requirements.
*   The template relies on pre-configured AMIs for both leader and worker nodes. Ensure that these AMIs are from trusted sources and are properly secured. The WAF helps secure this as well.
*   Utilizes Secrets Manager to secure the Cribl Auth Token.

## User Data

*   **Configures the instance as a leader or worker** - Based on the AMI, the correct configurations are assigned.
*   **Configures the S3 bucket** - Sets the default destination for the S3 bucket
*   **Sets the Cribl Auth Token from Secrets Manager** - Allows the CloudFormation to retrieve the secret and pass it into the instance

## Outputs

The template does not explicitly define any Outputs. However, the DNS name of the `LeaderLoadBalancerExternal` would provide the entrypoint for the Cribl Stream Web UI. This can be found in the AWS Console after the stack is deployed.

## Usage

1.  Populate the required parameters: `workerCount`, `vpcId`, `ImageId`, `subnetIds`, and `webAccessCidr`.
2.  Optionally, customize `leaderInstanceType`, `workerInstanceType`, and `AdditionalPolicies`.
3.  Launch the CloudFormation stack with the configured parameters.
4.  After deployment, retrieve the DNS name of the external load balancer from the AWS Console to access the Cribl Stream web UI.
5.  Verify that the worker nodes have joined the Cribl Stream cluster.

## Pre-requisites

*   An AWS account with sufficient permissions to create and manage the resources described above.
*   A configured VPC with at least two subnets in different Availability Zones.
*   An AMI with Cribl Stream pre-installed and configured.
*   Appropriate security policies and IAM roles to allow the CloudFormation template to create and manage resources in your AWS account.
```

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/11857645/4772d098-aed8-4bf9-8ece-128341be62f6/free_arm64_template.yaml

