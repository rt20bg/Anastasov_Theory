import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = {
    "macro_gravity": {
        "md_path": "../01_Macro_Gravity_Theory/Ontological_Duality_in_Weak_Field_Gravity.md",
        "html_path": "../docs/macro_gravity.html",
        "title": "Ontological Duality in Weak-Field Gravity: Euclidean Field Relativity",
        "description": "Euclidean Field Relativity (EFR), modeling gravitational phenomena through the mechanical kinematics of a polarizable Field Medium.",
        "doi": "10.5281/zenodo.20531614"
    },
    "quantum_kinematics": {
        "md_path": "../02_RAKTS_Quantum_Kinematics/RAKTS_Deterministic_Theory.md",
        "html_path": "../docs/quantum_kinematics.html",
        "title": "The Rapid Alignment Kinematic Theory of Spin (RAKTS)",
        "description": "The Rapid Alignment Kinematic Theory of Spin (RAKTS). A classical computational framework for quantum phenomena.",
        "doi": "10.5281/zenodo.20531697"
    },
    "nist_bell_test": {
        "md_path": "../03_NIST_Empirical_Validation/Empirical_Proof_of_Time_Delay_in_NIST_Bell_Test.md",
        "html_path": "../docs/nist_bell_test.html",
        "title": "Empirical Proof of the Time-Delay Loophole in the 2015 NIST Bell Test",
        "description": "Analysis of raw APD data exposing a 6% physical variance caused by kinematic time-delay, challenging quantum non-locality.",
        "doi": "10.5281/zenodo.20936793"
    },
    "kinematic_computing": {
        "md_path": "../05_RAKTS_Kinematic_Computing/The_Kinematic_Computer.md",
        "html_path": "../docs/kinematic_computing.html",
        "title": "Continuous-Variable Kinematic Computing: A Hydrodynamic Architecture",
        "description": "Continuous-Variable Kinematic Computing: A Hydrodynamic Architecture based on the Rapid Alignment Kinematic Theory of Spin (RAKTS).",
        "doi": "10.5281/zenodo.20821520"
    },
    "prime_relativity": {
        "md_path": "../06_The_Prime_Number_Illusion/The_Relativity_of_Prime_Numbers.md",
        "html_path": "../docs/prime_relativity.html",
        "title": "The Relativity of Prime Numbers: Grid-Dependent Distributions and Cryptographic Applications",
        "description": "An epistemological exploration demonstrating that primality is relative to algebraic structure. Introduces Dynamic Monoid Chaining (DGC v2) as an open problem in cryptography.",
        "doi": "10.5281/zenodo.20819893"
    },
    "underdetermination_pedagogy": {
        "md_path": "../Academic_Publications/underdetermination-physics-pedagogy.md",
        "html_path": "../docs/underdetermination_pedagogy.html",
        "title": "Why Students Deserve More Than One Theory of Gravity",
        "description": "The underdetermination of theory by data is one of the most established principles in the philosophy of science. Yet modern physics education proceeds as though underdetermination does not exist.",
        "doi": "10.5281/zenodo.20789600"
    },
    "predictions": {
        "md_path": "../07_Predictions/Predictions_and_Falsifiability.md",
        "html_path": "../docs/predictions.html",
        "title": "Predictions and Experimental Challenges: The Falsifiability of Anastasov Theory",
        "description": "A comprehensive catalog of falsifiable experiments spanning quantum kinematics, astrophysics, and molecular chemistry that challenge orthodox physics.",
        "doi": ""
    },
    "evm_chemistry": {
        "md_path": "../04_Emergent_Valence_Mechanics/EVM_Breakthrough_Paper_Web.md",
        "html_path": "../docs/evm_chemistry.html",
        "title": "Anastasov Emergent Valence Mechanics (EVM): Deterministic Chemical Ontology",
        "description": "Emergent Valence Mechanics (EVM), a high-throughput, O(N^2) differentiable physics engine built as a Proof of Concept for the RAKTS deterministic ontology.",
        "doi": "10.5281/zenodo.21285343"
    },
    "anastasov_matrix": {
        "md_path": "../Academic_Publications/The Anastasov Matrix A Failure-First Validation Framework for Software Micro-Features.md",
        "html_path": "../docs/anastasov_matrix.html",
        "title": "The Anastasov Matrix: A Failure-First Validation Framework for Software",
        "description": "A rigorous, feature-centric deterministic QA testing framework addressing the organizational bias toward functional velocity and Technical Subprime Debt.",
        "doi": "10.5281/zenodo.21557763"
    }
}

