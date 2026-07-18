#!/bin/bash
# Deployment script for AI Market Trend Analyzer
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-development}
APP_NAME="ai-market-analyzer"
DOCKER_REGISTRY=${DOCKER_REGISTRY:-docker.io}
DOCKER_USERNAME=${DOCKER_USERNAME:-chellamani777}
IMAGE_NAME="$DOCKER_REGISTRY/$DOCKER_USERNAME/$APP_NAME"
IMAGE_TAG=$(git rev-parse --short HEAD)
FULL_IMAGE="$IMAGE_NAME:$IMAGE_TAG"
LATEST_IMAGE="$IMAGE_NAME:latest"

echo "🚀 Deploying AI Market Trend Analyzer"
echo "Environment: $ENVIRONMENT"
echo "Image: $FULL_IMAGE"

# Build Docker image
echo "📦 Building Docker image..."
docker build -t $FULL_IMAGE -t $LATEST_IMAGE .

# Login to Docker registry (if credentials provided)
if [ -n "$DOCKER_PASSWORD" ]; then
    echo "🔐 Logging in to Docker registry..."
    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin $DOCKER_REGISTRY
fi

# Push image to registry
echo "📤 Pushing image to registry..."
docker push $FULL_IMAGE
docker push $LATEST_IMAGE

echo "✅ Docker image built and pushed successfully!"
echo "Image tag: $IMAGE_TAG"
echo "Full image: $FULL_IMAGE"

# Deploy based on environment
case $ENVIRONMENT in
    "development")
        echo "🏗️  Starting development environment..."
        docker-compose up -d
        echo "✅ Development app running at http://localhost:8501"
        ;;
    "staging")
        echo "🏗️  Deploying to staging..."
        # Add staging deployment commands here
        echo "✅ Staging deployment complete"
        ;;
    "production")
        echo "🏗️  Deploying to production..."
        # Add production deployment commands here
        echo "✅ Production deployment complete"
        ;;
    *)
        echo "❌ Unknown environment: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "🎉 Deployment complete!"
