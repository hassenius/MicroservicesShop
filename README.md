# Microservices Shop

## How to deploy the sample application

Please note that this demonstration uses the New Relic Service instance available through Bluemix. 
Only one New Relic Service instance is permitted per organisation in Bluemix. 
If you already have a New Relic service instance it is necessary to either delete this service instance, 
or make sure it is named NewRelic and exist in the same space as you deploy this application.

### Deploy with DevOps Pipelines
Click the button below to automatically deploy the Services and Applications using Bluemix DevOps Pipelines

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/hassenius/MicroservicesShop)

### Deploy using script
1. $ git clone https://github.com/hassenius/MicroservicesShop.git
1. $ cd MicroservicesShop
1. $ cf login
1. $ ./deploy_all.sh

This will create the necessary services and push the Bluemix runtimes necessary to run the application. 
After you have run this you can find the URL for the MicroservicesUI application by typing

```$ cf apps```

Connect to this URL in your webbrowser to verify that the application works and can get products from the MicroservicesCatalogAPI service.

### Deploy manually
1. $ git clone https://github.com/hassenius/MicroservicesShop.git
1. $ cd MicroservicesShop
1. $ cf login
1. $ cf create-service cloudantNoSQLDB Lite myMicroservicesCloudant
1. $ cf create-service newrelic standard NewRelic
1. $ cf push MicroservicesCatalogAPI # Take note of route/url of the service
1. $ cf push MicroservicesOrdersAPI # Take note of the route/url of the service
1. $ cf push MicroservicesUI --no-start
1. $ cf set-env MicroservicesUI OrderURL ```<insert orderservice_url from previous step>```
1. $ cf set-env MicroservicesUI CatalogURL ```<insert catalogservice_url from previous step>```
1. $ cf start MicroservicesUI


## How to introduce some errors into the code to verify monitoring
The MicroservicesCatalogAPI application includes some additional code in that triggers different errors that can be analysed using monitoring and logging tools. 
Using your browser or curl you can make calls to a number of URLs to trigger specific errors.
* https://MicroservicesCatalogAPI-URL/breakstuff/findUser/insert_anything_here

        This command will generate a application generated error in the error console. 
        For example 
        ERR Error: Could not find user Mary
        together with a stack trace
        This error will be visible in logging tools, such as splunk or when you type "cf logs MicroservicesCatalogAPI", but will not be visible as a coding error in New Relic


* https://MicroservicesCatalogAPI-URL/breakstuff/findNemo
        
        This will generate a Node.js ReferenceError and stacktrace, which will be visible in New Relic, as well as in application logs

* https://MicroservicesCatalogAPI-URL>/breakstuff/badMethod
        
        This will generate a Node.js ReferenceError and stacktrace, which will be visible New Relic, as well as in application logs

* https://MicroservicesCatalogAPI-URL>/breakstuff/leakMemory
        
        This will set off a memory leak within the application, which will over time be visible as increased memory usage, evenutally crashing the application triggering a Cloud Foundry container restart.
