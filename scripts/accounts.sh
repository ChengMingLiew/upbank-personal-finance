#!/bin/bash

source ../.env

curl https://api.up.com.au/api/v1/accounts -H "Authorization: Bearer $UP_API_TOKEN"