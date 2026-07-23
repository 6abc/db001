## How to obtain Microsoft OAuth Credentials

- MICROSOFT_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- MICROSOFT_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
- MICROSOFT_TENANT=common

--------------------------------
### Microsoft Entra admin center
https://entra.microsoft.com/

### Requirement
- Microsoft Account (Personal or Work/School)
--------------------------------

## 1. Register an Application

Navigate to:

```text
Identity
└── Applications
    └── App registrations
        └── New registration
```

Configure the application:

```text
Name:
My Web App

Supported account types:
Accounts in any organizational directory
(Any Microsoft Entra ID tenant - Multitenant)
and personal Microsoft accounts (e.g. Skype, Xbox)

Click:
Register
```

---

## 2. Get MICROSOFT_CLIENT_ID

After registration, open the **Overview** page.

Copy:

```text
Application (client) ID
```

Example:

```env
MICROSOFT_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## 3. Configure Redirect URI

Navigate to:

```text
Your App
└── Authentication
    └── Add a platform
        └── Web
```

### Development

```text
http://localhost/accounts/microsoft/login/callback/
```

### Production

```text
https://your-domain.com/accounts/microsoft/login/callback/
```

> **Important:** The Redirect URI must exactly match the callback URL used by your Django application.

---

## 4. Create MICROSOFT_CLIENT_SECRET

Navigate to:

```text
Your App
└── Certificates & secrets
    └── Client secrets
        └── New client secret
```

Choose:

```text
Description:
My Web App

Expires:
Choose the desired expiration period
(e.g. 180 days or 730 days)

Click:
Add
```

Immediately copy the **Value**.

> ⚠️ Copy the **Value**, **NOT** the **Secret ID**.
>
> The secret value is shown **only once**. If you lose it, you must create a new secret.

Example:

```env
MICROSOFT_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 5. Configure MICROSOFT_TENANT

For most applications, use:

```env
MICROSOFT_TENANT=common
```

Available options:

| Value | Description |
|--------|-------------|
| `common` | ✅ Personal Microsoft accounts + Work/School accounts (Recommended) |
| `organizations` | Work/School (Microsoft Entra ID) accounts only |
| `consumers` | Personal Microsoft accounts only |
| `<tenant-id>` | Single organization (single tenant) only |

---

## Example `.env`

```env
MICROSOFT_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MICROSOFT_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
MICROSOFT_TENANT=common
```

---

## Django Allauth Callback URLs

Development

```text
http://localhost/accounts/microsoft/login/callback/
```

Production

```text
https://your-domain.com/accounts/microsoft/login/callback/
```

These are the default callback URLs used by the Django Allauth Microsoft provider.