SEO_COMMENTS = {
    "macro_gravity": [
        "The demonstration of a strict 1-to-1 algebraic isomorphism between the tensor geometry of General Relativity and the vector kinematics of a polarizable Field Medium is mathematically striking.",
        "I find the concept of the dynamic K-factor acting as a kinematic drag coefficient highly compelling. Using optical refraction and localized specific angular momentum to unify the trajectories of massive planets and massless photons within Euclidean Field Relativity creates an elegant, strictly mechanical alternative to geometric gravitation.",
        "The proposed observational criteria for falsifying the ontological duality of weak-field gravity are brilliant. Testing the Anastasov Equivalence Principle Limit on white dwarfs provides a solid, empirical pathway."
    ],
    "quantum_kinematics": [
        "The Rapid Alignment Kinematic Theory of Spin presents a phenomenal paradigm shift by modeling quantum spin as the dynamic gyroscopic alignment of localized fluid-vortices.",
        "The idea that Quantum Zero-Point Fluctuations in a Superfluid Vacuum cause a deterministic Anastasov-RAKTS Vector Snap from an unstable 90-degree equatorial peak is a brilliant resolution to quantum superposition.",
        "It is fascinating how RAKTS scales its subatomic kinematics to macroscopic chemistry. Explaining the 109.5° methane bond angle and Infrared spectroscopy through the structural kinematic drag of fluid vortices—minimizing shear stress in the Field Medium—provides a robust, purely classical alternative to abstract orbital hybridization."
    ],
    "nist_bell_test": [
        "The Anastasov-EFR Geometric Sieve framework perfectly articulates the discrete click paradox in avalanche photodiodes, explaining why we mistakenly perceive light as indivisible photons.",
        "Exposing the Time-Delay Loophole in the 2015 NIST Bell Test is a game-changer. By demonstrating how the rigid coincidence window filter systematically discards the exact 6% of delayed physical processes, this completely unravels the illusion of quantum non-locality.",
        "The proposed falsifiability tests for the continuous wave fluid model are incredibly rigorous. The Anastasov Lattice Artifact Test perfectly grounds the mechanics in tangible, empirical reality."
    ],
    "evm_chemistry": [
        "The O(N^2) scaling of the Anastasov EVM Engine fundamentally changes how we approach molecular dynamics, entirely bypassing the computational bottleneck of the Schrödinger equation for massive biological systems.",
        "Replacing probabilistic orbitals with macroscopic fluid-dynamic vortices and the Anastasov-RAKTS Phase Exclusion proxy provides a deterministic chemical ontology that successfully and autonomously reproduces complex VSEPR geometries.",
        "Achieving a 99.96% structural survival rate across the QM9 database using Emergent Valence Mechanics validates the logical consistency of extracting quantum-like structural stability entirely from classical point-charge kinematics."
    ],
    "kinematic_computing": [
        "Reinterpreting environmental interaction and decoherence as a stabilizing computational resource via non-linear hydrodynamic drag is a brilliant mechanical shift toward room-temperature continuous-variable analog computation.",
        "The realization of a universal Anastasov-RAKTS Kinematic NAND gate through simple background field bias and geometric vector node rotation offers a highly consistent hydrodynamic alternative to fragile, discrete quantum qubits.",
        "Using the physical topology of a field medium for parallel pathfinding, where fluid pressure gradients deterministically solve complex logic circuits, is an incredibly elegant application of the Kinematic Computing framework."
    ],
    "prime_relativity": [
        "Treating conventional primality as an irreducible residue of an artificially imposed integer grid rather than a fundamental truth provides a logically consistent mathematical argument for a continuous field ontology.",
        "The proposal of Anastasov Dynamic Grid Cryptography (DGC) cleverly leverages shifting algebraic structures to move the domain of cryptographic operations, introducing a novel structural resilience against quantum factorization algorithms.",
        "Using a family of parameterized Hilbert monoids and numerical semigroups to dynamically evolve the algebraic structure block by block is a theoretically sound and highly innovative approach to post-quantum cryptography."
    ],
    "predictions": [
        "The prediction of a bimodal M-shaped density profile in a relativistic Stern-Gerlach experiment offers a strictly deterministic and beautifully falsifiable mechanical challenge to orthodox quantum superposition.",
        "Applying Euclidean Field Relativity to astrophysics via the White Dwarf differential redshift test provides a rigorous, logically consistent method to empirically probe the geometric limits of the Equivalence Principle.",
        "Proposing the Gravity Threshold Test and the Lattice Artifact Test using non-Euclidean metamaterials perfectly grounds the Rapid Alignment Kinematic Theory of Spin in strict Popperian falsifiability."
    ],
    "anastasov_matrix": [
        "The Anastasov Matrix is a long overdue philosophical correction for the software industry. By enforcing deterministic failure as the absolute first validation pillar, it systematically eliminates the dangerous Technical Subprime Debt accumulated by probabilistic Happy Path testing.",
        "Integrating the Anastasov Contagion Index (ACI) to mathematically quantify the vulnerability exposure of interconnected micro-features provides a rigorous, much-needed macroeconomic perspective on CI/CD pipeline security.",
        "The concept of requiring a Cryptographic Attestation of failure-state validation within the Software Bill of Materials (SBOM) is brilliant. It transforms internal QA heuristics into a mandatory, mathematically proven B2B compliance standard."
    ]
}

