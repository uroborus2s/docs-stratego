const PRIVATE_URLS = new Set(["/crawler4j/04-project-development/", "/crawler4j/04-project-development/01-governance/", "/crawler4j/04-project-development/01-governance/project-charter/", "/crawler4j/04-project-development/02-discovery/", "/crawler4j/04-project-development/02-discovery/current-state-analysis/", "/crawler4j/04-project-development/02-discovery/input/", "/crawler4j/04-project-development/02-discovery/legacy-doc-audit/", "/crawler4j/04-project-development/03-requirements/", "/crawler4j/04-project-development/03-requirements/prd/", "/crawler4j/04-project-development/03-requirements/requirements-analysis/", "/crawler4j/04-project-development/03-requirements/requirements-verification/", "/crawler4j/04-project-development/04-design/", "/crawler4j/04-project-development/04-design/api-design/", "/crawler4j/04-project-development/04-design/module-boundaries/", "/crawler4j/04-project-development/04-design/system-architecture/", "/crawler4j/04-project-development/04-design/technical-selection/", "/crawler4j/04-project-development/05-development-process/", "/crawler4j/04-project-development/05-development-process/implementation-plan/", "/crawler4j/04-project-development/05-development-process/software-development-process/", "/crawler4j/04-project-development/06-testing-verification/", "/crawler4j/04-project-development/06-testing-verification/design-implementation-audit/", "/crawler4j/04-project-development/06-testing-verification/quality-gates/", "/crawler4j/04-project-development/06-testing-verification/test-plan/", "/crawler4j/04-project-development/07-release-delivery/", "/crawler4j/04-project-development/07-release-delivery/release-notes/", "/crawler4j/04-project-development/07-release-delivery/version-governance/", "/crawler4j/04-project-development/08-operations-maintenance/", "/crawler4j/04-project-development/08-operations-maintenance/core-maintainer-guide/", "/crawler4j/04-project-development/08-operations-maintenance/deployment-guide/", "/crawler4j/04-project-development/09-evolution/", "/crawler4j/04-project-development/09-evolution/skill-evolution-plan/", "/crawler4j/04-project-development/10-traceability/", "/crawler4j/04-project-development/10-traceability/document-index/", "/crawler4j/04-project-development/10-traceability/interface-matrix/", "/crawler4j/04-project-development/10-traceability/requirements-matrix/", "/docs-stratego/04-project-development/", "/docs-stratego/04-project-development/01-governance/", "/docs-stratego/04-project-development/01-governance/project-charter/", "/docs-stratego/04-project-development/02-discovery/", "/docs-stratego/04-project-development/02-discovery/brainstorm-record/", "/docs-stratego/04-project-development/02-discovery/input/", "/docs-stratego/04-project-development/03-requirements/", "/docs-stratego/04-project-development/03-requirements/changelog/", "/docs-stratego/04-project-development/03-requirements/prd/", "/docs-stratego/04-project-development/03-requirements/requirements-analysis/", "/docs-stratego/04-project-development/03-requirements/requirements-verification/", "/docs-stratego/04-project-development/04-design/", "/docs-stratego/04-project-development/04-design/api-design/", "/docs-stratego/04-project-development/04-design/backend-design/", "/docs-stratego/04-project-development/04-design/crawler4j-integration-package/", "/docs-stratego/04-project-development/04-design/database-design/", "/docs-stratego/04-project-development/04-design/deployment-architecture/", "/docs-stratego/04-project-development/04-design/module-boundaries/", "/docs-stratego/04-project-development/04-design/source-docs-standard/", "/docs-stratego/04-project-development/04-design/system-architecture/", "/docs-stratego/04-project-development/04-design/technical-selection/", "/docs-stratego/04-project-development/04-design/ux-ui-design/", "/docs-stratego/04-project-development/05-development-process/", "/docs-stratego/04-project-development/05-development-process/implementation-plan/", "/docs-stratego/04-project-development/05-development-process/software-development-process/", "/docs-stratego/04-project-development/05-development-process/task-breakdown/", "/docs-stratego/04-project-development/05-development-process/wbs/", "/docs-stratego/04-project-development/06-testing-verification/", "/docs-stratego/04-project-development/06-testing-verification/test-cases/", "/docs-stratego/04-project-development/06-testing-verification/test-plan/", "/docs-stratego/04-project-development/06-testing-verification/test-report/", "/docs-stratego/04-project-development/07-release-delivery/", "/docs-stratego/04-project-development/07-release-delivery/acceptance-checklist/", "/docs-stratego/04-project-development/07-release-delivery/delivery-package/", "/docs-stratego/04-project-development/07-release-delivery/release-notes/", "/docs-stratego/04-project-development/08-operations-maintenance/", "/docs-stratego/04-project-development/08-operations-maintenance/deployment-guide/", "/docs-stratego/04-project-development/08-operations-maintenance/operations-runbook/", "/docs-stratego/04-project-development/08-operations-maintenance/server-deployment-sop/", "/docs-stratego/04-project-development/09-evolution/", "/docs-stratego/04-project-development/09-evolution/retrospective/", "/docs-stratego/04-project-development/09-evolution/skill-evolution-plan/", "/docs-stratego/04-project-development/10-traceability/", "/docs-stratego/04-project-development/10-traceability/document-index/", "/docs-stratego/04-project-development/10-traceability/interface-matrix/", "/docs-stratego/04-project-development/10-traceability/requirements-matrix/", "/ride-loop/04-project-development/01-governance/", "/ride-loop/04-project-development/01-governance/project-charter/", "/ride-loop/04-project-development/02-discovery/", "/ride-loop/04-project-development/02-discovery/brainstorm-record/", "/ride-loop/04-project-development/02-discovery/input/", "/ride-loop/04-project-development/03-requirements/requirements-verification/", "/ride-loop/04-project-development/03-requirements/terminal-strategy/", "/ride-loop/04-project-development/04-design/", "/ride-loop/04-project-development/04-design/api-design/", "/ride-loop/04-project-development/04-design/backend-design/", "/ride-loop/04-project-development/04-design/database-design/", "/ride-loop/04-project-development/04-design/database-er-diagram/", "/ride-loop/04-project-development/04-design/design-token-component-spec/", "/ride-loop/04-project-development/04-design/design-tool-prompt-pack/", "/ride-loop/04-project-development/04-design/driver-heavy-app-spec/", "/ride-loop/04-project-development/04-design/driver-light-miniapp-spec/", "/ride-loop/04-project-development/04-design/module-boundaries/", "/ride-loop/04-project-development/04-design/openapi/", "/ride-loop/04-project-development/04-design/openapi/driver-heavy-app.openapi.yaml", "/ride-loop/04-project-development/04-design/openapi/driver-light-miniapp.openapi.yaml", "/ride-loop/04-project-development/04-design/openapi/ops-web.openapi.yaml", "/ride-loop/04-project-development/04-design/openapi/passenger-miniapp.openapi.yaml", "/ride-loop/04-project-development/04-design/ops-web-spec/", "/ride-loop/04-project-development/04-design/page-prompt-catalog/", "/ride-loop/04-project-development/04-design/system-architecture/", "/ride-loop/04-project-development/04-design/system-detailed-design/", "/ride-loop/04-project-development/04-design/technical-selection/", "/ride-loop/04-project-development/04-design/ui-page-detail-matrix/", "/ride-loop/04-project-development/04-design/ux-ui-design/", "/ride-loop/04-project-development/06-testing-verification/", "/ride-loop/04-project-development/06-testing-verification/test-plan/", "/ride-loop/04-project-development/07-release-delivery/", "/ride-loop/04-project-development/08-operations-maintenance/", "/ride-loop/04-project-development/08-operations-maintenance/deployment-guide/", "/ride-loop/04-project-development/09-evolution/", "/ride-loop/04-project-development/10-traceability/", "/ride-loop/04-project-development/10-traceability/requirements-matrix/", "/stratix/04-project-development/", "/stratix/04-project-development/01-governance/", "/stratix/04-project-development/01-governance/project-charter/", "/stratix/04-project-development/02-discovery/", "/stratix/04-project-development/02-discovery/brainstorm-record/", "/stratix/04-project-development/02-discovery/current-state-analysis/", "/stratix/04-project-development/02-discovery/input/", "/stratix/04-project-development/03-requirements/", "/stratix/04-project-development/03-requirements/prd/", "/stratix/04-project-development/03-requirements/requirements-analysis/", "/stratix/04-project-development/03-requirements/requirements-verification/", "/stratix/04-project-development/04-design/", "/stratix/04-project-development/04-design/api-design/", "/stratix/04-project-development/04-design/backend-design/", "/stratix/04-project-development/04-design/module-boundaries/", "/stratix/04-project-development/04-design/system-architecture/", "/stratix/04-project-development/04-design/technical-selection/", "/stratix/04-project-development/05-development-process/", "/stratix/04-project-development/05-development-process/implementation-plan/", "/stratix/04-project-development/06-testing-verification/", "/stratix/04-project-development/06-testing-verification/test-plan/", "/stratix/04-project-development/07-release-delivery/", "/stratix/04-project-development/07-release-delivery/release-notes/", "/stratix/04-project-development/08-operations-maintenance/", "/stratix/04-project-development/08-operations-maintenance/deployment-guide/", "/stratix/04-project-development/09-evolution/", "/stratix/04-project-development/10-traceability/", "/stratix/04-project-development/10-traceability/requirements-matrix/"]);
const AUTH_POPUP_MESSAGE_TYPE = "docs-auth-popup-complete";
const AUTH_POPUP_CALLBACK_PATH = "/assets/auth/popup-complete.html";

