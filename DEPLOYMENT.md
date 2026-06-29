# Project TRIAD Deployment

## Production server

Domain:

```text
https://triad.bitflow92.co.za

## VPS path
/home/cdr2bok297/project-triad

## Deployment flow
#
# 1. Develop locally on the develop branch.
# 2. Commit and push changes to GitHub.
# 3. Pull changes on the VPS.
# 4. Restart the Docker container.

cd ~/project-triad
git pull
docker compose down
docker compose up -d

## Caddy reverse proxy:
triad.bitflow92.co.za {
    reverse_proxy 127.0.0.1:5090
}

## Docker port mapping
ports:
  - "127.0.0.1:5090:8000"

Gunicorn listens on port 8000 inside the container.

The VPS exposes it locally on 127.0.0.1:5090.

Caddy proxies to 127.0.0.1:5090.


## Git commands to use on VPS

# Clone your GitHub repo to the VPS

cd ~
git clone https://github.com/bitflow92/Project-TRIAD.git project-triad
cd project-triad
git checkout develop

# Checkout and pull updates from repo develop

cd ~/project-triad
git checkout develop
git pull origin develop

# Check GitHub repo status, check branch status and check origin of repor fetched and pulled

cd ~/project-triad

git status

git branch

git remote -v