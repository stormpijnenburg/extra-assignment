#!/bin/bash

# Define variables
DOCKER_IMAGE="stormpijnenburg/docker-extra"
DEPLOYMENT_NAME="my-application"
NAMESPACE="default"

while true; do
    # Get the latest commit SHA from GitHub
    latest_sha=$(git ls-remote https://github.com/stormpijnenburg/extra-assignment.git HEAD | cut -f 1)

    # Get the current image tag used by the deployment
    current_sha=$(kubectl get deployment $DEPLOYMENT_NAME -n $NAMESPACE -o=jsonpath='{.spec.template.spec.containers[0].image}' | cut -d ":" -f 2) #cut -d ':' -f 3)

    # Check if a new version is available
    if [ "$latest_sha" != "$current_sha" ]; then
        echo "New version available: $latest_sha"

        # Update the deployment with the new image
        kubectl set image deployment/$DEPLOYMENT_NAME -n $NAMESPACE app=$DOCKER_IMAGE:$latest_sha
        echo "Deployment updated to use version: $latest_sha"
    else
        echo "No new version available"
    fi

    # Sleep for 30 seconds before checking again
    sleep 30
done

