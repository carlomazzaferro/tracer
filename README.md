### Spec

Please refer to
the [Worktest Solution Proposal](https://elegant-journey-920.notion.site/Worktest-8e012b89dea641eeb713345d55bd8d2b)

### Locally running the services

Fill in the `.secrets.env` with your RPC URL, and then:

```shell
>>> ENV=local make up
```

Head to http://localhost:8080/docs to check out the live Swagger docs

### Logs from services

```shell
# Celery
>>> docker logs -f $(docker ps -qf "name=tracer_celeryworker" ) | tee >(grep -v "^{") | grep "^{" | jq .
# Service
>>> docker logs -f $(docker ps -qf "name=tracer_tracer" ) | tee >(grep -v "^{") | grep "^{" | jq .
```