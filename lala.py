import streamlit as st
import time
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="🍎 NutriScan - AI Nutrition Analyzer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #10b981, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f0fdf4, #fef3c7);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #d1fae5;
        margin: 1rem 0;
        text-align: center;
    }
    
    .nutrition-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .analyzing-text {
        text-align: center;
        color: #10b981;
        font-size: 1.2rem;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'nutrition_data' not in st.session_state:
    st.session_state.nutrition_data = None
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

# Header
st.markdown('<h1 class="main-header">🍎 NutriScan</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">📸 Upload a photo of your meal and get instant nutrition insights with AI-powered analysis!</p>', unsafe_allow_html=True)

# Feature cards (only show when no image uploaded)
if not st.session_state.uploaded_image:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📸 Instant Analysis</h3>
            <p>Simply take a photo and get detailed nutrition breakdown in seconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 AI Powered</h3>
            <p>Advanced machine learning recognizes thousands of foods accurately</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Track Goals</h3>
            <p>Monitor your daily intake and stay on track with your health goals</p>
        </div>
        """, unsafe_allow_html=True)

# File upload section
st.markdown("---")
if not st.session_state.uploaded_image:
    st.markdown("### 🚀 Upload Your Food Photo")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear photo of your meal for best results! 📷"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_image = uploaded_file
        st.session_state.analyzing = True
        st.rerun()

# Analysis section
if st.session_state.uploaded_image:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🖼️ Your Food Image")
        image = Image.open(st.session_state.uploaded_image)
        st.image(image, caption="Food to analyze", use_column_width=True)
        
        if st.button("🔄 Upload New Image", type="secondary"):
            st.session_state.uploaded_image = None
            st.session_state.nutrition_data = None
            st.session_state.analyzing = False
            st.rerun()
    
    with col2:
        if st.session_state.analyzing and not st.session_state.nutrition_data:
            st.markdown('<div class="analyzing-text">🧠 AI Analyzing... Identifying nutrients</div>', unsafe_allow_html=True)
            
            # Progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
            
            # Simulate nutrition analysis
            st.session_state.nutrition_data = {
                "foodName": "Grilled Chicken Salad",
                "calories": 285,
                "protein": 26.7,
                "carbs": 12.3,
                "fat": 15.8,
                "fiber": 4.2,
                "sugar": 8.1,
                "sodium": 456
            }
            st.session_state.analyzing = False
            st.rerun()
        
        elif st.session_state.nutrition_data:
            st.markdown("### 📊 Nutrition Analysis")
            data = st.session_state.nutrition_data
            
            # Main nutrition card
            st.markdown(f"""
            <div class="nutrition-card">
                <h3 style="color: #10b981; margin-bottom: 1rem;">🍽️ {data['foodName']}</h3>
                <div style="font-size: 2rem; font-weight: bold; color: #1f2937; text-align: center; margin: 1rem 0;">
                    {data['calories']} <span style="font-size: 1rem; color: #6b7280;">calories</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📈 Detailed Breakdown")
            
            # Nutrition metrics
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric("🥩 Protein", f"{data['protein']}g", "26%")
                st.metric("🍞 Carbs", f"{data['carbs']}g", "12%")
                st.metric("🥑 Fat", f"{data['fat']}g", "16%")
                st.metric("🌾 Fiber", f"{data['fiber']}g", "4%")
            
            with col_b:
                st.metric("🍯 Sugar", f"{data['sugar']}g", "8%")
                st.metric("🧂 Sodium", f"{data['sodium']}mg", "46%")
                
                # Health score
                st.markdown("#### 🏆 Health Score")
                health_score = 85
                st.progress(health_score / 100)
                st.markdown(f"**{health_score}/100** - Excellent choice! 🌟")
            
            # Success message
            st.success("✅ Analysis Complete! Your meal looks nutritious and balanced! 🎉")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f0fdf4, #fef3c7); border-radius: 1rem; margin-top: 2rem;">
    <p style="color: #6b7280; margin-bottom: 0.5rem;">❤️ Made with love for healthier eating</p>
    <p style="color: #9ca3af; font-size: 0.9rem;">© 2024 NutriScan. Powered by AI • Built with care</p>
</div>
""", unsafe_allow_html=True)
