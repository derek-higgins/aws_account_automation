# AWS account automations
step function triggered on successful account creation, to implement defaults that cannot be controlled through stacksets

![Architecture](/docs/stepfunctions_graph.png)

## Controls and defaults set for new accounts
- remove default VPC
- enable S3 public access block for the account
- enable ebs encryption by default
- block AMI sharing
- block ebs snapshot sharing

## deployment
- deploy stackset.yml as a stackset to create the role needed to implement the contorols to all accounts in the organization

- deploy the template.yml to a account where all organization events are forwarded to
