# Deploy gemini-web2api on Render

This copy includes a Render Blueprint (`render.yaml`). It builds the Dockerfile, listens on Render's `PORT`, and asks for a private API key during setup. The container refuses to start without that key.

## Deploy

1. Push **this modified copy** to a new, empty GitHub repository you control. The original upstream repository does not contain these Render files. If you received the ZIP, extract it and run these commands inside the extracted `gemini-web2api` folder (replace `YOUR_USERNAME`):

   ```powershell
   git init
   git add .
   git commit -m "Prepare Render deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/gemini-web2api-render.git
   git push -u origin main
   ```

2. In [Render](https://dashboard.render.com/), choose **New → Blueprint**, connect your GitHub repository, and select it.
3. When Render prompts for `GEMINI_WEB2API_API_KEY`, enter a long, random key. Save it somewhere private for your API client. Do not use the public `sk-gemini` example key.
4. Apply the Blueprint. It creates one Free Docker web service with a health check at `/`.
5. Once live, use `https://YOUR-SERVICE.onrender.com/v1` as the OpenAI-compatible base URL and your chosen key as the Bearer API key.

To verify, run this PowerShell command, substituting your URL and key:

```powershell
curl.exe -H "Authorization: Bearer YOUR-KEY" https://YOUR-SERVICE.onrender.com/v1/models
```

If the service starts but chat requests fail, inspect **Logs** in Render. The app needs outbound access to `gemini.google.com`; upstream may throttle or block cloud IPs. Render's Free plan sleeps after 15 minutes of no incoming traffic, so the first request after idle can be slow.

## Optional paid-account cookie

In the service's **Environment → Secret Files**, add a file named `cookie.txt` containing the cookie format described in the main README. Add the environment variable `GEMINI_WEB2API_COOKIE_FILE=/etc/secrets/cookie.txt`, then redeploy. Keep the cookie in Render's secret settings, never in Git.

## Update the code

Push changes to your connected GitHub repository. Render rebuilds the Docker service on commits. If you deployed from a public Git URL instead of a connected GitHub account, Render requires manual redeployment.
