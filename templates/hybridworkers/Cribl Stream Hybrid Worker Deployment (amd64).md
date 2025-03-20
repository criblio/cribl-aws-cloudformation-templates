<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# 

---

# Cribl Stream Hybrid Worker Deployment (amd64)

This CloudFormation template deploys a Cribl Stream Hybrid Worker setup on AWS using AMD64 architecture. It sets up a Network Load Balancer, EC2 instances for workers, and necessary security groups and IAM roles.

## Parameters

- `criblCloudLeader`: Hostname of the Cribl.Cloud or self-hosted Leader node (required)
- `criblclusterAuthToken`: Authentication token for the Cribl.Cloud or self-hosted Leader node (required)
- `workerGroup`: Cribl Stream Hybrid Worker Group name (default: defaultHybrid)
- `workerCount`: Number of worker nodes to deploy (required)
- `vpcId`: ID of the existing VPC (required)
- `subnetIds`: List of 2 subnet IDs in different AZs within the specified VPC (required)
- `ImageId`: AMI ID for the EC2 instances (required)
- `workerInstanceType`: EC2 instance type for worker nodes (default: c5a.xlarge)
- `AdditionalPolicies`: Comma-separated list of additional IAM policy ARNs


## Resources

The template creates the following main resources:

1. Network Load Balancer
2. Target Group for the Load Balancer
3. Listeners for ports 4200, 9514, 8088, and 10300
4. Security Group for worker instances
5. S3 Bucket for default destination
6. IAM Role and Instance Profile for EC2 instances
7. Secrets Manager Secret for cluster authentication token
8. Auto Scaling Group for worker instances
9. Launch Template for worker instances
10. Lambda function for worker shutdown handling

## Outputs

- `StreamWebUrlPublic`: URL for Cribl Cloud Stream Login
- `stackName`: Name of the CloudFormation stack
- `NetworkLoadBalancerDNS`: DNS name of the Network Load Balancer


## Usage

1. Prepare the required parameters, including VPC, subnet IDs, and Cribl.Cloud information.
2. Launch the CloudFormation stack using this template.
3. Once the stack is created, use the outputs to access your Cribl Stream deployment.

## Security Considerations

- The template uses Secrets Manager to store the cluster authentication token securely.
- EC2 instances are launched with a security group that restricts inbound traffic to necessary ports.
- IAM roles are created with least privilege access to required AWS services.


## Customization

You can customize the deployment by modifying the following:

- Instance types allowed for workers
- Additional IAM policies for worker instances
- Number of worker nodes
- Network configuration (VPC and subnets)

Ensure to review and adjust the template according to your specific requirements and security policies before deployment.

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/11857645/6d860f64-f518-4d4c-b086-6acb1f0e60c7/paste.txt

