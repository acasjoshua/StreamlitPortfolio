import io
import random
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

PROFILE = {
    "name": "Joshua Mikhail R. Acas",                                 
    "section": "CS 365 · Section F1",        
    "program": "BS Computer Science",            
    "year": "3rd Year",                                
    "school": "Cebu Institute of Technology University",                        
    "location": "Cebu, Philippines",                      
    "tagline": "Future Passionate Game / Software Developer",  
    "email": "jotjotacas2005@gmail.com",                           
    "github": "https://github.com/acasjoshua",         
    "linkedin": "https://www.linkedin.com/in/dot-dot-981a1b364/",  
    "short_bio": (
        """I am currently a 3rd year Computer Science student studying at Cebu Institute of Technology - University, 
        with interests on software and game development. I am passionate about creating engaging software solutions 
        that can make a positive impact on people's lives. I am always eager to learn new technologies and improve my 
        skills, and I am excited to explore the endless possibilities of the tech industry. My goal is to become a 
        skilled software developer who can contribute to the development of cutting-edge applications and games that 
        can inspire and entertain people around the world."""
    ),
}

BACKGROUND = (
    """I grew up at Dumlog, Talisay City, Cebu, Philippines, originally planning to be a civil engineer 
        to follow the footsteps or career path of my loving family, but now grew interest in the realm of technology. 
        always had that urge to become a good game developer, software thinker, and problem solver. Seeing how fun 
        video games were and curious on how to make them to fulfill a vision of my own game I have always wanted to 
        make, pushed me into studying the Computer Science course"""
)
EDUCATION = [  # (period, school / program, note)
    ("2012 – 2020", "Asian College of Technology - Bulacao Campus, Don Bosco Technical College Cebu", "Learned wire splicing, Construction of floor plans, Created First HTML project, Graduated with High Honors"),
    ("2020 – 2022", "Cebu Institute of Technology - University", "STEM strand, Finished with Honors"),
    ("2022 – Present", "Cebu Institute of Technology - University — BS Computer Science", "Focused on Game Development, Software Engineering, and Aspiring Video Game Creation."),
]
INTERESTS = ["Game Development", "Software Development", "Gaming", "Cooking"]
FUN_FACTS = [  # shown by the "Surprise me" button
    "I used to learn the drums and play a lot of badminton.",
    "I planned to be a civil engineer but now follow my interests as a computer science student.",
    "I love my girlfriend!",
]
MILESTONES = {  # year -> (title, story)
    2020: ("Wrote my first program in HTML", "A simple webpage about me."),
    2022: ("Started university", "The Computer Science journey is serious and coding is hard."),
    2026: ("Joined a Hackathon", "I'm excited to join more hackathons, and game jams in the future so I can make more relevant projects in relevant time"),
}

# Skill levels
SKILLS = pd.DataFrame(
    [
        ("Python", "Programming", 65),
        ("C++", "Programming", 70),
        ("Kotlin", "Mobile", 60),
        ("SQL", "Data", 60),
        ("Streamlit", "Data", 60),
        ("HTML / CSS", "Web", 60),
        ("JavaScript", "Web", 55),
        ("Git / GitHub", "Tools", 64),
        ("Communication", "Soft skills", 85),
        ("Teamwork", "Soft skills", 80),
    ],
    columns=["Skill", "Category", "Level"],
)

# How skill level grew
GROWTH_YEARS = [2021, 2022, 2023, 2024]
GROWTH_HISTORY = {
    "Python":        [15, 30, 45, 55],
    "C++":           [10, 25, 45, 60],
    "SQL":           [0, 15, 35, 50],
    "Kotlin":        [0, 15, 35, 50],
    "Streamlit":     [0, 0, 10, 35],
    "HTML / CSS":    [10, 25, 40, 50],
    "JavaScript":    [5, 15, 30, 45],
    "Git / GitHub":  [0, 15, 35, 50],
    "Communication": [55, 65, 72, 80],
    "Teamwork":      [50, 62, 72, 78],
}
_current = SKILLS.set_index("Skill")["Level"]
SKILL_GROWTH = pd.DataFrame(
    {skill: hist + [int(_current[skill])] for skill, hist in GROWTH_HISTORY.items()},
    index=GROWTH_YEARS + [2025],
)

