# Supplemental Update #3 verification report

## Build status

Applied via `_rebuild_supplemental3.py` (fix trailing `SCRIPT` artefact removed) plus manual HTML/CSS passes: FAQ WordPress cross-reference (Section 8), Section 8/9 markup indentation, print CSS for landscape sitemap, executive summary, TOC, tables, staircase, photography callout, and lead hero block.

## Page count

**Not measured in this environment.** Print to PDF from Chrome (or similar) and record:

- Cover (unnumbered)
- Body: target roughly 28–32 portrait pages plus **one** `letter landscape` page for the Section 7 sitemap block (`sitemap-landscape-page`)
- Appendices A–C

Chromium may vary on `@page landscape` support; if the sitemap does not land on a landscape spread, use the browser’s print dialog “Landscape” for that range or export the sitemap page separately.

## Compression / human review

- **Section 5 case studies** shortened in-script; confirm tone and PG&E / BrightWork nuance still match how MKTNG sells the firm.
- **Section 8 technology** no longer contains the long HubSpot/Salesflow paragraph from the prior build; CRM positioning is summarized in Architectural Notes and lead-gen/CRM copy in Section 9. Legal or sales may want that nuance reintroduced beside the table if needed.

## Cross-references

Spot-checked after resequence:

- Executive summary → Section 3 pricing; Appendices B & C note present.
- Investment includes-notes → Section 2 engagement detail.
- Approach → Section 7 architecture.
- Content cadence → Section 2 attention levels.
- Metrics baseline → Section 10.
- FAQ pricing → Section 3; AEO → Section 10; WordPress → Section 8.
- Appendix B quick reference AEO line → Section 10.
- Appendix C compliance table uses `qr-sec-num` remap to new section numbers.

Re-scan if you edit any section numbers again.

## Placeholders still for MKTNG

- `[FOUNDATION_BUILD_FLOOR]`, `[PARTNERSHIP_ANNUAL_FLOOR]` (executive summary; `ph-fee` / italic berry styling)
- `[FOUNDATION_BUILD]`, `[ENGINE_BUILD]`, `[PARTNERSHIP_BUILD]`, retainers in pricing and engagement table
- `[PHOTOGRAPHY]` in photography callout; optional add-ons still use `$[PHOTO]` etc.

## Script note

Do **not** re-run `_rebuild_supplemental3.py` against this file without restoring the pre-rebuild `document-main` from git: it expects the original section order and front matter.
