import streamlit as st
import pandas as pd
import os
import uuid
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(page_title="Marks Calculator")

file_name = r"C:\Stattr_Works\Streamlit_Mark_Calculator\student_marks.xlsx"


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Calculate button - Red */
div[data-testid="stButton"]:has(button[kind="primary"]) button {
    background-color: #dc3545 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px;
    font-weight: bold;
}

/* PASS button - Green */
.st-key-pass_button button {
    background-color: #198754 !important;
    color: white !important;
    border: none !important;
    width: 100%;
    border-radius: 8px;
    font-weight: bold;
}

/* FAIL button - Red */
.st-key-fail_button button {
    background-color: #dc3545 !important;
    color: white !important;
    border: none !important;
    width: 100%;
    border-radius: 8px;
    font-weight: bold;
}

/* PASS hover effect */
.st-key-pass_button button:hover {
    background-color: #146c43 !important;
    color: white !important;
}

/* FAIL hover effect */
.st-key-fail_button button:hover {
    background-color: #b02a37 !important;
    color: white !important;
}

/* Calculate hover effect */
div[data-testid="stButton"]:has(button[kind="primary"]) button:hover {
    background-color: #b02a37 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# EXCEL FILE HANDLING
# --------------------------------------------------

columns = [
    "RecordID",
    "Name",
    "Maths",
    "Physics",
    "Chemistry",
    "English",
    "Total",
    "Average",
    "Percentage",
    "Result"
]


def load_records():

    if os.path.exists(file_name):

        df = pd.read_excel(file_name)

        # Support existing Excel files
        if "RecordID" not in df.columns:
            df["RecordID"] = [
                str(uuid.uuid4()) for _ in range(len(df))
            ]

        if "Result" not in df.columns:
            df["Result"] = "Pending"

        df["Result"] = df["Result"].fillna("Pending")

        return df

    return pd.DataFrame(columns=columns)


def save_records(df):

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    df.to_excel(file_name, index=False)


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

defaults = {
    "calculated": False,
    "result_message": None,
    "resume_prompt_shown": False,
    "active_record_id": None,
    "name_input": "",
    "math_input": 0,
    "phy_input": 0,
    "che_input": 0,
    "eng_input": 0,
    "subject_marks":None
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# RESUME PREVIOUS SESSION DIALOG
# --------------------------------------------------

@st.dialog("Welcome Back!")
def resume_dialog(last_record):

    st.write("We found your previous student record.")

    st.write(f"**Last Student:** {last_record['Name']}")

    st.write(f"**Total Marks:** {last_record['Total']}/400")

    st.write(
        f"**Percentage:** {last_record['Percentage']:.2f}%"
    )

    previous_result = str(last_record["Result"]).lower()

    if previous_result == "pending":
        st.warning("Evaluation Status: Pending")

    elif previous_result == "pass":
        st.success("Evaluation Status: PASS")

    elif previous_result == "fail":
        st.error("Evaluation Status: FAIL")

    col1, col2 = st.columns(2)

    # Continue previous session
    with col1:

        if st.button("Continue", use_container_width=True):

            st.session_state.name_input = str(last_record["Name"])

            st.session_state.math_input = int(last_record["Maths"])
            st.session_state.phy_input = int(last_record["Physics"])
            st.session_state.che_input = int(last_record["Chemistry"])
            st.session_state.eng_input = int(last_record["English"])
            st.session_state.subject_marks = {
                "Maths": int(last_record["Maths"]),
                "Physics": int(last_record["Physics"]),
                "Chemistry": int(last_record["Chemistry"]),
                "English": int(last_record["English"])
            }

            st.session_state.total = last_record["Total"]
            st.session_state.avg = last_record["Average"]
            st.session_state.percentage = last_record["Percentage"]

            st.session_state.student_name = last_record["Name"]

            st.session_state.result_message = (
                previous_result
                if previous_result in ["pass", "fail"]
                else None
            )

            st.session_state.active_record_id = str(
                last_record["RecordID"]
            )

            st.session_state.calculated = True
            st.session_state.resume_prompt_shown = True

            st.rerun()

    # Start a new student
    with col2:

        if st.button("Start New", use_container_width=True):

            st.session_state.name_input = ""
            st.session_state.math_input = 0
            st.session_state.phy_input = 0
            st.session_state.che_input = 0
            st.session_state.eng_input = 0

            st.session_state.calculated = False
            st.session_state.result_message = None
            st.session_state.active_record_id = None

            st.session_state.resume_prompt_shown = True

            st.rerun()


# --------------------------------------------------
# CHECK FOR PREVIOUS STUDENT RECORDS
# --------------------------------------------------

old_data = load_records()

if not st.session_state.resume_prompt_shown:

    if not old_data.empty:

        resume_dialog(old_data.iloc[-1])

        st.stop()

    else:

        st.session_state.resume_prompt_shown = True


# --------------------------------------------------
# APPLICATION TITLE
# --------------------------------------------------

st.title("📚 Student Mark Calculator")


# --------------------------------------------------
# INPUT FIELDS
# --------------------------------------------------

name = st.text_input(
    "Enter Student Name",
    key="name_input"
)
col7,col8 = st.columns([1,1])
with col7:
    math = st.number_input(
        "Enter Maths Marks",
        min_value=0,
        max_value=100,
        key="math_input"
    )

with col8:
    phy = st.number_input(
        "Enter Physics Marks",
        min_value=0,
        max_value=100,
        key="phy_input"
    )

with col7:
    che = st.number_input(
        "Enter Chemistry Marks",
        min_value=0,
        max_value=100,
        key="che_input"
    )
with col8:
    eng = st.number_input(
        "Enter English Marks",
        min_value=0,
        max_value=100,
        key="eng_input"
    )

with col7:
    st.markdown(
        """
        <style>
        /* Hide the add-more-files (+) button */
        [data-testid="stFileUploader"] 
        button[aria-label="Add files"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    file_upload = st.file_uploader(
        "Upload Student Marks File (Optional)",
        type=["csv", "xlsx"]
    )





# --------------------------------------------------
# CALCULATE AND SAVE RECORD
# --------------------------------------------------

if st.button("Calculate and Save Record", type="primary"):

    st.toast("Calculating and saving the student record...", icon="💹")

    if not name.strip():

        st.warning("Please enter the student name.")

    else:

        total = math + phy + che + eng

        avg = total / 4

        percentage = (total / 400) * 100

        subject_marks = {
            "Maths": math,
            "Physics": phy,
            "Chemistry": che,
            "English": eng
        }
        st.session_state.subject_marks = subject_marks

        new_data = pd.DataFrame({

            "RecordID": [str(uuid.uuid4())],

            "Name": [name],
            "Maths": [math],
            "Physics": [phy],
            "Chemistry": [che],
            "English": [eng],

            "Total": [total],
            "Average": [avg],
            "Percentage": [percentage],

            "Result": ["Pending"]
        })

        old_data = load_records()

        updated_data = pd.concat(
            [old_data, new_data],
            ignore_index=True
        )

        save_records(updated_data)

        # Store calculated results
        st.session_state.total = total
        st.session_state.avg = avg
        st.session_state.percentage = percentage

        st.session_state.student_name = name

        st.session_state.active_record_id = (
            new_data.iloc[0]["RecordID"]
        )

        st.session_state.calculated = True

        st.session_state.result_message = None


# --------------------------------------------------
# CONFIRMATION DIALOG
# --------------------------------------------------

@st.dialog("Confirm your action")
def confirm_result(result):

    st.write(
        f"Are you sure you want to mark this student as {result.upper()}?"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Confirm", use_container_width=True):

            records = load_records()

            record_id = st.session_state.active_record_id

            matching_rows = (
                records["RecordID"].astype(str) == str(record_id)
            )

            if matching_rows.any():

                records.loc[matching_rows, "Result"] = result.capitalize()

                save_records(records)

                st.session_state.result_message = result

                st.rerun()

            else:

                st.error("Student record not found.")

    with col2:

        if st.button("Back", use_container_width=True):

            st.rerun()


# --------------------------------------------------
# DISPLAY CALCULATED RESULTS
# --------------------------------------------------

if st.session_state.calculated:

    st.success("Calculation Completed!")

    st.write("## Results")

    st.write(
        "#### Student Name:",
        st.session_state.student_name
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total",
        f"{st.session_state.total}/400"
    )

    col2.metric(
        "Average",
        f"{st.session_state.avg:.2f}"
    )

    col3.metric(
        "Percentage",
        f"{st.session_state.percentage:.2f}%"
    )


    # --------------------------------------------------
    # SUBJECT-WISE MARKS VISUALIZATION
    # --------------------------------------------------

    st.write("## 📊 Subject-wise Performance")

    subject_df = pd.DataFrame({
        "Subject": list(st.session_state.subject_marks.keys()),
        "Marks": list(st.session_state.subject_marks.values())
    })

    col1, col2 = st.columns(2)

    # BAR CHART
    with col1:

        st.write("### Subject-wise Marks")

        bar_fig = px.bar(
            subject_df,
            x="Subject",
            y="Marks",
            text="Marks",
            color="Subject",
            title="Marks Obtained in Each Subject"
        )

        bar_fig.update_layout(
            yaxis_title="Marks (out of 100)",
            xaxis_title="Subjects",
            yaxis=dict(range=[0, 110]),
            showlegend=False
        )

        bar_fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            bar_fig,
            use_container_width=True
        )

    # PIE CHART
    with col2:

        st.write("### Marks Distribution")

        pie_fig = px.pie(
            subject_df,
            names="Subject",
            values="Marks",
            title="Subject-wise Contribution to Total Marks",
            hole=0.35
        )

        pie_fig.update_traces(
            textinfo="label+percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Marks: %{value}/100<br>"
                "Contribution: %{percent}"
                "<extra></extra>"
            )
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

    st.divider()


    st.success("Student record saved successfully!")

    # Display current evaluation status
    if st.session_state.result_message == "pass":

        st.success("✅ Student Passed Hurray!")

    elif st.session_state.result_message == "fail":

        st.error("❌ Student Failed!")

    else:

        st.warning("⏳ Evaluation Pending - Select PASS or FAIL.")

    st.divider()


    # --------------------------------------------------
    # PASS AND FAIL BUTTONS
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col2:

        with st.container(key="pass_button"):

            if st.button(
                "PASS",
                key="pass",
                use_container_width=True
            ):

                confirm_result("pass")

    with col3:

        with st.container(key="fail_button"):

            if st.button(
                "FAIL",
                key="fail",
                use_container_width=True
            ):

                confirm_result("fail")
