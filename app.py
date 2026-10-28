import streamlit as st

from config import (
    APP_NAME,
    APP_DESCRIPTION,
    GROQ_MODELS,
    GEMINI_MODELS,
)

from llm import ask_llm


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎓",
    layout="wide",
)


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "provider" not in st.session_state:
    st.session_state.provider = "Groq"


# ==================================================
# TITLE
# ==================================================

st.title("🎓 PlacementMentor")

st.caption(APP_DESCRIPTION)

st.markdown(
    """
    Prepare smarter for placements with personalized
    roadmaps, DSA, technical interviews, HR interviews,
    coding practice and mock interviews.
    """
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Configuration")

    # --------------------------------------------------
    # AI PROVIDER
    # --------------------------------------------------

    provider = st.selectbox(
        "AI Provider",
        [
            "Groq",
            "Google Gemini",
        ],
        key="provider_select",
    )

    st.session_state.provider = provider

    # --------------------------------------------------
    # MODEL
    # --------------------------------------------------

    if provider == "Groq":

        model = st.selectbox(
            "Groq Model",
            GROQ_MODELS,
            key="groq_model",
        )

    else:

        model = st.selectbox(
            "Gemini Model",
            GEMINI_MODELS,
            key="gemini_model",
        )

    # --------------------------------------------------
    # API KEY
    # --------------------------------------------------

    api_key_input = st.text_input(
        f"{provider} API Key",
        type="password",
        placeholder="Enter your API key",
        key="api_key_input",
    )

    if api_key_input:
        st.session_state.api_key = api_key_input

    if st.session_state.api_key:
        st.success("✅ API key entered")
    else:
        st.warning("⚠️ Enter your API key")

    st.divider()

    # ==================================================
    # STUDENT PROFILE
    # ==================================================

    st.header("👨‍🎓 Student Profile")

    name = st.text_input(
        "Name",
        placeholder="Your name",
        key="student_name",
    )

    degree = st.text_input(
        "Degree",
        placeholder="B.Tech / B.E / MCA / etc.",
        key="student_degree",
    )

    branch = st.text_input(
        "Branch",
        placeholder="CSE / ECE / IT / etc.",
        key="student_branch",
    )

    year = st.selectbox(
        "Academic Year",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year",
            "Graduate",
        ],
        key="student_year",
    )

    languages = st.text_input(
        "Programming Languages",
        placeholder="Python, Java, C++",
        key="student_languages",
    )

    skills = st.text_area(
        "Current Skills",
        placeholder="Python, SQL, ML, React...",
        key="student_skills",
    )

    target_role = st.text_input(
        "Target Role",
        placeholder="Software Developer / Data Scientist",
        key="target_role",
    )

    company = st.text_input(
        "Target Company",
        placeholder="TCS / Infosys / Google / etc.",
        key="target_company",
    )

    duration = st.text_input(
        "Preparation Duration",
        placeholder="3 months / 6 months",
        key="preparation_duration",
    )

    # --------------------------------------------------
    # SAVE STUDENT PROFILE
    # --------------------------------------------------

    st.session_state.profile = {
        "name": name,
        "degree": degree,
        "branch": branch,
        "year": year,
        "languages": languages,
        "skills": skills,
        "target_role": target_role,
        "company": company,
        "duration": duration,
    }


# ==================================================
# TABS
# ==================================================

tab_chat, tab_roadmap, tab_skills, tab_dsa, tab_interview, tab_mock = st.tabs(
    [
        "💬 AI Chat",
        "🧭 Roadmap",
        "💻 Skills",
        "🧩 DSA",
        "🎯 Interview",
        "🤖 Mock Interview",
    ]
)


# ==================================================
# AI CHAT
# ==================================================

with tab_chat:

    st.subheader("💬 Placement Assistant")

    st.write(
        "Ask anything related to placement preparation."
    )

    # --------------------------------------------------
    # DISPLAY PREVIOUS MESSAGES
    # --------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    # --------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------

    user_input = st.chat_input(
        "Ask your placement question..."
    )

    if user_input:

        # Check API key before sending request

        if not st.session_state.api_key:

            st.error(
                "⚠️ Please enter your API key in the sidebar first."
            )

        else:

            # Add user message

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )

            with st.chat_message("user"):

                st.markdown(user_input)

            try:

                with st.chat_message("assistant"):

                    with st.spinner(
                        "Thinking..."
                    ):

                        answer = ask_llm(
                            provider,
                            st.session_state.api_key,
                            model,
                            st.session_state.messages,
                            st.session_state.profile,
                        )

                    st.markdown(answer)

                # Save assistant response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


# ==================================================
# ROADMAP
# ==================================================

