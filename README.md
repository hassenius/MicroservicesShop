# Microservices Shop

Based on the [Bluemix Microservices Sample Application](https://developer.ibm.com/bluemix/2015/03/16/sample-application-using-microservices-bluemix/)


Enchanced by the use of [Bluemix Service Discovery](https://console.ng.bluemix.net/docs/services/ServiceDiscovery/index.html) to tie the miocroservice components together

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/hassenius/MicroservicesShopPipelineTest&branch=PipelineTest)

## How to deploy the sample application
1. $ git clone https://github.com/hassenius/MicroservicesShop.git
1. $ cd MicroservicesShop
1. $ cf login
1. $ ./deploy_all.sh

This will create the necessary services and push the Bluemix runtimes necessary to run the application. After you have run this you can find the URL for the MicroservicesUI application by typing
$ cf apps
Connect to this URL in your webbrowser to verify that the application works and can get products from the MicroservicesCatalogAPI service.

## How to instrument the application with New Relic
The NewRelic branch is pre-instrumented with New Relic, so once you change to the NewRelic branch and insert the New Relic license key your application will start sending data to newrelic.com

1. Change to the NewRelic branch

        $ git checkout NewRelic
        
2. use your favourite editor to update new-relic.yaml with your New Relic license key
3. Push the new code to Bluemix
        
        $ cf push

## How to introduce some errors into the code to verify monitoring
After you have updated new-relic.yaml with your license key, you can change to the VerrifyMonitoring branch, which introduces some errors into the Microservices_CatalogAPI code.

1. Change to the VerifyMonitoring branch

        $ git checkout VerifyMonitoring

2. Push the new code for the MicroservicesCatalogAPI microservice

        cf push MicroservicesCatalogAPI


You now have some additional API calls you can use in the MicroservicesCatalogAPI which will generate various errors that you can see in Monitoring and Logging tools

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
        
        This will set off a memory leak within the application, which will over time be visible as increased memory usage.
