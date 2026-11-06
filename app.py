
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Marks Calculator")

# Custom CSS
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


st.title("📚 Student Mark Calculator")

# Input fields
name = st.text_input("Enter Student Name")
math = st.number_input("Enter Maths Marks", min_value=0, max_value=100)
phy = st.number_input("Enter Physics Marks", min_value=0, max_value=100)
che = st.number_input("Enter Chemistry Marks", min_value=0, max_value=100)
eng = st.number_input("Enter English Marks", min_value=0, max_value=100)


# Initialize session state
if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "result_message" not in st.session_state:
    st.session_state.result_message = None


# Calculate and Save Record button
if st.button("Calculate and Save Record", type="primary"):

    total = math + phy + che + eng
    avg = total / 4
    percentage = (total / 400) * 100

    new_data = pd.DataFrame({
        "Name": [name],
        "Maths": [math],
        "Physics": [phy],
        "Chemistry": [che],
        "English": [eng],
        "Total": [total],
        "Average": [avg],
        "Percentage": [percentage]
    })

    file_name = r"C:\Stattr_Works\Streamlit_Mark_Calculator\student_marks.xlsx"

    if os.path.exists(file_name):
        old_data = pd.read_excel(file_name)
        updated_data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_excel(file_name, index=False)

    # Store results in session state
    st.session_state.total = total
    st.session_state.avg = avg
    st.session_state.percentage = percentage
    st.session_state.student_name = name
    st.session_state.calculated = True
    st.session_state.result_message = None


# Display results
if st.session_state.calculated:

    st.success("Calculation Completed!")

    st.write("## Results")
    st.write("#### Student Name:", st.session_state.student_name)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total", f"{st.session_state.total}/400")
    col2.metric("Average", f"{st.session_state.avg:.2f}")
    col3.metric("Percentage", f"{st.session_state.percentage:.2f}%")

    st.success("Student record saved successfully!")

    st.divider()

    # PASS and FAIL buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    @st.dialog("Confirm your action")
    def confirm_result(result):
        st.write(f"Are you sure you want to mark this student as {result.upper()}?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Confirm", use_container_width=True):
                st.session_state.result_message = result
                st.rerun()

        with col2:
            if st.button("Back", use_container_width=True):
                st.rerun()

    with col2:
        with st.container(key="pass_button"):
            if st.button("PASS", key="pass", use_container_width=True):
                confirm_result("pass")

    with col3:
        with st.container(key="fail_button"):
            if st.button("FAIL", key="fail", use_container_width=True):
                confirm_result("fail")

    # Display selected result
    if st.session_state.result_message == "pass":
        st.success("✅ Student Passed Hurray!")

    elif st.session_state.result_message == "fail":
        st.error("❌ Student Failed!")
