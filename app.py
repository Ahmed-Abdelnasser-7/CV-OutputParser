import streamlit as st
import requests
from pypdf import PdfReader


# ============================================================
# Streamlit configuration
# ============================================================

st.set_page_config(
    page_title="CV Analyzer",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# AI Inference Server
# ============================================================

AI_SERVER_URL = "http://127.0.0.1:8000"


# ============================================================
# PDF extraction
# ============================================================

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)

    text = "\n\n".join(
        (page.extract_text() or "")
        for page in reader.pages
    ).strip()

    return text


# ============================================================
# Call the AI inference server
# ============================================================

def analyze_cv(cv_text):

    response = requests.post(
        f"{AI_SERVER_URL}/analyze",
        json={
            "cv_text": cv_text
        },
        timeout=300
    )

    response.raise_for_status()

    response_data = response.json()

    return response_data["result"]


# ============================================================
# Display helper
# ============================================================

def show_item(title, item, fields):

    with st.container(border=True):

        st.markdown(
            f"### {item.get(title, 'Item')}"
        )

        for label, key in fields:

            value = item.get(key)

            if value:

                if isinstance(value, list):
                    value = ", ".join(map(str, value))

                st.write(
                    f"**{label}:** {value}"
                )


# ============================================================
# Streamlit UI
# ============================================================

st.title("📄 CV Analyzer")

st.write(
    "Upload a CV and parse it into clear, structured sections."
)


uploaded_file = st.file_uploader(
    "Upload your CV",
    type=["pdf"]
)


if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🔍 Analyze / Parse CV",
        type="primary"
    ):

        try:

            # ------------------------------------------------
            # Step 1: Extract text from PDF
            # ------------------------------------------------

            with st.spinner(
                "Extracting text from CV..."
            ):

                cv_text = extract_pdf_text(
                    uploaded_file
                )


            if not cv_text:

                st.error(
                    "No text could be extracted. "
                    "This may be a scanned/image-only PDF "
                    "and would need OCR."
                )

                st.stop()


            # ------------------------------------------------
            # Step 2: Send CV text to FastAPI
            # ------------------------------------------------

            with st.spinner(
                "Analyzing CV with Mistral..."
            ):

                st.session_state["cv_result"] = analyze_cv(
                    cv_text
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the AI inference server. "
                "Make sure the FastAPI server is running "
                "on port 8000 in the notebook."
            )


        except requests.exceptions.Timeout:

            st.error(
                "The AI inference server took too long "
                "to respond. The CV analysis timed out."
            )


        except requests.exceptions.HTTPError as e:

            st.error(
                f"The AI inference server returned an error: {e}"
            )

            try:
                st.json(e.response.json())
            except Exception:
                pass


        except Exception as e:

            st.error(
                f"Could not analyze the CV: {e}"
            )


# ============================================================
# Display CV result
# ============================================================

if "cv_result" in st.session_state:

    data = st.session_state["cv_result"]

    st.divider()

    st.header("CV Analysis")


    # ========================================================
    # Personal Information
    # ========================================================

    st.subheader("👤 Personal Information")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"**Name:** "
            f"{data.get('full_name') or 'Not found'}"
        )

        st.markdown(
            f"**Email:** "
            f"{data.get('email') or 'Not found'}"
        )

        st.markdown(
            f"**Phone:** "
            f"{data.get('phone') or 'Not found'}"
        )


    with c2:

        st.markdown(
            f"**LinkedIn:** "
            f"{data.get('linkedin') or 'Not found'}"
        )

        st.markdown(
            f"**GitHub:** "
            f"{data.get('github') or 'Not found'}"
        )


    # ========================================================
    # Profile
    # ========================================================

    if data.get("profile"):

        st.subheader("📝 About / Profile")

        st.write(
            data["profile"]
        )


    # ========================================================
    # Education
    # ========================================================

    st.subheader("🎓 Education")

    education = data.get(
        "education",
        []
    )

    if education:

        for item in education:

            show_item(
                "degree",
                item,
                [
                    ("Institution", "institution"),
                    ("Location", "location"),
                    ("Start date", "start_date"),
                    ("End date", "end_date"),
                    ("Details", "details"),
                ]
            )

    else:

        st.info(
            "No education information found."
        )


    # ========================================================
    # Experience
    # ========================================================

    st.subheader("💼 Experience")

    experience = data.get(
        "experience",
        []
    )

    if experience:

        for item in experience:

            show_item(
                "job_title",
                item,
                [
                    ("Company", "company"),
                    ("Location", "location"),
                    ("Start date", "start_date"),
                    ("End date", "end_date"),
                    ("Description", "description"),
                ]
            )

    else:

        st.info(
            "No professional work experience found."
        )


    # ========================================================
    # Projects
    # ========================================================

    st.subheader("🚀 Projects")

    projects = data.get(
        "projects",
        []
    )

    if projects:

        for item in projects:

            show_item(
                "project_name",
                item,
                [
                    ("Dates", "dates"),
                    ("Technologies", "technologies"),
                    ("Description", "description"),
                ]
            )

    else:

        st.info(
            "No projects found."
        )


    # ========================================================
    # Skills
    # ========================================================

    st.subheader("🛠️ Skills")

    skills = data.get(
        "skills",
        []
    )

    if skills:

        cols = st.columns(3)

        for i, skill in enumerate(skills):

            cols[i % 3].markdown(
                f"- {skill}"
            )

    else:

        st.info(
            "No skills found."
        )


    # ========================================================
    # Languages
    # ========================================================

    st.subheader("🌐 Languages")

    languages = data.get(
        "languages",
        []
    )

    if languages:

        for language in languages:

            st.markdown(
                f"- {language}"
            )

    else:

        st.info(
            "No languages found."
        )


    # ========================================================
    # Certifications
    # ========================================================

    st.subheader("🏆 Certifications / Awards")

    certifications = data.get(
        "certifications",
        []
    )

    if certifications:

        for certification in certifications:

            st.markdown(
                f"- {certification}"
            )

    else:

        st.info(
            "No certifications or awards found."
        )


    # ========================================================
    # Raw JSON
    # ========================================================

    with st.expander("View parsed JSON"):

        st.json(data)