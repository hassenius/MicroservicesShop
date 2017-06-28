#!/bin/bash

echo "Creating services..."
cf create-service cloudantNoSQLDB Lite myMicroservicesCloudant
cf create-service newrelic standard NewRelic

echo "Pushing applications..."
cf push
