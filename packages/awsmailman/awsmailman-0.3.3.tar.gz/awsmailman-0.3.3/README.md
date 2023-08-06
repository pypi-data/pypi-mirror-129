# AWS Mailman

A utility for updating domain registrant information in Amazon Route 53.

## Requirements

- You must have the AWS CLI Installed
- You must have AWS credentials with the appropriate permissions setup locally

## Usage

Run `awsmailman` and follow the prompts.

## Purpose

When you move, changing the addresses for the registered contacts on all of your Route53 domains is a pain. This script will update all the contacts on any Route 53 domains for you.

## Quirks

- This uses the default AWS CLI credentials on your machine
- At the moment you have to use the same name as is currently provided in your domain registration. The address may change.

## New Features

Open a PR!