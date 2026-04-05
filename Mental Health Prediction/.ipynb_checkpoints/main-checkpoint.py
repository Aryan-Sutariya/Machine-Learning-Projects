import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import base64
import time

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64_image("analysis.jpg")

st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding: 0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Page config ---
st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

image = Image.open("analysis.jpg")

st.sidebar.image(
    image,
    use_container_width=True
)

# --- Enhanced CSS styling for login page ---
LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body, .main, .block-container {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    min-height: 100vh;
    color: white;
}

.login-container {
    display: flex;
    min-height: 100vh;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.login-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 50px 40px;
    width: 100%;
    max-width: 480px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.login-header {
    text-align: center;
    margin-bottom: 40px;
}

.login-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(45deg, #fff, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.login-header p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.1rem;
}

.input-group {
    margin-bottom: 25px;
    position: relative;
}

.input-group label {
    display: block;
    margin-bottom: 8px;
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
    font-size: 0.95rem;
}

.input-with-icon {
    position: relative;
}

.input-with-icon i {
    position: absolute;
    left: 18px;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 255, 255, 0.7);
    font-size: 1.1rem;
}

.input-with-icon input {
    width: 100%;
    padding: 16px 20px 16px 50px !important;
    background: rgba(255, 255, 255, 0.12) !important;
    border: 2px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.input-with-icon input:focus {
    border-color: #f093fb !important;
    background: rgba(255, 255, 255, 0.18) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(240, 147, 251, 0.2) !important;
}

.input-with-icon input::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
}

.login-btn {
    width: 100%;
    padding: 16px !important;
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin-top: 10px !important;
}

.login-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4) !important;
}

.login-footer {
    text-align: center;
    margin-top: 30px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
}

.login-footer a {
    color: #f093fb;
    text-decoration: none;
    font-weight: 500;
}

.features {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
    text-align: center;
}

.feature-item {
    flex: 1;
    padding: 15px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    margin: 0 5px;
}

.feature-item i {
    font-size: 1.5rem;
    margin-bottom: 10px;
    color: #f093fb;
}

.feature-item p {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.8);
}

.stAlert {
    border-radius: 10px !important;
    margin-top: 20px !important;
}

/* About Us Page Styles */
.about-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 80px 0 40px;
    text-align: center;
    border-radius: 0 0 30px 30px;
    margin-bottom: 40px;
}

.about-header h1 {
    font-size: 3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 20px;
}

.about-header p {
    font-size: 1.2rem;
    color: rgba(255, 255, 255, 0.9);
    max-width: 800px;
    margin: 0 auto;
}

.team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin: 40px 0;
}

.team-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.team-card:hover {
    transform: translateY(-10px);
}

.team-card img {
    width: 100%;
    height: 250px;
    object-fit: cover;
}

.team-info {
    padding: 25px;
}

.team-info h3 {
    color: #333;
    margin-bottom: 5px;
    font-size: 1.3rem;
}

.team-info .role {
    color: #667eea;
    font-weight: 600;
    margin-bottom: 15px;
}

.team-info p {
    color: #666;
    line-height: 1.6;
}

.mission-vision {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 20px;
    padding: 40px;
    margin: 50px 0;
    color: white;
}

.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 40px 0;
}