with tab_roadmap:

    st.subheader(
        "🧭 Personalized Placement Roadmap"
    )

    st.write(
        "Generate a roadmap based on your student profile."
    )

    if st.button(
        "Generate My Roadmap",
        key="roadmap_button",
    ):

        if not st.session_state.api_key:

            st.error(
                "⚠️ Please enter your API key in the sidebar first."
            )

        else:

            prompt = """
Create a personalized placement preparation roadmap
for this student.

Analyze:

1. Current skill level
2. Target role
3. Required technologies
4. Important concepts
5. DSA requirements
6. Projects
7. Interview preparation

Classify everything into:

- MUST LEARN
- GOOD TO LEARN
- ADVANCED

Create a weekly preparation plan.

Also provide:

- Daily practice strategy
- Coding strategy
- Interview strategy
- Final placement checklist

Keep the roadmap practical and beginner-friendly.
"""

            try:

                with st.spinner(
                    "Creating your roadmap..."
                ):

                    answer = ask_llm(
                        provider,
                        st.session_state.api_key,
                        model,
                        [
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        st.session_state.profile,
                    )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


# ==================================================
# SKILLS
# ==================================================

with tab_skills:

    st.subheader(
        "💻 Skills & Technology Analyzer"
    )

    st.write(
        "Find the technologies and skills required for your target role."
    )

    if st.button(
        "Analyze Required Skills",
        key="skills_button",
    ):

        if not st.session_state.api_key:

            st.error(
                "⚠️ Please enter your API key in the sidebar first."
            )

        else:

            prompt = """
Analyze the skills and technologies required for
the student's target role.

Provide:

1. Programming languages
2. Frameworks
3. Databases
4. Tools
5. Cloud technologies
6. Core CS concepts
7. DSA requirements
8. Projects to build
9. Interview topics

For every skill classify it as:

MUST LEARN
GOOD TO LEARN
ADVANCED
"""

            try:

                with st.spinner(
                    "Analyzing skills..."
                ):

                    answer = ask_llm(
                        provider,
                        st.session_state.api_key,
                        model,
                        [
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        st.session_state.profile,
                    )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


# ==================================================
# DSA
# ==================================================

with tab_dsa:

    st.subheader(
        "🧩 Data Structures & Algorithms"
    )

    st.write(
        "Build your DSA preparation plan."
    )

    if st.button(
        "Generate DSA Plan",
        key="dsa_button",
    ):

        if not st.session_state.api_key:

            st.error(
                "⚠️ Please enter your API key in the sidebar first."
            )

        else:

            prompt = """
Create a structured DSA preparation plan.

Cover:

1. Arrays
2. Strings
3. Linked Lists
4. Stacks
5. Queues
6. Hashing
7. Recursion
8. Sorting
9. Searching
10. Trees
11. Binary Search Trees
12. Graphs
13. Heaps
14. Greedy algorithms
15. Dynamic Programming

For every topic provide:

- Concepts
- Important patterns
- Difficulty
- Practice strategy
- Interview importance

Also create a recommended learning order.
"""

            try:

                with st.spinner(
                    "Creating DSA plan..."
                ):

                    answer = ask_llm(
                        provider,
                        st.session_state.api_key,
                        model,
                        [
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        st.session_state.profile,
                    )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


# ==================================================
# INTERVIEW
# ==================================================

with tab_interview:

    st.subheader(
        "🎯 Interview Preparation"
    )

    interview_type = st.selectbox(
        "Interview Type",
        [
            "Technical Interview",
            "Coding Interview",
            "HR Interview",
        ],
        key="interview_type",
    )

    if st.button(
        "Generate Interview Questions",
        key="interview_button",
    ):

        if not st.session_state.api_key:

            st.error(
                "⚠️ Please enter your API key in the sidebar first."
            )

        else:

            prompt = f"""
Prepare the student for a {interview_type}.

Generate:

1. Important questions
2. Expected answers
3. Concepts being tested
4. Common mistakes
5. Interview tips

Make the questions appropriate for
the student's target role and current skill level.
"""

            try:

                with st.spinner(
                    "Preparing interview questions..."
                ):

                    answer = ask_llm(
                        provider,
                        st.session_state.api_key,
                        model,
                        [
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        st.session_state.profile,
                    )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


# ==================================================
# MOCK INTERVIEW
# ==================================================

with tab_mock:

    st.subheader(
        "🤖 AI Mock Interview"
    )

    st.write(
        "Practice answering interview questions with AI."
    )

    if st.button(
        "Start Mock Interview",
        key="mock_button",
    ):

        if not st.session_state.api_key:

            st.error(
                "⚠️ Please enter your API key in the sidebar first."
            )

        else:

            prompt = """
Act as an interviewer.

Start a placement mock interview.

Rules:

- Ask only ONE question at a time.
- Start with an introduction question.
- Wait for the student's answer.
- Evaluate the answer.
- Give a score out of 10.
- Give constructive feedback.
- Then ask the next question.

Mix:

- Technical questions
- Coding questions
- Project questions
- HR questions
"""

            try:

                with st.spinner(
                    "Starting interview..."
                ):

                    answer = ask_llm(
                        provider,
                        st.session_state.api_key,
                        model,
                        [
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                        st.session_state.profile,
                    )

                st.markdown(answer)

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )