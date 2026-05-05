#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "CTW-Proposal-MKTNG-2026.html"
NEEDLE = "<!-- PLACEHOLDER: sections 2 through appendix inserted by patch -->"


def main() -> None:
    parts = []
    for i in range(2, 15):
        parts.append((ROOT / "proposal-parts" / f"frag{i:02d}.html").read_text(encoding="utf-8"))
    insert = "\n".join(parts)
    text = MAIN.read_text(encoding="utf-8")
    if NEEDLE not in text:
        raise SystemExit(f"Missing placeholder marker in {MAIN}")
    text = text.replace(NEEDLE, insert)
    script = """<script>
(function () {
  document.querySelectorAll("[data-work-sample-img]").forEach(function (img) {
    img.addEventListener("error", function () {
      img.style.display = "none";
      var ph = img.parentElement && img.parentElement.querySelector("[data-work-sample-ph]");
      if (ph) ph.hidden = false;
    });
  });
  document.querySelectorAll(".running-foot-left img").forEach(function (img) {
    img.addEventListener("load", function () {
      var sib = img.nextElementSibling;
      if (sib && sib.getAttribute("data-foot-text") === "1") sib.style.display = "none";
    });
    img.addEventListener("error", function () {
      img.style.display = "none";
    });
  });
})();
</script>
"""
    text = text.replace("</body>", script + "\n</body>")
    MAIN.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