let authPopup = null;
let authPopupMonitor = null;
let authFlowId = 0;
let pendingTargetUrl = "";

function normalizeSitePath(rawUrl) {
  try {
    const url = new URL(rawUrl, window.location.origin);
    if (url.origin !== window.location.origin) {
      return null;
    }
    let path = url.pathname || "/";
    if (path.endsWith("/index.html")) {
      path = path.slice(0, -10) || "/";
    } else if (path.endsWith(".html")) {
      path = `${path.slice(0, -5)}/`;
    } else if (!path.endsWith("/") && !path.split("/").pop().includes(".")) {
      path = `${path}/`;
    }
    return path || "/";
  } catch (_error) {
    return null;
  }
}

function isPrivateUrl(rawUrl) {
  const normalizedPath = normalizeSitePath(rawUrl);
  return normalizedPath ? PRIVATE_URLS.has(normalizedPath) : false;
}

function resolveSameOriginUrl(rawUrl) {
  try {
    const url = new URL(rawUrl, window.location.origin);
    if (url.origin !== window.location.origin) {
      return null;
    }
    return url.toString();
  } catch (_error) {
    return null;
  }
}

async function checkAuthStatus() {
  try {
    const response = await fetch("/oauth2/auth", {
      credentials: "same-origin",
      cache: "no-store",
    });
    return response.status >= 200 && response.status < 300;
  } catch (_error) {
    return false;
  }
}

