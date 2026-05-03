import streamlit as st
import requests

API_URL = " http://127.0.0.1:8000"

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🐾 Pet Registry",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    /* Background */
    .stApp { background: #0d0d0d; color: #f0ece4; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #151515;
        border-right: 1px solid #2a2a2a;
    }
    [data-testid="stSidebar"] * { color: #f0ece4 !important; }

    /* Title */
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #f0ece4 0%, #c8a97e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-sub {
        color: #666;
        font-size: 0.95rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Cards */
    .pet-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 14px;
        transition: border-color 0.2s;
    }
    .pet-card:hover { border-color: #c8a97e; }
    .pet-name {
        font-family: 'Syne', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #f0ece4;
    }
    .pet-meta { color: #888; font-size: 0.85rem; margin-top: 4px; }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        background: #2a2a2a;
        color: #c8a97e;
        border: 1px solid #3a3a3a;
        margin-right: 6px;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        color: #f0ece4 !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #c8a97e !important;
        box-shadow: 0 0 0 2px rgba(200,169,126,0.15) !important;
    }

    /* Labels */
    label { color: #aaa !important; font-size: 0.85rem !important; letter-spacing: 0.5px; }

    /* Buttons */
    .stButton > button {
        background: #c8a97e;
        color: #0d0d0d;
        border: none;
        border-radius: 8px;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
        padding: 10px 24px;
        transition: background 0.2s, transform 0.1s;
        width: 100%;
    }
    .stButton > button:hover {
        background: #e0c090;
        transform: translateY(-1px);
    }

    /* Delete button variant */
    .delete-btn > button {
        background: #2a1515 !important;
        color: #e05555 !important;
        border: 1px solid #3a2020 !important;
    }
    .delete-btn > button:hover { background: #3a1a1a !important; }

    /* Divider */
    hr { border-color: #2a2a2a; }

    /* Success / error */
    .stSuccess { background: #0d2010 !important; border: 1px solid #1a4020 !important; color: #5ecf8a !important; }
    .stError   { background: #200d0d !important; border: 1px solid #401a1a !important; color: #e05555 !important; }

    /* Section headers */
    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #c8a97e;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

SPECIES_ICONS = {
    "dog": "🐕", "cat": "🐈", "bird": "🐦",
    "rabbit": "🐇", "fish": "🐟", "hamster": "🐹",
    "reptile": "🦎", "other": "🐾",
}

def icon_for(species: str) -> str:
    return SPECIES_ICONS.get(species.lower(), "🐾")

def fetch_pets():
    try:
        r = requests.get(f"{API_URL}/pets", timeout=5)
        return r.json() if r.status_code == 200 else []
    except Exception:
        return None

def create_pet(data: dict):
    return requests.post(f"{API_URL}/pets", json=data, timeout=5)

def update_pet(pet_id: str, data: dict):
    return requests.put(f"{API_URL}/pets/{pet_id}", json=data, timeout=5)

def delete_pet(pet_id: str):
    return requests.delete(f"{API_URL}/pets/{pet_id}", timeout=5)

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title">🐾</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#f0ece4;">Pet Registry</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">v1.0</div>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["📋 All Pets", "➕ Register Pet", "✏️ Update Pet", "🗑️ Delete Pet"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown('<div style="color:#444;font-size:0.8rem;">API: ' + API_URL + '</div>', unsafe_allow_html=True)

# ── Shared pet form fields ────────────────────────────────────────────────────

def pet_form(prefix="", defaults=None):
    d = defaults or {}
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=d.get("name", ""), key=f"{prefix}_name", placeholder="Buddy")
        species = st.text_input("Species", value=d.get("species", ""), key=f"{prefix}_species", placeholder="Dog")
        breed = st.text_input("Breed", value=d.get("breed", ""), key=f"{prefix}_breed", placeholder="Labrador")
    with col2:
        age = st.number_input("Age (years)", min_value=1, max_value=100, value=int(d.get("age", 1)), key=f"{prefix}_age")
        gender = st.selectbox("Gender", ["male", "female"],
                              index=0 if d.get("gender", "male") == "male" else 1,
                              key=f"{prefix}_gender")
        comments = st.text_area("Comments", value=d.get("comments", "") or "", key=f"{prefix}_comments",
                                placeholder="Any notes about the pet…", height=100)
    return dict(name=name, species=species, breed=breed, age=age, gender=gender,
                comments=comments if comments else None)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: All Pets
# ══════════════════════════════════════════════════════════════════════════════
if page == "📋 All Pets":
    st.markdown('<div class="section-title">Registered animals</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2rem;">All Pets</div>', unsafe_allow_html=True)
    st.markdown("")

    pets = fetch_pets()

    if pets is None:
        st.error("⚠️ Cannot connect to API. Make sure the FastAPI server is running.")
    elif len(pets) == 0:
        st.info("No pets registered yet. Use **Register Pet** to add one.")
    else:
        st.markdown(f'<div style="color:#666;margin-bottom:20px;">{len(pets)} pet(s) on record</div>', unsafe_allow_html=True)

        # Search / filter
        search = st.text_input("🔍 Filter by name or species", placeholder="e.g. Max, Cat…")
        if search:
            pets = [p for p in pets if search.lower() in p["name"].lower() or search.lower() in p["species"].lower()]

        cols = st.columns(2)
        for i, pet in enumerate(pets):
            ico = icon_for(pet["species"])
            gender_sym = "♂" if pet["gender"] == "male" else "♀"
            comments_html = (
                f"<div style='color:#888;font-size:0.82rem;margin-top:8px;'>💬 {pet['comments']}</div>"
                if pet.get("comments") else ""
            )
            card_html = (
                f'<div class="pet-card">'
                f'<div class="pet-name">{ico} {pet["name"]}</div>'
                f'<div class="pet-meta">{pet["breed"]} · {pet["age"]} yr · {gender_sym}</div>'
                f'<div style="margin-top:10px;"><span class="badge">{pet["species"]}</span></div>'
                + comments_html +
                f'<div style="color:#555;font-size:0.7rem;margin-top:10px;font-family:monospace;">{pet["id"]}</div>'
                f'</div>'
            )
            with cols[i % 2]:
                st.markdown(card_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Register Pet
# ══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Register Pet":
    st.markdown('<div class="section-title">New entry</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2rem;">Register a Pet</div>', unsafe_allow_html=True)
    st.markdown("")

    with st.container():
        data = pet_form(prefix="create")
        st.markdown("")
        if st.button("Register Pet →", key="create_btn"):
            if not data["name"] or not data["species"] or not data["breed"]:
                st.error("Name, species, and breed are required.")
            else:
                try:
                    resp = create_pet(data)
                    if resp.status_code == 200:
                        pet = resp.json()
                        st.success(f"✅ **{pet['name']}** registered successfully! ID: `{pet['id']}`")
                    else:
                        st.error(f"API error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Update Pet
# ══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ Update Pet":
    st.markdown('<div class="section-title">Modify record</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2rem;">Update a Pet</div>', unsafe_allow_html=True)
    st.markdown("")

    pets = fetch_pets()
    if pets is None:
        st.error("Cannot connect to API.")
    elif len(pets) == 0:
        st.info("No pets to update yet.")
    else:
        options = {f"{p['name']} ({p['species']}) — {p['id'][:8]}…": p for p in pets}
        selected_label = st.selectbox("Select a pet to edit", list(options.keys()))
        selected_pet = options[selected_label]
        st.markdown("---")
        data = pet_form(prefix=f"update_{selected_pet['id']}", defaults=selected_pet)
        st.markdown("")
        if st.button("Save Changes →", key="update_btn"):
            if not data["name"] or not data["species"] or not data["breed"]:
                st.error("Name, species, and breed are required.")
            else:
                try:
                    resp = update_pet(selected_pet["id"], data)
                    if resp.status_code == 200:
                        st.success(f"✅ **{data['name']}** updated successfully!")
                    else:
                        st.error(f"API error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Delete Pet
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗑️ Delete Pet":
    st.markdown('<div class="section-title">Remove record</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2rem;">Delete a Pet</div>', unsafe_allow_html=True)
    st.markdown("")

    pets = fetch_pets()
    if pets is None:
        st.error("Cannot connect to API.")
    elif len(pets) == 0:
        st.info("No pets to delete.")
    else:
        options = {f"{p['name']} ({p['species']}) — {p['id'][:8]}…": p for p in pets}
        selected_label = st.selectbox("Select a pet to delete", list(options.keys()))
        selected_pet = options[selected_label]

        ico = icon_for(selected_pet["species"])
        st.markdown(
            f"""
            <div class="pet-card" style="border-color:#3a2020;">
                <div class="pet-name">{ico} {selected_pet['name']}</div>
                <div class="pet-meta">{selected_pet['breed']} · {selected_pet['age']} yr · {selected_pet['gender']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        confirm = st.checkbox(f"I confirm I want to permanently delete **{selected_pet['name']}**")
        st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
        if st.button("Delete Pet", key="delete_btn", disabled=not confirm):
            try:
                resp = delete_pet(selected_pet["id"])
                if resp.status_code == 200:
                    st.success(f"🗑️ **{selected_pet['name']}** has been deleted.")
                    st.rerun()
                else:
                    st.error(f"API error {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)