import streamlit as st
import config

def inject_custom_css():
    """
    Injects custom CSS to style the Streamlit app beautifully.
    Includes custom cards, badges, and layout tweaks.
    """
    st.markdown(
        """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        /* Apply fonts */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        code, pre, [class*="stCode"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 14px !important;
        }
        
        /* Gradient title text */
        .title-gradient {
            background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.75rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        
        .subtitle {
            font-size: 1.15rem;
            color: #94a3b8;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        /* Glassmorphic cards */
        .issue-card {
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .issue-card:hover {
            transform: translateY(-4px);
            border-color: rgba(255, 255, 255, 0.18);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
        }
        
        /* Header section inside card */
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        /* Badges */
        .badge {
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #ffffff !important;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .badge-critical {
            background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        }
        
        .badge-warning {
            background: linear-gradient(135deg, #f97316 0%, #c2410c 100%);
        }
        
        .badge-optimization {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        }
        
        .badge-info {
            background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        }
        
        /* Category label */
        .category-label {
            font-size: 14px;
            font-weight: 600;
            color: #e2e8f0;
            background: rgba(255, 255, 255, 0.06);
            padding: 4px 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }
        
        /* Line number */
        .line-number {
            font-size: 13px;
            color: #cbd5e1;
            font-family: 'JetBrains Mono', monospace;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 2px 8px;
            border-radius: 6px;
        }
        
        /* Card sections */
        .section-title {
            font-size: 13px;
            font-weight: 700;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 16px;
            margin-bottom: 6px;
        }
        
        .section-content {
            font-size: 15px;
            color: #f1f5f9;
            line-height: 1.6;
        }
        
        .fix-container {
            background: rgba(16, 185, 129, 0.05);
            border-left: 3px solid #10b981;
            padding: 12px 16px;
            border-radius: 0 8px 8px 0;
            margin-top: 12px;
        }
        
        /* Metrics row container */
        .metrics-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }
        
        .metric-tile {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            transition: all 0.2s ease;
        }
        
        .metric-tile:hover {
            background: rgba(255, 255, 255, 0.04);
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 700;
        }
        
        .metric-label {
            font-size: 12px;
            color: #94a3b8;
            margin-top: 4px;
            font-weight: 500;
        }
        
        /* Sidebar styling custom */
        .sidebar-logo {
            text-align: center;
            margin-bottom: 20px;
        }
        
        /* Footer custom */
        .footer {
            text-align: center;
            padding: 24px 0 10px 0;
            font-size: 13px;
            color: #64748b;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: 40px;
        }
        
        /* Pulse Animation for Status Indicators */
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.5; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.5; }
        }
        .pulse-active {
            animation: pulse 2s infinite;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header():
    """
    Renders the app main title and subtitle.
    """
    st.markdown('<div class="title-gradient">Antigravity Code Reviewer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Elevate your code quality with deep analysis powered by Groq Llama3</div>', unsafe_allow_html=True)

def render_score_gauge(score: int):
    """
    Renders a beautiful circular SVG gauge highlighting the code review score.
    The colors range from Red (low) to Yellow (mid) to Green (high).
    """
    # Determine color based on score
    if score >= 85:
        color = "#10b981"  # Emerald
        health_label = "Pristine / Excellent"
    elif score >= 70:
        color = "#3b82f6"  # Blue
        health_label = "Good / Stable"
    elif score >= 50:
        color = "#f97316"  # Orange
        health_label = "Needs Improvement"
    else:
        color = "#ef4444"  # Red
        health_label = "Critical / Major Vulnerabilities"

    # SVG geometry: Circumference = 2 * pi * r = 2 * 3.14159 * 50 = 314.16
    circumference = 314.16
    dashoffset = circumference - (score / 100.0) * circumference

    gauge_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 20px 0;">
        <svg width="150" height="150" viewBox="0 0 120 120" style="display: block; margin: auto;">
            <!-- Background circle -->
            <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255, 255, 255, 0.05)" stroke-width="9"></circle>
            <!-- Progress circle -->
            <circle cx="60" cy="60" r="50" fill="none" stroke="{color}" stroke-width="9" 
                    stroke-dasharray="{circumference}" stroke-dashoffset="{dashoffset}" 
                    stroke-linecap="round" transform="rotate(-90 60 60)" 
                    style="transition: stroke-dashoffset 1s ease-out;"></circle>
            <!-- Text -->
            <text x="60" y="62" text-anchor="middle" font-size="22" font-weight="800" fill="#ffffff" font-family="'Plus Jakarta Sans', sans-serif">{score}</text>
            <text x="60" y="78" text-anchor="middle" font-size="8" font-weight="700" fill="#94a3b8" font-family="'Plus Jakarta Sans', sans-serif" letter-spacing="0.05em">HEALTH SCORE</text>
        </svg>
        <div style="color: {color}; font-weight: 700; font-size: 16px; margin-top: 10px; text-transform: uppercase; letter-spacing: 0.05em;">{health_label}</div>
    </div>
    """
    st.markdown(gauge_html, unsafe_allow_html=True)

def render_severity_distribution(issues: list):
    """
    Renders metrics showing distribution of issues by severity.
    """
    counts = {"Critical": 0, "Warning": 0, "Optimization": 0, "Info": 0}
    for issue in issues:
        sev = issue.get("severity", "Info")
        if sev in counts:
            counts[sev] += 1
            
    # HTML grid layout
    metrics_html = f"""
    <div class="metrics-container">
        <div class="metric-tile" style="border-top: 3px solid #ef4444;">
            <div class="metric-value" style="color: #ef4444;">{counts['Critical']}</div>
            <div class="metric-label">🚨 CRITICAL</div>
        </div>
        <div class="metric-tile" style="border-top: 3px solid #f97316;">
            <div class="metric-value" style="color: #f97316;">{counts['Warning']}</div>
            <div class="metric-label">⚠️ WARNINGS</div>
        </div>
        <div class="metric-tile" style="border-top: 3px solid #3b82f6;">
            <div class="metric-value" style="color: #3b82f6;">{counts['Optimization']}</div>
            <div class="metric-label">⚡ OPTIMIZATIONS</div>
        </div>
        <div class="metric-tile" style="border-top: 3px solid #10b981;">
            <div class="metric-value" style="color: #10b981;">{counts['Info']}</div>
            <div class="metric-label">ℹ️ INFO</div>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

def render_issue_card(issue: dict, index: int):
    """
    Renders a single code issue inside a glassmorphic HTML card.
    """
    category = issue.get("category", "General")
    severity = issue.get("severity", "Info")
    line_number = issue.get("line_number")
    description = issue.get("description", "No description provided.")
    suggested_fix = issue.get("suggested_fix", "")
    
    # Severity Badge configuration
    sev_class = "badge-info"
    sev_icon = "ℹ️"
    if severity == "Critical":
        sev_class = "badge-critical"
        sev_icon = "🚨"
    elif severity == "Warning":
        sev_class = "badge-warning"
        sev_icon = "⚠️"
    elif severity == "Optimization":
        sev_class = "badge-optimization"
        sev_icon = "⚡"
        
    line_number_badge = f'<span class="line-number">Line {line_number}</span>' if line_number is not None else ""
    
    card_html = f"""
    <div class="issue-card">
        <div class="card-header">
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <span class="badge {sev_class}">{sev_icon} {severity}</span>
                <span class="category-label">{category}</span>
            </div>
            {line_number_badge}
        </div>
        
        <div class="section-title">Issue Description</div>
        <div class="section-content">{description}</div>
        
        {f'''
        <div class="section-title">Suggested Fix</div>
        <div class="fix-container">
            <div class="section-content" style="color: #a7f3d0; font-weight: 500;">{suggested_fix}</div>
        </div>
        ''' if suggested_fix else ''}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_footer():
    """
    Renders the app footer.
    """
    st.markdown(
        """
        <div class="footer">
            Built with ❤️ using Python, Streamlit, and Groq Llama3 • Powered by Antigravity AI
        </div>
        """,
        unsafe_allow_html=True
    )
