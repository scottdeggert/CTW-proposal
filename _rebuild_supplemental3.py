#!/usr/bin/env python3
"""Rebuild document-main for CTW-Proposal Supplemental Update #3."""
import re

PATH = "/Users/scotteggert/Development/Cursor/CTW-proposal/CTW-Proposal-MKTNG-2026.html"

# Old proposal section number (pre-resequence) -> new number
OLD_TO_NEW_SEC = {
    1: 1,
    2: 6,
    3: 7,
    4: 8,
    5: 9,
    6: 10,
    7: 11,
    8: 2,
    9: 4,
    10: 3,
    11: 5,
    12: 12,
    13: 13,
}


def remap_qr_sec_spans(html: str) -> str:
    def sub(m: re.Match) -> str:
        n = int(m.group(1))
        return f'<span class="qr-sec-num">Section {OLD_TO_NEW_SEC[n]}</span>'

    return re.sub(r'<span class="qr-sec-num">Section (\d+)</span>', sub, html)


def extract_section(inner: str, sid: str) -> str:
    pat = rf'(<section[^>]*id="{re.escape(sid)}"[^>]*>.*?</section>)'
    m = re.search(pat, inner, re.DOTALL)
    if not m:
        raise ValueError(f"Missing {sid}")
    return m.group(1)


def replace_h1(section: str, num: int, title: str) -> str:
    section = re.sub(r'id="section-\d+"', f'id="section-{num}"', section, count=1)
    section = re.sub(
        r'<h1 class="major-section-title display">.*?</h1>',
        f'<h1 class="major-section-title display">Section {num}: {title}</h1>',
        section,
        count=1,
        flags=re.DOTALL,
    )
    return section


def strip_executive_and_quickref(inner: str) -> str:
    inner = re.sub(
        r"\s*<!-- Executive Summary -->.*?<!-- Section 1 -->",
        "\n\n    <!-- Section 1 -->",
        inner,
        count=1,
        flags=re.DOTALL,
    )
    return inner


