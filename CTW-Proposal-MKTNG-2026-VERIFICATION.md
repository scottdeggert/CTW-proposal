# CTW Proposal Build Verification Report

Date: May 5, 2026 (updated after supplemental packet)  
Deliverable: `CTW-Proposal-MKTNG-2026.html`

## Page count estimate

Approximate `wc -w` on the HTML file: **14,760** words (includes markup noise). Rough print estimate ~**29–33** letter pages at ~450–500 words per page of body text, still inside the original **25–35** target depending on PDF engine.

## Supplemental updates applied (May 2026)

The following were merged into `CTW-Proposal-MKTNG-2026.html` per the supplemental instructions:

1. **Quick Reference Summary:** Added **RFP COMPLIANCE AUDIT** (structured two-column table with RFP section group headers). Closing line now reads **Sections 1 through 13** (was 1 through 12).
2. **Section 2:** Phase 5 references **Section 13** for quarterly business review alignment (was Section 12).
3. **Section 11:** Order is **Team → Work Samples → Case Studies → References**. Work sample screenshots use **paths relative to the HTML file**, e.g. `assets/screenshots/[filename].png`, so logos and screenshots resolve when opening `CTW-Proposal-MKTNG-2026.html` locally (`file://`) without relying on GitHub raw hosting. Ice Linen placeholders labeled **Screenshot pending** still appear on image error (inline script via `data-work-sample-img`).
4. **Section 12:** New **Success Metrics** section (verbatim from supplemental).
5. **Section 13:** Former **Approach to Partnership** content (unchanged prose), renumbered from Section 12.
6. **FAQ:** New entry **How will success be measured?** placed immediately before **Why are you recommending against WordPress?**

## Screenshots / assets for MKTNG to confirm

Repo paths under **`assets/screenshots/`** (referenced by the HTML):

- `moraga-screenshot.png` (present)
- `advocacy-chiefs-screenshot.png` (present)
- `mktng-screenshot.png` (present)

**Note:** Case study logos and MKTNG marks load from **`assets/logos/`** via the same relative pattern. Keep the HTML file at the repo root next to the `assets/` folder so paths resolve. If you distribute only the HTML without `assets/`, images will fall back to placeholders where wired.

Prior probes (historical): GitHub raw URLs failed when the repo was **private**. Keystatic’s former `keystatic.com/images/keystatic-logo.svg` URL returned **404** (vendor asset removed). Section 4 now uses **`assets/logos/keystatic-wordmark.svg`** (wordmark paths aligned with Thinkmill’s docs component). Astro uses **`assets/logos/astro-logo-dark.svg`** (official **logo on light** artwork; `astro-logo-light.svg` is for dark backgrounds only). Cloudflare SVG remains remote.

## Assets checked at build time (original packet)

Returned **404** in the original environment:

- `https://raw.githubusercontent.com/scottdeggert/CTW-proposal/main/assets/logos/MKTNG%20Logo-Black-Pink-Slash.png`
- `https://raw.githubusercontent.com/scottdeggert/CTW-proposal/main/assets/logos/advocacy-chiefs.png`
- `https://keystatic.com/images/keystatic-logo.svg` (obsolete path; replaced by local **`assets/logos/keystatic-wordmark.svg`**)

Returned **200**:

- `https://astro.build/assets/press/astro-logo-light.svg` (wrong variant for white backgrounds; proposal now ships **`assets/logos/astro-logo-dark.svg`** locally)
- `https://www.cloudflare.com/img/logo-cloudflare.svg`

## Sections that required drafting (original packet only)

Drafted earlier following voice rules:

1. Section 2: Approach and Methodology  
2. Section 3: Recommended Site Architecture  
3. Section 6: Content Engine body after the baseline exhibit  
4. Section 7: Trust, Compliance, and Accessibility  
5. Section 10: Pricing framing paragraph  

**Supplemental:** Success Metrics, Work Samples, References, Compliance Audit table, and FAQ success question were supplied **verbatim** in the supplemental packet (no paraphrase).

## Voice rule validation (supplemental)

- **Em dash (`—`):** Still present only in the Quick Reference **ALIGNMENT WITH CTW'S RFP OBJECTIVES** lines (original immutable packet block). None added in supplemental verbatim blocks checked by scan.
- **Banned vocabulary:** Spot-checked supplemental verbatim blocks; no banned-list hits in Work Samples, References, Success Metrics, Compliance Audit rows, or the new FAQ answer.
- Verbatim West Biofuels case study still contains **groundbreaking** (original immutable prose).

## Structural verification checklist

- Section numbering: **11 Team → 12 Success Metrics → 13 Approach to Partnership → FAQ → Appendix A**
- Quick Reference includes compliance table and **Sections 1 through 13** closer.
- Section 11 contains Work Samples (with screenshot URLs + fallbacks), Case Studies, References.
- FAQ includes success measurement answer pointing to **Section 12**.
- Internal references updated where required (**Section 13** business reviews in Section 2).

## Fragment sync / regeneration note

`proposal-parts/frag02.html`, `frag11.html`, `frag12.html`, and `frag13.html` were **rewritten from the canonical `CTW-Proposal-MKTNG-2026.html`** after this supplemental merge.

`assemble_proposal.py` still expects a `<!-- PLACEHOLDER: ... -->` marker inside the main HTML file (removed once the proposal was inlined). **Do not rely on assemble without restoring that marker or editing the script.** To refresh fragments from the main file, reuse the small extraction snippet from the supplemental merge commit or split manually.

## Original deviations / implementation choices

1. Engagement modes cards and sitemap tree sit inside **SVG `foreignObject`** nodes for SVG-rooted PDF export.
2. **`@page` margin boxes** plus **fixed** running header/footer for Chromium-class print preview; **`counter(page)`** may still be empty in some browsers.
3. Inline `<script>` handles logo/footer fallbacks and **work sample screenshot** fallbacks (`data-work-sample-img`).