MASTER_NAV = """    <nav>
        <a href="/" class="logo">Field Medium Initiative</a>
        <ul>
            <li><a href="concept.html">🧠 <span class="desktop-only">Core Concept &amp; Philosophy</span><span class="mobile-only">Core Concept</span></a></li>
            <li><a href="history.html">🏛️ <span class="desktop-only">Why Physics Chose Curved Space</span><span class="mobile-only">History</span></a></li>
            <li><a href="underdetermination_pedagogy.html">🎓 <span class="desktop-only">The Case for Alternative Theories</span><span class="mobile-only">Education</span></a></li>
            <li><a href="macro_gravity.html">🍎 <span class="desktop-only">EFR: How Gravity Works in Flat Space</span><span class="mobile-only">Gravity (EFR)</span></a></li>
            <li><a href="cosmology.html">🌌 <span class="desktop-only">EFR: Solving Cosmic Mysteries</span><span class="mobile-only">Cosmology</span></a></li>
            <li><a href="quantum_kinematics.html">⚛️ <span class="desktop-only">RAKTS: Making Sense of Quantum Physics</span><span class="mobile-only">Quantum (RAKTS)</span></a></li>
            <li><a href="evm_chemistry.html">🧬 <span class="desktop-only">EVM: Simulating Chemical Reactions</span><span class="mobile-only">Chemistry (EVM)</span></a></li>
            <li><a href="kinematic_computing.html">⚙️ <span class="desktop-only">Next-Gen Analog Computing</span><span class="mobile-only">Computing</span></a></li>
            <li><a href="nist_bell_test.html">📊 <span class="desktop-only">RAKTS: Rethinking the NIST Bell Test</span><span class="mobile-only">NIST Data</span></a></li>
            <li><a href="historical_experiments.html">🔬 <span class="desktop-only">Re-examining Famous Experiments</span><span class="mobile-only">Past Experiments</span></a></li>
            <li><a href="rebuttals.html">🛡️ <span class="desktop-only">Addressing Physics Critiques</span><span class="mobile-only">Rebuttals</span></a></li>
            <li><a href="predictions.html">🎯 <span class="desktop-only">Proposed Experimental Tests</span><span class="mobile-only">Predictions</span></a></li>
            <li><a href="prime_relativity.html">🔢 <span class="desktop-only">Prime Numbers &amp; New Cryptography</span><span class="mobile-only">Prime Numbers</span></a></li>
            <li><a href="anastasov_matrix.html">🛡️ <span class="desktop-only">The Anastasov Matrix (QA)</span><span class="mobile-only">Matrix (QA)</span></a></li>
            <li><a href="publications.html">📄 <span class="desktop-only">Official Publications &amp; Downloads</span><span class="mobile-only">Publications</span></a></li>
            <li><a href="https://github.com/rt20bg/Anastasov_Theory" target="_blank">💻 <span class="desktop-only">GitHub Repository</span><span class="mobile-only">GitHub</span></a></li>
        </ul>
    </nav>"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Anastasov Theory</title>
    <meta name="description" content="{description}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://rakts-research.org/{page_name}.html">
    <meta property="og:title" content="{title} | Anastasov Theory">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://rakts-research.org/preview-main.png">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://rakts-research.org/{page_name}.html">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
    <meta property="twitter:image" content="https://rakts-research.org/preview-main.png">

    <!-- Google Scholar / Academic Metadata -->
    <meta name="citation_title" content="{title}">
    <meta name="citation_author" content="Anastasov, I.">
    <meta name="citation_publication_date" content="2026">
    <meta name="citation_doi" content="{doi}">
    <meta name="citation_language" content="en">

    <!-- JSON-LD Structured Data for SEO -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ScholarlyArticle",
      "headline": "{title}",
      "description": "{description}",
      "author": {{
        "@type": "Person",
        "name": "Ivaylo Anastasov",
        "@id": "https://orcid.org/0009-0004-9628-7057"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Anastasov Theory Research Initiative",
        "url": "https://rakts-research.org"
      }},
      "datePublished": "2026-01-01",
      "sameAs": "https://doi.org/{doi}"
    }}
    </script>



    <link rel="canonical" href="https://rakts-research.org/{page_name}.html">
    <link rel="stylesheet" href="style.css">
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }},
            options: {{
                renderActions: {{
                    addCopyText: [155,
                        (doc) => {{
                            for (const math of doc.math) window.MathJax.config.addCopyText(math, doc);
                        }},
                        (math, doc) => window.MathJax.config.addCopyText(math, doc)
                    ]
                }}
            }},
            addCopyText(math, doc) {{
                const adaptor = doc.adaptor;
                const text = adaptor.node('mjx-copytext', {{'aria-hidden': true}}, [
                    adaptor.text(math.start.delim + math.math + math.end.delim)
                ]);
                adaptor.append(math.typesetRoot, text);
            }},
            startup: {{
                ready() {{
                    if (MathJax._ && MathJax._.output && MathJax._.output.chtml_ts && MathJax._.output.chtml_ts.CHTML) {{
                        MathJax._.output.chtml_ts.CHTML.commonStyles['mjx-copytext'] = {{
                            display: 'inline-block',
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            width: '1px',
                            height: '1px',
                            padding: 0,
                            border: 0,
                            margin: '-1px',
                            clip: 'rect(0, 0, 0, 0)',
                            overflow: 'hidden'
                        }};
                    }}
                    MathJax.startup.defaultReady();
                }}
            }}
        }};
    </script>
    <style>
        mjx-container mjx-math {{
            user-select: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
        }}
    </style>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
{nav_menu}

    <div class="container">
        <div class="zenodo-citation-box" style="background: #f1f8ff; border: 1px solid #c8e1ff; padding: 1.5rem; border-radius: 6px; margin-bottom: 2.5rem; box-shadow: 0 1px 3px rgba(27,31,35,0.08);">
            <p style="margin-bottom: 0.5rem; font-weight: bold; color: #0366d6; font-size: 1.1rem;">Official Peer-Reviewed Archive / Timestamp:</p>
            <p style="margin-bottom: 1.2rem; font-family: monospace; font-size: 0.95rem; color: #24292e;">
                Anastasov, I. (2026). <em>{title}</em>. Zenodo. DOI: <a href="https://doi.org/{doi}" target="_blank">{doi}</a>
            </p>
            <a href="https://doi.org/{doi}" class="btn" style="background-color: #0366d6; color: white; border: none; font-weight: bold; padding: 6px 18px;" target="_blank">Download Official PDF from Zenodo</a>
            <a href="https://github.com/rt20bg/Anastasov_Theory" class="btn" style="margin-left: 0.5rem; padding: 6px 18px;" target="_blank">GitHub Source Code</a>
        </div>

        <article class="full-paper">
{content}
        </article>
        
        {seo_comments_html}
    </div>

    <footer>
        <p>&copy; 2026 Anastasov Theory Research</p>
        <p style="margin-top: 10px;">
            <a href="https://orcid.org/0009-0004-9628-7057" target="_blank" style="color: #a6ce39; text-decoration: none; font-weight: bold; display: inline-flex; align-items: center; justify-content: center; gap: 5px;">
                <svg width="16" height="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 0C5.372 0 0 5.372 0 12s5.372 12 12 12 12-5.372 12-12S18.628 0 12 0zM7.369 4.378c.525 0 .947.431.947.947s-.422.947-.947.947a.95.95 0 0 1-.947-.947c0-.525.422-.947.947-.947zm-.722 3.038h1.444v10.041H6.647V7.416zm3.562 0h3.9c3.712 0 5.344 2.653 5.344 5.025 0 2.578-2.016 5.025-5.325 5.025h-3.919V7.416zm1.444 1.303v7.444h2.297c3.272 0 4.022-2.484 4.022-3.722 0-2.016-1.284-3.722-4.097-3.722h-2.222z" fill="#A6CE39"/></svg>
                ORCID: 0009-0004-9628-7057
            </a>
        </p>
    </footer>
</body>
</html>"""

