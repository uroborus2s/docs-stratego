const SCALAR_CDN_URL = "https://cdn.jsdelivr.net/npm/@scalar/api-reference";

let scalarScriptPromise = null;
let scalarMountedReferences = [];

function loadScalarScript() {
  if (window.Scalar && typeof window.Scalar.createApiReference === "function") {
    return Promise.resolve(window.Scalar);
  }
  if (scalarScriptPromise) {
    return scalarScriptPromise;
  }
  scalarScriptPromise = new Promise((resolve, reject) => {
    const existing = document.querySelector('script[data-docs-scalar-cdn="true"]');
    if (existing) {
      existing.addEventListener("load", () => resolve(window.Scalar), { once: true });
      existing.addEventListener("error", () => reject(new Error("Scalar CDN load failed")), { once: true });
      return;
    }
    const script = document.createElement("script");
    script.src = SCALAR_CDN_URL;
    script.async = true;
    script.dataset.docsScalarCdn = "true";
    script.addEventListener("load", () => resolve(window.Scalar), { once: true });
    script.addEventListener("error", () => reject(new Error("Scalar CDN load failed")), { once: true });
    document.head.appendChild(script);
  });
  return scalarScriptPromise;
}

function resolveScalarTheme() {
  const scheme = document.body?.getAttribute("data-md-color-scheme") || "";
  return scheme === "slate" ? "deepSpace" : "default";
}

function clearMountedScalarReferences() {
  scalarMountedReferences.forEach((instance) => {
    if (instance && typeof instance.destroy === "function") {
      try {
        instance.destroy();
      } catch (_error) {
        // ignore Scalar cleanup errors
      }
    }
  });
  scalarMountedReferences = [];
}

function renderScalarError(container, specUrl) {
  container.classList.remove("is-loading");
  container.classList.add("is-error");
  container.innerHTML = `
    <div class="docs-openapi-scalar__error">
      <p>Scalar API Reference 加载失败。</p>
      <p><a href="${specUrl}">打开原始契约</a></p>
    </div>
  `;
}

async function mountScalarReferences(root = document) {
  const containers = Array.from(root.querySelectorAll(".docs-openapi-scalar[data-openapi-url]"));
  if (!containers.length) {
    clearMountedScalarReferences();
    return;
  }
  clearMountedScalarReferences();
  let scalarApi = null;
  try {
    scalarApi = await loadScalarScript();
  } catch (_error) {
    containers.forEach((container) => renderScalarError(container, container.dataset.openapiUrl || "#"));
    return;
  }
  if (!scalarApi || typeof scalarApi.createApiReference !== "function") {
    containers.forEach((container) => renderScalarError(container, container.dataset.openapiUrl || "#"));
    return;
  }
  containers.forEach((container) => {
    const specUrl = container.dataset.openapiUrl;
    if (!specUrl || !container.id) {
      return;
    }
    container.classList.remove("is-loading", "is-error");
    container.innerHTML = "";
    try {
      const instance = scalarApi.createApiReference(`#${container.id}`, {
        url: specUrl,
        theme: resolveScalarTheme(),
        layout: "modern",
        showSidebar: true,
        showDeveloperTools: "never",
        withDefaultFonts: false,
      });
      scalarMountedReferences.push(instance);
    } catch (_error) {
      renderScalarError(container, specUrl);
    }
  });
}

document$.subscribe(() => {
  mountScalarReferences();
});
