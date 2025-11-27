#!/bin/bash

# Deployment script for Google Cloud Run
# This script builds and deploys the FastAPI backend to Google Cloud Run

set -e  # Exit on error

# Configuration
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-your-project-id}"
SERVICE_NAME="${SERVICE_NAME:-date-night-devil-api}"
REGION="${REGION:-us-central1}"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting deployment to Google Cloud Run...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed.${NC}"
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed.${NC}"
    echo "Install it from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Set the project
echo -e "${YELLOW}Setting GCP project to ${PROJECT_ID}...${NC}"
gcloud config set project "${PROJECT_ID}"

# Enable required APIs
echo -e "${YELLOW}Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the Docker image using Cloud Build
echo -e "${YELLOW}Building Docker image...${NC}"
gcloud builds submit --tag "${IMAGE_NAME}"

# Deploy to Cloud Run
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE_NAME}" \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}" \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10

# Get the service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
    --platform managed \
    --region "${REGION}" \
    --format 'value(status.url)')

echo -e "${GREEN}Deployment complete!${NC}"
echo -e "${GREEN}Service URL: ${SERVICE_URL}${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update your frontend's VITE_API_BASE_URL environment variable to: ${SERVICE_URL}"
echo "2. If you need to set CORS origins, update ALLOWED_ORIGINS in Cloud Run:"
echo "   gcloud run services update ${SERVICE_NAME} --region ${REGION} --set-env-vars ALLOWED_ORIGINS=https://your-vercel-domain.vercel.app"
echo ""
echo -e "${YELLOW}To view logs:${NC}"
echo "gcloud run services logs read ${SERVICE_NAME} --region ${REGION}"

