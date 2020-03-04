### Fuzzing API secrets
Here's a script to fuzz for API secrets.

You may want to use this to check hardening of your API implementation. All it takes, is an API endpoint.

#### Instructions

To run this script, execute in the root directory of this repository

    python main.py --url YOUR_TARGET_URL

YOUR_TARGET_URL is expected to be an API enpoint which accepts API secrets via URL parameter.

The URL parameter waiting for the secret should be at the end of variable YOUR_TARGET_URL.

A valid format for variable YOUR_TARGET_URL typically looks like this: *https://your-api-subdomain.com?variable=A&secret=*

Public endpoints of this type may be vulnerable to brute-force attacks.

This tool helps to identify possible vulnerabilities of your API endpoints.

#### Additional Parameters

Type

    python main.py -h

to find out about optional parameters.

Note that you may want to specify a known secret via parameter *--secret*. The value of this parameter will then be used to start fuzzing from.

Use *--debugging* to get extended output including error logs.
