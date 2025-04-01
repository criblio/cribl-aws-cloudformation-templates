<img src="https://cribl-logo-marketplace.s3.us-east-1.amazonaws.com/Cribl-Cloud-Logo-2C-Black.png" class="logo" width="120"/>

# Cribl Cloud Trust IAM Role CloudWatch Logs

---

## Overview

This CloudFormation template creates an IAM role in your AWS account to securely integrate with Cribl Cloud. The role facilitates access to AWS resources, particularly Amazon CloudWatch Logs, and establishes a trust relationship between your AWS account and the Cribl Cloud tenant.

---

## Template Details

### **Template Metadata**
- **AWSTemplateFormatVersion**: `2010-09-09`
- **Description**: Template to create an IAM role for Cribl Cloud with permissions for AWS Built-In and CloudWatch Logs.

---

### **Parameters**
1. **CriblCloudAccountID**:
   - **Description**: The AWS Account ID of the Cribl Cloud tenant.
   - **Type**: String
   - **Default Value**: `012345678910`

---

### **Resources**
#### **IAM Role: `CriblTrustCloud`**
- **Type**: `AWS::IAM::Role`
- **Purpose**: Provides Cribl Cloud access to AWS resources via a trust relationship.
  
#### **AssumeRolePolicyDocument**
Defines the trust relationship allowing Cribl Cloud to assume this role:
- **Version**: `2012-10-17`
- **Principal**: Specifies the Cribl Cloud IAM role (`main-default`) in the account identified by `CriblCloudAccountID`.
- **Actions Allowed**:
  - `sts:AssumeRole`
  - `sts:TagSession`
  - `sts:SetSourceIdentity`
- **Condition**: Ensures secure authentication using an External ID derived from the stack ID.

#### **Policies**
A policy named `CriblCloudCWLPolicy` is attached to the role, granting permissions for:
- Creating log groups (`logs:CreateLogGroup`)
- Creating log streams (`logs:CreateLogStream`)
- Putting log events (`logs:PutLogEvents`)
  
All actions apply universally across resources (`Resource: '*'`).

---

### **Outputs**
The template provides three outputs for reference and integration:
1. **RoleName**:
   - The name of the created IAM role.
2. **RoleArn**:
   - The Amazon Resource Name (ARN) of the IAM role.
3. **ExternalId**:
   - A unique identifier used for secure authentication between AWS and Cribl Cloud.

---

## Use Case

This template is designed for scenarios where Cribl Cloud requires access to your AWS resources, particularly for processing and managing logs via CloudWatch. It ensures secure integration by leveraging IAM roles, trust policies, and external IDs.

---

## Deployment Instructions

1. Deploy the template using AWS Management Console or CLI.
2. Provide the Cribl Cloud Account ID (`CriblCloudAccountID`) as a parameter during deployment.
3. Use the outputs (`RoleName`, `RoleArn`, and `ExternalId`) for configuring Cribl Cloud integrations.

---

## Security Considerations

- The trust relationship uses an External ID to prevent unauthorized access.
- Permissions granted are limited to logging operations (`logs:*`) to minimize exposure.

---

## Notes

For further customization, you can modify the attached policy to include additional permissions or resources required by your specific use case.