## How to get CLIENT creds
- GOOGLE_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
- GOOGLE_CLIENT_SECRET=GOCSPX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
--------------------------------
### Google Cloud Console : https://console.cloud.google.com/
### Requirement : Google Account
--------------------------------

1. Create or Select a Project
  - Google Cloud Console → Select Project → New Project (or choose an existing one)

2. Configure OAuth Consent Screen
  - APIs & Services → OAuth consent screen
```sh
User Type:
External

App Name:
My Web App

User Support Email:
your-email@example.com

Developer Contact Information:
your-email@example.com

Save and Continue
```

3. Create OAuth Client ID
  - APIs & Services → Credentials → Create Credentials → OAuth client ID
```sh
Application Type:
Web application

Name:
My Web App
```

4. Add Authorized Redirect URI
  - Under "Authorized redirect URIs" add:
```sh
http://localhost/accounts/google/login/callback/
```

For production:
```sh
https://your-domain.com/accounts/google/login/callback/
```

5. Get GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
  - After creating the OAuth Client, copy:
    - **Client ID** → GOOGLE_CLIENT_ID
    - **Client Secret** → GOOGLE_CLIENT_SECRET

6. (Optional) Add Authorized JavaScript Origins
```sh
http://localhost
```

For production:
```sh
https://your-domain.com
```
