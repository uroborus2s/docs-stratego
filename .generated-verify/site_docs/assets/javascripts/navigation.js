const PROJECT_TAB_MENUS = {"章略·墨衡": [{"title": "简介", "url": "/docs-stratego/", "kind": "section"}, {"title": "入门说明", "url": "/docs-stratego/01-getting-started/", "kind": "section"}, {"title": "用户指南", "url": "/docs-stratego/02-user-guide/", "kind": "section"}, {"title": "项目开发文档（内）", "url": "/docs-stratego/04-project-development/", "kind": "section"}, {"title": "GitHub 仓库", "url": "https://github.com/uroborus2s/docs-stratego", "kind": "external"}], "山海工枢": [{"title": "简介", "url": "/shanforge/", "kind": "section"}, {"title": "入门说明", "url": "/shanforge/01-getting-started/", "kind": "section"}, {"title": "用户指南", "url": "/shanforge/02-user-guide/", "kind": "section"}, {"title": "开发者指南", "url": "/shanforge/03-developer-guide/", "kind": "section"}, {"title": "项目开发文档（内）", "url": "/shanforge/04-project-development/", "kind": "section"}, {"title": "GitHub 仓库", "url": "https://github.com/uroborus2s/shanforge", "kind": "external"}], "蛛行演略": [{"title": "简介", "url": "/crawler4j/", "kind": "section"}, {"title": "入门说明", "url": "/crawler4j/01-getting-started/", "kind": "section"}, {"title": "用户指南", "url": "/crawler4j/02-user-guide/", "kind": "section"}, {"title": "开发者指南", "url": "/crawler4j/03-developer-guide/", "kind": "section"}, {"title": "项目开发文档（内）", "url": "/crawler4j/04-project-development/", "kind": "section"}, {"title": "GitHub 仓库", "url": "https://github.com/uroborus2s/crawler4j", "kind": "external"}], "灵枢枢机": [{"title": "简介", "url": "/stratix/", "kind": "section"}, {"title": "入门说明", "url": "/stratix/01-getting-started/", "kind": "section"}, {"title": "用户指南", "url": "/stratix/02-user-guide/", "kind": "section"}, {"title": "开发者指南", "url": "/stratix/03-developer-guide/", "kind": "section"}, {"title": "项目开发文档（内）", "url": "/stratix/04-project-development/", "kind": "section"}, {"title": "GitHub 仓库", "url": "https://github.com/uroborus2s/obsync-root", "kind": "external"}], "千乘坊": [{"title": "简介", "url": "/ride-loop/", "kind": "section"}, {"title": "入门说明", "url": "/ride-loop/01-getting-started/", "kind": "section"}, {"title": "用户指南", "url": "/ride-loop/02-user-guide/", "kind": "section"}, {"title": "项目开发文档（内）", "url": "/ride-loop/04-project-development/", "kind": "section"}, {"title": "GitHub 仓库", "url": "https://github.com/uroborus2s/ride-loop", "kind": "external"}]};

function closeProjectMenus(root = document) {
  root.querySelectorAll(".docs-tab-dropdown.is-open").forEach((menu) => {
    menu.classList.remove("is-open");
    const ownerId = menu.getAttribute("data-owner-id");
    if (ownerId) {
      const owner = root.getElementById(ownerId);
      if (owner) {
        owner.setAttribute("aria-expanded", "false");
      }
    }
  });
}

function openProjectMenu(anchor, dropdown) {
  closeProjectMenus(document);
  dropdown.classList.add("is-open");
  anchor.setAttribute("aria-expanded", "true");
}

function appendMenuGroup(container, label) {
  const group = document.createElement("div");
  group.className = "docs-tab-dropdown__group";
  group.textContent = label;
  container.appendChild(group);
}

function appendMenuLinks(container, items) {
  let lastKind = "";
  items.forEach((item) => {
    if (item.kind !== lastKind) {
      appendMenuGroup(container, item.kind === "external" ? "仓库链接" : "文档分区");
      lastKind = item.kind;
    }
    const link = document.createElement("a");
    link.className = "docs-tab-dropdown__link";
    if (item.kind === "external") {
      link.classList.add("docs-tab-dropdown__link--external");
    }
    link.href = item.url;
    link.textContent = item.title;
    link.setAttribute("role", "menuitem");
    if (item.url.startsWith("http")) {
      link.target = "_blank";
      link.rel = "noreferrer";
    }
    container.appendChild(link);
  });
}

