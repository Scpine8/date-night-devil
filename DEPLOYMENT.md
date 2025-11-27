# Deployment Guide

This guide covers deploying both the frontend (Vercel) and backend (Google Cloud Run) for the Date Night Devil application.

## Prerequisites

### Frontend (Vercel)

- Node.js 18+ installed locally
- Vercel account (free tier available)
- Vercel CLI (optional, for CLI deployment)

### Backend (Google Cloud Run)

- Google Cloud account with billing enabled
- `gcloud` CLI installed and configured
- Docker installed locally (for local testing)
- Google Maps API key

## Frontend Deployment (Vercel)

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**

   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Connect to Vercel**

   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Select the `frontend` folder as the root directory

3. **Configure Build Settings**

   - Framework Preset: Vite
   - Build Command: `yarn build`
   - Output Directory: `dist`
   - Install Command: `yarn install`

4. **Set Environment Variables**

   - Go to Project Settings > Environment Variables
   - Add: `VITE_API_BASE_URL` = `https://your-cloud-run-url.run.app`
   - Replace `your-cloud-run-url` with your actual Cloud Run service URL

5. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**

   ```bash
   npm i -g vercel
   ```

2. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

3. **Login to Vercel**

   ```bash
   vercel login
   ```

4. **Deploy**

   ```bash
   vercel
   ```

   - Follow the prompts
   - Set environment variable when prompted: `VITE_API_BASE_URL=https://your-cloud-run-url.run.app`

5. **Set production environment variable**
   ```bash
   vercel env add VITE_API_BASE_URL production
   ```
   - Enter your Cloud Run URL when prompted

## Backend Deployment (Google Cloud Run)

### Initial Setup

