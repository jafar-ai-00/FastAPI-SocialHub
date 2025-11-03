import streamlit as st
import requests
from datetime import datetime
import time

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Simple Social",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Feed"

API_BASE_URL = "http://localhost:8000"


# ─────────────────────────────────────────────
# Modern Styling
# ─────────────────────────────────────────────
def load_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Login Card */
        .login-container {
            max-width: 450px;
            margin: 5rem auto;
            padding: 3rem;
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            animation: fadeIn 0.6s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .login-subtitle {
            color: #718096;
            font-size: 1rem;
            font-weight: 400;
        }
        
        /* Feed Header */
        .feed-header {
            text-align: center;
            padding: 2rem 0 1rem 0;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 0 0 30px 30px;
            margin: -1rem -1rem 2rem -1rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .feed-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Post Card */
        .post-card {
            background: white;
            border-radius: 20px;
            padding: 0;
            margin: 1.5rem auto;
            max-width: 650px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            overflow: hidden;
        }
        
        .post-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
        }
        
        .post-header {
            display: flex;
            align-items: center;
            padding: 1.5rem;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.2rem;
            margin-right: 1rem;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .post-user-info {
            flex: 1;
        }
        
        .post-username {
            font-weight: 600;
            color: #2d3748;
            font-size: 0.95rem;
            margin: 0;
        }
        
        .post-time {
            color: #a0aec0;
            font-size: 0.85rem;
            margin-top: 2px;
        }
        
        .post-content {
            padding: 0;
        }
        
        .post-caption {
            padding: 1.5rem;
            background: #f7fafc;
            border-top: 1px solid #f0f0f0;
        }
        
        .caption-text {
            color: #2d3748;
            line-height: 1.6;
            margin: 0;
        }
        
        .caption-author {
            font-weight: 600;
            color: #667eea;
        }
        
        /* Upload Card */
        .upload-container {
            max-width: 700px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: white;
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }
        
        .upload-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            max-width: 500px;
            margin: 3rem auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .empty-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        
        .empty-text {
            color: #718096;
            font-size: 1.1rem;
            margin: 0;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        [data-testid="stSidebar"] .sidebar-content {
            padding: 2rem 1rem;
        }
        
        .sidebar-user {
            text-align: center;
            padding: 2rem 1rem;
            color: white;
        }
        
        .sidebar-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: white;
            color: #667eea;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 2rem;
            margin: 0 auto 1rem auto;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }
        
        .sidebar-email {
            font-weight: 600;
            font-size: 0.95rem;
            word-break: break-word;
        }
        
        /* Buttons */
        .stButton > button {
            width: 100%;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            font-size: 0.95rem;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Success/Error Messages */
        .stSuccess, .stError {
            border-radius: 12px;
            padding: 1rem;
            font-weight: 500;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Responsive */
        @media (max-width: 768px) {
            .login-container, .upload-container {
                margin: 2rem 1rem;
                padding: 2rem 1.5rem;
            }
            
            .feed-title, .login-title {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────
def get_headers():
    """Get authorization headers with current token"""
    return {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}


def get_avatar_letter(email: str) -> str:
    """Get first letter of email for avatar"""
    return email[0].upper() if email else "?"


def format_date(date_string: str) -> str:
    """Format date string to relative time"""
    try:
        post_date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        now = datetime.now(post_date.tzinfo)
        diff = now - post_date
        
        if diff.days == 0:
            if diff.seconds < 60:
                return "Just now"
            elif diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes}m ago"
            else:
                hours = diff.seconds // 3600
                return f"{hours}h ago"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days}d ago"
        else:
            return post_date.strftime("%b %d, %Y")
    except Exception:
        return date_string


# ─────────────────────────────────────────────
# Login Page
# ─────────────────────────────────────────────
def login_page():
    load_custom_css()
    
    st.markdown("""
        <div class='login-container'>
            <div class='login-header'>
                <div class='login-title'>🚀 Simple Social</div>
                <p class='login-subtitle'>Share your moments & connect with others</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            email = st.text_input(
                "Email Address",
                placeholder="your@email.com",
                key="login_email",
                label_visibility="collapsed"
            )
            
            st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
                label_visibility="collapsed"
            )
            
            st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
            
            col_login, col_signup = st.columns(2)
            
            with col_login:
                if st.button("🔐 Login", use_container_width=True, type="primary"):
                    if not email or not password:
                        st.error("⚠️ Please fill in all fields")
                    else:
                        with st.spinner("Logging in..."):
                            try:
                                response = requests.post(
                                    f"{API_BASE_URL}/auth/jwt/login",
                                    data={"username": email, "password": password},
                                    timeout=10
                                )
                                
                                if response.status_code == 200:
                                    st.session_state.token = response.json()["access_token"]
                                    user_response = requests.get(
                                        f"{API_BASE_URL}/users/me",
                                        headers=get_headers(),
                                        timeout=10
                                    )
                                    st.session_state.user = user_response.json()
                                    st.success("🎉 Welcome back!")
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    st.error("❌ Invalid email or password")
                            except requests.exceptions.ConnectionError:
                                st.error("⚠️ Cannot connect to server. Is it running?")
                            except Exception as e:
                                st.error(f"⚠️ Error: {str(e)}")
            
            with col_signup:
                if st.button("✨ Sign Up", use_container_width=True):
                    if not email or not password:
                        st.error("⚠️ Please fill in all fields")
                    elif len(password) < 6:
                        st.error("⚠️ Password must be at least 6 characters")
                    else:
                        with st.spinner("Creating account..."):
                            try:
                                response = requests.post(
                                    f"{API_BASE_URL}/auth/register",
                                    json={"email": email, "password": password},
                                    timeout=10
                                )
                                
                                if response.status_code == 201:
                                    st.success("✅ Account created! Please log in.")
                                else:
                                    error_detail = response.json().get('detail', 'Registration failed')
                                    st.error(f"❌ {error_detail}")
                            except requests.exceptions.ConnectionError:
                                st.error("⚠️ Cannot connect to server. Is it running?")
                            except Exception as e:
                                st.error(f"⚠️ Error: {str(e)}")


# ─────────────────────────────────────────────
# Upload Page
# ─────────────────────────────────────────────
def upload_page():
    load_custom_css()
    
    st.markdown("""
        <div class='upload-container'>
            <h1 class='upload-title'>📸 Share Something Amazing</h1>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'webm'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
            
            # Preview
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, use_container_width=True)
            else:
                st.video(uploaded_file)
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        caption = st.text_area(
            "Caption",
            placeholder="Write a caption for your post...",
            height=100,
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        if st.button("🚀 Share Post", use_container_width=True, type="primary", disabled=not uploaded_file):
            with st.spinner("Uploading your post..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"caption": caption if caption else ""}
                    
                    response = requests.post(
                        f"{API_BASE_URL}/upload",
                        files=files,
                        data=data,
                        headers=get_headers(),
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        st.balloons()
                        st.success("🎉 Post shared successfully!")
                        time.sleep(1)
                        st.session_state.page = "Feed"
                        st.rerun()
                    else:
                        st.error(f"❌ Upload failed: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"⚠️ Error uploading: {str(e)}")


# ─────────────────────────────────────────────
# Feed Page
# ─────────────────────────────────────────────
def feed_page():
    load_custom_css()
    
    st.markdown("""
        <div class='feed-header'>
            <h1 class='feed-title'>🏠 Your Feed</h1>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_BASE_URL}/feed", headers=get_headers(), timeout=10)
        
        if response.status_code != 200:
            st.error("❌ Failed to load feed. Please try again.")
            return
        
        posts = response.json().get("posts", [])
        
        if not posts:
            st.markdown("""
                <div class='empty-state'>
                    <div class='empty-icon'>🎨</div>
                    <p class='empty-text'>No posts yet. Be the first to share!</p>
                </div>
            """, unsafe_allow_html=True)
            return
        
        # Display posts
        for post in posts:
            email = post.get("email", "Anonymous")
            caption = post.get("caption", "")
            file_type = post.get("file_type", "image")
            created_at = format_date(post.get("created_at", ""))
            post_id = post.get("id")
            is_owner = post.get("is_owner", False)
            
            # Post container
            with st.container():
                st.markdown(f"""
                    <div class='post-card'>
                        <div class='post-header'>
                            <div class='avatar'>{get_avatar_letter(email)}</div>
                            <div class='post-user-info'>
                                <div class='post-username'>{email}</div>
                                <div class='post-time'>{created_at}</div>
                            </div>
                        </div>
                        <div class='post-content'>
                """, unsafe_allow_html=True)
                
                # Media content
                if file_type == "image":
                    st.image(post["url"], use_container_width=True)
                else:
                    st.video(post["url"])
                
                # Caption
                if caption:
                    st.markdown(f"""
                        <div class='post-caption'>
                            <p class='caption-text'>
                                <span class='caption-author'>{email.split('@')[0]}</span>
                                {' ' + caption}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Delete button for owner
                if is_owner:
                    col1, col2, col3 = st.columns([4, 1, 1])
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_{post_id}", use_container_width=True):
                            with st.spinner("Deleting..."):
                                try:
                                    del_response = requests.delete(
                                        f"{API_BASE_URL}/posts/{post_id}",
                                        headers=get_headers(),
                                        timeout=10
                                    )
                                    if del_response.status_code == 200:
                                        st.success("✅ Post deleted!")
                                        time.sleep(0.5)
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to delete post")
                                except Exception as e:
                                    st.error(f"⚠️ Error: {str(e)}")
                
                st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to server. Please check if it's running.")
    except Exception as e:
        st.error(f"⚠️ Error loading feed: {str(e)}")


# ─────────────────────────────────────────────
# Main Application Logic
# ─────────────────────────────────────────────
def main():
    if st.session_state.user is None:
        login_page()
    else:
        load_custom_css()
        user_email = st.session_state.user.get("email", "User")
        
        # Sidebar
        with st.sidebar:
            st.markdown(f"""
                <div class='sidebar-user'>
                    <div class='sidebar-avatar'>{get_avatar_letter(user_email)}</div>
                    <div class='sidebar-email'>{user_email}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            page_choice = st.radio(
                "Navigation",
                ["🏠 Feed", "📸 Upload"],
                label_visibility="collapsed"
            )
            
            st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.token = None
                st.rerun()
        
        # Main content
        if page_choice == "📸 Upload":
            upload_page()
        else:
            feed_page()


if __name__ == "__main__":
    main()