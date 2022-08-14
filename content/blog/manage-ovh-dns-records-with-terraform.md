Title: Manage OVH DNS records with Terraform
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Automation
Tags: Terraform
Summary: Save some time without using IHM

# Prerequisites

- Terraform is installed on your machine
- You have an OVH account
- You have a bucket on Infomaniak/OVH

# Generate tokens

## OVH

[You can follow this tutorial, clear enough](https://yunohost.org/en/providers/registrar/ovh/autodns) to create the required tokens on OVH.

Do not hesitate to store these tokens on a [Vault](https://learn.hashicorp.com/tutorials/vault/getting-started-install?in=vault/getting-started), storing them in the clear is literally forbidden, at the risk of having bad surprises with your DNS zone.

## S3 Provider

1 - Download OpenStack RC file from  Horizon GUI.

2- Source it: source openstack-rc.sh

3- Create new credentials

    openstack ec2 credentials create

4- Keep these credentials on Vault