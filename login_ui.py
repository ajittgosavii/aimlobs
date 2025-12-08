"""
Login UI Module
Provides login, registration, and password reset interfaces
"""

import streamlit as st
import auth

def show_login_page():
    """Display login page"""
    
    # Initialize session state
    auth.init_session_state()
    
    # If already authenticated, show welcome message
    if auth.is_authenticated():
        show_authenticated_ui()
        return
    
    # Login UI
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #1e40af;'>🔐 AI/ML Observability Platform</h1>
        <p style='color: #64748b; font-size: 1.1rem;'>Please sign in to continue</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for Login / Register / Reset
    tab1, tab2, tab3 = st.tabs(["🔑 Login", "📝 Register", "🔄 Reset Password"])
    
    # Login Tab
    with tab1:
        with st.form("login_form"):
            st.markdown("### Sign In")
            email = st.text_input("Email Address", placeholder="you@company.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                submit = st.form_submit_button("🔓 Sign In", use_container_width=True, type="primary")
            with col2:
                remember_me = st.checkbox("Remember me", value=True)
            
            if submit:
                if not email or not password:
                    st.error("❌ Please enter both email and password")
                else:
                    with st.spinner("Authenticating..."):
                        user_info = auth.verify_user(email, password)
                        
                        if user_info:
                            if user_info['status'] == 'active':
                                auth.login_user(user_info)
                                st.success(f"✅ Welcome back, {user_info['display_name']}!")
                                
                                if user_info['is_admin']:
                                    st.info("🔑 Admin access granted")
                                
                                st.rerun()
                            else:
                                st.error("❌ Your account has been deactivated. Please contact support.")
                        else:
                            st.error("❌ Invalid email or password")
    
    # Register Tab
    with tab2:
        with st.form("register_form"):
            st.markdown("### Create Account")
            
            st.info("⚠️ Self-registration is currently disabled. Please contact your administrator to create an account.")
            
            reg_email = st.text_input("Email Address", placeholder="you@company.com", disabled=True)
            reg_name = st.text_input("Full Name", placeholder="John Doe", disabled=True)
            reg_password = st.text_input("Password", type="password", placeholder="Min 6 characters", disabled=True)
            reg_password_confirm = st.text_input("Confirm Password", type="password", disabled=True)
            
            submit_register = st.form_submit_button("📝 Create Account", use_container_width=True, disabled=True)
    
    # Reset Password Tab
    with tab3:
        with st.form("reset_form"):
            st.markdown("### Reset Password")
            reset_email = st.text_input("Email Address", placeholder="you@company.com")
            
            submit_reset = st.form_submit_button("📧 Send Reset Link", use_container_width=True, type="primary")
            
            if submit_reset:
                if not reset_email:
                    st.error("❌ Please enter your email address")
                else:
                    with st.spinner("Sending reset link..."):
                        if auth.send_password_reset_email(reset_email):
                            st.success("✅ Password reset email sent! Check your inbox.")
                            st.info("💡 If you don't receive it, check your spam folder")
                        else:
                            st.error("❌ Failed to send reset email. Please try again.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>
        <p>© 2024 AI/ML Observability Platform • Secure Authentication via Firebase</p>
        <p>Need help? Contact support@yourcompany.com</p>
    </div>
    """, unsafe_allow_html=True)


def show_authenticated_ui():
    """Show UI for authenticated users"""
    
    user = auth.get_current_user()
    
    # User info in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 User Profile")
        
        st.markdown(f"""
        **{user['display_name']}**  
        {user['email']}
        """)
        
        if auth.is_admin():
            st.markdown("""
            <div style='background: #dbeafe; padding: 0.5rem; border-radius: 4px; text-align: center;'>
                <strong style='color: #1e40af;'>🔑 ADMIN</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            auth.logout_user()
            st.rerun()


def require_auth(func):
    """Decorator to require authentication for a page"""
    def wrapper(*args, **kwargs):
        if not auth.is_authenticated():
            show_login_page()
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_admin(func):
    """Decorator to require admin privileges for a page"""
    def wrapper(*args, **kwargs):
        if not auth.is_authenticated():
            show_login_page()
            st.stop()
        
        if not auth.is_admin():
            st.error("❌ Access Denied: Admin privileges required")
            st.stop()
        
        return func(*args, **kwargs)
    return wrapper
