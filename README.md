# README

## Overview

This repo manages a simple python-based SES-client script. 

The script is configured to consume data from a JSON file, populate an HTML template, and then email the message to a list of clients.

## Setup

Setup is easy, as long you have an AWS account with SES permissions. The script is configured to use your default profile. Simply fill in the JSON data and construct your HTML template to the desired message, then you're ready to fire away! 

### AWS SES Sandbox

By default, AWS has SES in "Sandbox" mode. This means you can only send messages to emails that are registered in the "Identity Management" section. To gain ability to send to any address, you have to file a support ticket. Follow the steps in this AWS Docs link:
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/manage-sending-quotas-request-increase-procedure.html

#### Note

There are certain sending guidelines you must follow in order to retain higher permissions. You'll receive and email documenting the guidelines in detail.

## TODO

Build this out to be a command line type tool.
