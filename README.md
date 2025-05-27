## Task: Understanding apache iceberg and taking care about one part of it differently. 
This should serve as an example how to connect docker-compose with minikube pods.
Most of the functions are just for demonstration purposes so they are very light...
## Tech stack
- MinIO for S3-compatible object storage  
- Trino as the SQL engine  
- Iceberg REST catalog served via Kubernetes (Minikube)


## Requirements
- Docker + Docker Compose
- Minikube with `kubectl` configured
- Python 3.11+ (for optional Python client)

## Overview
- MinIO: object storage accessible at http://localhost:9001 (UI)
- Trino: SQL engine Cluster Overview  at http://localhost:8080
- Iceberg REST catalog: deployed on Kubernetes via `k8s/iceberg-rest.yaml`

## Intro aka. how to control available parts of the system

Start Docker containers...

```bash
minikube start
```
```
docker-compose build --no-cache
```

From prj root
```
docker-compose down
docker-compose up -d

kubectl delete deployment iceberg-rest --ignore-not-found
kubectl delete service iceberg-rest --ignore-not-found
kubectl apply -f k8s/iceberg-rest.yaml
```
From new cmd...
Keep tunnel alive so minikube is exposed to host and to docker containers 
```
minikube tunnel
```


Interacting with Trino adjust for your prj name if needed :) ... docker exec -it <your-project-name>_trino-1 /bin/sh
```
docker exec -it icebergdemo-trino-1 /bin/sh
```
```
trino --catalog iceberg
```
```
CREATE SCHEMA iceberg.test_db;
```
```
CREATE TABLE iceberg.test_db.users (
  id INT,
  name VARCHAR,
  created_at TIMESTAMP
);
```
```
INSERT INTO iceberg.test_db.users VALUES (1, 'Adlo', current_timestamp);
```
```
SELECT * FROM iceberg.test_db.users;
```

Python Client Demo

A separate Python non-worker/cli_client container runs example.py to perform Trino operations.
See the python-client/ folder for a basic example using the trino Python package.

## CLI Interface (no web API)
Use the CLI container to interact with Iceberg tables:
```
docker-compose run --rm trino-cli create_table
```
```
docker-compose run --rm trino-cli insert 99 "Adlo"
```
```
docker-compose run --rm trino-cli select
```
```
docker-compose run --rm trino-cli update 99 "Adlo103"
```
```
docker-compose run --rm trino-cli delete 99
```

MinIO Console
Psst...
Login: admin / password

## Tips:
If you want to go Minikube + Docker Desktop way, you may need to adjust the hostAliases IP in iceberg-rest.yaml.
Copy the resolved IP into hostAliases
Use the following to determine the correct host IP based on minikube perspective:
```
minikube ssh
```
```
ping host.docker.internal
```
rest should be clear from k8s/iceberg-rest.yaml from comments