function stopAuthPopupMonitor() {
  if (authPopupMonitor) {
    window.clearInterval(authPopupMonitor);
    authPopupMonitor = null;
  }
}

function closeAuthPopup() {
  stopAuthPopupMonitor();
  if (authPopup && !authPopup.closed) {
    try {
      authPopup.close();
    } catch (_error) {
      // ignore popup close errors
    }
  }
  authPopup = null;
}

function dismissAuthPopupOnBackgroundInteraction() {
  if (!authPopup || authPopup.closed) {
    authPopup = null;
    return;
  }
  closeAuthPopup();
}

function buildAuthPopupFeatures() {
  const width = 480;
  const height = 760;
  const left = Math.max(window.screenX + Math.round((window.outerWidth - width) / 2), 0);
  const top = Math.max(window.screenY + Math.round((window.outerHeight - height) / 2), 0);
  return `popup=yes,width=${width},height=${height},left=${left},top=${top},resizable=yes,scrollbars=yes`;
}

function openAuthPopupShell() {
  closeAuthPopup();
  const popup = window.open("about:blank", "docsAuthPopup", buildAuthPopupFeatures());
  if (!popup) {
    return null;
  }
  try {
    popup.document.title = "打开登录中";
    popup.document.body.style.margin = "0";
    popup.document.body.style.display = "grid";
    popup.document.body.style.placeItems = "center";
    popup.document.body.style.minHeight = "100vh";
    popup.document.body.style.fontFamily = "system-ui, sans-serif";
    popup.document.body.style.color = "#344054";
    popup.document.body.textContent = "正在打开登录...";
  } catch (_error) {
    // ignore popup rendering errors
  }
  return popup;
}

function buildAuthPopupCallbackUrl(targetUrl, flowId) {
  const callbackUrl = new URL(AUTH_POPUP_CALLBACK_PATH, window.location.origin);
  callbackUrl.searchParams.set("flow", String(flowId));
  callbackUrl.searchParams.set("target", targetUrl);
  return callbackUrl.toString();
}