.stat-card {
    background: white;
    border-radius: 15px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.stat-card .number {
    font-size: 2.5rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 10px;
}

.stat-card .label {
    color: #666;
    font-size: 1.1rem;
    font-weight: 500;
}

.contact-info {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 40px;
    margin-top: 40px;
}
</style>
"""

# --- Initialize session state ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Enhanced Login page ---
def login_page():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <h1>🔐 Welcome Back</h1>
                <p>Sign in to access your Business Analytics Dashboard</p>
            </div>
            
            <form>
                <div class="input-group">
                    <label for="username">Username</label>
                    <div class="input-with-icon">
                        <i>👤</i>
                        <input type="text" id="username" name="username" placeholder="Enter your username">
                    </div>
                </div>
                
                <div class="input-group">
                    <label for="password">Password</label>
                    <div class="input-with-icon">
                        <i>🔒</i>
                        <input type="password" id="password" name="password" placeholder="Enter your password">
                    </div>
                </div>
                
                <button type="submit" class="login-btn">Sign In</button>
            </form>
            
            <div class="login-footer">
                <p>Demo credentials: admin / admin</p>
                <p>Need help? <a href="#">Contact Support</a></p>
            </div>
            
            <div class="features">
                <div class="feature-item">
                    <i>📊</i>
                    <p>Real-time Analytics</p>
                </div>
                <div class="feature-item">
                    <i>🔒</i>
                    <p>Secure Access</p>
                </div>
                <div class="feature-item">
                    <i>📈</i>
                    <p>Data Insights</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate form submission
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input(" ", placeholder="Enter username", key="username_input", label_visibility="collapsed")
            password = st.text_input(" ", placeholder="Enter password", type="password", key="password_input", label_visibility="collapsed")
            
            if st.button("Sign In", type="primary", use_container_width=True):
                if username == "admin" and password == "admin":
                    with st.spinner("Authenticating..."):
                        time.sleep(1)  # Simulate loading
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try admin/admin")

# --- About Us Page ---
def about_us_page():
    st.markdown("""
    <style>
    .about-container {
        padding: 20px;
    }
    .section {
        margin-bottom: 50px;
    }
    .section-title {
        color: #667eea;
        font-size: 2rem;
        margin-bottom: 20px;
        border-bottom: 3px solid #f093fb;
        padding-bottom: 10px;
    }
    .highlight-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(240, 147, 251, 0.1));
        border-left: 5px solid #667eea;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .team-member {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .team-member:hover {
        transform: translateY(-5px);
    }
    .team-member img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 15px;
        border: 5px solid #f093fb;
    }
    .contact-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    </style>
    
    <div class="about-container">
        <div style="text-align: center; margin-bottom: 40px;">
            <h1 style="font-size: 3rem; color: #667eea; margin-bottom: 20px;">🌟 About Us</h1>
            <p style="font-size: 1.2rem; color: #666; max-width: 800px; margin: 0 auto;">
                Empowering businesses with cutting-edge analytics solutions since 2015
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Company Overview
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Our Story</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="padding: 20px; background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h3 style="color: #667eea;">Who We Are</h3>
            <p style="color: #666; line-height: 1.6;">
                We are a team of passionate data scientists, business analysts, and technology experts 
                dedicated to transforming raw data into actionable insights. Our mission is to empower 
                organizations with intuitive analytics tools that drive informed decision-making and 
                sustainable growth.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 20px; background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h3 style="color: #667eea;">Our Vision</h3>
            <p style="color: #666; line-height: 1.6;">
                To become the global leader in business intelligence solutions, making advanced analytics 
                accessible to businesses of all sizes. We envision a world where data-driven decisions 
                are the norm, not the exception.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mission & Values
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Mission & Values</h2>', unsafe_allow_html=True)
    
    values = [
        {"icon": "🎯", "title": "Excellence", "desc": "Delivering exceptional quality in everything we do"},
        {"icon": "🤝", "title": "Integrity", "desc": "Building trust through transparency and honesty"},
        {"icon": "💡", "title": "Innovation", "desc": "Continuously pushing boundaries in analytics"},
        {"icon": "🌱", "title": "Sustainability", "desc": "Promoting ethical and sustainable business practices"},
    ]
    
    cols = st.columns(4)
    for idx, value in enumerate(values):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: white; border-radius: 15px; 
                        box-shadow: 0 5px 15px rgba(0,0,0,0.1); height: 250px;">
                <div style="font-size: 3rem; margin-bottom: 15px;">{value['icon']}</div>
                <h4 style="color: #667eea; margin-bottom: 10px;">{value['title']}</h4>
                <p style="color: #666; font-size: 0.9rem;">{value['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Team Section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Meet Our Team</h2>', unsafe_allow_html=True)
    
    team_members = [
        {"name": "Sarah Johnson", "role": "CEO & Founder", "desc": "15+ years in business analytics"},
        {"name": "Michael Chen", "role": "Chief Data Scientist", "desc": "PhD in Data Science, MIT"},
        {"name": "Emma Wilson", "role": "Product Director", "desc": "Ex-Google Product Manager"},
        {"name": "David Park", "role": "Lead Developer", "desc": "Full-stack & AI specialist"},
    ]
    
    cols = st.columns(4)
    for idx, member in enumerate(team_members):
        with cols[idx]:
            # Using placeholder images from placeholder.com
            st.markdown(f"""
            <div class="team-member">
                <img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&h=150&fit=crop&crop=face&facepad=3" 
                     alt="{member['name']}">
                <h4 style="color: #333; margin: 10px 0 5px;">{member['name']}</h4>
                <p style="color: #667eea; font-weight: 600; margin-bottom: 10px;">{member['role']}</p>
                <p style="color: #666; font-size: 0.9rem;">{member['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats Section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">By The Numbers</h2>', unsafe_allow_html=True)
    
    stats = [
        {"number": "500+", "label": "Clients Worldwide"},
        {"number": "98%", "label": "Client Retention Rate"},
        {"number": "24/7", "label": "Support Availability"},
        {"number": "50+", "label": "Countries Served"},
    ]
    
    cols = st.columns(4)
    for idx, stat in enumerate(stats):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea, #764ba2); 
                        border-radius: 15px; color: white;">
                <div style="font-size: 3rem; font-weight: 700; margin-bottom: 10px;">{stat['number']}</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Contact Section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Get In Touch</h2>', unsafe_allow_html=True)
    
    contact_info = """
    <div class="contact-card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
            <div>
                <h4 style="color: #667eea; margin-bottom: 15px;">📍 Location</h4>
                <p style="color: #666;">123 Analytics Street<br>San Francisco, CA 94107<br>United States</p>
            </div>
            <div>
                <h4 style="color: #667eea; margin-bottom: 15px;">📞 Contact</h4>
                <p style="color: #666;">Phone: +1 (555) 123-4567<br>Email: info@bizanalytics.com<br>Support: support@bizanalytics.com</p>
            </div>
            <div>
                <h4 style="color: #667eea; margin-bottom: 15px;">🕒 Business Hours</h4>
                <p style="color: #666;">Monday - Friday: 9am - 6pm PST<br>Saturday: 10am - 4pm PST<br>Sunday: Closed</p>
            </div>
        </div>
    </div>
    """
    st.markdown(contact_info, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Dashboard functions ---

def load_data():
    return pd.read_csv('customers.csv')

def metrics(df_selection):
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2, col3 = st.columns(3)

    col1.metric(label="Total Customers", value=df_selection.Gender.count(), delta="All customers")
    col2.metric(label="Total Annual Salary", value=f"{df_selection.AnnualSalary.sum():,.0f}", delta=df_selection.AnnualSalary.median())
    col3.metric(label="Annual Salary", value=f"{df_selection.AnnualSalary.max() - df_selection.AnnualSalary.min():,.0f}", delta="Annual Salary Range")

    style_metric_cards(background_color="#121270", border_left_color="#f20045", box_shadow="3px")

def pie_chart(df_selection, div):
    with div:
        theme_plotly = None
        fig = px.pie(df_selection, values='AnnualSalary', names='Department', title='Customers by Country')
        fig.update_layout(legend_title="Country", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

def bar_chart(df_selection, div):
    with div:
        theme_plotly = None
        fig = px.bar(df_selection, y='AnnualSalary', x='Department', text_auto='.2s',
                     title="Controlled text sizes, positions and angles")
        fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

def table(df, df_selection):
    with st.expander("Tabular"):
        shwdata = st.multiselect('Filter columns:', df.columns, default=["EEID","FullName","JobTitle","Department","BusinessUnit","Gender","Ethnicity","Age","HireDate","AnnualSalary","Bonus","Country","City","id"])
        st.dataframe(df_selection[shwdata], use_container_width=True)

def dashboard():
    df = load_data()

    # Sidebar filters
    st.sidebar.header("Please filter")
    department = st.sidebar.multiselect("Filter Department", options=df["Department"].unique(), default=df["Department"].unique())
    country = st.sidebar.multiselect("Filter Country", options=df["Country"].unique(), default=df["Country"].unique())
    businessunit = st.sidebar.multiselect("Filter Business", options=df["BusinessUnit"].unique(), default=df["BusinessUnit"].unique())

    df_selection = df.query("Department==@department & Country==@country & BusinessUnit==@businessunit")

    # Sidebar menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Table", "About Us", "Logout"],
            icons=["house", "book", "info-circle", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical"
        )

    # Main content based on menu selection
    if selected == "Home":
        st.subheader("📈 Business Analytics Dashboard ")
        div1, div2 = st.columns(2)
        pie_chart(df_selection, div1)
        bar_chart(df_selection, div2)
        metrics(df_selection)

    elif selected == "Table":
        st.subheader("📊 Customer Data Table")
        metrics(df_selection)
        table(df, df_selection)
    
    elif selected == "About Us":
        about_us_page()

    elif selected == "Logout":
        st.session_state.logged_in = False
        st.rerun()

# --- Main app flow ---
def main():
    if st.session_state.logged_in:
        dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()