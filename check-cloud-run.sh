#!/bin/bash

# Script to check Cloud Run services and update CORS

echo "Checking Cloud Run services..."
gcloud run services list

echo ""
echo "To update CORS, run:"
echo "gcloud run services update YOUR_SERVICE_NAME \\"
echo "  --region YOUR_REGION \\"
echo "  --set-env-vars ALLOWED_ORIGINS=https://date-night-devil-5zwo6rcpo-sean-pines-projects.vercel.app"

