#!/bin/bash

cf create-service cloudantNoSQLDB Shared myMicroservicesCloudant

cf create-service service_discovery free myServiceDiscovery

cf create-service mqlight standard mqLightService

cf create-service sqldb sqldb_free myMicroservicesSQL

cf push
