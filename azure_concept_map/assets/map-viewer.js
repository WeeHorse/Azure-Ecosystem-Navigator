(() => {
  "use strict";

  const svgHost = document.getElementById("svg-host");
  const modal = document.getElementById("concept-modal");
  const modalPanel = modal.querySelector(".modal-panel");
  const modalTitle = document.getElementById("modal-title");
  const modalContent = document.getElementById("modal-content");
  const closeButton = document.getElementById("modal-close");
  const scrollFrame = document.getElementById("scroll-frame");
  const zoomInButton = document.getElementById("zoom-in");
  const zoomOutButton = document.getElementById("zoom-out");
  const zoomResetButton = document.getElementById("zoom-reset");
  const XLINK_NS = "http://www.w3.org/1999/xlink";

  let lastFocusedElement = null;
  let currentZoom = 1;
  let fitScale = 1;
  let baseWidth = 0;

  function sanitizeFragment(fragmentRoot) {
    const blocked = fragmentRoot.querySelectorAll("script, iframe, object, embed, link[rel='import']");
    blocked.forEach((node) => node.remove());

    const allNodes = fragmentRoot.querySelectorAll("*");
    allNodes.forEach((node) => {
      for (const attr of [...node.attributes]) {
        const name = attr.name.toLowerCase();
        const value = (attr.value || "").trim().toLowerCase();
        if (name.startsWith("on")) {
          node.removeAttribute(attr.name);
        }
        if ((name === "href" || name === "src") && value.startsWith("javascript:")) {
          node.removeAttribute(attr.name);
        }
      }
    });
  }

  async function loadSvg() {
    const response = await fetch("../azure-concepts-clickable.svg", { credentials: "same-origin" });
    if (!response.ok) {
      throw new Error(`Could not load map SVG (${response.status}).`);
    }

    const rawSvg = await response.text();
    svgHost.innerHTML = rawSvg;

    const svg = svgHost.querySelector("svg");
    if (!svg) {
      throw new Error("Map SVG did not contain an <svg> element.");
    }

    svg.setAttribute("aria-label", "Azure concept map overview");
    svg.setAttribute("role", "img");

    const links = svg.querySelectorAll("a");
    links.forEach((linkNode) => {
      const slug = slugFromLink(linkNode);
      if (slug) {
        // Normalize link destinations so non-JS fallback does not resolve to html/html/*.html.
        linkNode.setAttribute("href", `./${slug}.html`);
        linkNode.setAttributeNS(XLINK_NS, "xlink:href", `./${slug}.html`);
      }
      const title = linkNode.getAttribute("xlink:title") || linkNode.getAttribute("title");
      if (title) {
        linkNode.setAttribute("aria-label", `${title} concept`);
      }
      linkNode.style.cursor = "pointer";
    });

    svgHost.addEventListener("click", handleSvgClick);

    setupZoom(svg);
  }

  function resolvedSvgWidth(svg) {
    if (svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width) {
      return svg.viewBox.baseVal.width;
    }
    const parsed = Number.parseFloat(svg.getAttribute("width") || "0");
    if (Number.isFinite(parsed) && parsed > 0) {
      return parsed;
    }
    return Math.max(1, svg.getBoundingClientRect().width);
  }

  function applyZoom(svg) {
    const scale = fitScale * currentZoom;
    const scaledWidth = Math.max(1, baseWidth * scale);
    svg.style.width = `${scaledWidth}px`;
    svg.style.height = "auto";
    zoomOutButton.disabled = currentZoom <= 0.401;
    zoomInButton.disabled = currentZoom >= 5.999;
    zoomResetButton.disabled = Math.abs(currentZoom - 1) < 0.001;
  }

  function updateFitScale(svg) {
    const frameWidth = Math.max(1, scrollFrame.clientWidth - 24);
    fitScale = frameWidth / baseWidth;
    applyZoom(svg);
  }

  function setupZoom(svg) {
    baseWidth = resolvedSvgWidth(svg);
    currentZoom = 1;
    updateFitScale(svg);

    zoomInButton.addEventListener("click", () => {
      currentZoom = Math.min(currentZoom * 1.2, 6);
      applyZoom(svg);
    });

    zoomOutButton.addEventListener("click", () => {
      currentZoom = Math.max(currentZoom / 1.2, 0.4);
      applyZoom(svg);
    });

    zoomResetButton.addEventListener("click", () => {
      currentZoom = 1;
      applyZoom(svg);
    });

    window.addEventListener("resize", () => updateFitScale(svg));
  }

  function linkHref(linkNode) {
    return linkNode.getAttribute("href") || linkNode.getAttribute("xlink:href") || linkNode.getAttributeNS(XLINK_NS, "href") || "";
  }

  function slugFromLink(linkNode) {
    const href = linkHref(linkNode);
    const match = href.match(/([^/]+)\.html$/i);
    return match ? match[1] : null;
  }

  async function handleSvgClick(event) {
    const linkNode = event.target.closest("a");
    if (!linkNode || !svgHost.contains(linkNode)) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();

    const slug = slugFromLink(linkNode);
    if (!slug) {
      return;
    }

    const title = linkNode.getAttribute("xlink:title") || slug.replace(/-/g, " ");
    await openConcept(slug, title);
  }

  async function openConcept(slug, title) {
    modalTitle.textContent = title;
    modalContent.innerHTML = '<p class="loading">Loading concept...</p>';
    lastFocusedElement = document.activeElement;
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");

    try {
      const response = await fetch(`./${slug}.html`, { credentials: "same-origin" });
      if (!response.ok) {
        throw new Error(`Could not load ${slug}.html (${response.status}).`);
      }

      const html = await response.text();
      const parsed = new DOMParser().parseFromString(html, "text/html");
      const body = parsed.body;

      const nodes = [...body.children].filter((el) => {
        if (el.tagName === "P") {
          const backLink = el.querySelector('a[href="index.html"]');
          if (backLink) {
            return false;
          }
        }
        return true;
      });

      const wrapper = document.createElement("div");
      nodes.forEach((node) => wrapper.appendChild(node.cloneNode(true)));
      sanitizeFragment(wrapper);

      wrapper.querySelectorAll("a").forEach((anchor) => {
        const href = anchor.getAttribute("href") || "";
        if (href === "index.html") {
          anchor.setAttribute("href", "#");
          anchor.addEventListener("click", (evt) => {
            evt.preventDefault();
            closeModal();
          });
          return;
        }

        if (/^[^#].*\.html$/i.test(href) && !/^https?:/i.test(href)) {
          anchor.setAttribute("target", "_blank");
          anchor.setAttribute("rel", "noopener noreferrer");
          return;
        }

        if (/^https?:/i.test(href)) {
          anchor.setAttribute("target", "_blank");
          anchor.setAttribute("rel", "noopener noreferrer");
        }
      });

      modalContent.innerHTML = "";
      modalContent.appendChild(wrapper);
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

  loadSvg().catch((error) => {
    svgHost.innerHTML = `<p class="loading">${error.message}</p>`;
  });
})();
