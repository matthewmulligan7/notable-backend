========
# restapi_
========

Description: api

### GITHUB ACTIONS 
Github actions is already stubbed in for this api, a dependency exists for github SECRETS for the folllowing:
```
DOCKER_USERNAME && DOCKER_PASSWORD
```
On proper configuration of the github actions workflow this api will auto build & push on release & develop branches

### Using the stubbed database
The database can be used either with a CLI flag for DEV=True (this reads db/db_config.ini develop section)
```
export DEV=True
```

### Migration of Schemas
The template can upgrade/alter schemas in a simple method, populated schema json files need to be place in db/schemas (a template is there) to disable/stop migration:
```
export MIGRATE_TABLES="FALSE"
```

### Using Visual Studio Rest Client
Install the vscode extension for rest-clients and use the file://./rest_client_tests.http file directly
```
open vscode:extension/humao.rest-client
```

### Helm deployments
This API can be deployed to Kubernetes using the Helm chart at https://github.com/5thColumn/k8s-restapi-deployment

An example configuration file for this API is located in helm/dev/values.yaml and can be deployed with the following example command:
(Note: this requires the docker image to be built and tagged on your local system prior to deployment)
```
cd ..
git clone git@github.com:5thColumn/k8s-restapi-deployment.git
helm install -f restapi_/helm/dev/values.yaml restapi- k8s-restapi-deployment/charts/restapi
```




