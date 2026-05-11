import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { isMsalConfigured, msalInitialize } from "./auth/msal";
import "./styles.css";

async function bootstrap() {
  if (isMsalConfigured()) {
    await msalInitialize();
  }
  ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
}

void bootstrap();
