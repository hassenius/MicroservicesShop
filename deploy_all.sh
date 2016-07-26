#!/bin/bash

echo "Creating services..."
cf create-service cloudantNoSQLDB Shared myMicroservicesCloudant

cf create-service service_discovery free myServiceDiscovery

echo "Pushing applications..."
cf push
