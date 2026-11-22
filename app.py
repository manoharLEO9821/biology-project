import streamlit as st
import pandas as pd
import plotly.express as px

from ai_engine import recommend_solutions
from biomimicry_data import BIOMIMICRY_DATA
from simulator import lotus_score, gecko_index, drag_index

# ---------- Disease & medical machine data (educational, not medical advice) ----------
DISEASE_DATA = [
    {
        "name": "Diabetes mellitus",
        "category": "Metabolic",
        "cause": "Type 1: immune system destroys insulin-making beta cells. Type 2: body cells respond poorly to insulin.",
        "mechanism": "Insulin moves glucose from blood into cells. When insulin is missing or ineffective, glucose stays high in the blood and slowly damages vessels, nerves, eyes and kidneys.",
        "symptoms": "Excess thirst, frequent urination, tiredness, blurred vision, slow-healing wounds.",
        "diagnosis": [
            ("Glucometer", "A test strip reacts with glucose in a blood drop and the meter converts the electrical signal into a glucose reading."),
            ("Continuous glucose monitor (CGM)", "A tiny sensor under the skin measures glucose in tissue fluid every few minutes."),
        ],
        "treatment": [
            ("Insulin pump", "A small programmable pump delivers insulin through a thin tube under the skin."),
        ],
        "bio_link": "Mosquito-proboscis-inspired microneedles are researched for near-painless blood sampling and drug delivery.",
    },
    {
        "name": "Asthma",
        "category": "Respiratory",
        "cause": "Chronic airway inflammation, often triggered by allergens, cold air, smoke or infections.",
        "mechanism": "Airway muscles tighten, the lining swells and mucus increases, so air flows out of the lungs with difficulty.",
        "symptoms": "Wheezing, cough, chest tightness, shortness of breath.",
        "diagnosis": [
            ("Spirometer", "Measures how much air you can blow out and how fast, showing airway narrowing."),
            ("Peak flow meter", "Handheld tube that measures the fastest speed of exhaled air."),
        ],
        "treatment": [
            ("Nebulizer", "Turns liquid medicine into a fine mist that is breathed in through a mask or mouthpiece."),
            ("Metered-dose inhaler", "Releases a measured puff of medicine directly to the airways."),
        ],
        "bio_link": "Airway branching in lungs inspires optimised aerosol-delivery and filter designs.",
    },
    {
        "name": "Hypertension (high blood pressure)",
        "category": "Cardiovascular",
        "cause": "Combination of genetics, high salt intake, stress, obesity, kidney conditions and ageing.",
        "mechanism": "Persistently high force against artery walls makes the heart work harder and damages vessels, raising the risk of stroke, heart attack and kidney disease.",
        "symptoms": "Often none (the 'silent' disease); sometimes headaches or dizziness at very high levels.",
        "diagnosis": [
            ("Sphygmomanometer (BP monitor)", "A cuff squeezes the arm artery and the device detects pressure at which blood flow starts and becomes smooth."),
            ("Ambulatory BP monitor", "A wearable cuff that records pressure automatically over 24 hours."),
        ],
        "treatment": [],
        "bio_link": "Elastic artery walls inspire compliant vascular grafts and flexible sensors.",
    },
    {
        "name": "Arrhythmia (heart rhythm disorder)",
        "category": "Cardiovascular",
        "cause": "Faulty electrical signalling in the heart due to heart disease, ageing, drugs or electrolyte imbalance.",
        "mechanism": "The heart's natural pacemaker (SA node) or conduction pathways misfire, so the heart beats too fast, too slow or irregularly and pumps blood less efficiently.",
        "symptoms": "Palpitations, dizziness, fainting, chest discomfort.",
        "diagnosis": [
            ("ECG / EKG machine", "Electrodes on the skin record the heart's tiny electrical signals as a waveform."),
            ("Holter monitor", "Portable ECG worn for 1-2 days to catch irregular beats."),
        ],
        "treatment": [
            ("Pacemaker", "Implanted device that sends small electrical pulses when the heart beats too slowly."),
            ("Defibrillator (ICD/AED)", "Delivers a controlled shock to reset a dangerous rhythm."),
        ],
        "bio_link": "The heart's own natural pacemaker cells inspire biological pacemaker and self-powered implant research.",
    },
    {
        "name": "Chronic kidney disease",
        "category": "Renal",
        "cause": "Long-term diabetes, hypertension, infections or inherited conditions.",
        "mechanism": "Nephrons (filter units) slowly lose function, so waste, extra fluid and salts build up in the blood.",
        "symptoms": "Swelling, fatigue, reduced urine, nausea, high blood pressure.",
        "diagnosis": [
            ("Blood/urine analyser", "Automated lab machine measuring creatinine, urea and protein."),
            ("Ultrasound scanner", "Uses sound waves to image kidney size and structure."),
        ],
        "treatment": [
            ("Dialysis machine (haemodialysis)", "Pumps blood through a filter (dialyser) where waste diffuses across a membrane into dialysis fluid, then returns cleaned blood."),
        ],
        "bio_link": "Kidney nephron filtering and aquaporin water channels inspire advanced filtration membranes.",
    },
    {
        "name": "Tuberculosis (TB)",
        "category": "Infectious",
        "cause": "Bacterium Mycobacterium tuberculosis, spread through airborne droplets.",
        "mechanism": "Bacteria settle in the lungs, immune cells wall them into granulomas, and if the immune system weakens the bacteria multiply and damage lung tissue.",
        "symptoms": "Cough lasting weeks, weight loss, night sweats, fever, blood in sputum.",
        "diagnosis": [
            ("Chest X-ray machine", "X-rays pass through the body and create a shadow image of lung damage."),
            ("Molecular test (e.g. GeneXpert / PCR)", "Copies bacterial DNA so even a few bacteria can be detected, also showing drug resistance."),
        ],
        "treatment": [],
        "bio_link": "Treated mainly with a long antibiotic course; nature-inspired work focuses on rapid diagnostics and air filtration.",
    },
    {
        "name": "Malaria",
        "category": "Infectious",
        "cause": "Plasmodium parasites carried by Anopheles mosquitoes.",
        "mechanism": "Parasites infect liver cells, then red blood cells, multiply and burst them, causing recurring fever and anaemia.",
        "symptoms": "Cyclic fever and chills, headache, sweating, fatigue.",
        "diagnosis": [
            ("Microscope", "Blood smear is stained and examined for parasites inside red blood cells."),
            ("Rapid diagnostic test (RDT)", "Paper strip that detects parasite proteins in a drop of blood in minutes."),
        ],
        "treatment": [],
        "bio_link": "Mosquito biology inspires traps, sensors and microneedle designs.",
    },
    {
        "name": "Cancer (general)",
        "category": "Oncology",
        "cause": "Genetic mutations from inheritance, radiation, tobacco, certain viruses or chance errors in cell division.",
        "mechanism": "Cells ignore normal stop signals, multiply uncontrollably, form tumours and may spread (metastasis) to other organs.",
        "symptoms": "Depends on type: lumps, unexplained weight loss, persistent pain, abnormal bleeding.",
        "diagnosis": [
            ("CT scanner", "Rotating X-ray source and detectors build 3D cross-sectional images."),
            ("MRI scanner", "Strong magnet and radio waves align hydrogen atoms in the body to create detailed soft-tissue images."),
            ("PET scanner", "Detects a tracer sugar that cancer cells absorb heavily, revealing active tumours."),
        ],
        "treatment": [
            ("Linear accelerator (radiotherapy)", "Produces high-energy beams shaped to the tumour to damage its DNA while sparing healthy tissue."),
        ],
        "bio_link": "Virus- and cell-inspired nanoparticles are being studied for targeted drug delivery.",
    },
    {
        "name": "Viral respiratory infections (e.g. COVID-19, flu)",
        "category": "Infectious",
        "cause": "Respiratory viruses spread by droplets and aerosols.",
        "mechanism": "Viruses enter cells in the airways, hijack them to copy themselves, and trigger inflammation that can reduce oxygen transfer in the lungs.",
        "symptoms": "Fever, cough, sore throat, fatigue, breathlessness in severe cases.",
        "diagnosis": [
            ("RT-PCR machine", "Converts viral RNA to DNA and copies it repeatedly so a tiny amount becomes detectable."),
            ("Pulse oximeter", "Shines light through a fingertip to estimate blood oxygen saturation."),
        ],
        "treatment": [
            ("Ventilator", "Pushes oxygen-rich air into the lungs when a patient cannot breathe adequately."),
        ],
        "bio_link": "Natural antiviral surfaces and filtration structures inspire masks and air-cleaning materials.",
    },
    {
        "name": "Obstructive sleep apnea",
        "category": "Respiratory",
        "cause": "Throat muscles relax and the airway narrows during sleep; linked to obesity and anatomy.",
        "mechanism": "Repeated airway collapse stops airflow for seconds at a time, dropping oxygen and fragmenting sleep.",
        "symptoms": "Loud snoring, daytime sleepiness, morning headaches, pauses in breathing.",
        "diagnosis": [
            ("Polysomnography (sleep study) system", "Records brain waves, breathing, oxygen and heart rate overnight."),
        ],
        "treatment": [
            ("CPAP machine", "A fan delivers gentle continuous air pressure through a mask to keep the airway open."),
        ],
        "bio_link": "Studies of animal airway mechanics inspire more comfortable mask and airway designs.",
    },
    {
        "name": "Osteoporosis",
        "category": "Musculoskeletal",
        "cause": "Ageing, hormone changes, low calcium/vitamin D, inactivity.",
        "mechanism": "Bone breakdown outpaces bone building, leaving the honeycomb-like inner bone thin and fragile.",
        "symptoms": "Often none until a fracture; loss of height, stooped posture, back pain.",
        "diagnosis": [
            ("DEXA scanner", "Uses two low-dose X-ray energies to measure bone mineral density."),
            ("X-ray machine", "Shows fractures and bone thinning."),
        ],
        "treatment": [],
        "bio_link": "Trabecular bone's light yet strong lattice inspires lightweight implants and 3D-printed structures.",
    },
    {
        "name": "Sensorineural hearing loss",
        "category": "Sensory",
        "cause": "Ageing, loud noise exposure, infections, genetics.",
        "mechanism": "Hair cells in the cochlea or the auditory nerve are damaged, so sound vibrations are not turned into nerve signals properly.",
        "symptoms": "Difficulty understanding speech, muffled sounds, ringing in ears.",
        "diagnosis": [
            ("Audiometer", "Plays tones at different pitches and volumes to map the quietest sounds you can hear."),
        ],
        "treatment": [
            ("Cochlear implant", "Microphone and processor send electrical signals straight to the cochlea's nerve endings."),
        ],
        "bio_link": "The cochlea's frequency-sorting basilar membrane inspires acoustic sensors and sound processors.",
    },
]


