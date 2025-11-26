# Troubleshooting REQUEST_DENIED Billing Error

## The Problem

You're getting `REQUEST_DENIED` with a billing error message, even though you believe billing is enabled.

## Most Common Causes

1. **The API key belongs to a different project than the one with billing enabled.**
2. **⚠️ The payment method on the billing account is expired, invalid, or not working** - Even if billing appears enabled, Google will deny requests if the payment method cannot be charged. **You must update the payment method to one that works.**

## Step-by-Step Verification

### Step 1: Identify Which Project Your API Key Belongs To

1. Go to [Google Cloud Console > APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Find your API key (starts with `AIzaSyDJPP...`)
3. **Click on the API key name** (not the key itself, but the name/label)
4. Look at the top of the page - it will show which **Project** this API key belongs to
5. **Write down the Project ID or Project Name**

### Step 2: Verify Billing is Enabled for THAT Specific Project

1. Make sure you're viewing the **correct project** (check the project dropdown in the top bar)
2. Go to [Billing Settings](https://console.cloud.google.com/billing)
3. You should see a list of projects and their billing status
4. **Find the project that matches your API key's project** from Step 1
5. Verify it shows:
   - ✅ "Billing account: [Your Billing Account]"
   - ✅ Status: "Active" or "Enabled"

### Step 3: If Billing Shows as Enabled But Still Getting Error

Try these steps:

#### Option A: Re-link Billing Account

1. Go to [Billing Settings](https://console.cloud.google.com/billing)
2. Click on your billing account
3. Under "Projects linked to this billing account", verify your project is listed
4. If not listed, click "Link a project" and select your project
5. Wait 2-3 minutes for changes to propagate

#### Option B: Verify Project Selection

1. In Google Cloud Console, check the **project dropdown** in the top bar
2. Make sure you're looking at the **same project** where your API key was created
3. Sometimes you might have multiple projects and be looking at the wrong one

#### Option C: Check Billing Account Status

1. Go to [Billing Accounts](https://console.cloud.google.com/billing/accounts)
2. Verify your billing account shows:
   - Status: "Open" (not "Closed" or "Cancelled")
   - **⚠️ CRITICAL: Payment method is valid and working** - If your payment method is expired, declined, or invalid, billing will not work even if it appears enabled. **You must update the payment method to one that works.**
   - No outstanding issues
3. **To update payment method:**
   - Click on your billing account
   - Go to "Payment methods" section
   - Add or update your payment method (credit card, bank account, etc.)
   - Ensure the payment method is active and has sufficient funds/credit
   - Wait 2-3 minutes for changes to propagate

#### Option D: Create a New API Key in the Correct Project

If billing is definitely enabled on a project:

1. Make sure you're in the project with billing enabled
2. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
3. Click "Create Credentials" > "API Key"
4. Copy the new API key
5. Update your `.env` file with the new key
6. Restart your server

### Step 4: Verify Places API is Enabled

1. Make sure you're in the **correct project** (the one with billing)
2. Go to [APIs & Services > Library](https://console.cloud.google.com/apis/library)
3. Search for "Places API"
4. Click on it and verify it shows "API enabled" (green checkmark)
5. If not enabled, click "Enable"

## Quick Checklist

- [ ] API key belongs to Project X
- [ ] Project X has billing enabled (check billing settings)
- [ ] **⚠️ Billing account has a valid, working payment method** - Payment method must be active, not expired, and have sufficient funds/credit
- [ ] Billing account status is "Open" (not "Closed" or "Cancelled")
- [ ] Project X has Places API enabled
- [ ] You're looking at Project X in the console (not a different project)
- [ ] API key restrictions allow Places API (if restrictions are set)

## Still Not Working?

If you've verified all of the above:

1. **Wait 5-10 minutes** - Sometimes Google's systems take time to propagate billing changes
2. **Try a different API key** - Create a new one in the project with billing enabled
3. **Check Google Cloud Status** - Visit [status.cloud.google.com](https://status.cloud.google.com) for any service issues
4. **Contact Google Support** - If billing is definitely enabled, there might be an account-level issue

## Testing After Changes

After making any changes:

1. Wait 2-3 minutes for changes to propagate
2. Restart your server: `make start` or `uvicorn app.main:app --reload`
3. Test the debug endpoint: `curl http://localhost:8000/debug/google-maps`
4. Check if the error persists
