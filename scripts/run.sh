#!/bin/bash -e

cd `dirname $0` && cd ..
source resources/secrets/.env
PYTHONPATH=$(pwd) \
 IS_LOCAL=true \
 DRIVE_SS_ID=$DRIVE_SS_ID \
 GOOGLE_CSE_ID=$GOOGLE_CSE_ID \
 GOOGLE_API_KEY=$GOOGLE_API_KEY \
 poetry run python b_moz/main.py

