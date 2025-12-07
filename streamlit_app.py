import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
import json

# Page configuration
st.set_page_config(
    page_title="AI/ML Observability Platform - Prototype",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling with centered navigation
st.markdown("""
<style>
    /* Professional sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
    }
    
    /* Center navigation items */
    [data-testid="stSidebar"] .stRadio > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        display: flex;
        justify-content: center;
        font-weight: 600;
        font-size: 1.1rem;
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
        gap: 0.75rem;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(30, 64, 175, 0.1);
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        text-align: center;
        font-size: 0.95rem;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        border-color: #60a5fa;
        color: white;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    
    /* Main content styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e40af 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Help bubble styling */
    .help-bubble {
        position: relative;
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        animation: pulse 2s infinite;
    }
    
    .help-bubble::before {
        content: "💡";
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }
        50% { box-shadow: 0 6px 25px rgba(59, 130, 246, 0.5); }
    }
    
    .info-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-card-title {
        font-weight: 700;
        color: #1e40af;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .info-card-content {
        color: #1e3a8a;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    /* Status boxes */
    .success-box {
        background-color: #d1fae5;
        border-left: 5px solid #10b981;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fef3c7;
        border-left: 5px solid #f59e0b;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #f9fafb;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        background-color: white;
        border-radius: 6px;
        border: 2px solid #e5e7eb;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border-color: #3b82f6;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
    }
    
    /* Sidebar metrics styling */
    [data-testid="stSidebar"] .stMetric {
        background: rgba(59, 130, 246, 0.1);
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }
    
    [data-testid="stSidebar"] .stMetric label {
        color: #94a3b8 !important;
        font-size: 0.85rem;
    }
    
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-size: 1.5rem;
    }
    
    /* Tour highlight */
    .tour-highlight {
        animation: highlight 2s ease-in-out infinite;
        border: 2px solid #fbbf24;
        border-radius: 8px;
        padding: 1rem;
    }
    
    @keyframes highlight {
        0%, 100% { box-shadow: 0 0 10px rgba(251, 191, 36, 0.5); }
        50% { box-shadow: 0 0 20px rgba(251, 191, 36, 0.8); }
    }
    
    /* Tooltip styling */
    .tooltip-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        background: #3b82f6;
        color: white;
        border-radius: 50%;
        font-size: 0.75rem;
        font-weight: bold;
        cursor: help;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'log_count' not in st.session_state:
    st.session_state.log_count = 0
if 'alert_count' not in st.session_state:
    st.session_state.alert_count = 0
if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0.0
if 'ingestion_active' not in st.session_state:
    st.session_state.ingestion_active = False
if 'log_history' not in st.session_state:
    st.session_state.log_history = []
if 'show_help' not in st.session_state:
    st.session_state.show_help = True
if 'tour_step' not in st.session_state:
    st.session_state.tour_step = 0

# Data generation functions
def generate_log_entry():
    """Generate realistic log entry"""
    models = ["GPT-4", "Claude-3", "Llama-2", "Gemini-Pro", "Mistral-7B"]
    stages = ["ingestion", "embedding", "retrieval", "inference", "post-processing"]
    users = ["user_001", "user_002", "user_003", "data_science_team", "ml_ops_team"]
    
    trace_id = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "trace_id": trace_id,
        "model": random.choice(models),
        "stage": random.choice(stages),
        "user_id": random.choice(users),
        "latency_ms": random.randint(50, 3000),
        "tokens_input": random.randint(100, 2000),
        "tokens_output": random.randint(50, 1000),
        "confidence_score": round(random.uniform(0.6, 0.99), 2),
        "cost_usd": round(random.uniform(0.001, 0.05), 4),
        "status": random.choice(["success", "success", "success", "warning", "error"])
    }
    return log

def generate_rag_chain():
    """Generate complete RAG execution chain"""
    trace_id = f"rag-{random.randint(1000, 9999)}"
    base_time = datetime.now()
    
    chain = [
        {
            "stage": "Ingestion",
            "service": "document-processor",
            "latency_ms": random.randint(10, 50),
            "status": "success",
            "timestamp": base_time.strftime("%H:%M:%S.%f")[:-3]
        },
        {
            "stage": "Embedding",
            "service": "embedding-service",
            "latency_ms": random.randint(100, 200),
            "status": "success",
            "timestamp": (base_time + timedelta(milliseconds=50)).strftime("%H:%M:%S.%f")[:-3]
        },
        {
            "stage": "Retrieval",
            "service": "vector-db",
            "latency_ms": random.randint(30, 80),
            "status": "success",
            "timestamp": (base_time + timedelta(milliseconds=250)).strftime("%H:%M:%S.%f")[:-3]
        },
        {
            "stage": "Prompt Construction",
            "service": "prompt-builder",
            "latency_ms": random.randint(5, 15),
            "status": "success",
            "timestamp": (base_time + timedelta(milliseconds=330)).strftime("%H:%M:%S.%f")[:-3]
        },
        {
            "stage": "LLM Inference",
            "service": "llm-gateway",
            "latency_ms": random.randint(1500, 2500),
            "status": "success",
            "timestamp": (base_time + timedelta(milliseconds=345)).strftime("%H:%M:%S.%f")[:-3]
        },
        {
            "stage": "Post-Processing",
            "service": "response-formatter",
            "latency_ms": random.randint(10, 30),
            "status": "success",
            "timestamp": (base_time + timedelta(milliseconds=2845)).strftime("%H:%M:%S.%f")[:-3]
        }
    ]
    
    return trace_id, chain

def show_help_bubble(message, key=None):
    """Display an animated help bubble"""
    st.markdown(f'<div class="help-bubble">{message}</div>', unsafe_allow_html=True)

def show_info_card(title, content):
    """Display an information card"""
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">{title}</div>
        <div class="info-card-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

# Header with welcome message
st.markdown('<h1 class="main-header">🔍 AI/ML Observability Platform</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive Prototype - Real-time Log Ingestion & Analytics with Splunk</p>', unsafe_allow_html=True)

# Welcome guide toggle
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.show_help:
        show_help_bubble("👋 Welcome! This prototype demonstrates a complete AI/ML observability platform. Navigate through layers using the sidebar.")
        if st.button("✕ Hide Help Mode", key="hide_help"):
            st.session_state.show_help = False
            st.rerun()
    else:
        if st.button("❓ Show Help Mode", key="show_help"):
            st.session_state.show_help = True
            st.rerun()

st.markdown("---")

# Professional centered sidebar navigation
with st.sidebar:
    # Logo/Brand
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <div style='background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 1rem;'>
            <h2 style='color: white; margin: 0; font-size: 1.5rem;'>🔍 SPLUNK</h2>
            <p style='color: #dbeafe; margin: 0.25rem 0 0 0; font-size: 0.9rem;'>AI/ML Observability</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation with centered styling
    page = st.radio(
        "🧭 Navigation Center",
        ["🏠 Overview Dashboard", 
         "📥 Layer 1: Log Ingestion",
         "⚙️ Layer 2: Processing",
         "💾 Layer 3: Storage",
         "📊 Layer 4: Consumption",
         "🔗 End-to-End Tracing",
         "⚡ Real-time Monitoring"],
        label_visibility="visible"
    )
    
    st.markdown("---")
    
    # System Status Section
    st.markdown("""
    <div style='text-align: center; margin-bottom: 1rem;'>
        <h3 style='color: #60a5fa; font-size: 1.1rem; margin-bottom: 1rem;'>⚙️ System Status</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ All systems operational")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Uptime", "99.97%", delta="0.02%")
    with col2:
        st.metric("Indexers", "12", delta="0")
    
    st.metric("Active Forwarders", "156", delta="2")
    
    st.markdown("---")
    
    # Quick Stats Section
    st.markdown("""
    <div style='text-align: center; margin-bottom: 1rem;'>
        <h3 style='color: #60a5fa; font-size: 1.1rem; margin-bottom: 1rem;'>📈 Quick Stats</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.metric("Total Logs Today", f"{st.session_state.log_count:,}", delta=f"+{random.randint(100, 500)}")
    st.metric("Active Alerts", st.session_state.alert_count, delta=f"{random.randint(-2, 3)}")
    st.metric("Total Cost (24h)", f"${st.session_state.total_cost:.2f}", delta=f"+${random.uniform(0.5, 2.0):.2f}")
    
    st.markdown("---")
    
    # Help section
    with st.expander("📖 Quick Guide"):
        st.markdown("""
        **Navigation:**
        - Click any layer to explore
        - Each layer simulates real functionality
        
        **Features:**
        - Real-time log generation
        - Interactive SPL queries  
        - RAG chain visualization
        - Cost analytics
        
        **Tip:** Start with Overview Dashboard!
        """)

# Page content based on selection
if page == "🏠 Overview Dashboard":
    if st.session_state.show_help:
        show_info_card(
            "🎯 Overview Dashboard", 
            "This executive dashboard provides high-level KPIs and metrics across all layers. " 
            "Monitor ingestion volume, query performance, model metrics, and system health at a glance."
        )
    
    st.header("📊 Executive Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Ingestion (24h)",
            value="2.4 TB",
            delta="+124 GB",
            help="Total data ingested across all forwarders in the last 24 hours"
        )
    
    with col2:
        st.metric(
            label="Avg Query Latency",
            value="847 ms",
            delta="-23 ms",
            delta_color="inverse",
            help="Average search query response time across the cluster"
        )
    
    with col3:
        st.metric(
            label="Model Inference Count",
            value="1.2M",
            delta="+45K",
            help="Total AI/ML model inference requests processed today"
        )
    
    with col4:
        st.metric(
            label="Hallucination Rate",
            value="2.3%",
            delta="-0.5%",
            delta_color="inverse",
            help="Percentage of LLM responses flagged as potential hallucinations"
        )
    
    with col5:
        st.metric(
            label="Cost Efficiency",
            value="$0.0023/req",
            delta="-$0.0002",
            delta_color="inverse",
            help="Average cost per model inference request"
        )
    
    st.markdown("---")
    
    if st.session_state.show_help:
        show_help_bubble("📈 These charts update in real-time. Hover over data points for detailed information!")
    
    # Two column layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Ingestion Volume (Last 24h)")
        
        # Generate time series data
        hours = pd.date_range(end=datetime.now(), periods=24, freq='H')
        volume_gb = [random.uniform(80, 120) for _ in range(24)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours,
            y=volume_gb,
            mode='lines+markers',
            name='Ingestion Volume',
            line=dict(color='#1E40AF', width=3),
            fill='tozeroy',
            fillcolor='rgba(30, 64, 175, 0.2)',
            hovertemplate='<b>Time:</b> %{x}<br><b>Volume:</b> %{y:.1f} GB<extra></extra>'
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Time",
            yaxis_title="Volume (GB/hour)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Model Performance Distribution")
        
        models = ["GPT-4", "Claude-3", "Llama-2", "Gemini-Pro", "Mistral-7B"]
        latencies = [850, 920, 1200, 780, 950]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=models,
            y=latencies,
            marker=dict(
                color=latencies,
                colorscale='Viridis',
                showscale=False
            ),
            text=[f"{l}ms" for l in latencies],
            textposition='outside',
            hovertemplate='<b>Model:</b> %{x}<br><b>Latency:</b> %{y}ms<extra></extra>'
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Model",
            yaxis_title="Avg Latency (ms)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # RAG Pipeline Health
    st.subheader("🔄 RAG Pipeline Stage Performance")
    
    if st.session_state.show_help:
        show_info_card(
            "🔄 RAG Pipeline Monitoring",
            "Monitor each stage of your Retrieval-Augmented Generation pipeline. "
            "Track latency and throughput to identify bottlenecks and optimize performance."
        )
    
    stages = ["Ingestion", "Embedding", "Retrieval", "Prompt", "Inference", "Post-Proc"]
    avg_latency = [35, 150, 60, 12, 2100, 18]
    p95_latency = [45, 200, 85, 18, 2800, 25]
    throughput = [12000, 11800, 11500, 11400, 9800, 9750]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Avg Latency', 
            x=stages, 
            y=avg_latency, 
            marker_color='#10B981',
            hovertemplate='<b>%{x}</b><br>Avg: %{y}ms<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            name='P95 Latency', 
            x=stages, 
            y=p95_latency, 
            marker_color='#F59E0B',
            hovertemplate='<b>%{x}</b><br>P95: %{y}ms<extra></extra>'
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            barmode='group',
            xaxis_title="Pipeline Stage",
            yaxis_title="Latency (ms)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=stages,
            y=throughput,
            mode='lines+markers',
            line=dict(color='#8B5CF6', width=3),
            marker=dict(size=10),
            hovertemplate='<b>%{x}</b><br>Throughput: %{y} req/sec<extra></extra>'
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Pipeline Stage",
            yaxis_title="Throughput (req/sec)",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Active Alerts
    st.subheader("⚠️ Active Alerts & Anomalies")
    
    if st.session_state.show_help:
        show_help_bubble("🚨 Alerts are automatically generated based on predefined thresholds and ML-powered anomaly detection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="error-box">
            <strong>🔴 CRITICAL</strong><br/>
            High hallucination rate detected in GPT-4<br/>
            <small>Threshold: 15% | Current: 18.3%</small><br/>
            <small>📍 Action: PagerDuty incident #12345 created</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
            <strong>🟡 WARNING</strong><br/>
            Claude-3 latency increasing<br/>
            <small>Baseline: 850ms | Current: 1240ms</small><br/>
            <small>📍 Action: Slack notification sent to #ml-ops</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="success-box">
            <strong>🟢 INFO</strong><br/>
            Cost optimization detected<br/>
            <small>Savings: $234.50 (24h)</small><br/>
            <small>📍 Action: Report emailed to FinOps team</small>
        </div>
        """, unsafe_allow_html=True)

elif page == "📥 Layer 1: Log Ingestion":
    if st.session_state.show_help:
        show_info_card(
            "📥 Log Ingestion Layer",
            "This layer captures logs from all sources using Universal and Heavy Forwarders. "
            "Start the simulator to see real-time log ingestion in action!"
        )
    
    st.header("📥 Layer 1: Log Ingestion & Collection Infrastructure")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎮 Live Simulator", 
        "📊 Forwarder Status", 
        "🔍 Log Inspector", 
        "📈 Metrics"
    ])
    
    with tab1:
        st.subheader("🎮 Real-time Log Ingestion Simulator")
        
        if st.session_state.show_help:
            show_help_bubble("🎮 Click 'Start Ingestion' to simulate real-time log collection from multiple sources. Watch the metrics update live!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Start Ingestion", type="primary", use_container_width=True):
                st.session_state.ingestion_active = True
        
        with col2:
            if st.button("⏸️ Pause Ingestion", use_container_width=True):
                st.session_state.ingestion_active = False
        
        with col3:
            if st.button("🔄 Reset Stats", use_container_width=True):
                st.session_state.log_count = 0
                st.session_state.total_cost = 0.0
                st.session_state.log_history = []
        
        st.markdown("---")
        
        # Live stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Logs Ingested", st.session_state.log_count, help="Total logs captured since start")
        with col2:
            st.metric("Ingestion Rate", f"{random.randint(1000, 3000)}/sec", help="Current logs per second")
        with col3:
            st.metric("Total Cost", f"${st.session_state.total_cost:.4f}", help="Accumulated processing cost")
        with col4:
            st.metric("Buffer Usage", f"{random.randint(20, 60)}%", help="Heavy Forwarder buffer utilization")
        
        # Live log stream
        st.subheader("📜 Live Log Stream")
        
        if st.session_state.show_help:
            show_info_card(
                "📜 Understanding Log Stream",
                "Each log entry shows: timestamp, trace ID (for request correlation), model used, "
                "processing stage, latency, token usage, and cost. Status indicators: 🟢 Success | 🟡 Warning | 🔴 Error"
            )
        
        log_container = st.container()
        
        if st.session_state.ingestion_active:
            with log_container:
                # Generate and display logs
                for _ in range(5):
                    log = generate_log_entry()
                    st.session_state.log_count += 1
                    st.session_state.total_cost += log['cost_usd']
                    st.session_state.log_history.append(log)
                    
                    # Keep only last 100 logs
                    if len(st.session_state.log_history) > 100:
                        st.session_state.log_history.pop(0)
                    
                    status_color = {
                        "success": "🟢",
                        "warning": "🟡",
                        "error": "🔴"
                    }
                    
                    st.code(
                        f"{status_color[log['status']]} [{log['timestamp']}] "
                        f"trace_id={log['trace_id']} | model={log['model']} | "
                        f"stage={log['stage']} | latency={log['latency_ms']}ms | "
                        f"tokens={log['tokens_input']}→{log['tokens_output']} | "
                        f"cost=${log['cost_usd']:.4f}",
                        language="log"
                    )
                
                time.sleep(0.1)
                st.rerun()
        else:
            with log_container:
                st.info("👆 Click 'Start Ingestion' above to begin streaming logs in real-time...")
    
    with tab2:
        st.subheader("📊 Universal Forwarder Status")
        
        if st.session_state.show_help:
            show_info_card(
                "📊 Forwarder Monitoring",
                "Universal Forwarders are lightweight agents installed on application servers. "
                "They collect logs and forward them to Heavy Forwarders for processing."
            )
        
        # Generate forwarder data
        forwarders_data = []
        for i in range(10):
            status = random.choice(["🟢 Active", "🟢 Active", "🟢 Active", "🟡 Warning"])
            forwarders_data.append({
                "Forwarder ID": f"UF-{i+1:03d}",
                "Host": f"app-server-{i+1:02d}.prod.internal",
                "Status": status,
                "CPU %": f"{random.randint(10, 70)}%",
                "Memory": f"{random.randint(50, 95)} MB",
                "Logs/sec": f"{random.randint(100, 1500)}",
                "Buffer": f"{random.randint(5, 45)}%"
            })
        
        df = pd.DataFrame(forwarders_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Forwarder Health Distribution")
            health_data = {"Active": 156, "Warning": 3, "Error": 1}
            fig = go.Figure(data=[go.Pie(
                labels=list(health_data.keys()),
                values=list(health_data.values()),
                marker=dict(colors=['#10B981', '#F59E0B', '#EF4444']),
                hole=0.4,
                hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
            )])
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top Forwarders by Volume")
            top_forwarders = [f"UF-{i:03d}" for i in range(1, 6)]
            volumes = [random.randint(50000, 150000) for _ in range(5)]
            
            fig = go.Figure(go.Bar(
                x=volumes,
                y=top_forwarders,
                orientation='h',
                marker_color='#1E40AF',
                hovertemplate='<b>%{y}</b><br>Volume: %{x:,} logs/hour<extra></extra>'
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Logs/hour",
                yaxis_title="Forwarder"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🔍 Log Inspector & Parser")
        
        if st.session_state.show_help:
            show_info_card(
                "🔍 Log Parsing",
                "Heavy Forwarders parse logs to extract structured fields. "
                "This enables fast searching and correlation across millions of events."
            )
        
        if st.session_state.log_history:
            selected_log = random.choice(st.session_state.log_history[-20:])
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("##### 📄 Raw Log")
                st.json(selected_log)
            
            with col2:
                st.markdown("##### 🏷️ Extracted Fields")
                st.markdown(f"""
                - **Trace ID**: `{selected_log['trace_id']}`
                - **Model**: `{selected_log['model']}`
                - **Stage**: `{selected_log['stage']}`
                - **User**: `{selected_log['user_id']}`
                - **Status**: `{selected_log['status']}`
                """)
                
                st.markdown("##### 🎯 Metadata Enrichment")
                st.markdown(f"""
                - **Environment**: `production`
                - **Region**: `us-west-2`
                - **Cluster**: `ml-cluster-01`
                - **Version**: `v2.4.1`
                """)
        else:
            st.info("📭 Start ingestion in the 'Live Simulator' tab to see log details...")
    
    with tab4:
        st.subheader("📈 Ingestion Metrics & Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Logs by Source Type")
            sources = ["AI/ML Apps", "RAG Pipeline", "Infrastructure", "Security", "DevOps"]
            counts = [45000, 32000, 28000, 15000, 8000]
            
            fig = go.Figure(data=[go.Pie(
                labels=sources,
                values=counts,
                hole=0.3,
                hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>'
            )])
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Ingestion Rate (last hour)")
            minutes = list(range(60))
            rates = [random.randint(2000, 4000) for _ in range(60)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=minutes,
                y=rates,
                mode='lines',
                fill='tozeroy',
                line=dict(color='#8B5CF6'),
                fillcolor='rgba(139, 92, 246, 0.2)',
                hovertemplate='<b>%{x} min ago</b><br>Rate: %{y} logs/sec<extra></extra>'
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Minutes Ago",
                yaxis_title="Logs/sec"
            )
            st.plotly_chart(fig, use_container_width=True)

elif page == "⚙️ Layer 2: Processing":
    if st.session_state.show_help:
        show_info_card(
            "⚙️ Processing & Analytics Layer",
            "This layer processes ingested logs using Splunk Processing Language (SPL), " 
            "performs ML-powered analytics, and generates alerts based on anomalies and thresholds."
        )
    
    st.header("⚙️ Layer 2: Real-Time Processing & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["🔧 SPL Queries", "🤖 ML Analytics", "⚡ Alerting"])
    
    with tab1:
        st.subheader("🔧 Search Processing Language (SPL) Console")
        
        if st.session_state.show_help:
            show_help_bubble("💡 SPL is Splunk's query language. Select a template, customize if needed, and click 'Run Query' to see results!")
        
        # Predefined queries
        query_templates = {
            "Model Performance": "index=aiml_models | stats avg(latency_ms), avg(tokens_total), sum(cost_usd) by model_name",
            "Hallucination Detection": "index=aiml_models | where confidence_score < 0.7 AND citation_count = 0 | stats count by model_name",
            "RAG Chain": 'index=aiml_rag trace_id="xyz123" | transaction trace_id | table _time, stage, latency_ms',
            "Cost by User": "index=aiml_models | stats sum(cost_usd) as total_cost by user_id | sort -total_cost",
            "Error Rate": "index=aiml_models | stats count(eval(status='error')) as errors, count as total | eval error_rate=errors/total*100"
        }
        
        selected_template = st.selectbox(
            "Select Query Template", 
            list(query_templates.keys()),
            help="Choose from pre-built queries for common use cases"
        )
        
        query = st.text_area("SPL Query", value=query_templates[selected_template], height=100)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            run_query = st.button("▶️ Run Query", type="primary")
        with col2:
            st.button("💾 Save Query")
        
        if run_query:
            with st.spinner("Executing query..."):
                time.sleep(1)
                
                st.success("✅ Query completed in 0.847 seconds | Scanned 2.4M events")
                
                # Generate results based on query type
                if "Model Performance" in selected_template:
                    results = pd.DataFrame({
                        "model_name": ["GPT-4", "Claude-3", "Llama-2", "Gemini-Pro", "Mistral-7B"],
                        "avg(latency_ms)": [850, 920, 1200, 780, 950],
                        "avg(tokens_total)": [1250, 1180, 890, 1320, 1050],
                        "sum(cost_usd)": [234.56, 189.23, 145.67, 267.89, 178.90]
                    })
                elif "Hallucination" in selected_template:
                    results = pd.DataFrame({
                        "model_name": ["GPT-4", "Claude-3", "Llama-2"],
                        "count": [145, 87, 234]
                    })
                elif "Cost by User" in selected_template:
                    results = pd.DataFrame({
                        "user_id": ["data_science_team", "user_001", "ml_ops_team", "user_002", "user_003"],
                        "total_cost": [456.78, 234.56, 189.45, 145.67, 98.34]
                    })
                else:
                    results = pd.DataFrame({
                        "_time": pd.date_range(end=datetime.now(), periods=5, freq='1S'),
                        "stage": ["ingestion", "embedding", "retrieval", "inference", "post-processing"],
                        "latency_ms": [35, 150, 60, 2100, 18]
                    })
                
                st.dataframe(results, use_container_width=True, hide_index=True)
                
                # Visualization
                if "Model Performance" in selected_template or "Hallucination" in selected_template:
                    fig = px.bar(
                        results, 
                        x=results.columns[0], 
                        y=results.columns[1], 
                        title="Query Results Visualization",
                        color=results.columns[1],
                        color_continuous_scale='Viridis'
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🤖 Machine Learning Toolkit (MLTK)")
        
        if st.session_state.show_help:
            show_info_card(
                "🤖 ML-Powered Analytics",
                "Splunk's ML Toolkit detects anomalies, predicts trends, and identifies drift automatically. "
                "Red markers indicate detected anomalies that exceed thresholds."
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🎯 Anomaly Detection")
            
            # Generate time series with anomalies
            hours = pd.date_range(end=datetime.now(), periods=48, freq='H')
            normal_latency = [random.uniform(800, 1200) for _ in range(48)]
            # Inject anomalies
            normal_latency[15] = 3500
            normal_latency[32] = 3200
            normal_latency[40] = 3800
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hours,
                y=normal_latency,
                mode='lines+markers',
                name='Latency',
                line=dict(color='#3B82F6', width=2),
                marker=dict(
                    size=[15 if l > 2000 else 5 for l in normal_latency],
                    color=['red' if l > 2000 else '#3B82F6' for l in normal_latency]
                ),
                hovertemplate='<b>Time:</b> %{x}<br><b>Latency:</b> %{y:.0f}ms<extra></extra>'
            ))
            fig.add_hline(
                y=2000, 
                line_dash="dash", 
                line_color="red", 
                annotation_text="Anomaly Threshold (2000ms)",
                annotation_position="top right"
            )
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                title="Latency Anomaly Detection (48h)",
                xaxis_title="Time",
                yaxis_title="Latency (ms)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("🔍 Detected 3 anomalies in the last 48 hours (marked in red)")
        
        with col2:
            st.markdown("##### 📊 Model Drift Detection")
            
            features = ["Feature_A", "Feature_B", "Feature_C", "Feature_D", "Feature_E"]
            drift_scores = [0.05, 0.12, 0.18, 0.08, 0.22]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=features,
                x=drift_scores,
                orientation='h',
                marker=dict(
                    color=drift_scores,
                    colorscale=[[0, 'green'], [0.5, 'yellow'], [1, 'red']],
                    showscale=True,
                    colorbar=dict(title="Drift Score")
                ),
                hovertemplate='<b>%{y}</b><br>Drift Score: %{x:.2f}<extra></extra>'
            ))
            fig.add_vline(
                x=0.15, 
                line_dash="dash", 
                line_color="red",
                annotation_text="Warning Threshold",
                annotation_position="top"
            )
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                title="Feature Drift Analysis (KS Test)",
                xaxis_title="Drift Score (KS Statistic)",
                yaxis_title="Feature"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.warning("⚠️ Features C and E exceed drift threshold (>0.15)")
        
        st.markdown("---")
        
        st.markdown("##### 📈 Predictive Analytics - Capacity Forecast")
        
        if st.session_state.show_help:
            show_help_bubble("📊 Forecasting helps plan infrastructure capacity and prevent resource shortages")
        
        days = pd.date_range(start=datetime.now() - timedelta(days=30), 
                            end=datetime.now() + timedelta(days=7), freq='D')
        historical = [random.uniform(80, 120) for _ in range(30)]
        forecast = [random.uniform(110, 150) for _ in range(8)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=days[:30],
            y=historical,
            mode='lines',
            name='Historical Data',
            line=dict(color='#1E40AF', width=2),
            hovertemplate='<b>Date:</b> %{x}<br><b>Volume:</b> %{y:.1f} GB<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=days[30:],
            y=forecast,
            mode='lines',
            name='Forecast (ML-predicted)',
            line=dict(color='#F59E0B', width=2, dash='dash'),
            hovertemplate='<b>Date:</b> %{x}<br><b>Forecast:</b> %{y:.1f} GB<extra></extra>'
        ))
        fig.add_hline(
            y=140, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Capacity Limit",
            annotation_position="right"
        )
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Date",
            yaxis_title="Ingestion Volume (GB/day)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("⚡ Alert Manager & Notification System")
        
        if st.session_state.show_help:
            show_info_card(
                "⚡ Intelligent Alerting",
                "Alerts are automatically generated when metrics exceed thresholds or anomalies are detected. "
                "Different severity levels route to different notification channels."
            )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### 🔔 Active Alerts")
            
            alerts = [
                {
                    "severity": "🔴 CRITICAL",
                    "title": "High Hallucination Rate - GPT-4",
                    "description": "Hallucination rate exceeded 15% threshold",
                    "value": "18.3%",
                    "time": "2 minutes ago",
                    "action": "PagerDuty incident #12345 created"
                },
                {
                    "severity": "🟡 WARNING",
                    "title": "Increased Latency - Claude-3",
                    "description": "P95 latency above baseline",
                    "value": "1240ms (baseline: 850ms)",
                    "time": "15 minutes ago",
                    "action": "Slack notification sent to #ml-ops"
                },
                {
                    "severity": "🟡 WARNING",
                    "title": "Cost Anomaly Detected",
                    "description": "Hourly cost spike detected",
                    "value": "$125/hr (avg: $87/hr)",
                    "time": "32 minutes ago",
                    "action": "Email sent to FinOps team"
                }
            ]
            
            for alert in alerts:
                severity_color = {
                    "🔴 CRITICAL": "error-box",
                    "🟡 WARNING": "warning-box",
                    "🟢 INFO": "success-box"
                }
                
                st.markdown(f"""
                <div class="{severity_color[alert['severity']]}">
                    <strong>{alert['severity']}: {alert['title']}</strong><br/>
                    {alert['description']}<br/>
                    <strong>Value:</strong> {alert['value']}<br/>
                    <small>⏰ {alert['time']} | 📤 {alert['action']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("##### 📊 Alert Statistics")
            
            alert_stats = pd.DataFrame({
                "Type": ["Critical", "Warning", "Info"],
                "Last 24h": [12, 45, 156],
                "Last 7d": [89, 324, 1245]
            })
            
            st.dataframe(alert_stats, use_container_width=True, hide_index=True)
            
            st.markdown("##### 🎯 MTTR")
            st.metric(
                "Mean Time To Resolve", 
                "12.3 min", 
                delta="-2.1 min",
                help="Average time from alert generation to resolution"
            )
            
            st.markdown("##### 📨 Notification Channels")
            st.markdown("""
            - 🔔 PagerDuty: **Enabled**
            - 💬 Slack: **Enabled**
            - 📧 Email: **Enabled**
            - 📱 Teams: **Enabled**
            """)

elif page == "💾 Layer 3: Storage":
    if st.session_state.show_help:
        show_info_card(
            "💾 Storage & Lifecycle Management",
            "Data moves through storage tiers automatically based on age and access patterns. "
            "Hot storage for real-time queries, cold storage for compliance and historical analysis."
        )
    
    st.header("💾 Layer 3: Data Storage & Lifecycle Management")
    
    tab1, tab2 = st.tabs(["🗄️ Storage Tiers", "📋 Retention Policies"])
    
    with tab1:
        st.subheader("🗄️ Splunk Indexer Cluster - Storage Tier Status")
        
        if st.session_state.show_help:
            show_help_bubble("💡 Data automatically moves through tiers: Hot (fast, expensive) → Warm → Cold → Frozen (slow, cheap)")
        
        # Storage overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Hot Storage", "2.4 TB", delta="+124 GB", help="NVMe SSD - Last 7-30 days")
        with col2:
            st.metric("Warm Storage", "8.7 TB", delta="+89 GB", help="SATA SSD - 30-90 days")
        with col3:
            st.metric("Cold Storage", "45.2 TB", delta="+234 GB", help="S3 - 90-365 days")
        with col4:
            st.metric("Frozen/Archive", "234.5 TB", delta="+1.2 TB", help="Glacier - 1-7 years")
        
        st.markdown("---")
        
        # Storage tier details
        tier_data = {
            "Tier": ["Hot (NVMe SSD)", "Warm (SATA SSD)", "Cold (S3)", "Frozen (Glacier)"],
            "Capacity": ["5 TB", "15 TB", "100 TB", "500 TB"],
            "Used": ["2.4 TB", "8.7 TB", "45.2 TB", "234.5 TB"],
            "Usage %": ["48%", "58%", "45%", "47%"],
            "Retention": ["7-30 days", "30-90 days", "90-365 days", "1-7 years"],
            "Search Speed": ["< 1s", "2-5s", "10-30s", "1-12h"],
            "Replication": ["3x", "2x", "1x", "1x"],
            "Cost/GB/Month": ["$0.15", "$0.08", "$0.023", "$0.004"]
        }
        
        df = pd.DataFrame(tier_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 Storage Distribution")
            
            sizes = [2.4, 8.7, 45.2, 234.5]
            labels = ["Hot", "Warm", "Cold", "Frozen"]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=sizes,
                hole=0.4,
                marker=dict(colors=['#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6']),
                hovertemplate='<b>%{label}</b><br>Size: %{value} TB<br>Percentage: %{percent}<extra></extra>'
            )])
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### 📈 Storage Growth Trend")
            
            days = pd.date_range(end=datetime.now(), periods=30, freq='D')
            growth = np.cumsum([random.uniform(50, 150) for _ in range(30)])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=days,
                y=growth,
                mode='lines',
                fill='tozeroy',
                line=dict(color='#1E40AF', width=3),
                fillcolor='rgba(30, 64, 175, 0.2)',
                hovertemplate='<b>Date:</b> %{x}<br><b>Total:</b> %{y:.1f} TB<extra></extra>'
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Date",
                yaxis_title="Total Storage (TB)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("##### 🔄 Data Lifecycle Automation")
        
        st.info("""
        **Automated Data Movement Schedule:**
        - **Hot → Warm**: After 7 days (AI/ML logs), 3 days (Infrastructure)
        - **Warm → Cold**: After 30 days (Application logs), 60 days (Model logs)
        - **Cold → Frozen**: After 90 days (Application), 180 days (Model logs)
        - **Frozen → Purge**: After retention period expires (configurable by index)
        
        💡 **Benefit**: Automatic cost optimization while maintaining compliance requirements
        """)
    
    with tab2:
        st.subheader("📋 Data Retention Policies by Index")
        
        if st.session_state.show_help:
            show_info_card(
                "📋 Retention Policies",
                "Different log types have different retention requirements based on compliance, " 
                "business needs, and cost considerations. Security logs are kept longest for audit purposes."
            )
        
        retention_data = {
            "Index": ["aiml_models", "aiml_training", "aiml_rag", "infrastructure", "security_audit", "devops_ci_cd"],
            "Hot": ["14 days", "7 days", "14 days", "3 days", "30 days", "7 days"],
            "Warm": ["60 days", "30 days", "60 days", "14 days", "90 days", "30 days"],
            "Cold": ["180 days", "90 days", "180 days", "90 days", "365 days", "90 days"],
            "Archive": ["3 years", "1 year", "3 years", "Purge", "7 years", "1 year"],
            "Total Size": ["12.5 TB", "8.3 TB", "15.7 TB", "45.2 TB", "23.4 TB", "5.6 TB"],
            "Compliance": ["SOC2", "Internal", "SOC2", "Internal", "SOC2, HIPAA, GDPR", "Internal"]
        }
        
        df = pd.DataFrame(retention_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 💰 Storage Cost by Index")
            
            indices = list(retention_data["Index"])
            costs = [1245, 834, 1570, 452, 2340, 560]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=indices,
                y=costs,
                marker_color='#8B5CF6',
                text=[f"${c}" for c in costs],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Monthly Cost: $%{y}<extra></extra>'
            ))
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Index",
                yaxis_title="Monthly Cost (USD)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### 🔄 Data Movement Events (Last 24h)")
            
            movements = {
                "Hot → Warm": 2345,
                "Warm → Cold": 1876,
                "Cold → Frozen": 456,
                "Frozen → Purge": 89
            }
            
            fig = go.Figure(data=[go.Pie(
                labels=list(movements.keys()),
                values=list(movements.values()),
                hole=0.3,
                hovertemplate='<b>%{label}</b><br>Events: %{value:,}<extra></extra>'
            )])
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Layer 4: Consumption":
    if st.session_state.show_help:
        show_info_card(
            "📊 Consumption & Visualization Layer",
            "This layer provides dashboards, APIs, and integrations for consuming the observability data. "
            "Different stakeholders access data through role-appropriate interfaces."
        )
    
    st.header("📊 Layer 4: Consumption, Visualization & Integration")
    
    tab1, tab2, tab3 = st.tabs(["📈 Dashboards", "🔌 API Explorer", "🔗 Integrations"])
    
    with tab1:
        st.subheader("📈 Pre-built Dashboards")
        
        dashboard_type = st.selectbox(
            "Select Dashboard",
            ["AI/ML Operations", "RAG Pipeline", "Infrastructure", "Security & Compliance", "Cost Analytics"],
            help="Choose from role-specific dashboards"
        )
        
        if dashboard_type == "AI/ML Operations":
            if st.session_state.show_help:
                show_help_bubble("📊 This dashboard provides real-time insights into all AI/ML models across your organization")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Inferences (24h)", "1.2M", delta="+45K")
            with col2:
                st.metric("Avg Latency", "847ms", delta="-23ms")
            with col3:
                st.metric("Cost per 1K Tokens", "$0.0023", delta="-$0.0002")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Model comparison
                models = ["GPT-4", "Claude-3", "Llama-2", "Gemini-Pro", "Mistral-7B"]
                metrics = {
                    "Latency (ms)": [850, 920, 1200, 780, 950],
                    "Cost ($/1K)": [0.0030, 0.0025, 0.0015, 0.0028, 0.0020],
                    "Quality Score": [0.94, 0.96, 0.87, 0.93, 0.89]
                }
                
                df = pd.DataFrame(metrics, index=models)
                st.dataframe(df, use_container_width=True)
            
            with col2:
                # Token usage over time
                hours = list(range(24))
                tokens = [random.randint(40000, 60000) for _ in range(24)]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=hours,
                    y=tokens,
                    mode='lines',
                    fill='tozeroy',
                    line=dict(color='#8B5CF6', width=2),
                    hovertemplate='<b>Hour:</b> %{x}<br><b>Tokens:</b> %{y:,}<extra></extra>'
                ))
                fig.update_layout(
                    title="Token Usage (Last 24h)",
                    height=250,
                    margin=dict(l=0, r=0, t=30, b=0),
                    xaxis_title="Hour",
                    yaxis_title="Tokens"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif dashboard_type == "Cost Analytics":
            if st.session_state.show_help:
                show_help_bubble("💰 Track and optimize AI/ML costs across teams, models, and time periods")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 💰 Cost by Team (Last 30 Days)")
                
                teams = ["Data Science", "ML Ops", "Product", "Engineering", "Research"]
                costs = [4567, 3234, 2890, 2345, 1890]
                
                fig = go.Figure(data=[go.Pie(
                    labels=teams,
                    values=costs,
                    hole=0.4,
                    hovertemplate='<b>%{label}</b><br>Cost: $%{value:,}<br>Percentage: %{percent}<extra></extra>'
                )])
                fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("##### 📈 Daily Cost Trend")
                
                days = pd.date_range(end=datetime.now(), periods=30, freq='D')
                daily_costs = [random.uniform(400, 600) for _ in range(30)]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=days,
                    y=daily_costs,
                    mode='lines+markers',
                    line=dict(color='#F59E0B', width=2),
                    hovertemplate='<b>Date:</b> %{x}<br><b>Cost:</b> $%{y:.2f}<extra></extra>'
                ))
                fig.add_hline(
                    y=500, 
                    line_dash="dash", 
                    line_color="red",
                    annotation_text="Budget Threshold",
                    annotation_position="right"
                )
                fig.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title="Date",
                    yaxis_title="Cost (USD)"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🔌 Splunk REST API Explorer")
        
        if st.session_state.show_help:
            show_info_card(
                "🔌 API Access",
                "Use REST APIs to programmatically access Splunk data. " 
                "Integrate with custom applications, scripts, and other tools in your ecosystem."
            )
        
        endpoint = st.selectbox(
            "Select API Endpoint",
            [
                "GET /services/search/jobs - Create search job",
                "GET /services/search/jobs/{sid}/results - Get search results",
                "POST /services/data/indexes - Manage indexes",
                "GET /services/saved/searches - List saved searches",
                "GET /services/server/info - Server information"
            ]
        )
        
        st.markdown("##### 📋 Request")
        
        if "search/jobs" in endpoint and "results" not in endpoint:
            request_body = {
                "search": "search index=aiml_models | stats avg(latency_ms) by model_name",
                "earliest_time": "-24h",
                "latest_time": "now",
                "output_mode": "json"
            }
        else:
            request_body = {
                "output_mode": "json",
                "count": 100
            }
        
        st.json(request_body)
        
        if st.button("🚀 Execute API Call", type="primary"):
            with st.spinner("Executing API request..."):
                time.sleep(1)
                
                st.success("✅ API call successful (Response time: 234ms)")
                
                st.markdown("##### 📥 Response")
                
                response = {
                    "status": "success",
                    "execution_time": "0.234s",
                    "results": [
                        {"model_name": "GPT-4", "avg_latency_ms": 850},
                        {"model_name": "Claude-3", "avg_latency_ms": 920},
                        {"model_name": "Llama-2", "avg_latency_ms": 1200}
                    ],
                    "result_count": 3
                }
                
                st.json(response)
                
                st.markdown("##### 💻 Python SDK Example")
                st.code("""
import splunklib.client as client

# Connect to Splunk
service = client.connect(
    host="splunk.example.com",
    port=8089,
    username="admin",
    token="your-token-here"
)

# Create search job
job = service.jobs.create(
    "search index=aiml_models | stats avg(latency_ms)"
)

# Get results
for result in job.results():
    print(result)
                """, language="python")
    
    with tab3:
        st.subheader("🔗 External System Integrations")
        
        if st.session_state.show_help:
            show_help_bubble("🔗 Pre-configured integrations with ITSM, incident management, and collaboration tools")
        
        integrations = {
            "ServiceNow": {
                "status": "🟢 Connected",
                "description": "ITSM Ticketing",
                "metrics": {"Incidents Created (24h)": 12, "Avg Resolution Time": "2.3 hours"}
            },
            "PagerDuty": {
                "status": "🟢 Connected",
                "description": "Incident Management",
                "metrics": {"Alerts Sent (24h)": 45, "On-Call Engineers": 8}
            },
            "Slack": {
                "status": "🟢 Connected",
                "description": "ChatOps Notifications",
                "metrics": {"Messages Sent (24h)": 234, "Channels": 12}
            },
            "Grafana": {
                "status": "🟢 Connected",
                "description": "Metrics Visualization",
                "metrics": {"Dashboards": 23, "Active Users": 156}
            },
            "Datadog": {
                "status": "🟢 Connected",
                "description": "APM & Tracing",
                "metrics": {"Traces/sec": 2345, "Services Monitored": 45}
            },
            "Azure AD": {
                "status": "🟢 Connected",
                "description": "SSO Authentication",
                "metrics": {"Active Users": 234, "Auth Requests (24h)": 5678}
            }
        }
        
        for name, details in integrations.items():
            with st.expander(f"{details['status']} **{name}** - {details['description']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Configuration**")
                    st.markdown(f"- Status: {details['status']}")
                    st.markdown(f"- Type: {details['description']}")
                    st.markdown("- Authentication: ✅ OAuth2")
                    st.markdown("- Last Sync: 2 minutes ago")
                
                with col2:
                    st.markdown("**Metrics (Last 24h)**")
                    for metric, value in details['metrics'].items():
                        st.markdown(f"- {metric}: **{value}**")

elif page == "🔗 End-to-End Tracing":
    if st.session_state.show_help:
        show_info_card(
            "🔗 End-to-End Request Tracing",
            "Trace complete request flows through your RAG pipeline. " 
            "Every request gets a unique trace ID that links all processing stages together."
        )
    
    st.header("🔗 End-to-End Request Tracing")
    
    st.info("""
    **W3C Trace Context Implementation** - Every request gets a unique trace ID that propagates 
    through all services, enabling complete chain reconstruction from API gateway to final response.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🎲 Generate New RAG Chain Trace", type="primary", use_container_width=True):
            trace_id, chain = generate_rag_chain()
            st.session_state.current_trace = (trace_id, chain)
    
    with col2:
        st.code("traceparent: 00-4bf92f...-01", language="text")
    
    if 'current_trace' in st.session_state:
        trace_id, chain = st.session_state.current_trace
        
        if st.session_state.show_help:
            show_help_bubble("🔍 This timeline shows each stage of the RAG pipeline execution with exact timing")
        
        st.markdown(f"### 🔍 Trace ID: `{trace_id}`")
        
        # Timeline visualization
        st.markdown("##### ⏱️ Execution Timeline")
        
        # Create Gantt-like chart
        start_times = []
        durations = []
        cumulative_time = 0
        
        for step in chain:
            start_times.append(cumulative_time)
            durations.append(step['latency_ms'])
            cumulative_time += step['latency_ms']
        
        fig = go.Figure()
        
        colors = ['#10B981', '#3B82F6', '#8B5CF6', '#F59E0B', '#EF4444', '#6B7280']
        
        for i, step in enumerate(chain):
            fig.add_trace(go.Bar(
                name=step['stage'],
                x=[durations[i]],
                y=[step['stage']],
                orientation='h',
                marker=dict(color=colors[i % len(colors)]),
                text=f"{durations[i]}ms",
                textposition='inside',
                hovertemplate=f"<b>{step['stage']}</b><br>" +
                             f"Service: {step['service']}<br>" +
                             f"Latency: {step['latency_ms']}ms<br>" +
                             f"Status: {step['status']}<br>" +
                             f"<extra></extra>"
            ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=0, b=0),
            barmode='stack',
            showlegend=False,
            xaxis_title="Time (ms)",
            yaxis_title="Stage"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown
        st.markdown("##### 📋 Stage Details")
        
        chain_df = pd.DataFrame(chain)
        chain_df = chain_df[['timestamp', 'stage', 'service', 'latency_ms', 'status']]
        st.dataframe(chain_df, use_container_width=True, hide_index=True)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_latency = sum(step['latency_ms'] for step in chain)
        
        with col1:
            st.metric("Total Latency", f"{total_latency}ms", help="Sum of all stage latencies")
        with col2:
            st.metric("Stages Completed", len(chain), help="Number of pipeline stages")
        with col3:
            st.metric("Success Rate", "100%", help="Percentage of successful stages")
        with col4:
            slowest = max(chain, key=lambda x: x['latency_ms'])
            st.metric("Slowest Stage", slowest['stage'], help=f"{slowest['latency_ms']}ms")
        
        st.markdown("---")
        
        # SPL Query to retrieve this trace
        st.markdown("##### 💻 SPL Query to Reconstruct This Chain")
        
        if st.session_state.show_help:
            show_info_card(
                "💻 Trace Reconstruction",
                "This SPL query retrieves all log entries with the same trace ID and orders them chronologically. " 
                "Copy this query and run it in the Processing layer to see actual results."
            )
        
        spl_query = f"""index=aiml_rag trace_id="{trace_id}" 
| transaction trace_id maxspan=30s 
| table _time, service, stage, latency_ms, status
| sort _time"""
        
        st.code(spl_query, language="spl")
        
        # Raw log samples
        with st.expander("📄 View Raw Log Samples"):
            for step in chain:
                st.json({
                    "timestamp": step['timestamp'],
                    "trace_id": trace_id,
                    "service": step['service'],
                    "stage": step['stage'],
                    "latency_ms": step['latency_ms'],
                    "status": step['status'],
                    "environment": "production",
                    "region": "us-west-2"
                })

else:  # Real-time Monitoring
    if st.session_state.show_help:
        show_info_card(
            "⚡ Real-time System Monitoring",
            "Live dashboard showing current system status across all components. " 
            "Enable auto-refresh to see metrics update automatically every 5 seconds."
        )
    
    st.header("⚡ Real-time System Monitoring")
    
    st.markdown("##### 🎛️ Live System Metrics")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox(
        "🔄 Auto-refresh (5 seconds)", 
        value=True,
        help="Automatically refresh metrics every 5 seconds"
    )
    
    if auto_refresh:
        time.sleep(5)
        st.rerun()
    
    if st.session_state.show_help:
        show_help_bubble("📊 All metrics refresh automatically when auto-refresh is enabled")
    
    # Real-time metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Ingestion Rate", 
            f"{random.randint(2500, 3500)}/s", 
            delta=f"+{random.randint(50, 200)}",
            help="Events ingested per second"
        )
    with col2:
        st.metric(
            "Query Load", 
            f"{random.randint(150, 250)}/s", 
            delta=f"+{random.randint(-20, 30)}",
            help="Search queries per second"
        )
    with col3:
        st.metric(
            "Indexer CPU", 
            f"{random.randint(45, 75)}%", 
            delta=f"+{random.randint(-5, 10)}%",
            help="Average CPU across indexers"
        )
    with col4:
        st.metric(
            "Network I/O", 
            f"{random.randint(800, 1200)} Mbps", 
            delta=f"+{random.randint(-50, 100)}",
            help="Network throughput"
        )
    with col5:
        st.metric(
            "Active Queries", 
            f"{random.randint(50, 100)}", 
            delta=f"+{random.randint(-10, 15)}",
            help="Currently executing queries"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📊 Live Ingestion Rate")
        
        # Generate live data
        seconds = list(range(60))
        rates = [random.randint(2000, 4000) for _ in range(60)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=seconds,
            y=rates,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#10B981', width=2),
            fillcolor='rgba(16, 185, 129, 0.2)',
            hovertemplate='<b>%{x} sec ago</b><br>Rate: %{y} logs/sec<extra></extra>'
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Seconds Ago",
            yaxis_title="Events/sec"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### ⚡ Query Response Time")
        
        seconds = list(range(60))
        response_times = [random.randint(200, 1000) for _ in range(60)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=seconds,
            y=response_times,
            mode='lines',
            line=dict(color='#3B82F6', width=2),
            hovertemplate='<b>%{x} sec ago</b><br>Response: %{y}ms<extra></extra>'
        ))
        fig.add_hline(
            y=800, 
            line_dash="dash", 
            line_color="red",
            annotation_text="SLA Threshold (800ms)",
            annotation_position="right"
        )
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Seconds Ago",
            yaxis_title="Response Time (ms)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("##### 🖥️ Cluster Health")
    
    if st.session_state.show_help:
        show_help_bubble("🖥️ Monitor the health and resource usage of all cluster components in real-time")
    
    # Cluster status
    cluster_data = {
        "Component": ["Search Head 1", "Search Head 2", "Search Head 3", "Indexer 1", "Indexer 2", 
                     "Indexer 3", "Indexer 4", "Master Node", "License Server", "Deployment Server"],
        "Status": ["🟢 Healthy", "🟢 Healthy", "🟢 Healthy", "🟢 Healthy", "🟢 Healthy",
                  "🟢 Healthy", "🟡 Warning", "🟢 Healthy", "🟢 Healthy", "🟢 Healthy"],
        "CPU %": [f"{random.randint(30, 70)}%" for _ in range(10)],
        "Memory %": [f"{random.randint(40, 80)}%" for _ in range(10)],
        "Disk %": [f"{random.randint(20, 60)}%" for _ in range(10)],
        "Network": [f"{random.randint(500, 1500)} Mbps" for _ in range(10)]
    }
    
    df = pd.DataFrame(cluster_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 2rem 0;'>
    <p><strong>🔍 AI/ML Observability Platform</strong> | Interactive Prototype v1.0</p>
    <p style='font-size: 0.9rem;'>Powered by Splunk | Built for Demonstration & Education</p>
    <p style='font-size: 0.85rem; margin-top: 0.5rem;'>
        💡 <strong>Tip:</strong> Explore all layers to see the complete platform capabilities
    </p>
</div>
""", unsafe_allow_html=True)