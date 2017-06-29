#!/bin/bash

echo "Creating services..."
cf create-service cloudantNoSQLDB Lite myMicroservicesCloudant
cf create-service newrelic standard NewRelic

echo "Pushing CatalogAPI Microservice..."
cf push MicroservicesCatalogAPI
echo "Pushing OrdersAPI Microservice..."
cf push MicroservicesOrdersAPI

echo "Getting OrderAPI URL "
OrderURL=$(cf routes | grep -i MicroservicesOrdersAPI | awk '{OFS="." ; print $2,$3}')
echo -e "Detected ${OrderURL}"
echo -e "Getting CatalogAPI URL "
CatalogURL=$(cf routes | grep -i MicroservicesCatalogAPI | awk '{OFS="." ; print $2,$3}')
echo -e "Detected ${CatalogURL} "
echo -e "Pushing MicroservicesUI"
cf push MicroservicesUI --no-start
echo "Setting environment variables for backend mircroservices"
cf set-env MicroservicesUI OrderURL ${OrderURL}
cf set-env MicroservicesUI CatalogURL ${CatalogURL}
echo "Starting application"
cf start MicroservicesUI
