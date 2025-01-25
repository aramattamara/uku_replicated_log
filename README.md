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
curl -X POST 127.0.0.1:3000/message?concern=1
```
<img width="695" alt="Screenshot 2024-11-15 at 8 14 39 PM" src="https://github.com/user-attachments/assets/56bc87d1-a493-410c-852d-ae4eb912c96f">


