# Github Action

[GitHub Actions](https://docs.github.com/en/actions) stands as an automation and continuous integration/continuous deployment (CI/CD) solution offered by GitHub. Within Surge, we've harnessed its capabilities to automate specific tasks and workflows, including the creation of releases and the building and pushing of Docker images to [Docker Hub](https://hub.docker.com/r/nfdi4chem/cloud-surge). The YAML files detailing these processes are outlined below and can also be located in the repository's 'workflows' directory.

- Creating auto releases using [release-please](https://github.com/google-github-actions/release-please-action) with [Conventional Commit Messages](https://www.conventionalcommits.org/en/v1.0.0/).

```bash
name: release-please-action

on:
  push:
    branches:
      - main

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: google-github-actions/release-please-action@v3
        with:
          release-type: python
          package-name: release-please-action
          token: ${{ secrets.GITHUB_TOKEN }}
          prerelease: true

```

- Build and Push Docker Images to [Docker Hub](https://hub.docker.com/r/nfdi4chem/cloud-surge).

```bash
name : Dev Build and Publish

on:
  release:
    types: [published]

env:
  DOCKER_HUB_USERNAME : ${{ secrets.DOCKER_HUB_USERNAME  }}
  DOCKER_HUB_PASSWORD : ${{ secrets.DOCKER_HUB_PASSWORD  }}
  REPOSITORY_NAME: cloud-surge
  REPOSITORY_NAMESPACE: nfdi4chem

jobs:
  push_to_registry:
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repo
        uses: actions/checkout@v3
      
      - name: Log in to Docker Hub
        uses: docker/login-action@f4ef78c080cd8ba55a85445d5b36e214a81df20a
        with:
          username: ${{ env.DOCKER_HUB_USERNAME  }}
          password: ${{ env.DOCKER_HUB_PASSWORD  }}

      #Fetch Latest release
      - name: Fetch latest release
        id: fetch-latest-release
        uses: InsonusK/get-latest-release@v1.0.1
        with:
          myToken: ${{ github.token }}
          exclude_types: "draft"
          view_top: 10
      - name: "Print release name"
        run: |
          echo "tag_name: ${{ steps.fetch-latest-release.outputs.tag_name }}"
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: ./ops
          file: ./ops/Dockerfile  
          push: true
          tags: ${{ env.REPOSITORY_NAMESPACE }}/${{ env.REPOSITORY_NAME }}:${{ steps.fetch-latest-release.outputs.tag_name }}
          username: ${{ env.DOCKER_HUB_USERNAME  }}
          password: ${{ env.DOCKER_HUB_PASSWORD  }}
```

All the sensitiove informations such as Docker Hub username and password are stored as Secrets in the repository's settings which can be used securely in the workflows.

- Build and Deploy [Surge docs](https://steinbeck-lab.github.io/cloud-surge/actions.html) to GitHub Pages.

```bash
# Sample workflow for building and deploying a VitePress site to GitHub Pages
#
name: Deploy VitePress site to Pages

on:
  # Runs on pushes targeting the `main` branch. Change this to `master` if you're
  # using the `master` branch as the default branch.
  push:
    branches: [main]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest queued.
# However, do NOT cancel in-progress runs as we want to allow these production deployments to complete.
concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  # Build job
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0 # Not needed if lastUpdated is not enabled
      # - uses: pnpm/action-setup@v2 # Uncomment this if you're using pnpm
      # - uses: oven-sh/setup-bun@v1 # Uncomment this if you're using Bun
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: npm # or pnpm / yarn
      - name: Setup Pages
        uses: actions/configure-pages@v3
      - name: Install dependencies
        run: npm ci # or pnpm install / yarn install / bun install
      - name: Build with VitePress
        run: |
          npm run docs:build # or pnpm docs:build / yarn docs:build / bun run docs:build
          touch docs/.vitepress/dist/.nojekyll
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: docs/.vitepress/dist

  # Deployment job
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    needs: build
    runs-on: ubuntu-latest
    name: Deploy
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```
