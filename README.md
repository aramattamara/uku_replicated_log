## Instructions
### Requirements:
* `docker` and `docker compose` to run the cluster
* Make sure ports `3000-3002` are available

### Start:
```bash
# Run pre-build cluster 
docker compose build && docker compose up
```
`docker-compose.yml` by default is configured to run single instance of `master` at `3000` port node and 2 instances of `secondary` nodes at ports `3001` and `3002`.

### Usage:
```bash
curl -X POST 127.0.0.1:3000/message
```
