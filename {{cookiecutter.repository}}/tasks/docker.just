# Define docker tasks workflow to run when running 'just docker'
[group('docker')]
docker: docker-build docker-run

# Build docker image based on latest tag (see commit for bumping of tag)
[group('docker')]
docker-build tag="latest": package-build
    {% raw %}docker build --tag={{REPOSITORY}}:{{tag}} .{% endraw %}

# Run docker compose if using multiple related containers as a single application
[group('docker')]
docker-compose:
    docker compose up

# Run latest docker image
[group('docker')]
docker-run tag="latest":
    {% raw %}docker run --rm {{REPOSITORY}}:{{tag}}{% endraw %}