function simplifyPrimarySidebar() {
  const activeProjects = document.querySelectorAll(
    ".md-nav--primary > .md-nav__list > .md-nav__item--section.md-nav__item--active"
  );

  activeProjects.forEach((activeProject) => {
    if (activeProject.dataset.docsSidebarSimplified === "true") {
      return;
    }
    activeProject.dataset.docsSidebarSimplified = "true";

    const levelOneList = activeProject.querySelector(":scope > nav.md-nav > ul.md-nav__list");
    if (!levelOneList) {
      return;
    }

    const sectionItems = Array.from(levelOneList.children).filter(
      (item) => item.classList.contains("md-nav__item--nested")
    );
    if (!sectionItems.length) {
      return;
    }

    const activeSection =
      sectionItems.find(
        (item) =>
          item.classList.contains("md-nav__item--active") ||
          item.querySelector(":scope .md-nav__link--active, :scope .md-nav__item--active")
      ) || sectionItems[0];

    const nestedList = activeSection.querySelector(":scope > nav.md-nav > ul.md-nav__list");
    if (!nestedList) {
      return;
    }

    const sectionTitle = activeSection.querySelector(":scope > label .md-ellipsis")?.textContent?.trim() || "";
    const nestedChildren = Array.from(nestedList.children);
    const sectionOverview = nestedChildren.find(
      (child) =>
        child.classList.contains("md-nav__item") && !child.classList.contains("md-nav__item--nested")
    );
    if (sectionOverview) {
      const overviewLabels = sectionOverview.querySelectorAll(
        ":scope > .md-nav__link .md-ellipsis, :scope > a.md-nav__link .md-ellipsis"
      );
      if (overviewLabels.length && sectionTitle) {
        overviewLabels.forEach((overviewLabel) => {
          overviewLabel.textContent = sectionTitle;
        });
      }
    }

    levelOneList.innerHTML = "";
    nestedChildren.forEach((child) => {
      levelOneList.appendChild(child);
    });
  });
}

document$.subscribe(() => {
  closeProjectMenus();
  simplifyPrimarySidebar();
  const tabAnchors = document.querySelectorAll(".md-tabs__list > .md-tabs__item > .md-tabs__link");
  tabAnchors.forEach((anchor, index) => {
    const title = anchor.textContent?.trim() || "";
    const items = PROJECT_TAB_MENUS[title];
    if (!items || !items.length) {
      return;
    }

    const parent = anchor.parentElement;
    if (!parent || parent.dataset.docsMenuBound === "true") {
      return;
    }
    parent.dataset.docsMenuBound = "true";
    const menuToggle = anchor.cloneNode(true);
    menuToggle.classList.add("docs-tab-toggle");
    menuToggle.removeAttribute("href");
    menuToggle.setAttribute("aria-haspopup", "true");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("role", "button");
    menuToggle.setAttribute("tabindex", "0");
    menuToggle.setAttribute("aria-label", `${title} 菜单`);
    menuToggle.id = anchor.id || `docs-tab-toggle-${index}`;
    parent.replaceChild(menuToggle, anchor);

    const dropdown = document.createElement("div");
    dropdown.className = "docs-tab-dropdown";
    dropdown.setAttribute("role", "menu");
    dropdown.setAttribute("data-owner-id", menuToggle.id);
    appendMenuLinks(dropdown, items);

    parent.appendChild(dropdown);
    menuToggle.addEventListener("click", (event) => {
      event.preventDefault();
      const opened = dropdown.classList.contains("is-open");
      if (!opened) {
        openProjectMenu(menuToggle, dropdown);
      } else {
        closeProjectMenus(document);
      }
    });

    menuToggle.addEventListener("keydown", (event) => {
      if (!(event.key === "Enter" || event.key === " " || event.key === "ArrowDown")) {
        if (event.key === "Escape") {
          closeProjectMenus(document);
        }
        return;
      }
      event.preventDefault();
      openProjectMenu(menuToggle, dropdown);
      dropdown.querySelector(".docs-tab-dropdown__link")?.focus();
    });
  });

  if (window.__docsProjectMenuHandlersBound) {
    return;
  }
  window.__docsProjectMenuHandlersBound = true;

  document.addEventListener("click", (event) => {
    if (!(event.target instanceof Element) || !event.target.closest(".md-tabs__item")) {
      closeProjectMenus(document);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeProjectMenus(document);
    }
  });
});