PROJECTS = [
    {
        "title": "FocusFuel",
        "role": "Developer",
        "tools": ["Kotlin", "Android Studio", "Git / GitHub"],
        "summary": "A productivity app that helps users stay focused and manage their time effectively. It includes features such as a Pomodoro timer, task management, and progress tracking.",
        "outcome": "Presented, Finished, and Graded. Learned how to use Android Studio and Kotlin to create a mobile application.",
        "link": "https://github.com/acasjoshua/FocusFuel.git",
        "status": "Completed",
        "hours": 200,
    },
    {
        "title": "CookBookSite",
        "role": "Developer",
        "tools": ["HTML", "CSS", "C#", "Visua Studio Code", "Git / GitHub"],
        "summary": "A web application that allows users to browse and search for recipes.",
        "outcome": "Still needs peer evaluation.",
        "link": "https://github.com/acasjoshua/CookBookSite.git",
        "status": "Incomplete",
        "hours": 30,
    },
    {
        "title": "JavaBox",
        "role": "Co-Developer",
        "tools": ["Java", "CSS", "Git / GitHub"],
        "summary": "A local-multiplayer party game suite built in Java using JavaFX. It acts as a centralized game hub that hosts a catalog of mini-games designed for couch-play, bringing competitive fun to any gathering without needing multiple setups.",
        "outcome": "Presented, Finished, and Graded. A step into Game Development.",
        "link": "https://github.com/X3N0Xeno/CSIT228-Capstonee.git",
        "status": "Completed",
        "hours": 150,
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title=f"{PROFILE['name']} | Portfolio",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": f"Autobiography & portfolio of {PROFILE['name']} — {PROFILE['section']}",
    },
)

# ═══════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════
st.session_state.setdefault("likes", 0)
st.session_state.setdefault("fun_fact", None)
st.session_state.setdefault("messages", [])  # messages sent from the contact form

# ═══════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════
ACCENTS = {"Indigo": "#4F46E5", "Teal": "#0D9488", "Rose": "#E11D48", "Amber": "#D97706"}


