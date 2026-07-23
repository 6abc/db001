## How to get CLIENT creds
- MICROSOFT_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- MICROSOFT_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
- MICROSOFT_TENANT=common
----------------------------
### Microsoft Entra admin center link : https://entra.microsoft.com/
### Requirement : Microsoft Account
----------------------------

1. Open App registrations - Microsoft Entra admin center
  -  Identity → Applications → App registrations → New registration

2. Register the app
```sh
Name:
My Web App
Supported account types:
Accounts in any organizational directory and personal Microsoft accounts
Click Register
```

3. Get MICROSOFT_CLIENT_ID
  -  After registration, you will see **Application (client) ID**

4. Add the Redirect URI
  -  Your Web App → Authentication → Add a platform → Web
Enter URI: [localhost/domain]
```sh
http://localhost/accounts/microsoft/login/callback/
```

5. Create MICROSOFT_CLIENT_SECRET
  -  Your App → Certificates & secrets → Client secrets → New client secret
  -  **Copy the Value immediately. Do not copy Secret ID**
