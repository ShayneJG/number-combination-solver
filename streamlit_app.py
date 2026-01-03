#!/usr/bin/env python3
"""
Streamlit web app for the Number Combinations Solver.
Find expressions using integers and operators to reach a target number.
"""

import streamlit as st
import time
import re
import urllib.parse
from pathlib import Path
import streamlit.components.v1 as components

# ============== Core Logic (from number_combinations.py) ==============

from number_combinations import *

# ============== Render Functions ==============

def render_solver():
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

def render_mermaid(code: str, height: int = 600):
    """Render mermaid code using an HTML component."""
    # Escape single quotes and backslashes for the template
    escaped_code = code.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    
    components.html(
        f"""
        <div class="mermaid-container" style="background-color: white; border-radius: 8px; padding: 10px; min-height: {height-40}px;">
            <pre class="mermaid">
{escaped_code}
            </pre>
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose',
                useMaxWidth: true
            }});
        </script>
        """,
        height=height,
        scrolling=False
    )

def render_docs():
    st.markdown("### 📚 Project Documentation")
    
    # scan for docs
    docs_dir = Path("docs")
    if not docs_dir.exists():
        st.error("Documentation directory not found!")
        return

    # Gather all markdown files
    files = sorted(list(docs_dir.rglob("*.md")))
    
    if not files:
        st.warning("No documentation files found.")
        return

    # Create mappings for display logic
    file_map = {}
    path_to_key = {}
    
    for f in files:
        # Create cleaner names
        name = str(f.relative_to(docs_dir)).replace("\\", "/").replace(".md", "")
        if name == "README":
            name = "Documentation Index"
            
        # Title case
        name = " / ".join(part.replace("-", " ").title() for part in name.split("/"))
        file_map[name] = f
        
        # Store absolute resolved path logic for linking
        # Use simple string matching for now to avoid complexity
        path_to_key[str(f.resolve()).lower()] = name

    # Determine default selection from Query Params
    qp = st.query_params
    default_index = 0
    if "doc" in qp:
        target_doc = qp["doc"]
        if target_doc in file_map:
            try:
                default_index = list(file_map.keys()).index(target_doc)
            except ValueError:
                pass

    # Selection 
    selected_name = st.selectbox("Select Document", list(file_map.keys()), index=default_index)
    
    # Update query params on change (optional, but st.selectbox handles state)
    # We can't easily pushState without reload in basic Streamlit, but selection works.
    
    if selected_name:
        file_path = file_map[selected_name]
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # --- Link Pre-processing ---
            # Replace [Text](path/to/file.md) with <a href="?doc=Key">Text</a>
            
            def replace_link(match):
                text = match.group(1)
                link = match.group(2)
                
                # Ignore external links or non-md
                if link.startswith("http") or not link.endswith(".md"):
                    return match.group(0)
                
                # Resolve relative path
                # Base is current file_path parent
                try:
                    target_path = (file_path.parent / link).resolve()
                    target_key = path_to_key.get(str(target_path).lower())
                    
                    if target_key:
                        # Encode for URL
                        encoded_key = urllib.parse.quote(target_key)
                        return f'<a href="?doc={encoded_key}" target="_self">{text}</a>'
                except Exception:
                    pass
                
                return match.group(0)

            # Apply regex
            # Pattern: [Label](Link)
            processed_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
            
            st.markdown("---")
            
            # --- Mermaid Rendering ---
            # Split by mermaid blocks
            parts = re.split(r'(```mermaid\n.*?\n```)', processed_content, flags=re.DOTALL)
            
            for part in parts:
                if part.startswith("```mermaid"):
                    # Extract code
                    match = re.search(r'```mermaid\n(.*?)\n```', part, re.DOTALL)
                    if match:
                        mermaid_code = match.group(1)
                        # Find a reasonable title for the expander
                        with st.expander("📊 View Algorithm Flowchart", expanded=True):
                            render_mermaid(mermaid_code, height=800)
                elif part.strip():
                    st.markdown(part, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error reading file: {e}")


# ============== Main App Entry ==============

st.set_page_config(
    page_title="Number Combinations Solver",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Number Combinations Solver")

# Tab Navigation
# Check for deep link to determine tab order/active tab
start_on_docs = "doc" in st.query_params

if start_on_docs:
    tab_docs, tab_solver = st.tabs(["📚 Documentation", "🔍 Solver"])
    
    with tab_docs:
        render_docs()
    with tab_solver:
        render_solver()
else:
    tab_solver, tab_docs = st.tabs(["🔍 Solver", "📚 Documentation"])
    
    with tab_solver:
        render_solver()
    with tab_docs:
        render_docs()
