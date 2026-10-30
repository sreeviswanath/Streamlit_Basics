import streamlit as st

st.set_page_config(page_title="Marks Calculator")

st.title("📚 Student Mark Calculator")

# Input fields
name = st.text_input("Enter Student Name")
math = st.number_input("Enter Maths Marks", min_value=0, max_value=100)
phy = st.number_input("Enter Physics Marks", min_value=0, max_value=100)
che = st.number_input("Enter Chemistry Marks", min_value=0, max_value=100)
eng = st.number_input("Enter English Marks", min_value=0, max_value=100)


# Button
if st.button("Calculate"):

    total = math + phy + che + eng
    avg = total / 4
    percentage = (total / 400) * 100

    st.success("Calculation Completed!")

    st.write("## Results")
    st.write("#### Student Name:",name)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total", f"{total}/400")
    col2.metric("Average", f"{avg:.2f}")
    col3.metric("Percentage", f"{percentage:.2f}%")