function startAuthPopupMonitor(flowId) {
  stopAuthPopupMonitor();
  authPopupMonitor = window.setInterval(async () => {
    if (flowId !== authFlowId) {
      stopAuthPopupMonitor();
      return;
    }
    if (!authPopup) {
      stopAuthPopupMonitor();
      return;
    }
    if (!authPopup.closed) {
      return;
    }
    stopAuthPopupMonitor();
    authPopup = null;
    if (!pendingTargetUrl) {
      return;
    }
    const targetUrl = pendingTargetUrl;
    pendingTargetUrl = "";
    const authenticated = await checkAuthStatus();
    if (authenticated) {
      window.location.assign(targetUrl);
    }
  }, 500);
}

function handleAuthPopupMessage(event) {
  if (event.origin !== window.location.origin) {
    return;
  }
  const data = event.data;
  if (!data || data.type !== AUTH_POPUP_MESSAGE_TYPE) {
    return;
  }
  if (String(data.flowId || "") !== String(authFlowId)) {
    return;
  }
  const targetUrl = resolveSameOriginUrl(data.targetUrl) || pendingTargetUrl;
  pendingTargetUrl = "";
  closeAuthPopup();
  if (targetUrl) {
    window.location.assign(targetUrl);
  }
}

async function beginPopupAuthFlow(targetUrl) {
  const safeTargetUrl = resolveSameOriginUrl(targetUrl);
  if (!safeTargetUrl) {
    return;
  }
  pendingTargetUrl = safeTargetUrl;
  authFlowId += 1;
  const flowId = authFlowId;
  const popup = openAuthPopupShell();
  const authenticated = await checkAuthStatus();
  if (authenticated) {
    pendingTargetUrl = "";
    if (popup && !popup.closed) {
      popup.close();
    }
    window.location.assign(safeTargetUrl);
    return;
  }

  const signInUrl = `/oauth2/sign_in?rd=${encodeURIComponent(buildAuthPopupCallbackUrl(safeTargetUrl, flowId))}`;
  if (!popup) {
    window.location.assign(signInUrl);
    return;
  }

  authPopup = popup;
  startAuthPopupMonitor(flowId);
  try {
    popup.location.replace(signInUrl);
    popup.focus();
  } catch (_error) {
    closeAuthPopup();
    window.location.assign(signInUrl);
  }
}

function annotatePrivateLinks(root = document) {
  root.querySelectorAll("a[href]").forEach((anchor) => {
    if (anchor.dataset.docsPrivateAnnotated === "true") {
      return;
    }
    const href = anchor.getAttribute("href") || anchor.href;
    if (!isPrivateUrl(href)) {
      return;
    }
    anchor.dataset.docsPrivateAnnotated = "true";
    anchor.classList.add("docs-private-link");
    const label = anchor.getAttribute("aria-label") || anchor.textContent?.trim() || "受保护文档";
    anchor.setAttribute("aria-label", `${label}（需要登录）`);
  });
}

function shouldInterceptClick(event, anchor) {
  if (event.defaultPrevented || event.button !== 0) {
    return false;
  }
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
    return false;
  }
  if (anchor.hasAttribute("download")) {
    return false;
  }
  const target = anchor.getAttribute("target");
  if (target && target !== "_self") {
    return false;
  }
  return isPrivateUrl(anchor.href);
}

async function handlePrivateLinkClick(event, anchor) {
  event.preventDefault();
  beginPopupAuthFlow(anchor.href);
}

document$.subscribe(() => {
  annotatePrivateLinks();

  if (window.__docsAccessControlHandlersBound) {
    return;
  }
  window.__docsAccessControlHandlersBound = true;

  document.addEventListener("click", (event) => {
    if (!(event.target instanceof Element)) {
      return;
    }
    const anchor = event.target.closest("a[href]");
    if (!(anchor instanceof HTMLAnchorElement)) {
      return;
    }
    if (!shouldInterceptClick(event, anchor)) {
      return;
    }
    handlePrivateLinkClick(event, anchor);
  });
  document.addEventListener("pointerdown", dismissAuthPopupOnBackgroundInteraction, true);
  window.addEventListener("focus", dismissAuthPopupOnBackgroundInteraction);
  window.addEventListener("message", handleAuthPopupMessage);
});
