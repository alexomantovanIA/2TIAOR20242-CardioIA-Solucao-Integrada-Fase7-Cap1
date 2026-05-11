import {
  InteractionRequiredAuthError,
  PublicClientApplication,
} from "@azure/msal-browser";

const tenantId = import.meta.env.VITE_ENTRA_TENANT_ID ?? "";
const clientId = import.meta.env.VITE_ENTRA_WEB_CLIENT_ID ?? "";
const apiScope = import.meta.env.VITE_ENTRA_API_SCOPE ?? "";

let instance: PublicClientApplication | null = null;

export function isMsalConfigured(): boolean {
  return Boolean(tenantId && clientId && apiScope);
}

export function getApiScope(): string {
  return apiScope;
}

function getInstance(): PublicClientApplication {
  if (!isMsalConfigured()) {
    throw new Error(
      "Defina VITE_ENTRA_TENANT_ID, VITE_ENTRA_WEB_CLIENT_ID e VITE_ENTRA_API_SCOPE para usar o login Entra ID.",
    );
  }
  if (!instance) {
    instance = new PublicClientApplication({
      auth: {
        clientId,
        authority: `https://login.microsoftonline.com/${tenantId}`,
        redirectUri: window.location.origin,
      },
      cache: {
        cacheLocation: "sessionStorage",
        storeAuthStateInCookie: false,
      },
    });
  }
  return instance;
}

export async function msalInitialize(): Promise<void> {
  const app = getInstance();
  await app.initialize();
  await app.handleRedirectPromise();
}

/** Só use após `msalInitialize()` (o bootstrap em `main.tsx` já faz isso antes de montar a UI). */
export function hasMsalAccount(): boolean {
  if (!isMsalConfigured()) {
    return false;
  }
  try {
    return getInstance().getAllAccounts().length > 0;
  } catch {
    return false;
  }
}

export async function loginEntraPopup(): Promise<void> {
  const app = getInstance();
  const result = await app.loginPopup({ scopes: [apiScope] });
  if (result.account) {
    app.setActiveAccount(result.account);
  }
}

export async function acquireApiToken(): Promise<string> {
  const app = getInstance();
  const account = app.getActiveAccount() ?? app.getAllAccounts()[0];
  if (!account) {
    throw new Error("Nenhuma conta Entra ID ativa. Faça login novamente.");
  }
  try {
    const result = await app.acquireTokenSilent({
      account,
      scopes: [apiScope],
    });
    return result.accessToken;
  } catch (err) {
    if (err instanceof InteractionRequiredAuthError) {
      const result = await app.acquireTokenPopup({
        account,
        scopes: [apiScope],
      });
      return result.accessToken;
    }
    throw err;
  }
}

export async function logoutEntra(): Promise<void> {
  const app = getInstance();
  const account = app.getActiveAccount() ?? app.getAllAccounts()[0];
  if (account) {
    await app.logoutPopup({ account });
  } else {
    await app.logoutPopup();
  }
}