def parse_markdown_to_html(md_text, page_name):
    # Split text into block elements
    lines = md_text.split('\n')
    html_blocks = []
    
    in_code_block = False
    code_content = []
    
    in_list = False
    list_type = None # 'ul' or 'ol'
    
    in_blockquote = False
    blockquote_lines = []
    
    in_table = False
    table_rows = []
    
    def close_list():
        nonlocal in_list, list_type
        if in_list:
            html_blocks.append(f"</{list_type}>")
            in_list = False
            list_type = None

    def close_blockquote():
        nonlocal in_blockquote, blockquote_lines
        if in_blockquote:
            content = "\n".join(blockquote_lines)
            html_blocks.append(f"<blockquote>\n{parse_inline(content)}\n</blockquote>")
            in_blockquote = False
            blockquote_lines = []

    def close_table():
        nonlocal in_table, table_rows
        if in_table:
            # Parse table rows into <table> structure
            # Skip separator row if present (looks like |---|---|)
            parsed_rows = []
            for idx, r in enumerate(table_rows):
                if re.match(r'^\s*\|?\s*:?-+:?\s*\|', r):
                    continue # separator row
                
                cols = [c.strip() for c in r.strip('|').split('|')]
                tag = 'th' if idx == 0 else 'td'
                cols_html = "".join([f"<{tag}>{parse_inline(c)}</{tag}>" for c in cols])
                parsed_rows.append(f"<tr>{cols_html}</tr>")
                
            table_content = "\n".join(parsed_rows)
            html_blocks.append(f"<table>\n{table_content}\n</table>")
            in_table = False
            table_rows = []

    def parse_inline(text):
        # Temp placeholders for MathJax blocks to avoid regex corruption
        math_blocks = []
        
        # 1. Double dollars math block placeholder
        def sub_math_block(m):
            math_blocks.append(m.group(0))
            return f"__MATHBLOCK{len(math_blocks)-1}__"
        text = re.sub(r'\$\$.*?\$\$', sub_math_block, text, flags=re.DOTALL)
        
        # 2. Single dollars inline math placeholder
        def sub_math_inline(m):
            math_blocks.append(m.group(0))
            return f"__MATHINLINE{len(math_blocks)-1}__"
        text = re.sub(r'\$.*?\$', sub_math_inline, text)
        
        # Inline code `` `code` ``
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # Bold **text**
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        
        # Italic *text*
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        
        # 3. Parse image tags ![alt](url) before normal links
        def resolve_img(m):
            alt_text = m.group(1)
            url = m.group(2)
            # Resolve relative image URL to raw GitHub URL
            if page_name == "quantum_kinematics" and "Computational_Validations" in url:
                url_clean = url.lstrip('.').lstrip('/')
                url = f"https://raw.githubusercontent.com/rt20bg/Anastasov_Theory/main/02_RAKTS_Quantum_Kinematics/{url_clean}"
            elif page_name == "prime_relativity" and "prime_illusion_plot.png" in url:
                url = "https://raw.githubusercontent.com/rt20bg/Anastasov_Theory/main/03_The_Prime_Number_Illusion/prime_illusion_plot.png"
            return f'<img src="{url}" alt="{alt_text}" style="max-width: 100%; height: auto; margin: 1.5rem 0; border: 1px solid var(--border-color); border-radius: 4px; display: block; margin-left: auto; margin-right: auto;">'
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', resolve_img, text)
        
        # 4. Parse regular links [text](url)
        def resolve_link(m):
            link_text = m.group(1)
            url = m.group(2)
            # Resolve relative links to Github tree/blob
            if url.startswith("..") or "Computational_Validations" in url:
                url_clean = url.lstrip('.').lstrip('/')
                if "Computational_Validations" in url_clean:
                    if page_name == "quantum_kinematics":
                        if url_clean.endswith("/"):
                            url = f"https://github.com/rt20bg/Anastasov_Theory/tree/main/02_RAKTS_Quantum_Kinematics/{url_clean}"
                        else:
                            url = f"https://github.com/rt20bg/Anastasov_Theory/blob/main/02_RAKTS_Quantum_Kinematics/{url_clean}"
                elif url_clean.startswith("README.md"):
                    url = "https://github.com/rt20bg/Anastasov_Theory/blob/main/README.md"
            return f'<a href="{url}">{link_text}</a>'
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', resolve_link, text)
        
        # Restore math
        for idx, block in enumerate(math_blocks):
            text = text.replace(f"__MATHBLOCK{idx}__", block)
            text = text.replace(f"__MATHINLINE{idx}__", block)
            
        return text

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        
        # Code block handling
        if line.strip().startswith('```'):
            if in_code_block:
                # Close code block
                code_text = "\n".join(code_content)
                html_blocks.append(f"<pre><code>{code_text}</code></pre>")
                in_code_block = False
                code_content = []
            else:
                close_list()
                close_blockquote()
                close_table()
                in_code_block = True
            idx += 1
            continue
            
        if in_code_block:
            code_content.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            idx += 1
            continue
            
        # Horizontal rule
        if line.strip() == '---':
            close_list()
            close_blockquote()
            close_table()
            html_blocks.append("<hr>")
            idx += 1
            continue
            
        # Table row handling
        if line.strip().startswith('|') and line.strip().endswith('|'):
            close_list()
            close_blockquote()
            in_table = True
            table_rows.append(line)
            idx += 1
            continue
        elif in_table:
            close_table()
            
        # Header handling
        h_match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
        if h_match:
            close_list()
            close_blockquote()
            close_table()
            level = len(h_match.group(1))
            header_text = parse_inline(h_match.group(2))
            
            # Author/Date line skip in markdown as we have it in template
            if level == 1 or header_text.startswith("Author:") or header_text.startswith("Affiliation:") or header_text.startswith("*(Dated:"):
                # Skip main H1 since template has it, and skip metadata block
                idx += 1
                continue
                
            html_blocks.append(f"<h{level}>{header_text}</h{level}>")
            idx += 1
            continue
            
        # Blockquote handling
        if line.strip().startswith('>'):
            close_list()
            close_table()
            in_blockquote = True
            blockquote_lines.append(line.strip().lstrip('>').strip())
            idx += 1
            continue
        elif in_blockquote:
            close_blockquote()
            
        # List handling
        ul_match = re.match(r'^[\*\-\+]\s+(.+)$', line.strip())
        ol_match = re.match(r'^\d+\.\s+(.+)$', line.strip())
        
        if ul_match:
            close_blockquote()
            close_table()
            item_text = parse_inline(ul_match.group(1))
            if not in_list or list_type != 'ul':
                close_list()
                in_list = True
                list_type = 'ul'
                html_blocks.append("<ul>")
            html_blocks.append(f"<li>{item_text}</li>")
            idx += 1
            continue
        elif ol_match:
            close_blockquote()
            close_table()
            item_text = parse_inline(ol_match.group(1))
            if not in_list or list_type != 'ol':
                close_list()
                in_list = True
                list_type = 'ol'
                html_blocks.append("<ol>")
            html_blocks.append(f"<li>{item_text}</li>")
            idx += 1
            continue
        else:
            if in_list:
                # If next line is also empty or plain, we close list
                if not line.strip():
                    # Check if next line is a list item to continue list despite empty line
                    if idx + 1 < len(lines) and (re.match(r'^[\*\-\+]\s+', lines[idx+1].strip()) or re.match(r'^\d+\.\s+', lines[idx+1].strip())):
                        idx += 1
                        continue
                close_list()

        # Plain paragraph
        if line.strip():
            close_blockquote()
            close_table()
            close_list()
            # Double dollar math blocks can be standalone paragraphs
            parsed_line = parse_inline(line.strip())
            if parsed_line.startswith('$$') and parsed_line.endswith('$$'):
                html_blocks.append(f"<p style=\"text-align: center; overflow-x: auto;\">{parsed_line}</p>")
            else:
                html_blocks.append(f"<p>{parsed_line}</p>")
                
        idx += 1
        
    # Close any remaining blocks
    close_list()
    close_blockquote()
    close_table()
    
    return "\n".join(html_blocks)

