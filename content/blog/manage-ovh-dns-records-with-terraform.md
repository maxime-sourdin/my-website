Title: Managing OVH DNS records with Terraform (with state storage on an S3 bucket)
original_url: managing-dns-records-at-ovh-with-terraform-with-state-storage-on-an-s3-bucket
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

1- Download OpenStack RC file from  Horizon GUI.

2- Source it: source openstack-rc.sh

3- Create new credentials

    openstack ec2 credentials create

4- Keep these credentials on Vault

# Setting up Github repo

## Create new repo on Github

## Create new secrets for Actions, like this:

    APPLICATION_KEY
    APPLICATION_SECRET
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    CONSUMER_KEY

## Adding essentials files

### versions.tf
    terraform {
    required_version = "~> 1.0"

    required_providers {
        ovh = {
        source  = "ovh/ovh"
        version = "~> 0.19"
        }
    }
    }

### variables.tf

    variable "APPLICATION_KEY" {
    description = "application key"
    type        = string
    }

    variable "APPLICATION_SECRET" {
    description = "application secret"
    type        = string
    }

    variable "CONSUMER_KEY" {
    description = "consumer key"
    type        = string
    }


    variable "records" {
    description = "records to be created"
    type        = map(any)
    default     = { 
        record1 = {
        zone      = "sourdin.ovh"
        subdomain = "maxime"
        fieldtype = "A"
        ttl       = "0"
        target    = "192.168.1.1"
        }
    }
    }

### provider.tf

    provider "ovh" {
    endpoint           = "ovh-eu"
    application_key    = var.APPLICATION_KEY
    application_secret = var.APPLICATION_SECRET
    consumer_key       = var.CONSUMER_KEY
    }

Here, we configure the OVH DNS provider, it will look for its secrets in variables (that's why 'TF_VAR_' preced the variable name)

### main.tf

    resource "ovh_domain_zone_record" "dns_record_terajob" {
    for_each  = var.records
    zone      = each.value.zone
    subdomain = each.value.subdomain
    fieldtype = each.value.fieldtype
    ttl       = each.value.ttl
    target    = each.value.target
    }

### backend.tf

    terraform {
    backend "s3" {
        bucket         = "terraform-state"
        region         = "us-east-1"
        key            = "dns/sourdin.tfstate"
        encrypt        = false
        endpoint =  "s3.pub1.infomaniak.cloud"  
        force_path_style = true
        skip_credentials_validation = true
        skip_region_validation = true    
    }
    }

Here, you can configure on which bucket the states will be saved, the provider's endpoint and region.

## Configure Github actions

### .github/workflows/main.yml

    name: ovh_dns_management
    on: [push, pull_request]
    jobs:
        build:
            name: OVH DNS
            runs-on: ubuntu-20.04
            env:
                CONSUMER_KEY: "${{ secrets.CONSUMER_KEY }}"
                APPLICATION_KEY: "${{ secrets.APPLICATION_KEY }}"
                APPLICATION_SECRET: "${{ secrets.APPLICATION_SECRET }}"    
                TF_VAR_CONSUMER_KEY: "${{ secrets.CONSUMER_KEY }}"
                TF_VAR_APPLICATION_KEY: "${{ secrets.APPLICATION_KEY }}"
                TF_VAR_APPLICATION_SECRET: "${{ secrets.APPLICATION_SECRET }}"
                AWS_ACCESS_KEY_ID: "${{ secrets.AWS_ACCESS_KEY_ID }}"
                AWS_SECRET_ACCESS_KEY: "${{ secrets.AWS_SECRET_ACCESS_KEY }}"
                TF_VAR_AWS_ACCESS_KEY_ID: "${{ secrets.AWS_ACCESS_KEY_ID }}"
                TF_VAR_AWS_SECRET_ACCESS_KEY: "${{ secrets.AWS_SECRET_ACCESS_KEY }}"
            steps:
            - name: Checkout code
                uses: actions/checkout@v3
            - name: Setup Terraform 
                uses: hashicorp/setup-terraform@v2
            - name: Terraform fmt
                id: fmt
                run: terraform fmt -check
                continue-on-error: true
            - name: Terraform Init
                id: init
                run: terraform init
                continue-on-error: false
            - name: Terraform Validate
                id: validate
                run: terraform validate -no-color
                continue-on-error: false
            - name: Terraform Plan
                id: plan
                run: terraform plan -no-color -input=false
                continue-on-error: false
            - name: Terraform Apply
                id: apply
                run: terraform apply -no-color -auto-approve
                continue-on-error: false

Several steps here:

- We define the name of the action, and when it's triggered (push, pull request).

- Then we prepare the environment, which runs on Ubuntu 20.04. We also define the environment variables necessary for Terraform

- Then we define each action:

    - We check the code, we install Terraform
    - Formatting and cleaning the Terraform files
    - Prepare the runtime environment, by retrieving the dependencies (providers)
    - Revalidate the syntax and the actions
    - We prepare the Terraform action plan (everything it will do in relation to the existant objects).
    - We apply if everything is OK.

## Enjoy !

Each time you re-add a new DNS entry in variables.tf, the CI/CD chain will restart, and add the sub-domain, with the added bonus of storing the current state of the DNS records on an S3 bucket