1. **Create a Google Cloud Project** (if you don't have one)

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click the project dropdown at the top
   - Click "New Project"
   - Enter a project name (e.g., "Date Night Devil")
   - **Important**: Note the Project ID (it may be different from the name, e.g., `date-night-devil-123456`)
   - Click "Create"
   - Wait for the project to be created

2. **Enable Billing** (Required even for free tier)

   - Go to [Billing Settings](https://console.cloud.google.com/billing)
   - Click "Link a billing account"
   - Select or create a billing account
   - Link it to your project
   - **Note**: Google Cloud Run has a generous free tier (2M requests/month)

3. **Install Google Cloud SDK**

   ```bash
   # macOS
   # macOS
   brew install google-cloud-sdk

   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

4. **Authenticate and Set Project**

   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

   **Important**: Use the actual Project ID from step 1, not the project name!

5. **Enable Required APIs**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

### Deploy Using the Script

1. **Set Environment Variables**

   ```bash
   # IMPORTANT: Use your actual Project ID from Google Cloud Console
   # The Project ID is shown in the project dropdown (may differ from project name)
   export GOOGLE_CLOUD_PROJECT="your-actual-project-id"
   export SERVICE_NAME="date-night-devil-api"
   export REGION="us-central1"  # or your preferred region
   export GOOGLE_MAPS_API_KEY="your-api-key"
   ```

   **How to find your Project ID:**

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click the project dropdown at the top
   - Your Project ID is shown next to each project (format: `project-name-123456`)
   - Copy the exact Project ID (not the project name)

2. **Run Deployment Script**

   ```bash
   ./deploy.sh
   ```

   The script will:

   - Build the Docker image using Cloud Build
   - Push the image to Google Container Registry
   - Deploy to Cloud Run
   - Output the service URL

3. **Note the Service URL**
   - Copy the service URL from the output
   - You'll need this for the frontend's `VITE_API_BASE_URL`

### Manual Deployment Steps

If you prefer to deploy manually:

1. **Build and Push Docker Image**

   ```bash
   # Build using Cloud Build
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/date-night-devil-api
   ```

2. **Deploy to Cloud Run**

   ```bash
   gcloud run deploy date-night-devil-api \
     --image gcr.io/YOUR_PROJECT_ID/date-night-devil-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars "GOOGLE_MAPS_API_KEY=your-api-key" \
     --port 8080 \
     --memory 512Mi \
     --cpu 1 \
     --timeout 300 \
     --max-instances 10
   ```

3. **Get the Service URL**
   ```bash
   gcloud run services describe date-night-devil-api \
     --platform managed \
     --region us-central1 \
     --format 'value(status.url)'
   ```

### Configure CORS for Production

After deploying both frontend and backend:

1. **Get your Vercel domain**

   - Found in Vercel dashboard: `https://your-project.vercel.app`

2. **Update Cloud Run CORS settings**

   ```bash
   gcloud run services update date-night-devil-api \
     --region us-central1 \
     --set-env-vars ALLOWED_ORIGINS=https://your-project.vercel.app,https://your-project.vercel.app
   ```

   Or set multiple origins (comma-separated):

   ```bash
   gcloud run services update date-night-devil-api \
     --region us-central1 \
     --set-env-vars ALLOWED_ORIGINS=https://your-project.vercel.app,https://your-custom-domain.com
   ```

## Environment Variables Summary

### Frontend (Vercel)

- `VITE_API_BASE_URL`: Your Cloud Run service URL (e.g., `https://date-night-devil-api-xxx.run.app`)

### Backend (Cloud Run)

- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key
- `PORT`: Automatically set by Cloud Run (default: 8080)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins (optional)

## Updating Deployments

### Frontend Updates

- Push changes to GitHub
- Vercel will automatically redeploy (if connected via Git)
- Or run `vercel --prod` from the frontend directory

### Backend Updates

- Make your code changes
- Run `./deploy.sh` again
- Cloud Run will perform a rolling update

## Monitoring and Logs

### View Cloud Run Logs

```bash
gcloud run services logs read date-night-devil-api --region us-central1
```

### View Cloud Run Metrics

- Go to [Cloud Run Console](https://console.cloud.google.com/run)
- Select your service
- View metrics, logs, and revisions

### View Vercel Logs

- Go to Vercel Dashboard
- Select your project
- Click on "Deployments" > Select a deployment > View logs

## Troubleshooting

### Frontend Issues

**Build fails:**

- Check Node.js version (should be 18+)
- Verify all dependencies are in `package.json`
- Check build logs in Vercel dashboard

**API calls fail:**

- Verify `VITE_API_BASE_URL` is set correctly
- Check browser console for CORS errors
- Ensure backend is deployed and accessible

### Backend Issues

**Deployment fails:**

- Verify `gcloud` is authenticated: `gcloud auth list`
- Check project ID is correct: `gcloud config get-value project`
- Ensure billing is enabled on your GCP project
- Check Cloud Build logs: `gcloud builds list`

**Service not accessible:**

- Verify service is deployed: `gcloud run services list`
- Check service URL is correct
- Verify `--allow-unauthenticated` flag was used
- Check service logs for errors

**CORS errors:**

- Verify `ALLOWED_ORIGINS` includes your Vercel domain
- Check that origins don't have trailing slashes
- Ensure frontend is using the correct API URL

**Google Maps API errors:**

- Verify `GOOGLE_MAPS_API_KEY` is set correctly
- Check API key restrictions in Google Cloud Console
- Ensure Places API is enabled
- Verify billing is enabled

## Cost Estimation

### Vercel

- **Free Tier**: Unlimited personal projects, 100GB bandwidth/month
- **Pro**: $20/month for team features

### Google Cloud Run

- **Free Tier**: 2 million requests/month, 360,000 GB-seconds, 180,000 vCPU-seconds
- **Pricing**: Pay only for what you use after free tier
- Typical small app: **$0-5/month** (well within free tier)

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Restrict Google Maps API key** - Limit to Places API only
3. **Use HTTPS** - Both Vercel and Cloud Run provide HTTPS by default
4. **Set CORS origins** - Only allow your Vercel domain(s)
5. **Monitor usage** - Set up billing alerts in Google Cloud Console

## Next Steps

After successful deployment:

1. Test the deployed frontend and backend
2. Set up a custom domain (optional)
3. Configure monitoring and alerts
4. Set up CI/CD for automatic deployments
5. Review and optimize costs