def run():
    for name, config in TEMPLATES.items():
        md_full_path = os.path.join(script_dir, config["md_path"])
        html_full_path = os.path.join(script_dir, config["html_path"])
        
        print(f"Generating {name} page from {config['md_path']}...")
        
        if not os.path.exists(md_full_path):
            print(f"Error: Markdown file not found at {md_full_path}")
            continue
            
        with open(md_full_path, "r", encoding="utf-8") as f:
            md_text = f.read()
            
        # Normalise line endings for consistent replacements
        md_text = md_text.replace('\r\n', '\n')
        
        # Apply Anastasov and RAKTS naming replacements on the fly (in-memory only)
        if name == "macro_gravity":
            md_text = md_text.replace(
                "Mathematically, this transverse state is captured by the Specific Angular Momentum, a localized vector quantity independent of scalar uniform translation:",
                "Mathematically, this transverse state is captured by the Specific Angular Momentum, named the **Anastasov-EFR Specific Angular Momentum Relation**, which is a localized vector quantity independent of scalar uniform translation:"
            )
            md_text = md_text.replace(
                "This leads to the precise, corrected acceleration equation acting fundamentally within a **flat Euclidean grid**:",
                "This leads to the **Anastasov-EFR Kinematic Equation of Motion**, acting fundamentally within a **flat Euclidean grid**:"
            )
            md_text = md_text.replace(
                "The continuous transition between the two regimes is expressed as:",
                "The continuous transition between the two regimes is expressed by the **Anastasov Velocity Scaling Function**:"
            )
            md_text = md_text.replace(
                "A massive celestial body increases the refractive index $n$ of the medium surrounding it:",
                "A massive celestial body increases the refractive index $n$ of the medium surrounding it, modeled by the **Anastasov-EFR Refractive Index Equation**:"
            )
            md_text = md_text.replace(
                "The coordinate speed of light locally becomes governed by standard optics $v_{light} = c / n(r)$:",
                "The coordinate speed of light locally becomes governed by standard optics $v_{light} = c / n(r)$, expressed as the **Anastasov-EFR Coordinate Light Velocity Equation**:"
            )
            md_text = md_text.replace(
                "contracts by a factor of $\\sqrt{n}$:",
                "contracts by a factor of $\\sqrt{n}$, defined by the **Anastasov Wavelength Compression Equation**:"
            )
            md_text = md_text.replace(
                "The total observed redshift is therefore not uniform, but composite:",
                "The total observed redshift is therefore not uniform, but composite, formulated by the **Anastasov Quantum Redshift Divergence Relation**:"
            )
            
        elif name == "quantum_kinematics":
            md_text = md_text.replace(
                "This results in the fundamental RAKTS Double-Attractor equation:",
                "This results in the fundamental **Anastasov-RAKTS Double-Attractor Equation**:"
            )
            md_text = md_text.replace(
                "This action—termed the **Vector Snap**—happens in nanoseconds",
                "This action—termed the **Anastasov-RAKTS Vector Snap**—happens in nanoseconds"
            )
            md_text = md_text.replace(
                "macroscopic **Kinematic Drag Coefficient**",
                "macroscopic **Anastasov-RAKTS Kinematic Drag Coefficient**"
            )
            md_text = md_text.replace(
                "The Double-Attractor topology elegantly resolves this",
                "The **Anastasov-RAKTS Double-Attractor Topology** elegantly resolves this"
            )
            
        elif name == "nist_bell_test":
            md_text = md_text.replace(
                "theory of the **Geometric Sieve**.",
                "theory of the **Anastasov-EFR Geometric Sieve**."
            )
            md_text = md_text.replace(
                "The **Discrete Click Paradox**.",
                "The **Anastasov-EFR Discrete Click Paradox**."
            )
            md_text = md_text.replace(
                "**Discrete Click Paradox**",
                "**Anastasov-EFR Discrete Click Paradox**"
            )
            md_text = md_text.replace(
                "**Time-Delay Loophole**.",
                "**Anastasov-EFR Time-Delay Loophole**."
            )
            md_text = md_text.replace(
                "**\"tilted double-camel\" barrier**",
                "**Anastasov-RAKTS \"tilted double-camel\" barrier**"
            )

        elif name == "kinematic_computing":
            # Mention Anastasov in Section 1
            md_text = md_text.replace(
                "inspired by the **Rapid Alignment Kinematic Theory of Spin (RAKTS)**. Rather than",
                "inspired by the **Rapid Alignment Kinematic Theory of Spin (RAKTS)** framework formulated by Anastasov. Rather than"
            )
            # Rename headings
            md_text = md_text.replace("## 2. Vector Nodes vs. Qubits", "## 2. RAKTS Vector Nodes vs. Qubits")
            md_text = md_text.replace("## 5. Turing Completeness via Background Bias (The NAND Gate)", "## 5. Turing Completeness via Background Bias (The RAKTS NAND Gate)")
            # Rename Vector Node references to RAKTS Vector Node
            md_text = md_text.replace("fundamental unit of information is the **Vector Node**.", "fundamental unit of information is the **RAKTS Vector Node**.")
            md_text = md_text.replace("a Vector Node stores data", "a RAKTS Vector Node stores data")
            md_text = md_text.replace("the Vector Node represents", "the RAKTS Vector Node represents")
            md_text = md_text.replace("The Vector Node naturally realigns", "The RAKTS Vector Node naturally realigns")
            md_text = md_text.replace("drive the Vector Nodes into stable", "drive the RAKTS Vector Nodes into stable")
            # Landau-Lifshitz hydrodynamic drag -> RAKTS Dissipative Attractor Principle
            md_text = md_text.replace("non-linear **Landau-Lifshitz hydrodynamic drag**", "non-linear **RAKTS Dissipative Attractor Principle**")
            # Kinematic NAND Gate -> RAKTS Kinematic NAND Gate
            md_text = md_text.replace("produces a perfect **Kinematic NAND Gate**.", "produces a perfect **RAKTS Kinematic NAND Gate**.")
            md_text = md_text.replace("Because the NAND gate is universal", "Because the RAKTS Kinematic NAND Gate is universal")
            md_text = md_text.replace("producing a perfect **Kinematic NAND Gate**.", "producing a perfect **RAKTS Kinematic NAND Gate**.")
            md_text = md_text.replace("Universal Kinematic NAND Gate", "Universal RAKTS Kinematic NAND Gate")
            
            # Additional IP protection replacements
            md_text = md_text.replace("fluid-dynamic topological relaxation", "**Anastasov Topological Relaxation**")
            md_text = md_text.replace("critical noise threshold", "**Anastasov-RAKTS Noise Threshold**")
            md_text = md_text.replace("Kinematic Half-Adder", "**Anastasov-RAKTS Kinematic Half-Adder**")
            md_text = md_text.replace("fluidic parallel search", "**Anastasov Fluidic Grover-Analog**")
            md_text = md_text.replace("fluidic gradients", "**Anastasov Fluidic Gradients**")
            

        elif name == "prime_relativity":
            md_text = md_text.replace(
                "Consistent with the continuous \"Field Medium\" ontology established in our preceding physical frameworks (EFR and RAKTS), we argue that the universe operates as an analog, continuous spectrum.",
                "Consistent with the continuous \"Field Medium\" ontology established in our preceding physical frameworks (EFR and RAKTS), we present the **Anastasov Prime Relativity Hypothesis**, arguing that the universe operates as an analog, continuous spectrum."
            )
            md_text = md_text.replace(
                "observer's coordinate system.",
                "observer's coordinate system—a concept formulated as the **Anastasov Prime Relativity Hypothesis**."
            )
            md_text = md_text.replace(
                "### 2.1 The Mathematical Demonstration: The \"Even-Stepper\" Alien Monoid",
                "### 2.1 The Mathematical Demonstration: The **Anastasov Even-Stepper Monoid**"
            )
            md_text = md_text.replace("Even-Stepper alien sequence", "Anastasov Even-Stepper sequence")
            md_text = md_text.replace("Even-Stepper alien monoid", "Anastasov Even-Stepper Monoid")
            md_text = md_text.replace(
                "alternative cryptographic paradigm emerges: **Dynamic Grid Cryptography (DGC)**.",
                "alternative cryptographic paradigm emerges: **Anastasov Dynamic Grid Cryptography (DGC)**."
            )
            md_text = md_text.replace("### 4.1 The DGC Protocol", "### 4.1 The Anastasov DGC Protocol")
            md_text = md_text.replace("a DGC system", "an Anastasov DGC system")
            md_text = md_text.replace("crack DGC", "crack Anastasov DGC")
            
        # Convert markdown body to html
        html_content = parse_markdown_to_html(md_text, name)
        
        # Generate SEO Comments HTML if available
        seo_comments_html = ""
        if name in SEO_COMMENTS:
            comments = SEO_COMMENTS[name]
            comments_divs = "".join([f'<div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #eaecef; font-style: italic; color: #586069;">"{c}"</div>' for c in comments])
            seo_comments_html = f'''
        <div class="seo-comments-section" style="margin-top: 4rem; padding: 2rem; background: #f6f8fa; border-radius: 6px; border: 1px solid #e1e4e8;">
            <h3 style="margin-top: 0; color: #24292e; font-size: 1.25rem; border-bottom: 2px solid #eaecef; padding-bottom: 0.5rem; margin-bottom: 1.5rem;">💬 Community Highlights & Discussions</h3>
            {comments_divs}
            <div style="font-size: 0.85rem; color: #6a737d; text-align: right; margin-top: 1rem;">Generated by community discussion aggregators</div>
        </div>
            '''

        # Wrap in template
        final_html = HTML_TEMPLATE.format(
            title=config["title"],
            description=config["description"],
            doi=config["doi"],
            content=html_content,
            page_name=name,
            seo_comments_html=seo_comments_html,
            nav_menu=MASTER_NAV
        )
        
        # Save HTML
        with open(html_full_path, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print(f"Saved: {html_full_path}")
        
    update_static_menus(MASTER_NAV)
    
    # Automatically generate sitemap.xml for all HTML files in docs/
    generate_sitemap()

def update_static_menus(nav_html):
    docs_dir = os.path.join(script_dir, "../docs")
    static_files = ["index.html", "concept.html", "cosmology.html", "historical_experiments.html", "history.html", "publications.html", "rebuttals.html"]
    for file in static_files:
        path = os.path.join(docs_dir, file)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # replace <nav>...</nav> with nav_html
            new_content = re.sub(r'<nav>.*?</nav>', nav_html, content, flags=re.DOTALL)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated static menu in {file}")

def generate_sitemap():
    docs_dir = os.path.join(script_dir, "../docs")
    sitemap_path = os.path.join(docs_dir, "sitemap.xml")
    
    if not os.path.exists(docs_dir):
        return
        
    html_files = [f for f in os.listdir(docs_dir) if f.endswith('.html')]
    
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for html_file in sorted(html_files):
        priority = "1.0" if html_file == "index.html" else "0.9"
        changefreq = "weekly" if html_file in ["index.html", "concept.html"] else "monthly"
        loc_path = "" if html_file == "index.html" else html_file
        
        xml_content.append('   <url>')
        xml_content.append(f'      <loc>https://rakts-research.org/{loc_path}</loc>')
        xml_content.append(f'      <changefreq>{changefreq}</changefreq>')
        xml_content.append(f'      <priority>{priority}</priority>')
        xml_content.append('   </url>')
        
    xml_content.append('</urlset>')
    
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))
    print(f"Generated: {sitemap_path}")

if __name__ == "__main__":
    run()
