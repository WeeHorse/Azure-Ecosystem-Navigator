import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

(() => {
  "use strict";

  const svgHost = document.getElementById("svg-host");
  const modal = document.getElementById("concept-modal");
  const modalPanel = modal.querySelector(".modal-panel");
  const modalTitle = document.getElementById("modal-title");
  const modalContent = document.getElementById("modal-content");
  const closeButton = document.getElementById("modal-close");
  const XLINK_NS = "http://www.w3.org/1999/xlink";

  let lastFocusedElement = null;

  function escapeHtml(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function inlineMarkdownToHtml(text) {
    const escaped = escapeHtml(text);
    const withMarkdownLinks = escaped.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, href) => {
      const safeHref = href.trim();
      const isOffsite = /^https?:/i.test(safeHref);
      const attrs = isOffsite ? ' target="_blank" rel="noopener noreferrer"' : "";
      return `<a href="${safeHref}"${attrs}>${label}</a>`;
    });

    // Autolink plain URLs (common in these concept cards).
    return withMarkdownLinks.replace(/(^|\s)(https?:\/\/[^\s<]+)/g, (match, lead, url) => {
      return `${lead}<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
    });
  }

  function markdownToHtml(markdown) {
    const lines = markdown.split(/\r?\n/);
    const parts = [];
    let inList = false;

    for (const line of lines) {
      const trimmed = line.trim();

      if (!trimmed) {
        if (inList) {
          parts.push("</ul>");
          inList = false;
        }
        continue;
      }

      if (trimmed.startsWith("# ")) {
        if (inList) {
          parts.push("</ul>");
          inList = false;
        }
        parts.push(`<h1>${inlineMarkdownToHtml(trimmed.slice(2))}</h1>`);
        continue;
      }

      if (trimmed.startsWith("## ")) {
        if (inList) {
          parts.push("</ul>");
          inList = false;
        }
        parts.push(`<h2>${inlineMarkdownToHtml(trimmed.slice(3))}</h2>`);
        continue;
      }

      if (trimmed.startsWith("- ")) {
        if (!inList) {
          parts.push("<ul>");
          inList = true;
        }
        parts.push(`<li>${inlineMarkdownToHtml(trimmed.slice(2))}</li>`);
        continue;
      }

      if (inList) {
        parts.push("</ul>");
        inList = false;
      }
      parts.push(`<p>${inlineMarkdownToHtml(trimmed)}</p>`);
    }

    if (inList) {
      parts.push("</ul>");
    }

    return parts.join("\n");
  }

  function mermaidSourceFromMarkdown(content) {
    const match = content.match(/```mermaid\n([\s\S]*?)```/);
    if (!match) {
      throw new Error("Could not find Mermaid block in diagram.md.");
    }
    return match[1].trim();
  }

  function conceptPathFromHref(href) {
    const match = href.match(/concepts\/([^./]+)\.md$/i);
    return match ? `./concepts/${match[1]}.md` : null;
  }

  function linkHref(linkNode) {
    return linkNode.getAttribute("href")
      || linkNode.getAttribute("xlink:href")
      || linkNode.getAttributeNS(XLINK_NS, "href")
      || "";
  }

  function conceptTitleFromPath(path) {
    const slug = path.replace("./concepts/", "").replace(".md", "");
    return slug
      .split("-")
      .map((part) => part ? part[0].toUpperCase() + part.slice(1) : part)
      .join(" ");
  }

  async function loadSecurityMap() {
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      flowchart: { useMaxWidth: false, htmlLabels: false }
    });

    const diagramResponse = await fetch("./diagram.md", { credentials: "same-origin" });
    if (!diagramResponse.ok) {
      throw new Error(`Could not load diagram.md (${diagramResponse.status}).`);
    }

    const markdown = await diagramResponse.text();
    const source = mermaidSourceFromMarkdown(markdown);
    const { svg: svgMarkup } = await mermaid.render("security-map", source);

    svgHost.innerHTML = svgMarkup;

    const svg = svgHost.querySelector("svg");
    if (!svg) {
      throw new Error("Mermaid did not produce an SVG output.");
    }

    svg.setAttribute("aria-label", "Azure security concept map overview");
    svg.setAttribute("role", "img");

    const links = svg.querySelectorAll("a");
    links.forEach((linkNode) => {
      const href = linkHref(linkNode);
      const conceptPath = conceptPathFromHref(href);
      if (!conceptPath) {
        return;
      }

      // Persist concept target for JS and neutralize native file navigation.
      linkNode.setAttribute("data-concept-path", conceptPath);
      linkNode.setAttribute("data-concept-title", conceptTitleFromPath(conceptPath));
      linkNode.setAttribute("href", "#");
      linkNode.setAttribute("xlink:href", "#");
      linkNode.setAttributeNS(XLINK_NS, "xlink:href", "#");
    });

    svgHost.addEventListener("click", handleSvgClick, true);
  }

  async function handleSvgClick(event) {
    const linkNode = event.target.closest("a");
    if (!linkNode || !svgHost.contains(linkNode)) {
      return;
    }

    // Never let browser perform native navigation/download from SVG anchors.
    event.preventDefault();
    event.stopPropagation();

    const conceptPath = linkNode.getAttribute("data-concept-path") || "";
    if (!conceptPath) {
      return;
    }

    const fallbackTitle = linkNode.getAttribute("data-concept-title") || conceptTitleFromPath(conceptPath);

    const titleNode = linkNode.querySelector("title");
    const title = (titleNode ? titleNode.textContent : "") || fallbackTitle;
    await openConcept(conceptPath, title);
  }

  async function openConcept(path, title) {
    modalTitle.textContent = title;
    modalContent.innerHTML = '<p class="loading">Loading concept...</p>';
    lastFocusedElement = document.activeElement;
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");

    try {
      const response = await fetch(path, { credentials: "same-origin" });
      if (!response.ok) {
        throw new Error(`Could not load ${path} (${response.status}).`);
      }

      const markdown = await response.text();
      modalContent.innerHTML = markdownToHtml(markdown);
      modalPanel.focus();
    } catch (error) {
      modalContent.innerHTML = `<p class="loading">${error.message}</p>`;
      modalPanel.focus();
    }
  }

  function closeModal() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
      lastFocusedElement.focus();
    }
  }

  document.addEventListener("click", (event) => {
    if (event.target.closest("[data-close-modal='true']") || event.target === closeButton) {
      closeModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (!modal.classList.contains("is-open")) {
      return;
    }

    if (event.key === "Escape") {
      event.preventDefault();
      closeModal();
    }
  });

  loadSecurityMap().catch((error) => {
    svgHost.innerHTML = `<p class="loading">${error.message}</p>`;
  });
})();