def main():
    with open(PATH) as f:
        full = f.read()
    m = re.search(r'(<div class="document-main">)(.*)(</div>\s*\n\n<script>)', full, re.DOTALL)
    if not m:
        raise SystemExit("Could not find document-main")
    prefix, inner, suffix = m.group(1), m.group(2), m.group(3)

    s1 = extract_section(inner, "section-1")
    s2_approach = extract_section(inner, "section-2")
    s3_arch = extract_section(inner, "section-3")
    s4_tech = extract_section(inner, "section-4")
    s5_lead = extract_section(inner, "section-5")
    s6_content = extract_section(inner, "section-6")
    s7_trust = extract_section(inner, "section-7")
    s8_eng = extract_section(inner, "section-8")
    s9_time = extract_section(inner, "section-9")
    s10_price = extract_section(inner, "section-10")
    s11_team = extract_section(inner, "section-11")
    s12 = extract_section(inner, "section-12")
    s13 = extract_section(inner, "section-13")
    faq = extract_section(inner, "faq")
    app_a = extract_section(inner, "appendix-a")
    quick = extract_section(inner, "quick-reference-summary")

    # --- Quick reference split for Appendix B / C ---
    q_inner = re.search(
        r'(<section[^>]*id="quick-reference-summary"[^>]*>)(\s*<div class="quick-ref">)(.*?)(</div>\s*</section>)',
        quick,
        re.DOTALL,
    )
    if not q_inner:
        raise SystemExit("quick ref parse fail")
    qr_open, qr_div_open, qr_body, qr_close = q_inner.groups()
    # Remove compliance from qr_body
    qr_body_nc = re.sub(
        r'<div class="qr-label">RFP COMPLIANCE AUDIT</div>.*',
        "",
        qr_body,
        count=1,
        flags=re.DOTALL,
    )
    qr_body_nc = qr_body_nc.replace(
        "results in Section 6).",
        "results in Section 10).",
    )
    qr_body_nc = re.sub(
        r"\s*<p>Full detail on each item follows in Sections 1 through 13\.</p>\s*",
        "",
        qr_body_nc,
        count=1,
    )
    qr_body_nc = re.sub(
        r'^\s*<h2>QUICK REFERENCE SUMMARY</h2>\s*<p>This summary is structured for fast review by readers and AI assistants\. Full detail follows in subsequent sections\.</p>\s*',
        "",
        qr_body_nc,
        count=1,
        flags=re.DOTALL | re.MULTILINE,
    )
    compliance_block = re.search(
        r'(<div class="qr-label">RFP COMPLIANCE AUDIT</div>.*?)(?=<p>Full detail on each item|$)',
        qr_body,
        re.DOTALL,
    )
    if not compliance_block:
        raise SystemExit("compliance block missing")
    compliance_html = compliance_block.group(1)
    # compliance table only (starts after intro p)
    comp_match = re.search(
        r'(<p>This proposal is structured.*?</p>\s*)(<table class="qr-compliance-table">.*?</table>)',
        compliance_html,
        re.DOTALL,
    )
    if not comp_match:
        raise SystemExit("compliance table missing")
    comp_intro_app = """        <p>This appendix maps each requirement specified in CTW's Request for Proposal dated April 13, 2026 to the section in this proposal that addresses it.</p>
"""
    comp_table = remap_qr_sec_spans(comp_match.group(2))

    appendix_b = f"""    <section class="major-section section-anchor" id="appendix-b">
      <h1 class="major-section-title display">Appendix B: Quick Reference Summary</h1>
      <div class="quick-ref">
        <h2 class="display">APPENDIX B: QUICK REFERENCE SUMMARY</h2>
        <p>This appendix is structured for fast review by readers and AI assistants. It restates the key elements of the proposal in a structured format suitable for parsing, comparison, and rapid review.</p>
{qr_body_nc.strip()}
        <p>Full detail on each item appears in the body of the proposal.</p>
      </div>
    </section>

    <section class="major-section section-anchor" id="appendix-c">
      <h1 class="major-section-title display">Appendix C: RFP Compliance Matrix</h1>
      <div class="quick-ref">
        <h2 class="display">APPENDIX C: RFP COMPLIANCE MATRIX</h2>
{comp_intro_app}{comp_table}
      </div>
    </section>
"""

    # --- New executive summary (one page) ---
    exec_one = """    <section class="major-section no-break-before exec-summary-page section-anchor" id="executive-summary">
      <h1 class="exec-sum-head display">EXECUTIVE SUMMARY</h1>
      <p class="exec-sum-sub display">CTW has the right firm. The website should reflect it.</p>
      <p class="exec-sum-lead">The current site reflects a generalist compliance shop with sixty service pages and twenty-eight industries. The firm has moved past that. Advisory-led work with middle-market owners and CFOs through capital events is now the core. The website should be the next thing to catch up.</p>
      <p class="exec-sum-lead">We propose to close the gap in four weeks for the core build, twelve weeks for the full launch with original photography. Three engagement modes let CTW choose how deep the partnership goes.</p>
      <div class="exec-modes-row">
        <div class="exec-mode-card">
          <div class="exec-mode-name display">PATH FORWARD FOUNDATION</div>
          <p class="exec-mode-line">The website rebuild itself, ready in four weeks. Astro on Cloudflare with Keystatic, sub-one-second load times, AEO foundation built in, lead generation system operational at launch.</p>
        </div>
        <div class="exec-mode-card">
          <div class="exec-mode-name display">PATH FORWARD ENGINE</div>
          <p class="exec-mode-line">Foundation plus the content production system. Podcast launch, quarterly original research, monthly press releases, partner LinkedIn programs, AI Concierge.</p>
        </div>
        <div class="exec-mode-card">
          <div class="exec-mode-name display">PATH FORWARD PARTNERSHIP</div>
          <p class="exec-mode-line">Engine plus full ongoing program. Quarterly business reviews, AEO citation tracking, AI training for CTW staff, continuous content production.</p>
        </div>
      </div>
      <h2 class="exec-why-head display">WHY MKTNG</h2>
      <div class="exec-callouts">
        <p><span class="exec-lead-phrase">Speed.</span> Most rebuilds run six to nine months. Ours runs four weeks for the core.</p>
        <p><span class="exec-lead-phrase">AEO baseline already done.</span> We ran an analysis of how CTW currently appears across five major AI search engines as part of preparing this proposal. Findings inform the strategy. No other bidder will have done this work.</p>
        <p><span class="exec-lead-phrase">A senior team that stays.</span> Most of our client relationships run two to three years or longer. We are not a developer who hands off. We are a communications partner.</p>
      </div>
      <p class="exec-invest display">Investment ranges from <span class="ph-fee">[FOUNDATION_BUILD_FLOOR]</span> for Foundation through <span class="ph-fee">[PARTNERSHIP_ANNUAL_FLOOR]</span> annualized for Partnership, with detailed pricing in Section 3.</p>
      <p class="exec-close">We would welcome an interview the week of May 11.</p>
      <p class="exec-appendix-note">A structured Quick Reference Summary and complete RFP compliance matrix appear in Appendices B and C.</p>
    </section>

"""

    toc = """    <section class="major-section toc-page section-anchor" id="table-of-contents">
      <h1 class="major-section-title display">Table of Contents</h1>
      <ul class="toc-list">
        <li class="toc-item"><span class="toc-title display">EXECUTIVE SUMMARY</span></li>
        <li class="toc-item"><span class="toc-title display">SECTION 1: READING THE MOMENT</span><span class="toc-pnum"></span><p class="toc-abs">The current site reflects the firm CTW used to be. The opportunity is to make it reflect the firm CTW already is.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 2: ENGAGEMENT MODES</span><span class="toc-pnum"></span><p class="toc-abs">Three levels of partnership: Foundation, Engine, Partnership. Each is complete on its own.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 3: INVESTMENT</span><span class="toc-pnum"></span><p class="toc-abs">What each engagement mode costs and what is included.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 4: TIMELINE</span><span class="toc-pnum"></span><p class="toc-abs">Four weeks to core launch. Twelve weeks for the full launch with original photography.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 5: TEAM AND RELEVANT EXPERIENCE</span><span class="toc-pnum"></span><p class="toc-abs">Senior practitioners running the engagement, work samples, case studies, references.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 6: APPROACH AND METHODOLOGY</span><span class="toc-pnum"></span><p class="toc-abs">Five phases from brand sprint through stabilization. How we deliver in four weeks.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 7: RECOMMENDED SITE ARCHITECTURE</span><span class="toc-pnum"></span><p class="toc-abs">The proposed sitemap, with rationale for what stays, what consolidates, and what gets added.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 8: TECHNOLOGY RECOMMENDATIONS</span><span class="toc-pnum"></span><p class="toc-abs">Astro on Cloudflare with Keystatic. Why we are recommending against another WordPress build.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 9: LEAD GENERATION SYSTEM</span><span class="toc-pnum"></span><p class="toc-abs">Calendar booking, the Capital Event Readiness Assessment, calculators, AI Concierge, CRM-ready architecture.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 10: CONTENT ENGINE AND AEO STRATEGY</span><span class="toc-pnum"></span><p class="toc-abs">The system that fills the new site with work that compounds. Includes baseline AEO analysis already conducted.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 11: TRUST, COMPLIANCE, AND ACCESSIBILITY</span><span class="toc-pnum"></span><p class="toc-abs">WCAG 2.2 AA, security posture, privacy and data handling.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 12: SUCCESS METRICS</span><span class="toc-pnum"></span><p class="toc-abs">What we track, what we expect, how we report.</p></li>
        <li class="toc-item"><span class="toc-title display">SECTION 13: APPROACH TO PARTNERSHIP</span><span class="toc-pnum"></span><p class="toc-abs">What "long-term partner, not just a developer" actually looks like in practice.</p></li>
        <li class="toc-item"><span class="toc-title display">FREQUENTLY ASKED QUESTIONS</span><span class="toc-pnum"></span></li>
        <li class="toc-item"><span class="toc-title display">APPENDIX A: AEO BASELINE FULL DATA</span><span class="toc-pnum"></span></li>
        <li class="toc-item"><span class="toc-title display">APPENDIX B: QUICK REFERENCE SUMMARY (structured for AI review)</span><span class="toc-pnum"></span></li>
        <li class="toc-item"><span class="toc-title display">APPENDIX C: RFP COMPLIANCE MATRIX</span><span class="toc-pnum"></span></li>
      </ul>
    </section>

"""

    # --- Section 6 approach: fix cross refs ---
    s6_new = replace_h1(s2_approach, 6, "Approach and Methodology")
    s6_new = s6_new.replace(
        "Section 3 lays out the recommended site architecture",
        "Section 7 lays out the recommended site architecture",
    )
    s6_new = s6_new.replace(
        "quarterly business reviews run as outlined in Section 13",
        "quarterly business reviews run as outlined in Section 13",
    )

    # --- Section 7 architecture: landscape wrap for tree+budget only (intro + notes stay portrait) ---
    s7_new = replace_h1(s3_arch, 7, "Recommended Site Architecture")
    s7_new = s7_new.replace(
        "      </div>\n\n      <div class=\"sitemap-tree\"",
        "      </div>\n\n      <div class=\"sitemap-landscape-page\">\n      <div class=\"sitemap-tree\"",
        1,
    )
    s7_new = s7_new.replace(
        "      </div>\n\n      <h2 class=\"block-heading display\">NOTES ON THE ARCHITECTURE</h2>",
        "      </div>\n      </div>\n\n      <h2 class=\"block-heading display\">NOTES ON THE ARCHITECTURE</h2>",
        1,
    )

    # --- Section 8 tech: replace body between THE STACK close and NOTE ON WORDPRESS ---
    s8_new = replace_h1(s4_tech, 8, "Technology Recommendations")
    wp_note_match = re.search(
        r'(<h2 class="block-heading display">A NOTE ON WORDPRESS</h2>\s*<p>.*?</p>\s*)',
        s8_new,
        re.DOTALL,
    )
    if not wp_note_match:
        raise SystemExit("wordpress note missing")
    wp_block = wp_note_match.group(1)
    tech_intro = """      <h2 class="block-heading display">THE STACK</h2>
      <p>We recommend Astro for the website framework, Cloudflare for hosting and delivery, and Keystatic for content management. The combined stack gives CTW a site that loads in under one second on every page, costs a fraction of typical WordPress hosting to operate, and gives non-technical content stewards a clean interface for managing day-to-day content.</p>
      <p>The technology underneath matters less than what it produces. Here is what the difference looks like in practice.</p>
      <table class="tech-compare-table">
        <thead>
          <tr>
            <th scope="col" class="tc-dim">Dimension</th>
            <th scope="col" class="tc-wp">WordPress (Most Bidders Will Recommend)</th>
            <th scope="col" class="tc-rec">Astro on Cloudflare with Keystatic (Our Recommendation)</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Performance</td><td>5 to 10 seconds load time on mobile</td><td>Under 1 second on every page, every device</td></tr>
          <tr><td>Security surface area</td><td>Plugin ecosystem, PHP runtime, frequent vulnerabilities</td><td>Static HTML, no server runtime, Cloudflare WAF and DDoS built in</td></tr>
          <tr><td>Hosting cost</td><td>$1,500 to $6,000 per year</td><td>$0 to $300 per year</td></tr>
          <tr><td>Update workflow for non-developers</td><td>WordPress dashboard with plugin variation</td><td>Web-based editor that reads like Google Docs</td></tr>
          <tr><td>AEO readiness</td><td>Possible with significant configuration</td><td>Built into the architecture from day one</td></tr>
          <tr><td>Rebrand flexibility</td><td>Page-by-page edits required</td><td>Configuration change, propagates in under an hour</td></tr>
          <tr><td>Maintenance burden</td><td>Constant plugin updates, security patches</td><td>Effectively zero ongoing maintenance</td></tr>
          <tr><td>Time to launch</td><td>6 to 9 months typical for a rebuild</td><td>4 weeks for the core build</td></tr>
        </tbody>
      </table>
      <h2 class="block-heading display">ARCHITECTURAL NOTES</h2>
      <p>Performance comes from architecture, not optimization. Astro ships static HTML with near-zero JavaScript by default. Cloudflare delivers pages from edge servers physically close to every visitor. Speed is not a target we hit after months of tuning. It is the launch baseline.</p>
      <p>Security comes from absence. Static HTML pages cannot be SQL-injected. There is no PHP runtime to exploit. The plugin ecosystem that creates most WordPress security incidents simply does not exist in this stack.</p>
      <p>The CMS is built for non-developers. Keystatic looks and works like a modern document editor. Four content stewards at CTW will be trained in a single session, with a recorded video and a one-page reference guide for follow-up. Routine updates take minutes.</p>
      <p>The architecture is built rebrand-ready. Brand tokens (name, logo, color, typography) live as configuration. A future rebrand updates the token file and propagates across the site in under an hour. No page-by-page work required.</p>
      <p>The data layer is CRM-ready. Forms, calculators, the Capital Event Readiness Assessment, and calendar bookings all write to a unified event schema designed to map cleanly to HubSpot or Salesforce on day one.</p>
      <h2 class="block-heading display">WHY YOU WILL NOT BE STRANDED</h2>
      <p>CTW does not maintain an internal development team, and the proposal recommends moving off WordPress, which is the most common open-source platform on the market. The reasonable concern is platform lock-in: what happens if MKTNG goes away?</p>
      <p>The codebase is structured so any competent developer can pick it up and ship changes quickly. Astro is open source, fully documented, and has an active developer community. Keystatic is open source. Cloudflare hosting is portable to any other platform with minimal effort. The brand tokens, content schema, and component architecture are all standard patterns that any modern web developer will recognize.</p>
      <p>We do not build black boxes. We build systems CTW can hand to anyone, including us, and have them ship change quickly.</p>
"""
    s8_new = re.sub(
        r"<h2 class=\"block-heading display\">THE STACK</h2>.*?(?=<h2 class=\"block-heading display\">A NOTE ON WORDPRESS)",
        tech_intro,
        s8_new,
        count=1,
        flags=re.DOTALL,
    )

    # --- Section 9 leads ---
    cap_start = '<h2 class="block-heading display">2. CAPITAL EVENT READINESS ASSESSMENT</h2>'
    cap_end = '<h2 class="block-heading display">3. LIVE CALCULATORS</h2>'
    cs = s5_lead.find(cap_start)
    ce = s5_lead.find(cap_end)
    if cs < 0 or ce < 0:
        raise SystemExit("capital assessment block not found")
    capital_inner = s5_lead[cs + len(cap_start) : ce].strip()

    supporting = """
      <h3 class="sub-heading display">CALENDAR BOOKING WITH INTELLIGENT ROUTING</h3>
      <p>Calendly Teams integrated across the site. A short qualifying form (three questions: nature of inquiry, timeline, current client status) routes the prospect to the right partner or senior manager. Capital event inquiries reach the Capital Markets practice. Audit and tax inquiries route by service line. Existing clients route to a different path so current relationships do not enter the prospect funnel. Calendly integrates natively with Microsoft 365 and Outlook, which CTW's team is already using.</p>
      <h3 class="sub-heading display">LIVE CALCULATORS</h3>
      <p>Two embedded calculators ship with Foundation. The R&amp;D Tax Credit Estimator and the Cost Segregation Benefit Estimator. Both produce defensible estimates and capture email at the "send detailed report" step. Both rank well in AEO retrieval and convert at materially higher rates than average site traffic. Additional calculators (Section 199A, QoE preparation checklist, business valuation rough cut) are available as Phase 2 builds.</p>
      <h3 class="sub-heading display">AI CONCIERGE (Engine and Partnership tiers)</h3>
      <p>A conversational assistant trained on CTW's content. Answers prospect questions in CTW's voice, twenty-four hours a day. When intent is clear, hands off to calendar booking. Operating cost runs $50 to $200 per month. Most CPA firms in the region will not have this for at least two more years.</p>
      <h3 class="sub-heading display">CRM-READY ARCHITECTURE</h3>
      <p>Every form, calculator, assessment, and calendar booking writes to a unified event schema mapped for HubSpot or Salesforce. The day CTW signs the CRM engagement letter, migration takes days, not weeks. The lead generation system does not pause during CRM rollout. We recommend HubSpot for CTW's stage. Salesforce becomes the right call when the firm is ready to scale beyond fifty staff.</p>
"""

    s9_intro = """      <p>Most accounting firm websites are passive. Visitors arrive, browse, leave, and someone hopes they remember to follow up. CTW's site is built to work harder than that.</p>
      <p>The lead generation architecture has five components. One is the hero. The others are the supporting infrastructure that ensures every prospect interaction captures intent and routes correctly.</p>
      <h2 class="block-heading display">THE HERO: CAPITAL EVENT READINESS ASSESSMENT</h2>
      <div class="lead-hero-block">
"""
    s9_mid = """
      </div>
      <h2 class="block-heading display">THE SUPPORTING INFRASTRUCTURE</h2>
"""
    s9_body = s9_intro + capital_inner + s9_mid + supporting.strip() + "\n"

    s9_new = replace_h1(s5_lead, 9, "Lead Generation System")
    s9_new = re.sub(
        r'(<section[^>]*id="section-9"[^>]*>\s*<h1 class="major-section-title display">Section 9: Lead Generation System</h1>\s*).*?(</section>)',
        r"\1" + s9_body + r"\2",
        s9_new,
        count=1,
        flags=re.DOTALL,
    )

    # --- Section 10 content: trim AEO para, fix section ref ---
    s10_new = replace_h1(s6_content, 10, "Content Engine and AEO Strategy")
    s10_new = s10_new.replace(
        "We will deliver every one of these to the highest standard. Other bidders will too. AEO compliance is becoming the price of admission.",
        "AEO compliance is becoming the price of admission.",
    )
    s10_new = re.sub(
        r"<p>The baseline marks where CTW appears today.*?</p>",
        "<p>The chart above shows where CTW currently stands. The engine that follows is built to close that gap.</p>",
        s10_new,
        count=1,
        flags=re.DOTALL,
    )
    s10_new = s10_new.replace(
        "three attention levels outlined in Section 8",
        "three attention levels outlined in Section 2",
    )

    # --- Section 11 trust compressed ---
    s11_trust_new = replace_h1(s7_trust, 11, "Trust, Compliance, and Accessibility")
    s11_trust_new = re.sub(
        r"<h1.*?</h1>\s*.*",
        """<h1 class="major-section-title display">Section 11: Trust, Compliance, and Accessibility</h1>
      <p>The site ships with the technical and procedural foundations that signal a firm worth trusting. Three areas: accessibility, privacy and data handling, security posture.</p>
      <h2 class="block-heading display">ACCESSIBILITY</h2>
      <p>WCAG 2.2 AA conformance built into the build, not bolted on. Semantic HTML, contrast ratios, keyboard navigation, focus management, screen reader compatibility. A published accessibility statement on the site names the standard and provides a contact path for accessibility issues. We do not use accessibility widget overlays, which are performative and do not satisfy WCAG conformance requirements.</p>
      <h2 class="block-heading display">PRIVACY AND DATA HANDLING</h2>
      <p>CCPA-aware data handling baseline. Modernized privacy policy and disclaimer pages drafted to current standards. Form data and PII handled with industry-standard encryption in transit and at rest. Cookie consent surface for visitors in regulatory environments that require it.</p>
      <h2 class="block-heading display">SECURITY POSTURE</h2>
      <p>Cloudflare-level infrastructure security baseline (DDoS protection, web application firewall, bot mitigation, automatic SSL). The static site architecture eliminates the most common vectors of attack on professional services firms (SQL injection, plugin exploits). The site's security posture is published on the site as a trust signal alongside the privacy and accessibility statements.</p>
      <p>These three pages are not compliance checkboxes hidden in a footer. They are trust signals positioned with the same visual weight as the firm's value propositions.</p>
""",
        s11_trust_new,
        count=1,
        flags=re.DOTALL,
    )

    # --- Section 2 engagement: full rebuild ---
    eng_table_rows = """          <tr><td>Brand and messaging sprint</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Full website rebuild on Astro / Cloudflare / Keystatic</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Content audit and rewrite</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>AEO foundation (schema, FAQ, plain-language structure)</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Calendar booking with intelligent routing</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Capital Event Readiness Assessment</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Two embedded calculators</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>WCAG 2.2 AA accessibility</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Training for four content stewards</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Ninety days of stabilization support</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Podcast launch and twelve episodes</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Quarterly original research piece</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Monthly press release program</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Partner LinkedIn personal brand playbooks</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>LinkedIn newsletter</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>AI Concierge</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Twelve-month content velocity contract</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td><td class="ec-yes">&check;</td></tr>
          <tr><td>Full ongoing content production</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td></tr>
          <tr><td>Quarterly business reviews with AEO citation tracking</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td></tr>
          <tr><td>AI content production training for CTW staff</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td></tr>
          <tr><td>Priority response on new content needs</td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-dash"><span class="ec-dash-mark">&ndash;</span></td><td class="ec-yes">&check;</td></tr>
          <tr class="ec-price-row"><td><strong>Build investment</strong></td><td><span class="ph-fee">[FOUNDATION_BUILD]</span></td><td><span class="ph-fee">[ENGINE_BUILD]</span></td><td><span class="ph-fee">[PARTNERSHIP_BUILD]</span></td></tr>
          <tr class="ec-price-row"><td><strong>Monthly retainer</strong></td><td><span class="ph-fee">[FOUNDATION_RETAINER]</span></td><td><span class="ph-fee">[ENGINE_RETAINER]</span></td><td><span class="ph-fee">[PARTNERSHIP_RETAINER]</span></td></tr>"""

    photo_callout = """      <aside class="photography-callout" aria-label="Optional original photography">
        <h3 class="photo-callout-head display">OPTIONAL: ORIGINAL PHOTOGRAPHY</h3>
        <p class="photo-callout-sub display">Stock photography is the most common signal that a website was rushed. We recommend, but do not require, original photography as part of CTW's rebuild.</p>
        <p>The session captures professional headshots for all partners and staff plus a series of in-office b-roll images: the team collaborating, meeting with clients, working in the space. These images replace stock photography across the site and become reusable assets for press releases, LinkedIn content, podcast promotional material, and future marketing work.</p>
        <p><span class="photo-callout-label display">What's included:</span></p>
        <ul class="photo-callout-list clean-list">
          <li>Professional headshots for up to 25 staff members, lit and styled consistently for a unified team presentation</li>
          <li>In-office b-roll capturing the firm's culture and professionalism</li>
          <li>Full editing, retouching, and web optimization for every selected image</li>
          <li>Delivered as a curated library of 80 to 120 final images</li>
        </ul>
        <p class="photo-invest">Investment: <span class="ph-fee">[PHOTOGRAPHY]</span> one-time. Includes the photography day, post-production, and delivery. Custom quotes available for staff counts above 25.</p>
        <p><span class="photo-callout-label display">Timeline impact:</span> Original photography extends the core launch from four weeks to twelve weeks. The photography day is scheduled in week 5. Editing and selection runs through week 8. Site integration through week 10. Public launch with original photography in weeks 11 to 12.</p>
        <p><span class="photo-callout-label display">Without photography:</span> We launch the four-week core build with brand-treated existing partner headshots and licensed editorial imagery. Photography can be added as a Phase 4 swap-in after launch without rebuilding the site. The architecture supports image swaps as content updates rather than as design changes.</p>
      </aside>"""

    attention_html = """      <p>Every engagement we run is built around one question: who is paying attention to your firm, and how do you turn that attention into business? There are three levels of attention worth building toward. Each engagement mode is designed to reach a different one.</p>
      <div class="attention-staircase" role="img" aria-label="Three levels of attention">
        <div class="attention-step attention-step-3">
          <span class="attention-num display">3</span>
          <div class="attention-body">
            <div class="attention-name display">PEOPLE TALK ABOUT YOU</div>
            <p class="attention-desc">The human attention that AI has not yet replaced and won't anytime soon.</p>
          </div>
          <span class="attention-tag display">PARTNERSHIP</span>
        </div>
        <div class="attention-step attention-step-2">
          <span class="attention-num display">2</span>
          <div class="attention-body">
            <div class="attention-name display">AI RECOMMENDS YOU</div>
            <p class="attention-desc">The sustained content production that moves CTW from "mentioned" to "recommended" on the answer engines that drive the largest share of prospect research.</p>
          </div>
          <span class="attention-tag display">ENGINE</span>
        </div>
        <div class="attention-step attention-step-1">
          <span class="attention-num display">1</span>
          <div class="attention-body">
            <div class="attention-name display">AI MENTIONS YOU</div>
            <p class="attention-desc">The technical foundation that gets CTW cited by AI search engines when prospects ask category questions.</p>
          </div>
          <span class="attention-tag display">FOUNDATION</span>
        </div>
      </div>
      <p>CTW can stop at any of the three levels. Most firms in the category are not yet operating past the first.</p>
      <table class="engagement-compare-table">
        <thead>
          <tr>
            <th scope="col" class="ec-feature">Feature</th>
            <th scope="col" class="ec-f">PATH FORWARD FOUNDATION</th>
            <th scope="col" class="ec-e">PATH FORWARD ENGINE</th>
            <th scope="col" class="ec-p">PATH FORWARD PARTNERSHIP</th>
          </tr>
        </thead>
        <tbody>
""" + eng_table_rows + """
        </tbody>
      </table>
      <div class="mode-taglines">
        <p class="mode-tagline"><span class="display mode-tagline-label">PATH FORWARD FOUNDATION:</span> The website rebuild itself, ready in four weeks. Many firms launch here, run the new site for a year, and add the content engine in year two. CTW could absolutely do that.</p>
      </div>
""" + photo_callout + """
      <div class="mode-taglines mode-taglines-rest">
        <p class="mode-tagline"><span class="display mode-tagline-label">PATH FORWARD ENGINE:</span> For CTW if the firm wants to be cited, found, and remembered through a sustained content presence, not just rebuilt.</p>
        <p class="mode-tagline"><span class="display mode-tagline-label">PATH FORWARD PARTNERSHIP:</span> For CTW if the firm wants the website and the surrounding communications work to keep getting smarter without leadership having to manage it.</p>
      </div>
"""
    s2_eng = f"""    <section class="major-section section-anchor" id="section-2">
      <h1 class="major-section-title display">Section 2: Engagement Modes</h1>
{attention_html}
    </section>
"""

    # --- Section 4 timeline ---
    s4_time = replace_h1(s9_time, 4, "Timeline")
    s4_time = re.sub(
        r'<h1 class="major-section-title display">Section 4: Timeline</h1>\s*<p>Target dates.*?</p>\s*(?:<p>Week.*?</p>\s*)+',
        '<h1 class="major-section-title display">Section 4: Timeline</h1>\n',
        s4_time,
        count=1,
        flags=re.DOTALL,
    )
    s4_time = re.sub(
        r"</figure>\s*<p>Final dates.*?</p>\s*</section>",
        """</figure>
      <h2 class="block-heading display">KEY MILESTONES</h2>
      <ul class="clean-list timeline-milestones">
        <li>Week 1 (May 20, 2026): Discovery, brand sprint kickoff</li>
        <li>Week 2: Content audit complete, AEO baseline expanded to 25 priority queries</li>
        <li>Week 3: Three design directions presented for selection</li>
        <li>Week 4: Foundation core build complete, ready for soft launch</li>
        <li>Weeks 5 to 8 (if photography elected): Photography, video, expanded content production</li>
        <li>Weeks 9 to 12: Public launch, stabilization, content steward training</li>
      </ul>
      <p>Final dates and milestone confirmations are set in the engagement letter. CTW's leadership team confirms one design direction by end of week three to hold the four-week core delivery commitment.</p>
    </section>""",
        s4_time,
        count=1,
        flags=re.DOTALL,
    )

    # --- Section 3 investment ---
    s3_inv = replace_h1(s10_price, 3, "Investment")
    s3_inv = s3_inv.replace("Section 8 under Path Forward", "Section 2 under Path Forward")

    # --- Section 5 team: compress case studies ---
    s5_team = replace_h1(s11_team, 5, "Team and Relevant Experience")
    # Advocacy chiefs case
    s5_team = re.sub(
        r"<article class=\"case-block\">.*?ADVOCACY CHIEFS.*?</article>",
        """<article class="case-block">
        <div style="margin-bottom:6px;">
          <img class="logo-inline" src="assets/logos/advocacy-chiefs.png" alt="Advocacy Chiefs logo" loading="lazy" decoding="async" />
        </div>
        <div class="case-heading display">ADVOCACY CHIEFS</div>
        <div class="case-tagline display">Brand architecture for an integrated services firm.</div>
        <p>A coalition of consultants offering grants, government relations, legal compliance, and partnership development as separate services. The market kept treating them as four firms.</p>
        <p>We ran a positioning sprint that surfaced their core value (Impact Multiplier: integration as the product) and built a visual identity around it. The brand now lets the team show up as one firm to clients who need integration and as four practices to clients who need depth.</p>
        <p>Why this matters for CTW: this is the same work we will run in the brand sprint phase, surfacing the actual position, structuring the messaging, and building the architecture that lets a complex firm read as a coherent one.</p>
      </article>""",
        s5_team,
        count=1,
        flags=re.DOTALL,
    )
    s5_team = re.sub(
        r"<article class=\"case-block\">.*?PG&amp;E AND CALIFORNIA.*?</article>",
        """<article class="case-block">
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:6px;">
          <img class="logo-inline on-white-border" src="assets/logos/pg-and-e.png" alt="PG&amp;E logo" loading="lazy" decoding="async" />
          <img class="logo-inline on-white-border" src="assets/logos/socalgas.png" alt="SoCalGas logo" loading="lazy" decoding="async" />
        </div>
        <div class="case-heading display">PG&amp;E AND CALIFORNIA ENERGY COMMISSION WORKSHOP PROGRAM</div>
        <div class="case-tagline display">Communications for audiences that are skeptical before you speak.</div>
        <p>Audiences arrive expecting to be managed, not heard. Pacific Gas and Electric needed real information to community stakeholders, regulators, and rural construction partners across California regions where utility communication had been received cynically.</p>
        <p>We built the program from the ground up through follow-through documentation. The work has run for three years across PG&amp;E, SoCalGas, and the California Energy Commission and has been replicated for adjacent audiences.</p>
        <p>This case matters for CTW because middle-market business owners are not naive audiences. Trust gets earned by the firms that show up with actual depth in the room. The communications discipline that produces a trusted utility workshop is the same discipline that produces a trusted advisory firm presence online.</p>
      </article>""",
        s5_team,
        count=1,
        flags=re.DOTALL,
    )
    s5_team = re.sub(
        r"<article class=\"case-block\">.*?BEN OLSEN AT BRIGHTWORK.*?</article>",
        """<article class="case-block">
        <div style="margin-bottom:6px;">
          <img class="logo-inline" src="assets/logos/brightwork.png" alt="BrightWork Realty Advocates logo" loading="lazy" decoding="async" />
        </div>
        <div class="case-heading display">BEN OLSEN AT BRIGHTWORK REALTY ADVOCATES</div>
        <div class="case-tagline display">Two ways to write something for them, not for everyone.</div>
        <p>Ben Olsen works Moraga Country Club in the East Bay. Standard mass-market plays do not distinguish him from dozens of agents at the same addresses.</p>
        <p>We built MoragaCountryClubRealEstate.com with property value estimates from hyperlocal data Zillow cannot replicate, plus a direct mail program that writes individual letters in Ben's voice at scale.</p>
        <p>The Capital Event Readiness Assessment we are proposing for CTW uses the same architecture for middle-market owners two to five years ahead of a sale. We have built this kind of system before. We know how it converts.</p>
      </article>""",
        s5_team,
        count=1,
        flags=re.DOTALL,
    )
    s5_team = re.sub(
        r"<article class=\"case-block\">.*?WEST BIOFUELS LLC.*?</article>",
        """<article class="case-block">
        <div style="margin-bottom:6px;">
          <img class="logo-inline" src="assets/logos/west-biofuels.png" alt="West Biofuels logo" loading="lazy" decoding="async" />
        </div>
        <div class="case-heading display">WEST BIOFUELS LLC</div>
        <div class="case-tagline display">Communications under regulatory scrutiny.</div>
        <p>West Biofuels built a three-megawatt biomass facility in Northern California where regulators, construction partners, and skeptical community stakeholders all required sustained communication at every milestone.</p>
        <p>We built and ran the program through groundbreaking: coordination across regulators and trade press, earned media at milestones, and partnership development with industry associations through state and federal grant recognition.</p>
        <p>CTW's clients live in the same environment: FAR compliance, government audits, multi-state manufacturing. The discipline that holds up under regulatory scrutiny is the discipline that earns trust with audiences who have memory.</p>
      </article>""",
        s5_team,
        count=1,
        flags=re.DOTALL,
    )

    # --- Section 13 partnership ---
    s13_new = replace_h1(s13, 13, "Approach to Partnership")
    s13_new = re.sub(
        r"<h1.*?</h1>\s*.*",
        """<h1 class="major-section-title display">Section 13: Approach to Partnership</h1>
      <p>CTW's RFP says it directly: the firm is looking for a long-term partner, not just a developer. Most agency proposals respond to that line with a sentence about ongoing support and move on. We want to be more specific.</p>
      <h2 class="block-heading display">QUARTERLY BUSINESS REVIEWS</h2>
      <p>Every ninety days, MKTNG's senior leadership presents to CTW's leadership team. Site performance. AEO citation tracking against named competitors. Lead funnel analysis. Content production review. A prioritized recommendation list for the following quarter. Two named MKTNG leaders attend every review.</p>
      <h2 class="block-heading display">NAMED ACCOUNTS</h2>
      <p>Two MKTNG contacts for the duration of the engagement. The day-to-day account lead handles production and client services. The senior strategic contact handles partner-level communication. CTW's partners can call either of us directly.</p>
      <h2 class="block-heading display">PROACTIVE STRATEGIC INPUT</h2>
      <p>The website, the content engine, and the surrounding communications work will need to evolve. Regulatory developments shift. AI search platforms change. Competitor firms move. Our job is to surface signals before they become problems and to bring CTW recommendations rather than wait to be asked. Specifically: a monthly written brief covering relevant changes in the competitive environment, regulatory context, and AI search behavior, with flagged items requiring CTW's attention.</p>
      <h2 class="block-heading display">ONGOING ECONOMICS</h2>
      <p>The engagement modes are designed for sustainability. We do not bill in surprises. We do not churn through hours. CTW knows what the relationship costs and what it produces every month.</p>
      <h2 class="block-heading display">WHAT WE ARE</h2>
      <p>We are senior practitioners who run strategy, write copy, design visuals, and ship the build, then stay around to keep building. Most of our client relationships run two, three, or more years. The work compounds when the team stays.</p>
      <p>This is the firm CTW will still be working with in 2030.</p>
""",
        s13_new,
        count=1,
        flags=re.DOTALL,
    )

    # --- FAQ updates ---
    faq_new = faq.replace("Section 6 and Appendix A", "Section 10 and Appendix A")
    faq_new = faq_new.replace("Full results are included in Section 6 and Appendix A", "Full results are included in Section 10 and Appendix A")
    faq_new = faq_new.replace("Detailed pricing is in Section 10", "Detailed pricing is in Section 3")
    faq_new = faq_new.replace("we address this in detail in Section 4.", "we address this in detail in Section 8.")

    # --- Section 12 metrics ---
    s12_new = s12.replace(
        "baseline already established in Section 6",
        "baseline already established in Section 10",
    )

    # --- Section 7 fix landscape wrapper: my replace may be wrong ---
    # Check s7_new has duplicate closing - fix sitemap structure
    if s7_new.count("sitemap-landscape-page") != 1:
        print("WARN landscape count", s7_new.count("sitemap-landscape-page"))

    new_inner = (
        "\n"
        + exec_one
        + toc
        + s1
        + "\n\n"
        + s2_eng
        + "\n\n"
        + s3_inv
        + "\n\n"
        + s4_time
        + "\n\n"
        + s5_team
        + "\n\n"
        + s6_new
        + "\n\n"
        + s7_new
        + "\n\n"
        + s8_new
        + "\n\n"
        + s9_new
        + "\n\n"
        + s10_new
        + "\n\n"
        + s11_trust_new
        + "\n\n"
        + s12_new
        + "\n\n"
        + s13_new
        + "\n\n"
        + faq_new
        + "\n\n"
        + app_a
        + "\n\n"
        + appendix_b
        + "\n"
    )

    new_full = full[: m.start(2)] + new_inner + full[m.end(2) :]
    out_report = "/Users/scotteggert/Development/Cursor/CTW-proposal/SUPPLEMENTAL-3-VERIFICATION.md"
    with open(PATH, "w") as f:
        f.write(new_full)
    with open(out_report, "w") as f:
        f.write(
            """# Supplemental Update #3 verification report

## Page count
Run print to PDF locally (Chrome) and record page count. Target: roughly 28-32 portrait pages plus 1 landscape, plus appendices.

## Compression review
- Case studies in Section 5 were shortened; confirm nuance still matches firm positioning.
- Technology Section 8 condensed prior subsections into a comparison table plus notes; verify no lost commitment on HubSpot/Salesforce nuance if needed for legal review.

## Cross-references spot-check
- FAQ, Quick Reference (Appendix B), and compliance matrix use new section numbers.
- Engagement pricing cards reference Section 2.

## Placeholders
- [FOUNDATION_BUILD_FLOOR], [PARTNERSHIP_ANNUAL_FLOOR], [FOUNDATION_BUILD], [ENGINE_BUILD], [PARTNERSHIP_BUILD], retainers, [PHOTOGRAPHY] in photography callout.

## Lead generation section
If the automated hero extraction misordered headings, manually verify Section 9 structure in the HTML.
"""
        )
    print("Wrote", PATH, "and", out_report)


if __name__ == "__main__":
    main()
