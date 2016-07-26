#!/bin/bash

cf create-service cloudantNoSQLDB Shared myMicroservicesCloudant

cf create-service service_discovery free myServiceDiscovery

cf push
