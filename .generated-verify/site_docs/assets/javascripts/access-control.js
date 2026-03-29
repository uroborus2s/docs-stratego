const PRIVATE_URLS = new Set(["/crawler4j/04-project-development/", "/crawler4j/04-project-development/01-governance/", "/crawler4j/04-project-development/01-governance/project-charter/", "/crawler4j/04-project-development/02-discovery/", "/crawler4j/04-project-development/02-discovery/current-state-analysis/", "/crawler4j/04-project-development/02-discovery/input/", "/crawler4j/04-project-development/02-discovery/legacy-doc-audit/", "/crawler4j/04-project-development/03-requirements/", "/crawler4j/04-project-development/03-requirements/prd/", "/crawler4j/04-project-development/03-requirements/requirements-analysis/", "/crawler4j/04-project-development/03-requirements/requirements-verification/", "/crawler4j/04-project-development/04-design/", "/crawler4j/04-project-development/04-design/api-design/", "/crawler4j/04-project-development/04-design/module-boundaries/", "/crawler4j/04-project-development/04-design/system-architecture/", "/crawler4j/04-project-development/04-design/technical-selection/", "/crawler4j/04-project-development/05-development-process/", "/crawler4j/04-project-development/05-development-process/implementation-plan/", "/crawler4j/04-project-development/05-development-process/software-development-process/", "/crawler4j/04-project-development/06-testing-verification/", "/crawler4j/04-project-development/06-testing-verification/design-implementation-audit/", "/crawler4j/04-project-development/06-testing-verification/quality-gates/", "/crawler4j/04-project-development/06-testing-verification/test-plan/", "/crawler4j/04-project-development/07-release-delivery/", "/crawler4j/04-project-development/07-release-delivery/release-notes/", "/crawler4j/04-project-development/07-release-delivery/version-governance/", "/crawler4j/04-project-development/08-operations-maintenance/", "/crawler4j/04-project-development/08-operations-maintenance/core-maintainer-guide/", "/crawler4j/04-project-development/08-operations-maintenance/deployment-guide/", "/crawler4j/04-project-development/09-evolution/", "/crawler4j/04-project-development/09-evolution/skill-evolution-plan/", "/crawler4j/04-project-development/10-traceability/", "/crawler4j/04-project-development/10-traceability/document-index/", "/crawler4j/04-project-development/10-traceability/interface-matrix/", "/crawler4j/04-project-development/10-traceability/requirements-matrix/", "/docs-stratego/04-project-development/", "/docs-stratego/04-project-development/01-governance/", "/docs-stratego/04-project-development/01-governance/project-charter/", "/docs-stratego/04-project-development/02-discovery/", "/docs-stratego/04-project-development/02-discovery/brainstorm-record/", "/docs-stratego/04-project-development/02-discovery/input/", "/docs-stratego/04-project-development/03-requirements/", "/docs-stratego/04-project-development/03-requirements/changelog/", "/docs-stratego/04-project-development/03-requirements/prd/", "/docs-stratego/04-project-development/03-requirements/requirements-analysis/", "/docs-stratego/04-project-development/03-requirements/requirements-verification/", "/docs-stratego/04-project-development/04-design/", "/docs-stratego/04-project-development/04-design/api-design/", "/docs-stratego/04-project-development/04-design/backend-design/", "/docs-stratego/04-project-development/04-design/crawler4j-integration-package/", "/docs-stratego/04-project-development/04-design/database-design/", "/docs-stratego/04-project-development/04-design/deployment-architecture/", "/docs-stratego/04-project-development/04-design/module-boundaries/", "/docs-stratego/04-project-development/04-design/source-docs-standard/", "/docs-stratego/04-project-development/04-design/system-architecture/", "/docs-stratego/04-project-development/04-design/technical-selection/", "/docs-stratego/04-project-development/04-design/ux-ui-design/", "/docs-stratego/04-project-development/05-development-process/", "/docs-stratego/04-project-development/05-development-process/implementation-plan/", "/docs-stratego/04-project-development/05-development-process/software-development-process/", "/docs-stratego/04-project-development/05-development-process/task-breakdown/", "/docs-stratego/04-project-development/05-development-process/wbs/", "/docs-stratego/04-project-development/06-testing-verification/", "/docs-stratego/04-project-development/06-testing-verification/test-cases/", "/docs-stratego/04-project-development/06-testing-verification/test-plan/", "/docs-stratego/04-project-development/06-testing-verification/test-report/", "/docs-stratego/04-project-development/07-release-delivery/", "/docs-stratego/04-project-development/07-release-delivery/acceptance-checklist/", "/docs-stratego/04-project-development/07-release-delivery/delivery-package/", "/docs-stratego/04-project-development/07-release-delivery/release-notes/", "/docs-stratego/04-project-development/08-operations-maintenance/", "/docs-stratego/04-project-development/08-operations-maintenance/deployment-guide/", "/docs-stratego/04-project-development/08-operations-maintenance/operations-runbook/", "/docs-stratego/04-project-development/08-operations-maintenance/server-deployment-sop/", "/docs-stratego/04-project-development/09-evolution/", "/docs-stratego/04-project-development/09-evolution/retrospective/", "/docs-stratego/04-project-development/09-evolution/skill-evolution-plan/", "/docs-stratego/04-project-development/10-traceability/", "/docs-stratego/04-project-development/10-traceability/document-index/", "/docs-stratego/04-project-development/10-traceability/interface-matrix/", "/docs-stratego/04-project-development/10-traceability/requirements-matrix/", "/ride-loop/04-project-development/01-governance/", "/ride-loop/04-project-development/01-governance/project-charter/", "/ride-loop/04-project-development/02-discovery/", "/ride-loop/04-project-development/02-discovery/brainstorm-record/", "/ride-loop/04-project-development/02-discovery/input/", "/ride-loop/04-project-development/03-requirements/requirements-verification/", "/ride-loop/04-project-development/03-requirements/terminal-strategy/", "/ride-loop/04-project-development/04-design/", "/ride-loop/04-project-development/04-design/api-design/", "/ride-loop/04-project-development/04-design/backend-design/", "/ride-loop/04-project-development/04-design/database-design/", "/ride-loop/04-project-development/04-design/database-er-diagram/", "/ride-loop/04-project-development/04-design/design-token-component-spec/", "/ride-loop/04-project-development/04-design/design-tool-prompt-pack/", "/ride-loop/04-project-development/04-design/driver-heavy-app-spec/", "/ride-loop/04-project-development/04-design/driver-light-miniapp-spec/", "/ride-loop/04-project-development/04-design/module-boundaries/", "/ride-loop/04-project-development/04-design/openapi/", "/ride-loop/04-project-development/04-design/openapi/driver-heavy-app.openapi.yaml", "/ride-loop/04-project-development/04-design/openapi/driver-light-miniapp.openapi.yaml", "/ride-loop/04-project-development/04-design/openapi/ops-web.openapi.yaml", "/ride-loop/04-project-development/04-design/openapi/passenger-miniapp.openapi.yaml", "/ride-loop/04-project-development/04-design/ops-web-spec/", "/ride-loop/04-project-development/04-design/page-prompt-catalog/", "/ride-loop/04-project-development/04-design/system-architecture/", "/ride-loop/04-project-development/04-design/system-detailed-design/", "/ride-loop/04-project-development/04-design/technical-selection/", "/ride-loop/04-project-development/04-design/ui-page-detail-matrix/", "/ride-loop/04-project-development/04-design/ux-ui-design/", "/ride-loop/04-project-development/06-testing-verification/", "/ride-loop/04-project-development/06-testing-verification/test-plan/", "/ride-loop/04-project-development/07-release-delivery/", "/ride-loop/04-project-development/08-operations-maintenance/", "/ride-loop/04-project-development/08-operations-maintenance/deployment-guide/", "/ride-loop/04-project-development/09-evolution/", "/ride-loop/04-project-development/10-traceability/", "/ride-loop/04-project-development/10-traceability/requirements-matrix/", "/stratix/04-project-development/", "/stratix/04-project-development/01-governance/", "/stratix/04-project-development/01-governance/project-charter/", "/stratix/04-project-development/02-discovery/", "/stratix/04-project-development/02-discovery/brainstorm-record/", "/stratix/04-project-development/02-discovery/current-state-analysis/", "/stratix/04-project-development/02-discovery/input/", "/stratix/04-project-development/03-requirements/", "/stratix/04-project-development/03-requirements/prd/", "/stratix/04-project-development/03-requirements/requirements-analysis/", "/stratix/04-project-development/03-requirements/requirements-verification/", "/stratix/04-project-development/04-design/", "/stratix/04-project-development/04-design/api-design/", "/stratix/04-project-development/04-design/backend-design/", "/stratix/04-project-development/04-design/module-boundaries/", "/stratix/04-project-development/04-design/system-architecture/", "/stratix/04-project-development/04-design/technical-selection/", "/stratix/04-project-development/05-development-process/", "/stratix/04-project-development/05-development-process/implementation-plan/", "/stratix/04-project-development/06-testing-verification/", "/stratix/04-project-development/06-testing-verification/test-plan/", "/stratix/04-project-development/07-release-delivery/", "/stratix/04-project-development/07-release-delivery/release-notes/", "/stratix/04-project-development/08-operations-maintenance/", "/stratix/04-project-development/08-operations-maintenance/deployment-guide/", "/stratix/04-project-development/09-evolution/", "/stratix/04-project-development/10-traceability/", "/stratix/04-project-development/10-traceability/requirements-matrix/"]);

