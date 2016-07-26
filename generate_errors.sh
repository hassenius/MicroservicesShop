#!/bin/bash

show_usage() {
cat <<EOF
Usage: ${0##*/} [-m] [-c COUNT] [-h]
Call the MicroservicesCatalogAPI methods to generate internal server errors that will show 
up in logs and monitoring tools or other error analytics.

    -m      Include memory leak function. This will eventually crash the Catalog Microservice. Disabled by default
    -c      Number of loops to perform. Defaults to 100
    -h      Print this help screen.
EOF
}

# Initialize our own variables
iterations=100
leakMemory=false

# Get options
while getopts "mhc:" opt; do
    case "$opt" in
        h)
            show_usage
            exit 0
            ;;
        m)
            leakMemory=true
            ;;
        c)
            iterations=$OPTARG
            ;;
        '?')
            show_usage
            exit 1
            ;;
    esac
done

echo
show_usage
echo
echo "Starting script..."
echo
echo "Doing ${iterations} loops of bad things (generating internal server errors)"
echo "Memory leak is set to ${leakMemory}"
echo
echo "Getting MicroservicesCatalogAPI url..."

url=$(cf routes | grep -m1 MicroservicesCatalogAPI | awk '{print $2"."$3}')
echo
echo "url set to ${url}"
echo
for (( i=1; i<=$iterations; i++ ))
do
    echo -e "\nIteration $i"
    curl https://${url}/breakstuff/badMethod
    curl https://${url}/breakstuff/findNemo
    if $leakMemory ; then
        echo "Starting leaky thread"
        curl https://${url}/breakstuff/leakMemory &
    fi
done