@st.cache_data
def make_avatar(name: str, size: int = 480) -> Image.Image:
    """Clearly labeled stand-in photo (initials on a gradient)."""
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            px[x, y] = (int(79 + 120 * t), int(70 + 40 * t), int(229 - 60 * t))
    d = ImageDraw.Draw(img)
    initials = "".join(w[0] for w in name.split()[:2]).upper() or "?"
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", size // 3)
        small = ImageFont.truetype("DejaVuSans.ttf", size // 22)
    except OSError:
        font = small = ImageFont.load_default()
    d.text((size / 2, size / 2 - 10), initials, fill="white", font=font, anchor="mm")
    d.text((size / 2, size - 28), "PLACEHOLDER PHOTO", fill="white", font=small, anchor="mm")
    return img


def get_photo():
    local = Path(__file__).parent / "profile.jpg"
    if local.exists():
        return Image.open(local)
    return make_avatar(PROFILE["name"])


def resume_text() -> str:
    lines = [PROFILE["name"], f"{PROFILE['program']} · {PROFILE['year']} · {PROFILE['school']}",
             PROFILE["email"], "", "SUMMARY", PROFILE["short_bio"], "", "SKILLS"]
    lines += [f"- {r.Skill} ({r.Category}): {r.Level}/100" for r in SKILLS.itertuples()]
    lines += ["", "PROJECTS"]
    for p in PROJECTS:
        lines += [f"- {p['title']} | {p['role']} | {', '.join(p['tools'])}", f"  {p['outcome']}"]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image(get_photo(), width="stretch", caption=f"{PROFILE['name']} · {PROFILE['section']}")

    st.markdown(f"### {PROFILE['name']}")
    st.caption(f"{PROFILE['program']} · {PROFILE['year']}")

    st.link_button("GitHub", PROFILE["github"], width="stretch")
    st.link_button("LinkedIn", PROFILE["linkedin"], width="stretch")
    st.divider()

    st.subheader("🎛️ Display options")
    accent_name = st.selectbox("Accent color", list(ACCENTS), index=0)
    show_timeline = st.checkbox("Show milestone timeline", value=True)
    show_tables = st.toggle("Show raw data tables", value=True)
    st.divider()

    st.subheader("💬 Like this site?")
    if st.button("👍 Give a like", width="stretch"):
        st.session_state.likes += 1
        st.toast("Thanks for the love!", icon="💜")
    st.metric("Likes this session", st.session_state.likes)
    st.divider()

    st.download_button("📄 Download résumé (.txt)", resume_text(),
                       file_name=f"{PROFILE['name'].replace(' ', '_')}_resume.txt",
                       width="stretch")

ACCENT = ACCENTS[accent_name]

# ═══════════════════════════════════════════════════════════════════════════
# STYLING (small, on purpose — theme lives in .streamlit/config.toml)
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    f"""
    <style>
      .hero {{
        background: linear-gradient(135deg, {ACCENT} 0%, #1e1b4b 100%);
        color: white; padding: 2.2rem 2.4rem; border-radius: 20px; margin-bottom: 1rem;
      }}
      .hero h1 {{ color: white; margin: 0; font-size: 2.8rem; }}
      .hero p  {{ margin: .3rem 0 0; font-size: 1.15rem; opacity: .92; }}
      .badge {{
        display:inline-block; background:rgba(255,255,255,.18); color:white;
        padding:.2rem .75rem; border-radius:999px; font-size:.85rem; margin: .8rem .4rem 0 0;
      }}
      .chip {{
        display:inline-block; background:{ACCENT}22; color:{ACCENT};
        padding:.15rem .65rem; border-radius:999px; font-size:.82rem; margin:.1rem .25rem .1rem 0;
        border:1px solid {ACCENT}55; font-weight:600;
      }}
      div[data-testid="stMetric"] {{
        background:{ACCENT}12; border:1px solid {ACCENT}33; padding:.8rem 1rem; border-radius:14px;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════════════════
st.markdown(
    f"""
    <div class="hero">
      <h1>👋 Hi, I'm {PROFILE['name']}</h1>
      <p>{PROFILE['tagline']}</p>
      <span class="badge">🎓 {PROFILE['program']} · {PROFILE['year']}</span>
      <span class="badge">🏫 {PROFILE['school']}</span>
      <span class="badge">📍 {PROFILE['location']}</span>
      <span class="badge">🧾 {PROFILE['section']}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Projects", len(PROJECTS), f"{sum(p['status'] == 'Completed' for p in PROJECTS)} completed")
m2.metric("Skills tracked", len(SKILLS))
m3.metric("Top skill", SKILLS.loc[SKILLS["Level"].idxmax(), "Skill"],
          f"{SKILLS['Level'].max()}/100")
m4.metric("Avg. skill level", f"{SKILLS['Level'].mean():.0f}/100")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ═══════════════════════════════════════════════════════════════════════════
tab_about, tab_story, tab_skills, tab_projects, tab_contact = st.tabs(
    ["🙋 About me", "📖 Autobiography", "🧠 Skills", "🚀 Projects", "✉️ Contact"]
)

# ───────────────────────────── ABOUT ───────────────────────────────────────
with tab_about:
    left, right = st.columns([2, 1], gap="large")
    with left:
        st.header("About me")
        st.write(PROFILE["short_bio"])
        st.subheader("Things I'm into")
        st.markdown("".join(f'<span class="chip">{i}</span>' for i in INTERESTS),
                    unsafe_allow_html=True)

        st.subheader("Get to know me")
        c1, c2 = st.columns(2)
        if c1.button("🎲 Surprise me with a fun fact", width="stretch"):
            st.session_state.fun_fact = random.choice(FUN_FACTS)
        if c2.button("🎈 Celebrate", width="stretch"):
            st.balloons()
        if st.session_state.fun_fact:
            st.info(st.session_state.fun_fact, icon="💡")
    with right:
        with st.container(border=True):
            st.subheader("Quick facts")
            st.markdown(
                f"- **Program:** {PROFILE['program']}\n"
                f"- **Year:** {PROFILE['year']}\n"
                f"- **School:** {PROFILE['school']}\n"
                f"- **Section:** {PROFILE['section']}\n"
                f"- **Based in:** {PROFILE['location']}"
            )
            st.caption(f"Page loaded {datetime.now():%b %d, %Y}")

# ───────────────────────────── AUTOBIOGRAPHY ───────────────────────────────
with tab_story:
    st.header("My story")
    chapter = st.radio("Choose a chapter", ["🌱 Background", "🎓 Education", "🎯 Interests"],
                       horizontal=True)

    if chapter.endswith("Background"):
        st.write(BACKGROUND)
        st.markdown(f"> *{PROFILE['tagline']}*")
    elif chapter.endswith("Education"):
        edu_df = pd.DataFrame(EDUCATION, columns=["Period", "School / Program", "Notes"])
        for period, school, note in EDUCATION:
            with st.container(border=True):
                a, b = st.columns([1, 4])
                a.markdown(f"**{period}**")
                b.markdown(f"**{school}**  \n{note}")
        if show_tables:
            with st.expander("View as table"):
                st.table(edu_df)
    else:
        st.write("Beyond the classroom, here's what keeps me curious:")
        picked = st.multiselect("Pick interests to read about", INTERESTS, default=INTERESTS[:2])
        for i in picked:
            st.markdown(f"- **{i}** — [PLACEHOLDER] why you like it.")

    if show_timeline:
        st.divider()
        st.subheader("⏳ Milestones")
        years = sorted(MILESTONES)
        year = st.select_slider("Slide through the years", options=years, value=years[0])
        title, story = MILESTONES[year]
        with st.container(border=True):
            st.markdown(f"### {year} — {title}")
            st.write(story)
        st.progress((years.index(year) + 1) / len(years),
                    text=f"Milestone {years.index(year) + 1} of {len(years)}")

# ───────────────────────────── SKILLS ──────────────────────────────────────
with tab_skills:
    st.header("Skills")
    st.write("Self-rated from 0 to 100. Use the filters to explore.")

    f1, f2 = st.columns([2, 1])
    cats = f1.multiselect("Categories", sorted(SKILLS["Category"].unique()),
                          default=sorted(SKILLS["Category"].unique()))
    min_level = f2.slider("Minimum level", 0, 100, 0, step=5)

    view = SKILLS[SKILLS["Category"].isin(cats) & (SKILLS["Level"] >= min_level)]

    if view.empty:
        st.warning("No skills match those filters — try lowering the minimum.")
    else:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.subheader("By level")
            st.bar_chart(view.set_index("Skill")["Level"], color=ACCENT, horizontal=True)
        with c2:
            st.subheader("Average by category")
            st.bar_chart(view.groupby("Category")["Level"].mean().round(1), color=ACCENT)

        if show_tables:
            st.dataframe(
                view.sort_values("Level", ascending=False),
                hide_index=True,
                width="stretch",
                column_config={
                    "Level": st.column_config.ProgressColumn("Level", min_value=0, max_value=100,
                                                             format="%d"),
                },
            )

    st.subheader("📈 How I've grown")
    growth_cols = st.multiselect("Compare", list(SKILL_GROWTH.columns),
                                 default=list(SKILL_GROWTH.columns))
    if growth_cols:
        st.line_chart(SKILL_GROWTH[growth_cols])
    st.caption("Growth numbers are my own estimates per year.")

# ───────────────────────────── PROJECTS ────────────────────────────────────
with tab_projects:
    st.header("Projects")

    all_tools = sorted({t for p in PROJECTS for t in p["tools"]})
    p1, p2 = st.columns([2, 1])
    tool_filter = p1.multiselect("Filter by tool", all_tools, placeholder="All tools")
    status_filter = p2.selectbox("Status", ["All", "Completed", "In progress"])

    shown = [
        p for p in PROJECTS
        if (not tool_filter or set(tool_filter) & set(p["tools"]))
        and (status_filter == "All" or p["status"] == status_filter)
    ]

    if not shown:
        st.info("No projects match those filters.")
    cols = st.columns(3, gap="medium")
    for col, p in zip(cols * ((len(shown) // 3) + 1), shown):
        with col, st.container(border=True):
            st.subheader(p["title"])
            st.caption(f"**Role:** {p['role']}")
            st.markdown("".join(f'<span class="chip">{t}</span>' for t in p["tools"]),
                        unsafe_allow_html=True)
            st.write(p["summary"])
            st.success(p["outcome"], icon="✅")
            st.link_button("View project ↗", p["link"], width="stretch")

    if shown and show_tables:
        st.subheader("Effort at a glance")
        effort = pd.DataFrame(shown).set_index("title")["hours"]
        if len(effort) > 1:
            st.area_chart(effort, color=ACCENT)
        else:
            st.bar_chart(effort, color=ACCENT)
        st.caption("Approximate hours spent on each project.")

# ───────────────────────────── CONTACT ─────────────────────────────────────
with tab_contact:
    st.header("Say hello")
    form_col, info_col = st.columns([3, 2], gap="large")

    with form_col:
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Your name *")
            email = st.text_input("Your email *", placeholder="you@example.com")
            reason = st.radio("I'm reaching out about", ["Feedback", "Collaboration", "Just saying hi"],
                              horizontal=True)
            rating = st.slider("How would you rate this site?", 1, 5, 4)
            message = st.text_area("Message *", height=130)
            agree = st.checkbox("I'm okay with being replied to by email")
            submitted = st.form_submit_button("Send message 🚀", type="primary")

        if submitted:
            if not (name.strip() and email.strip() and message.strip()):
                st.error("Please fill in your name, email, and message.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("That email doesn't look right.")
            elif not agree:
                st.warning("Please tick the checkbox so I know I can reply.")
            else:
                st.session_state.messages.append(
                    {"time": datetime.now().strftime("%H:%M:%S"), "from": name, "topic": reason,
                     "rating": rating, "message": message}
                )
                st.success(f"Thanks, {name}! Your {reason.lower()} message was received. "
                           "I'll get back to you soon.")
                st.toast("Message sent!", icon="📬")
                if rating >= 4:
                    st.balloons()

    with info_col:
        with st.container(border=True):
            st.subheader("Other ways to reach me")
            st.markdown(f"📧 {PROFILE['email']}  \n📍 {PROFILE['location']}")
            st.link_button("Open GitHub ↗", PROFILE["github"])

        st.write("**Was this page helpful?**")
        fb = st.feedback("stars")
        if fb is not None:
            st.caption(f"You gave {fb + 1} / 5 — thank you!")

    if st.session_state.messages:
        st.subheader("📬 Messages sent this session")
        st.dataframe(pd.DataFrame(st.session_state.messages), hide_index=True,
                     width="stretch")
        st.caption("Stored in session state only — nothing is saved on a server.")

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════
st.divider()
st.caption(f"© {datetime.now().year} {PROFILE['name']} · {PROFILE['section']} · Built with Streamlit")
