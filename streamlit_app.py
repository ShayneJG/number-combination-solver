#!/usr/bin/env python3
"""
Streamlit web app for the Number Combinations Solver.
Find expressions using integers and operators to reach a target number.
"""

import streamlit as st
import time


# ============== Core Logic (from number_combinations.py) ==============

from number_combinations import *

# ============== Streamlit UI ==============

st.set_page_config(
    page_title="Number Combinations Solver",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Number Combinations Solver")
st.markdown("Find expressions using integers and operators to reach a target number.")

# Input section
col1, col2 = st.columns(2)

with col1:
    target = st.number_input("Target Number", value=100, min_value=1, step=1)
    max_int = st.number_input("Maximum Integer", value=9, min_value=1, max_value=20, step=1)

with col2:
    max_numbers = st.slider("Max Numbers in Expression", min_value=2, max_value=10, value=6)
    top_n = st.slider("Number of Solutions", min_value=1, max_value=20, value=5)

# Operators
st.subheader("Operators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    use_add = st.checkbox("Addition (+)", value=True, disabled=True)
with col2:
    use_multiply = st.checkbox("Multiplication (×)", value=True)
with col3:
    use_subtract = st.checkbox("Subtraction (−)", value=True)
with col4:
    use_divide = st.checkbox("Division (÷)", value=False)

# Exclude numbers
exclude_input = st.text_input(
    "Exclude Numbers (comma-separated)", 
    placeholder="e.g., 10, 11, 12",
    help="Numbers to exclude from available integers"
)

exclude = []
if exclude_input.strip():
    try:
        exclude = [int(x.strip()) for x in exclude_input.split(",") if x.strip()]
    except ValueError:
        st.error("Invalid exclude list. Please enter comma-separated numbers.")

# Mode
exhaustive = st.checkbox(
    "Exhaustive Search", 
    value=False,
    help="Guaranteed optimal results but slower. Use for important searches."
)

# Search button
if st.button("🔍 Find Solutions", type="primary", use_container_width=True):
    # Build description
    available = [n for n in range(1, max_int + 1) if n not in exclude]
    
    if not available:
        st.error("No numbers available after exclusions!")
    else:
        ops_list = ["addition"]
        if use_multiply:
            ops_list.append("multiplication")
        if use_subtract:
            ops_list.append("subtraction")
        if use_divide:
            ops_list.append("division")
        
        st.info(f"Searching for **{target}** using integers {', '.join(map(str, available[:5]))}{'...' if len(available) > 5 else ''} with {', '.join(ops_list)}")
        
        progress_placeholder = st.empty()
        
        def update_progress(msg):
            progress_placeholder.text(msg)
        
        start_time = time.time()
        
        with st.spinner("Searching..."):
            solutions = find_solutions(
                target=target,
                max_int=max_int,
                allow_multiply=use_multiply,
                allow_subtract=use_subtract,
                allow_divide=use_divide,
                exclude=exclude,
                max_numbers=max_numbers,
                top_n=top_n,
                exhaustive=exhaustive,
                progress_callback=update_progress
            )
        
        elapsed = time.time() - start_time
        progress_placeholder.empty()
        
        if not solutions:
            st.warning(f"No solutions found. (searched in {elapsed:.2f}s)")
        else:
            st.success(f"Found {len(solutions)} solution(s) in {elapsed:.2f}s")
            
            for i, sol in enumerate(solutions, 1):
                unique_str = ", ".join(str(n) for n in sol.unique_nums)
                
                with st.container():
                    st.markdown(f"""
                    **{i}.** `{sol.expression}` = **{sol.result}**
                    
                    <small>Unique integers: {unique_str} ({len(sol.unique_nums)}) • Operations: {sol.op_count}</small>
                    """, unsafe_allow_html=True)
                    st.divider()

# Footer
st.markdown("---")
st.markdown(
    "<small>Uses meet-in-the-middle algorithm for fast searching. "
    "Enable 'Exhaustive Search' for guaranteed optimal results.</small>",
    unsafe_allow_html=True
)