let authModal = null;
let authFrame = null;
let authPollTimer = null;
let authPollBusy = false;
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

function stopAuthPolling() {
  if (authPollTimer) {
    window.clearInterval(authPollTimer);
    authPollTimer = null;
  }
}

function closeAuthModal() {
  stopAuthPolling();
  pendingTargetUrl = "";
  if (authFrame) {
    authFrame.src = "about:blank";
  }
  if (!authModal) {
    return;
  }
  authModal.classList.remove("is-open");
  document.body.classList.remove("docs-auth-modal-open");
}

function ensureAuthModal() {
  if (authModal) {
    return authModal;
  }

  authModal = document.createElement("div");
  authModal.className = "docs-auth-modal";
  authModal.innerHTML = `
    <div class="docs-auth-modal__dialog" role="dialog" aria-modal="true" aria-label="受保护文档登录">
      <iframe class="docs-auth-modal__frame" title="Casdoor 登录" src="about:blank"></iframe>
    </div>
  `;

  authFrame = authModal.querySelector(".docs-auth-modal__frame");
  authModal.addEventListener("click", (event) => {
    if (event.target === authModal) {
      closeAuthModal();
    }
  });
  document.body.appendChild(authModal);
  return authModal;
}

function openAuthModal(targetUrl) {
  ensureAuthModal();
  pendingTargetUrl = targetUrl;
  authModal.classList.add("is-open");
  document.body.classList.add("docs-auth-modal-open");
}

function beginAuthFlow() {
  if (!pendingTargetUrl || !authFrame) {
    return;
  }

  const signInUrl = `/oauth2/sign_in?rd=${encodeURIComponent(pendingTargetUrl)}`;
  authFrame.src = signInUrl;
  stopAuthPolling();
  authPollTimer = window.setInterval(async () => {
    if (authPollBusy || !pendingTargetUrl) {
      return;
    }
    authPollBusy = true;
    try {
      const authenticated = await checkAuthStatus();
      if (authenticated) {
        stopAuthPolling();
        const targetUrl = pendingTargetUrl;
        closeAuthModal();
        window.location.assign(targetUrl);
        return;
      }
    } finally {
      authPollBusy = false;
    }
  }, 1000);
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
  const targetUrl = anchor.href;
  const authenticated = await checkAuthStatus();
  if (authenticated) {
    window.location.assign(targetUrl);
    return;
  }
  openAuthModal(targetUrl);
  beginAuthFlow();
}

document$.subscribe(() => {
  ensureAuthModal();
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

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && authModal?.classList.contains("is-open")) {
      closeAuthModal();
    }
  });
});
