# pyrefly: ignore [missing-import]
import streamlit as st
import config
import review_service
import ui_components

# Page configurations
st.set_page_config(
    page_title="Antigravity AI Code Reviewer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "review_results" not in st.session_state:
    st.session_state.review_results = None
if "history" not in st.session_state:
    st.session_state.history = []
if "last_language" not in st.session_state:
    st.session_state.last_language = "Python"

# Apply Custom CSS
ui_components.inject_custom_css()

# --- SIDEBAR CONFIGURATION ---
st.sidebar.markdown(
    """
    <div class="sidebar-logo">
        <h2 style="color: #6366f1; margin-bottom: 0;">🔍 AI REVIEWER</h2>
        <span style="color: #64748b; font-size: 12px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;">Groq Llama-3 Powered</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# API Key Section
st.sidebar.subheader("Configuration")
env_key = config.GROQ_API_KEY

if env_key:
    api_key = env_key
    st.sidebar.markdown(
        """
        <div style="background-color: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 10px 14px; border-radius: 8px; margin-bottom: 15px;">
            <span style="color: #10b981; font-weight: 600; font-size: 14px;">🔑 API Key Loaded</span><br/>
            <span style="color: #a7f3d0; font-size: 11px;">Environment variable detected</span>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    api_key = st.sidebar.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        value=st.session_state.groq_api_key,
        help="Get your API key from console.groq.com"
    )
    if api_key:
        st.session_state.groq_api_key = api_key
    else:
        st.sidebar.warning("⚠️ Please provide a Groq API Key to proceed.")

# Language Selector
st.sidebar.subheader("Language & Model")
languages = list(config.SUPPORTED_LANGUAGES.keys()) + ["Other"]
selected_lang = st.sidebar.selectbox(
    "Source Language",
    options=languages,
    index=languages.index(st.session_state.last_language) if st.session_state.last_language in languages else 0
)

# Update state if language changes to load corresponding template code
if selected_lang != st.session_state.last_language:
    st.session_state.last_language = selected_lang
    st.session_state.review_results = None  # Reset results on language change to keep clean

# Model Display (fixed to llama3-70b-8192 as required)
st.sidebar.text_input("Active Model", value=config.GROQ_MODEL, disabled=True)

# App Info Box
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.markdown(
    """
    This tool audits your code for quality and safety.
    
    **Audit dimensions:**
    - Logical Bugs
    - Security Flaws
    - Speed/Memory Optimizations
    - Readability Improvements
    - Coding Best Practices
    """
)

# Reset Button
if st.sidebar.button("Clear App Session", type="secondary"):
    st.session_state.review_results = None
    st.session_state.history = []
    st.rerun()

# --- MAIN CONTENT AREA ---
ui_components.render_header()

# Layout: Split into Input Pane and Results Pane (when available)
if st.session_state.review_results is None:
    # Only input form is visible
    st.subheader("Submit Code for Review")
else:
    col1, col2 = st.columns([1, 1])
    
# Input block creation
def render_input_form(api_key):
    # Choose between paste or upload
    input_method = st.radio("Choose Input Method:", ["Paste Code Snippet", "Upload File"], horizontal=True)
    
    input_code = ""
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Drag and drop your source file here",
            type=["py", "js", "ts", "java", "cpp", "h", "sql", "go", "rs", "html", "css", "txt"]
        )
        if uploaded_file is not None:
            try:
                input_code = uploaded_file.read().decode("utf-8")
                st.success(f"Successfully uploaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    else:
        # Load snippet template or default blank
        default_snippet = config.SUPPORTED_LANGUAGES.get(selected_lang, "# Enter your code here...")
        input_code = st.text_area(
            "Paste your code here:",
            value=default_snippet,
            height=300,
            help="Paste the raw source code you want the AI to review."
        )

    submit_button = st.button("Review Code 🔍", type="primary", use_container_width=True)
    
    if submit_button:
        if not api_key:
            st.error("Missing API Key! Please configure the Groq API key in the sidebar.")
            return
            
        if not input_code.strip() or input_code == "# Enter your code here...":
            st.error("Please enter or upload valid code snippet to review.")
            return
            
        with st.spinner("Analyzing code for logical bugs, security gaps, performance Bottlenecks, and style guidelines..."):
            result = review_service.review_code(input_code, selected_lang, api_key)
            
            if result.get("success"):
                data = result["data"]
                st.session_state.review_results = {
                    "original_code": input_code,
                    "language": selected_lang,
                    "summary": data.get("summary", {}),
                    "issues": data.get("issues", []),
                    "improved_code": data.get("improved_code", input_code)
                }
                # Log to session history
                st.session_state.history.append({
                    "language": selected_lang,
                    "score": data.get("summary", {}).get("score", 100),
                    "issues_count": len(data.get("issues", []))
                })
                st.rerun()
            else:
                st.error(result.get("error", "An unknown error occurred during code analysis."))
                if "raw_response" in result and result["raw_response"]:
                    with st.expander("Show raw API response for debugging"):
                        st.code(result["raw_response"])

# Render the layout based on execution state
if st.session_state.review_results is None:
    # Full width input
    render_input_form(api_key)
else:
    # Split view: Input on Left, Results on Right
    with col1:
        st.subheader("Source Code Input")
        render_input_form(api_key)
        
        # Display the code submitted
        st.subheader("Submitted Code Preview")
        st.code(st.session_state.review_results["original_code"], language=selected_lang.lower())
        
    with col2:
        st.subheader("Review Analysis")
        res = st.session_state.review_results
        summary = res["summary"]
        issues = res["issues"]
        improved_code = res["improved_code"]
        orig_code = res["original_code"]
        
        # Health gauge & statistics
        ui_components.render_score_gauge(summary.get("score", 100))
        ui_components.render_severity_distribution(issues)
        
        # Result tabs
        tab_issues, tab_improved, tab_overview = st.tabs([
            f"🔍 Issues ({len(issues)})", 
            "💻 Improved Code", 
            "📝 Overview & Report"
        ])
        
        with tab_issues:
            if not issues:
                st.balloons()
                st.success("🎉 Excellent! No issues were found in the code.")
            else:
                for idx, issue in enumerate(issues):
                    ui_components.render_issue_card(issue, idx)
                    
        with tab_improved:
            st.markdown("### Refactored & Optimized Code")
            st.markdown("This version implements all fixes detailed in the findings:")
            
            # Syntax highlight mapping
            lang_highlight = selected_lang.lower()
            if lang_highlight == "other":
                lang_highlight = "python"
                
            st.code(improved_code, language=lang_highlight)
            
            # Quick downloads
            col_down_1, col_down_2 = st.columns(2)
            with col_down_1:
                st.download_button(
                    label="Download Fixed File 📥",
                    data=improved_code,
                    file_name=f"improved_code.{'py' if selected_lang == 'Python' else 'txt'}",
                    mime="text/plain",
                    use_container_width=True
                )
                
        with tab_overview:
            st.markdown("### Qualitative Assessment")
            st.info(summary.get("overview", "No qualitative assessment provided."))
            
            # Generate Markdown report
            report_md = f"""# AI Code Review Report
- **Language**: {res['language']}
- **Code Health Score**: {summary.get('score', 100)}/100
- **Total Issues Found**: {len(issues)}

## Overview
{summary.get('overview', 'No summary available.')}

## Detailed Issues
"""
            for idx, issue in enumerate(issues):
                report_md += f"""
### {idx+1}. [{issue.get('severity', 'Info')}] {issue.get('category', 'General')}
- **Line Number**: {issue.get('line_number') or 'Global'}
- **Description**: {issue.get('description')}
- **Suggested Fix**: {issue.get('suggested_fix')}
"""
            report_md += f"""
## Improved Code
```{lang_highlight}
{improved_code}
```
"""
            
            st.markdown("### Review Export")
            st.download_button(
                label="Download Full Review Report (MD) 📄",
                data=report_md,
                file_name="code_review_report.md",
                mime="text/markdown",
                use_container_width=True
            )

# History Log in Sidebar
if st.session_state.history:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Session History")
    for i, hist in enumerate(reversed(st.session_state.history)):
        st.sidebar.markdown(
            f"""
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 10px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 600;">
                    <span>Run #{len(st.session_state.history) - i} ({hist['language']})</span>
                    <span style="color: {'#10b981' if hist['score'] >= 85 else '#3b82f6' if hist['score'] >= 70 else '#f97316' if hist['score'] >= 50 else '#ef4444'};">Score: {hist['score']}</span>
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 4px;">
                    Issues Detected: {hist['issues_count']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Render Footer
ui_components.render_footer()