def all_machines():
    """Flatten the data into a machine directory.

    Returns a list of dicts: machine, role ('Diagnosis'/'Treatment'), how, diseases (list).
    """
    directory = {}
    for d in DISEASE_DATA:
        for role, key in (("Diagnosis", "diagnosis"), ("Treatment", "treatment")):
            for machine, how in d[key]:
                entry = directory.setdefault(
                    machine, {"machine": machine, "role": role, "how": how, "diseases": []}
                )
                entry["diseases"].append(d["name"])
    return sorted(directory.values(), key=lambda x: x["machine"].lower())


st.set_page_config(page_title="BioInspired Studio", page_icon="🌿", layout="wide")


def stretch(func):
    """Return the right 'full width' keyword for this Streamlit version.

    Newer Streamlit uses width="stretch"; older versions use use_container_width=True.
    """
    import inspect
    try:
        params = inspect.signature(func).parameters
    except (TypeError, ValueError):
        params = {}
    if "width" in params:
        return {"width": "stretch"}
    return {"use_container_width": True}


BUTTON_FULL = stretch(st.button)
PLOT_FULL = stretch(st.plotly_chart)

st.markdown("""
<style>
.block-container {padding-top:1.2rem;max-width:1400px}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#062b1d,#0d4930)}
[data-testid="stSidebar"] * {color:#f1fff4!important}
.hero {padding:1.5rem 1.8rem;border-radius:22px;background:linear-gradient(120deg,#082d20,#187243);color:#effff4;margin-bottom:1rem}
.hero h1 {color:white!important}
div.stButton > button[kind="primary"] {background:linear-gradient(90deg,#138440,#24a85a);border:0}
div[data-testid="stMetric"] {background:#effaf1;padding:12px;border-radius:12px}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🌿 BioInspired Studio")
    page = st.radio(
        "Navigation",
        ["Home & AI Finder", "Nature Library", "Diseases & Medical Machines", "Simulators", "About"],
    )
    st.caption(f"Library size: {len(BIOMIMICRY_DATA)} entries")
    st.caption(f"Disease library: {len(DISEASE_DATA)} conditions")

if page == "Home & AI Finder":
    st.markdown('<div class="hero"><h1>AI Biomimicry Design Simulator</h1><p>Turn engineering challenges into nature-inspired ideas.</p></div>', unsafe_allow_html=True)
    st.markdown("### 💡 Describe your engineering challenge")
    problem = st.text_area(
        "Problem",
        placeholder="Example: How can I reduce heat inside buildings without using much electricity?",
        height=110,
        label_visibility="collapsed",
    )
    if st.button("🌱 Find nature-inspired ideas", type="primary", **BUTTON_FULL):
        if len(problem.strip()) < 5:
            st.warning("Please describe the problem in a little more detail.")
        else:
            matches = recommend_solutions(problem, top_k=3)
            st.session_state["last_problem"] = problem
            st.session_state["last_matches"] = matches
            if not matches:
                st.info("No close matches found. Try adding more detail or different keywords (for example: heat, water, drag, grip, noise).")

    if st.session_state.get("last_matches"):
        st.subheader("Recommended biological inspirations")
        for rank, item in enumerate(st.session_state["last_matches"], 1):
            with st.container(border=True):
                st.markdown(f"### {rank}. {item['name']} · {item['category']}")
                st.write("**Biological principle:**", item["mechanism"])
                st.write("**Engineering idea:**", item["engineering"])
                st.progress(float(item["similarity"]))
                st.caption(f"Relevance score: {item['similarity']*100:.1f}% — text similarity, not real-world performance prediction.")

        if st.session_state.get("last_problem"):
            report = "BIOMIMICRY RECOMMENDATION REPORT\n\nEngineering challenge: " + st.session_state["last_problem"] + "\n\n"
            for i, item in enumerate(st.session_state["last_matches"], 1):
                report += (
                    f"{i}. {item['name']} — {item['category']}\n"
                    f"Biological principle: {item['mechanism']}\n"
                    f"Engineering idea: {item['engineering']}\n"
                    f"Relevance: {item['similarity']*100:.1f}%\n\n"
                )
            st.download_button("⬇️ Download recommendation report (.txt)", report, file_name="biomimicry_report.txt")

    st.info("Matching method: TF-IDF + cosine similarity against your curated biological inspiration library. It can suggest ideas for many problem types, but it is a prototype—not a validated engineering design.")

elif page == "Nature Library":
    st.markdown('<div class="hero"><h1>Nature Inspiration Library</h1><p>Browse biological strategies and engineering ideas.</p></div>', unsafe_allow_html=True)
    categories = sorted({x["category"] for x in BIOMIMICRY_DATA})
    col1, col2 = st.columns([1, 2])
    with col1:
        category = st.selectbox("Filter by theme", ["All"] + categories)
    with col2:
        query = st.text_input("Search by organism, mechanism, or keyword", placeholder="e.g. beetle, wing, drag, water, heat").strip().lower()

    filtered = BIOMIMICRY_DATA if category == "All" else [x for x in BIOMIMICRY_DATA if x["category"] == category]
    if query:
        filtered = [
            x for x in filtered
            if query in x["name"].lower()
            or query in x["category"].lower()
            or query in x["mechanism"].lower()
            or query in x["engineering"].lower()
            or query in x["problem"].lower()
        ]

    st.caption(f"Showing {len(filtered)} of {len(BIOMIMICRY_DATA)} biological inspirations")
    for item in filtered:
        with st.expander(f"{item['name']} — {item['category']}"):
            st.write("**Biological mechanism:**", item["mechanism"])
            st.write("**Engineering inspiration:**", item["engineering"])
            st.write("**Problem themes:**", item["problem"])

elif page == "Diseases & Medical Machines":
    st.markdown('<div class="hero"><h1>Diseases & Medical Machines</h1><p>How common diseases work in the body, and the machines used to detect and treat them.</p></div>', unsafe_allow_html=True)
    tab_d, tab_m, tab_c = st.tabs(["🧬 Disease explorer", "🩺 Machine directory", "📊 Overview"])

    with tab_d:
        d_categories = sorted({x["category"] for x in DISEASE_DATA})
        c1, c2 = st.columns([1, 2])
        with c1:
            d_cat = st.selectbox("Filter by body system / type", ["All"] + d_categories, key="d_cat")
        with c2:
            d_query = st.text_input(
                "Search disease, symptom, or machine",
                placeholder="e.g. lung, ECG, insulin, X-ray",
                key="d_query",
            ).strip().lower()

        diseases = DISEASE_DATA if d_cat == "All" else [x for x in DISEASE_DATA if x["category"] == d_cat]
        if d_query:
            def haystack(x):
                machines = " ".join(m for m, _ in x["diagnosis"] + x["treatment"])
                return " ".join([x["name"], x["category"], x["cause"], x["mechanism"], x["symptoms"], machines]).lower()
            diseases = [x for x in diseases if d_query in haystack(x)]

        st.caption(f"Showing {len(diseases)} of {len(DISEASE_DATA)} conditions")
        if not diseases:
            st.info("No matches. Try a broader keyword such as 'heart', 'lung', or 'scan'.")
        for d in diseases:
            with st.expander(f"{d['name']} — {d['category']}"):
                st.write("**Cause:**", d["cause"])
                st.write("**How it affects the body:**", d["mechanism"])
                st.write("**Common symptoms:**", d["symptoms"])

                left, right = st.columns(2)
                with left:
                    st.markdown("**🔍 Diagnosis machines**")
                    if d["diagnosis"]:
                        for machine, how in d["diagnosis"]:
                            st.markdown(f"- **{machine}** — {how}")
                    else:
                        st.caption("No specific machine listed.")
                with right:
                    st.markdown("**💊 Treatment / support machines**")
                    if d["treatment"]:
                        for machine, how in d["treatment"]:
                            st.markdown(f"- **{machine}** — {how}")
                    else:
                        st.caption("Mainly treated with medicines or lifestyle changes.")

                st.success(f"🌿 **Nature connection:** {d['bio_link']}")

    with tab_m:
        machines = all_machines()
        role_filter = st.radio("Show", ["All", "Diagnosis", "Treatment"], horizontal=True, key="m_role")
        m_query = st.text_input("Search machines", placeholder="e.g. scanner, pump, monitor", key="m_query").strip().lower()
        shown = [
            m for m in machines
            if (role_filter == "All" or m["role"] == role_filter)
            and (not m_query or m_query in m["machine"].lower() or m_query in m["how"].lower())
        ]
        st.caption(f"Showing {len(shown)} of {len(machines)} machines")
        if shown:
            table = pd.DataFrame({
                "Machine": [m["machine"] for m in shown],
                "Used for": [m["role"] for m in shown],
                "How it works": [m["how"] for m in shown],
                "Related conditions": [", ".join(m["diseases"]) for m in shown],
            })
            st.dataframe(table, hide_index=True, **stretch(st.dataframe))

    with tab_c:
        counts = pd.Series([d["category"] for d in DISEASE_DATA]).value_counts().reset_index()
        counts.columns = ["Category", "Conditions"]
        st.plotly_chart(
            px.bar(counts, x="Category", y="Conditions", title="Conditions in the library by category"),
            key="disease_chart", **PLOT_FULL,
        )
        st.metric("Total machines catalogued", len(all_machines()))

    st.warning("This section is general educational content for a student project. It is not medical advice, diagnosis or treatment guidance. Please consult a qualified doctor for any health concern.")

elif page == "Simulators":
    st.markdown('<div class="hero"><h1>Interactive Simulators</h1><p>Adjust virtual parameters to explore simplified concepts.</p></div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🍃 Lotus surface", "🦎 Gecko adhesion", "🐦 Shape / drag"])
    with tab1:
        st.subheader("Lotus-inspired surface concept")
        water = st.slider("Virtual water availability", 0, 100, 70)
        surface = st.slider("Surface suitability", 0, 100, 70)
        dirt = st.slider("Initial dirt level", 0, 100, 40)
        score, label = lotus_score(water, surface, dirt)
        st.metric("Illustrative surface score", f"{score:.1f}/100", label)
        chart = pd.DataFrame({
            "Factor": ["Water availability", "Surface suitability", "Dirt control"],
            "Value": [water, surface, 100 - dirt],
        })
        st.plotly_chart(
            px.bar(chart, x="Factor", y="Value", range_y=[0, 100], title="Input values"),
            key="lotus_chart", **PLOT_FULL,
        )
    with tab2:
        st.subheader("Gecko-inspired adhesion concept")
        contact = st.slider("Contact level", 0, 100, 65)
        compat = st.slider("Virtual surface compatibility", 0, 100, 70)
        condition = st.slider("Virtual condition factor", 0, 100, 80)
        score = gecko_index(contact, compat, condition)
        st.metric("Illustrative adhesion index", f"{score:.1f}/100")
        df = pd.DataFrame({
            "Factor": ["Contact", "Surface compatibility", "Condition"],
            "Value": [contact, compat, condition],
        })
        st.plotly_chart(
            px.bar(df, x="Factor", y="Value", range_y=[0, 100], title="Adhesion input factors"),
            key="gecko_chart", **PLOT_FULL,
        )
    with tab3:
        st.subheader("Streamlined shape concept")
        speed = st.slider("Relative speed setting", 10, 100, 60)
        shape_names = ["Blunt", "Rounded", "Streamlined"]
        vals = [drag_index(shape, speed) for shape in shape_names]
        df = pd.DataFrame({"Shape concept": shape_names, "Illustrative drag index": vals})
        st.plotly_chart(
            px.bar(df, x="Shape concept", y="Illustrative drag index", range_y=[0, 100],
                   title="Shape comparison — lower is better in this demo"),
            key="drag_chart", **PLOT_FULL,
        )
        st.caption(f"Illustrative values at selected speed: {dict(zip(shape_names, vals))}")
    st.warning("These are simplified teaching simulations, not validated biological measurements or engineering predictions.")

else:
    st.markdown('<div class="hero"><h1>About BioInspired Studio</h1><p>Biomimicry concepts explored using text matching and simple interactive simulations.</p></div>', unsafe_allow_html=True)
    st.markdown(f"""
### Project objectives
- Explore engineering challenges through biological strategies.
- Use TF-IDF and cosine similarity to rank ideas across **{len(BIOMIMICRY_DATA)}** curated biological entries.
- Explore three interactive, simplified simulator concepts.
- Learn how **{len(DISEASE_DATA)}** common diseases work and which machines diagnose and treat them.
- Present results and charts in a student-friendly interface.

### Technology stack
Python · Streamlit · scikit-learn · Pandas · Plotly · NumPy

### Limitations
The recommendations are text-based inspiration, not a substitute for engineering analysis, testing, safety review, or professional design. The disease section is educational only and is not medical advice.
""")

st.divider()
st.caption("Student prototype • software-only • no hardware required")
