import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import numpy as np

st.set_page_config(
    page_title="Green Guardian",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: 
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: 
        text-align: center;
        margin-bottom: 1rem;
    }
    .score-display {
        font-size: 2rem;
        color: 
        text-align: center;
        background: linear-gradient(90deg, 
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid 
    }
    .tip-box {
        background: linear-gradient(135deg, 
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid 
        margin: 1rem 0;
    }
    .material-table {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .pledge-container {
        background: linear-gradient(135deg, 
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid 
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

if 'building_type' not in st.session_state:
    st.session_state.building_type = "Home"
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Home"
if 'questionnaire_completed' not in st.session_state:
    st.session_state.questionnaire_completed = False
if 'questionnaire_answers' not in st.session_state:
    st.session_state.questionnaire_answers = {}
if 'missed_items' not in st.session_state:
    st.session_state.missed_items = []
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'pledges_made' not in st.session_state:
    st.session_state.pledges_made = 0
if 'co2_reduced' not in st.session_state:
    st.session_state.co2_reduced = 0
if 'buildings_improved' not in st.session_state:
    st.session_state.buildings_improved = 0

st.sidebar.markdown("## 🌱 Green Guardian Navigation")

if 'page_redirect' in st.session_state and st.session_state.page_redirect:
    st.session_state.current_page = st.session_state.page_redirect
    st.session_state.page_redirect = None

page = st.sidebar.selectbox(
    "Choose a page:",
    ["🏠 Home", "📊 Evaluation", "💡 Tips", "📈 Infographic", "🔍 Material Comparison", "🏆 Green Pledge"],
    index=["🏠 Home", "📊 Evaluation", "💡 Tips", "📈 Infographic", "🔍 Material Comparison", "🏆 Green Pledge"].index(st.session_state.current_page)
)

if page != st.session_state.current_page:
    st.session_state.current_page = page

def calculate_score():
    """Calculate weighted + normalized professional-grade sustainability score"""

    if not st.session_state.questionnaire_completed:
        return 0

    questionnaire_data = get_questionnaire_data()

    weights = {
        "Energy Efficiency": 0.30,
        "Water Conservation": 0.25,
        "Waste Management": 0.25,
        "Material Sustainability": 0.20
    }

    total_weighted_score = 0

    for category, questions in questionnaire_data.items():
        yes_count = sum(
            1 for q in questions
            if st.session_state.questionnaire_answers.get(q, False)
        )

        category_score = yes_count / len(questions)       
        weighted_score = category_score * weights[category]

        total_weighted_score += weighted_score

    final_score = total_weighted_score * 100

    
    critical_questions = [
        "Does your building use LED lighting throughout?",
        "Is your building well-insulated (walls, attic, basement)?",
        "Is there a rainwater harvesting system in place?",
        "Is there a comprehensive recycling program?"
    ]

    penalty = 0
    for cq in critical_questions:
        if not st.session_state.questionnaire_answers.get(cq, False):
            penalty += 5       

    final_score -= penalty


    final_score = max(0, min(100, round(final_score)))

    st.session_state.total_score = final_score
    return final_score


def get_questionnaire_data():
    """Get questionnaire questions organized by category"""
    return {
        "Energy Efficiency": [
            "Does your building use LED lighting throughout?",
            "Is your building well-insulated (walls, attic, basement)?",
            "Do you have a programmable or smart thermostat?",
            "Does your building use solar panels or renewable energy?",
            "Are your windows energy-efficient (double/triple-pane)?"
        ],
        "Water Conservation": [
            "Does your building have low-flow showerheads and faucets?",
            "Do you use dual-flush or low-flow toilets?",
            "Is there a rainwater harvesting system in place?",
            "Does your landscaping use drought-resistant plants?",
            "Are there systems in place to quickly detect and fix leaks?"
        ],
        "Waste Management": [
            "Is there a comprehensive recycling program?",
            "Do you compost organic waste?",
            "Are there efforts to reduce packaging waste?",
            "Do you donate or repurpose items instead of discarding?",
            "Are reusable materials prioritized over single-use items?"
        ],
        "Material Sustainability": [
            "Are building materials made from recycled content?",
            "Do you use locally-sourced building materials?",
            "Are low-VOC paints and finishes used throughout?",
            "Is sustainable flooring (bamboo, cork, reclaimed wood) installed?",
            "Are furniture and fixtures made from sustainable materials?"
        ]
    }

def get_score_category(score):
    """Get score category and emoji"""
    if score >= 80:
        return "Excellent", "🌟"
    elif score >= 60:
        return "Good", "👍"
    elif score >= 40:
        return "Fair", "⚠️"
    else:
        return "Needs Improvement", "🔧"

def home_page():
    """Home page with welcome message and description"""
    st.markdown('<h1 class="main-header">🌱 Welcome to Green Guardian</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #F0FFF0, #E6FFE6); border-radius: 15px; border: 2px solid #2E8B57;">
            <h2 style="color: #2E8B57;">🏗️ Sustainable Construction Evaluation Platform</h2>
            <p style="font-size: 1.2rem; color: #1E4D3D; line-height: 1.6;">
                Green Guardian is your comprehensive tool for evaluating and promoting sustainable construction practices. 
                Our platform helps you assess building sustainability, learn about eco-friendly materials, 
                and get personalized recommendations for creating greener spaces.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<h2 class="sub-header">🎯 What You Can Do</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="tip-box">
            <h3>📊 Building Evaluation</h3>
            <p>Assess your building's sustainability across four key areas: Energy Efficiency, Water Conservation, Waste Management, and Material Sustainability.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="tip-box">
            <h3>💡 Personalized Tips</h3>
            <p>Receive customized recommendations based on your evaluation scores to improve your building's environmental impact.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="tip-box">
            <h3>🏆 Green Certification</h3>
            <p>Generate and download your personalized Green Guardian certificate to showcase your commitment to sustainability.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Your Green Building Evaluation", type="primary", use_container_width=True):
            st.session_state.page_redirect = "📊 Evaluation"
            st.rerun()

def evaluation_page():
    """Evaluation page with questionnaire system"""
    st.markdown('<h1 class="main-header">📊 Green Building Evaluation</h1>', unsafe_allow_html=True)

    st.markdown("### 🏢 Building Information")
    st.session_state.building_type = st.selectbox(
        "Select Building Type:",
        ["Home", "Office", "School"],
        index=["Home", "Office", "School"].index(st.session_state.building_type)
    )

    st.markdown("---")

    st.markdown("### 📋 Sustainability Questionnaire")
    st.markdown("""
    <div class="tip-box">
        <p><strong>Instructions:</strong> Answer the following questions honestly about your building. Each "Yes" earns you points toward your sustainability score. Questions you answer "No" to will generate personalized improvement recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    questionnaire_data = get_questionnaire_data()

    for category, questions in questionnaire_data.items():
        for question in questions:
            if question not in st.session_state.questionnaire_answers:
                st.session_state.questionnaire_answers[question] = False

    col1, col2 = st.columns([2, 1])

    with col1:

        missed_items = []

        for category, questions in questionnaire_data.items():

            icons = {
                "Energy Efficiency": "⚡",
                "Water Conservation": "💧", 
                "Waste Management": "♻️",
                "Material Sustainability": "🌿"
            }

            st.markdown(f"#### {icons[category]} {category}")

            for i, question in enumerate(questions):
                col_q1, col_q2 = st.columns([4, 1])

                with col_q1:
                    st.markdown(f"**{question}**")

                with col_q2:

                    answer = st.radio(
                        "Answer",
                        ["No", "Yes"],
                        index=1 if st.session_state.questionnaire_answers[question] else 0,
                        key=f"question_{category}_{i}",
                        horizontal=True,
                        label_visibility="collapsed"
                    )

                    st.session_state.questionnaire_answers[question] = (answer == "Yes")

                    if answer == "No":
                        missed_items.append({
                            "category": category,
                            "question": question,
                            "icon": icons[category]
                        })

            st.markdown("---")

        st.session_state.missed_items = missed_items

        st.session_state.questionnaire_completed = True

        if st.button("🎯 Complete Evaluation & View Results", type="primary", use_container_width=True):
            st.success("✅ Evaluation completed! Your personalized results and tips are ready.")
            st.balloons()

    with col2:

        current_score = calculate_score()
        category, emoji = get_score_category(current_score)

        st.markdown(f"""
        <div class="score-display">
            <h3>Your Green Score</h3>
            <h1>{emoji} {current_score}%</h1>
            <h4>{category}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📋 Score Breakdown")

        category_scores = {}
        for cat, questions in questionnaire_data.items():
            yes_count = sum(1 for q in questions if st.session_state.questionnaire_answers.get(q, False))
            category_score = round((yes_count / len(questions)) * 100)
            category_scores[cat] = category_score
            st.metric(cat, f"{category_score}%")

        st.markdown("### 📊 Visual Progress")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Green Score"},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#32CD32"},
                'steps': [
                    {'range': [0, 40], 'color': "#FFB6C1"},
                    {'range': [40, 60], 'color': "#FFFF99"},
                    {'range': [60, 80], 'color': "#98FB98"},
                    {'range': [80, 100], 'color': "#32CD32"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📈 Quick Stats")
        questionnaire_data = get_questionnaire_data()
        total_questions = sum(len(questions) for questions in questionnaire_data.values())
        yes_answers = sum(1 for answer in st.session_state.questionnaire_answers.values() if answer)

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Questions Answered", f"{len(st.session_state.questionnaire_answers)}/{total_questions}")
        with col_b:
            st.metric("Yes Answers", f"{yes_answers}/{total_questions}")

        if current_score > 0:
            st.markdown("---")
            st.markdown("""
            <div style="background: #E6FFE6; padding: 1rem; border-radius: 8px; border-left: 4px solid #32CD32;">
                <p><strong>Next Steps:</strong></p>
                <p>📊 View your detailed results in the <strong>Infographic</strong> page</p>
                <p>💡 Get personalized tips in the <strong>Tips</strong> page</p>
                <p>🏆 Generate your certificate in the <strong>Green Pledge</strong> page</p>
            </div>
            """, unsafe_allow_html=True)

def tips_page():
    """Tips page with personalized recommendations based on questionnaire"""
    st.markdown('<h1 class="main-header">💡 Personalized Green Building Tips</h1>', unsafe_allow_html=True)

    current_score = calculate_score()
    category, emoji = get_score_category(current_score)

    st.markdown(f"""
    <div class="score-display">
        <h3>Your Current Score: {emoji} {current_score}% ({category})</h3>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.questionnaire_completed:
        st.markdown("""
        <div class="tip-box">
            <h3>⚠️ Complete Your Evaluation First</h3>
            <p>To receive personalized recommendations, please complete the building evaluation questionnaire first.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Go to Evaluation", type="primary"):
            st.session_state.page_redirect = "📊 Evaluation"
            st.rerun()
        return

    question_tips = {
        "Home": {
            "Does your building use LED lighting throughout?": "🔌 Replace incandescent and CFL bulbs with LED lighting throughout your home - they use 75% less energy and last 25 times longer",
            "Is your building well-insulated (walls, attic, basement)?": "🏠 Add insulation to walls, attic, and basement to reduce heating/cooling costs by up to 30%",
            "Do you have a programmable or smart thermostat?": "🌡️ Install a programmable thermostat to automatically adjust temperature when away - save up to $180/year",
            "Does your building use solar panels or renewable energy?": "☀️ Consider solar panel installation - federal tax credits can cover 30% of costs",
            "Are your windows energy-efficient (double/triple-pane)?": "🪟 Upgrade to double or triple-pane windows to reduce energy loss by up to 25%",
            "Does your building have low-flow showerheads and faucets?": "🚿 Install low-flow showerheads (2.5 GPM or less) and faucet aerators to reduce water use by 30%",
            "Do you use dual-flush or low-flow toilets?": "🚽 Upgrade to dual-flush toilets that use 20% less water than standard models",
            "Is there a rainwater harvesting system in place?": "🌧️ Set up rain barrels or cisterns to collect rainwater for garden irrigation",
            "Does your landscaping use drought-resistant plants?": "🏡 Replace lawn areas with native, drought-resistant plants to reduce water usage by 50%",
            "Are there systems in place to quickly detect and fix leaks?": "💧 Install smart water leak detectors and check for leaks monthly - a small drip can waste 3,000 gallons/year",
            "Is there a comprehensive recycling program?": "♻️ Set up clearly labeled bins for different recyclables and establish pickup schedules",
            "Do you compost organic waste?": "🌱 Start a backyard compost bin for food scraps and yard waste - reduces garbage by 30%",
            "Are there efforts to reduce packaging waste?": "📦 Buy in bulk, choose products with minimal packaging, and bring reusable bags when shopping",
            "Do you donate or repurpose items instead of discarding?": "🔄 Create a donation station and research local charities that accept household items",
            "Are reusable materials prioritized over single-use items?": "🗑️ Switch to reusable containers, water bottles, and shopping bags",
            "Are building materials made from recycled content?": "🌲 Choose materials with high recycled content - recycled steel, reclaimed wood, recycled glass countertops",
            "Do you use locally-sourced building materials?": "🏠 Source materials within 500 miles to reduce transportation emissions and support local economy",
            "Are low-VOC paints and finishes used throughout?": "🎨 Use zero or low-VOC paints, stains, and finishes to improve indoor air quality",
            "Is sustainable flooring (bamboo, cork, reclaimed wood) installed?": "⚡ Install bamboo, cork, or reclaimed wood flooring - renewable and durable options",
            "Are furniture and fixtures made from sustainable materials?": "🪑 Choose furniture made from certified sustainable wood, recycled materials, or rapidly renewable resources"
        },
        "Office": {
            "Does your building use LED lighting throughout?": "💡 Convert to LED lighting with motion sensors to reduce office energy consumption by 40%",
            "Is your building well-insulated (walls, attic, basement)?": "🏢 Improve building envelope insulation to reduce HVAC costs significantly",
            "Do you have a programmable or smart thermostat?": "🌡️ Install smart building management systems for zone-based temperature control",
            "Does your building use solar panels or renewable energy?": "⚡ Consider rooftop solar or purchase renewable energy credits for your office",
            "Are your windows energy-efficient (double/triple-pane)?": "🪟 Upgrade to energy-efficient windows and add automated blinds for optimal light control",
            "Does your building have low-flow showerheads and faucets?": "🚰 Install sensor-activated faucets and low-flow fixtures in restrooms",
            "Do you use dual-flush or low-flow toilets?": "♻️ Upgrade to water-efficient toilets and consider waterless urinals",
            "Is there a rainwater harvesting system in place?": "🌧️ Install rainwater collection systems for landscape irrigation",
            "Does your landscaping use drought-resistant plants?": "🌿 Design xeriscaped areas with native, drought-resistant plants around the office",
            "Are there systems in place to quickly detect and fix leaks?": "💧 Install smart water monitoring systems to detect leaks immediately",
            "Is there a comprehensive recycling program?": "♻️ Implement comprehensive recycling stations with clear labeling throughout the office",
            "Do you compost organic waste?": "🍃 Set up composting programs for cafeteria and break room organic waste",
            "Are there efforts to reduce packaging waste?": "📄 Implement paperless policies and choose suppliers with minimal packaging",
            "Do you donate or repurpose items instead of discarding?": "🔄 Create furniture donation programs and electronics refurbishment initiatives",
            "Are reusable materials prioritized over single-use items?": "☕ Provide reusable cups, utensils, and encourage employees to bring their own",
            "Are building materials made from recycled content?": "🏢 Specify high recycled content materials for office buildouts and renovations",
            "Do you use locally-sourced building materials?": "🌱 Partner with local suppliers for office materials and furniture",
            "Are low-VOC paints and finishes used throughout?": "🎨 Use only low-emission materials to maintain healthy indoor air quality",
            "Is sustainable flooring (bamboo, cork, reclaimed wood) installed?": "⚡ Install sustainable flooring options like bamboo or carpet with recycled content",
            "Are furniture and fixtures made from sustainable materials?": "🪑 Choose office furniture with certified sustainable materials and take-back programs"
        },
        "School": {
            "Does your building use LED lighting throughout?": "💡 Upgrade to LED lighting and use this as a teaching opportunity about energy efficiency",
            "Is your building well-insulated (walls, attic, basement)?": "🏫 Improve insulation and incorporate energy monitoring into STEM curriculum",
            "Do you have a programmable or smart thermostat?": "🌡️ Install smart thermostats in each classroom for zone-based control and energy education",
            "Does your building use solar panels or renewable energy?": "⚡ Install solar panels as both energy source and educational tool for science classes",
            "Are your windows energy-efficient (double/triple-pane)?": "🪟 Upgrade windows and teach students about heat transfer and energy efficiency",
            "Does your building have low-flow showerheads and faucets?": "🚰 Install water-efficient fixtures and bottle-filling stations to reduce plastic waste",
            "Do you use dual-flush or low-flow toilets?": "♻️ Upgrade to efficient toilets and educate students about water conservation",
            "Is there a rainwater harvesting system in place?": "🌧️ Create rain gardens and collection systems as outdoor classrooms",
            "Does your landscaping use drought-resistant plants?": "💧 Plant native species and create educational gardens for biology classes",
            "Are there systems in place to quickly detect and fix leaks?": "🔧 Implement maintenance programs and teach students about water systems",
            "Is there a comprehensive recycling program?": "📚 Create student-led recycling programs with monitoring and education components",
            "Do you compost organic waste?": "🍎 Start cafeteria composting programs managed by students and science classes",
            "Are there efforts to reduce packaging waste?": "♻️ Educate students about waste reduction and implement waste-free lunch days",
            "Do you donate or repurpose items instead of discarding?": "🔄 Create student programs for electronics recycling and furniture refurbishment",
            "Are reusable materials prioritized over single-use items?": "🎒 Encourage reusable lunch containers and water bottles through incentive programs",
            "Are building materials made from recycled content?": "📚 Use recycled content materials and incorporate sustainability into construction trades classes",
            "Do you use locally-sourced building materials?": "🌱 Source local materials and teach students about supply chains and environmental impact",
            "Are low-VOC paints and finishes used throughout?": "🎨 Use healthy materials and educate about indoor air quality",
            "Is sustainable flooring (bamboo, cork, reclaimed wood) installed?": "🏫 Install sustainable flooring and use it to teach about renewable materials",
            "Are furniture and fixtures made from sustainable materials?": "♻️ Choose sustainable furniture and incorporate green building principles into curriculum"
        }
    }

    if st.session_state.missed_items:
        st.markdown("### 🎯 Your Priority Improvement Areas")
        st.markdown("""
        <div class="tip-box">
            <p><strong>Based on your questionnaire responses, here are specific recommendations for areas where you answered "No":</strong></p>
        </div>
        """, unsafe_allow_html=True)

        missed_by_category = {}
        for item in st.session_state.missed_items:
            category = item['category']
            if category not in missed_by_category:
                missed_by_category[category] = []
            missed_by_category[category].append(item)

        for category, items in missed_by_category.items():
            with st.expander(f"{items[0]['icon']} {category} - {len(items)} improvement opportunities", expanded=True):
                for item in items:
                    question = item['question']
                    if question in question_tips[st.session_state.building_type]:
                        tip = question_tips[st.session_state.building_type][question]
                        st.markdown(f"**{question}**")
                        st.markdown(f"💡 {tip}")
                        st.markdown("---")
    else:
        st.markdown("""
        <div class="score-display">
            <h3>🌟 Excellent Work!</h3>
            <p>You answered "Yes" to all sustainability questions. Your building is already highly sustainable!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📚 Additional Sustainability Tips")
    st.markdown("Even if you've implemented many green features, there's always room for improvement:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="tip-box">
            <h4>🔄 Ongoing Maintenance</h4>
            <ul>
                <li>Regular HVAC system maintenance</li>
                <li>Annual energy audits</li>
                <li>Continuous monitoring of water usage</li>
                <li>Updating older efficient systems</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="tip-box">
            <h4>🌱 Future Innovations</h4>
            <ul>
                <li>Smart home/building technologies</li>
                <li>Advanced renewable energy systems</li>
                <li>Green roof and wall installations</li>
                <li>Electric vehicle charging stations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🌟 General Green Building Tips")

    general_tips = [
        "🏆 Set specific, measurable sustainability goals",
        "📊 Regularly monitor and track your environmental impact",
        "👥 Engage all occupants in sustainability efforts",
        "🎓 Stay informed about new green building technologies",
        "🤝 Partner with local environmental organizations",
        "💚 Make sustainability a core value in your space"
    ]

    for tip in general_tips:
        st.markdown(f"- {tip}")

def infographic_page():
    """Infographic page with charts and download functionality"""
    st.markdown('<h1 class="main-header">📈 Green Building Infographic</h1>', unsafe_allow_html=True)

    current_score = calculate_score()

    if not st.session_state.questionnaire_completed:
        st.markdown("""
        <div class="tip-box">
            <h3>⚠️ Complete Your Evaluation First</h3>
            <p>To view your personalized infographic, please complete the building evaluation questionnaire first.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Go to Evaluation", type="primary"):
            st.session_state.page_redirect = "📊 Evaluation"
            st.rerun()
        return

    questionnaire_data = get_questionnaire_data()
    categories = ["Energy Efficiency", "Water Conservation", "Waste Management", "Material Sustainability"]
    scores = []

    for category in categories:
        questions = questionnaire_data[category]
        yes_count = sum(1 for q in questions if st.session_state.questionnaire_answers.get(q, False))
        category_score = round((yes_count / len(questions)) * 100)
        scores.append(category_score)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🥧 Score Distribution")
        fig_pie = px.pie(
            values=scores,
            names=categories,
            title="Green Building Score Breakdown",
            color_discrete_sequence=['#32CD32', '#90EE90', '#98FB98', '#00FF7F']
        )
        fig_pie.update_layout(
            font=dict(size=14),
            title_font_size=16,
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:

        st.markdown("### 📊 Category Performance")
        fig_bar = px.bar(
            x=categories,
            y=scores,
            title="Scores by Category",
            labels={'x': 'Categories', 'y': 'Score (%)'},
            color=scores,
            color_continuous_scale='Greens'
        )
        fig_bar.update_layout(
            font=dict(size=12),
            title_font_size=16,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 🎯 Overall Performance")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Overall Green Score<br><span style='font-size:0.8em'>Building Type: {st.session_state.building_type}</span>"},
            delta = {'reference': 70, 'increasing': {'color': "RebeccaPurple"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#32CD32"},
                'steps': [
                    {'range': [0, 40], 'color': "#FFB6C1"},
                    {'range': [40, 60], 'color': "#FFFF99"},
                    {'range': [60, 80], 'color': "#98FB98"},
                    {'range': [80, 100], 'color': "#32CD32"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=400)
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("### 📈 Improvement Potential")

    ideal_scores = [100, 100, 100, 100]

    df_comparison = pd.DataFrame({
        'Category': categories + categories,
        'Score': scores + ideal_scores,
        'Type': ['Current'] * 4 + ['Target'] * 4
    })

    fig_comparison = px.bar(
        df_comparison,
        x='Category',
        y='Score',
        color='Type',
        title="Current vs Target Performance",
        barmode='group',
        color_discrete_map={'Current': '#32CD32', 'Target': '#90EE90'}
    )
    fig_comparison.update_layout(
        font=dict(size=12),
        title_font_size=16,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_comparison, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📥 Download Your Infographic")

    col1, col2, col3 = st.columns(3)

    def create_matplotlib_chart():
        """Create a comprehensive matplotlib chart for download"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Green Guardian Report - {st.session_state.building_type}', fontsize=20, fontweight='bold', color='#2E8B57')

        colors = ['#32CD32', '#90EE90', '#98FB98', '#00FF7F']
        ax1.pie(scores, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Score Distribution', fontsize=14, fontweight='bold')

        bars = ax2.bar(categories, scores, color=colors)
        ax2.set_title('Category Performance', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Score (%)')
        ax2.set_ylim(0, 100)
        ax2.tick_params(axis='x', rotation=45)

        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{score}%', ha='center', va='bottom', fontweight='bold')

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        scores_radar = [score/100 for score in scores]  
        scores_radar += scores_radar[:1]  
        angles += angles[:1]

        ax3.plot(angles, scores_radar, 'o-', linewidth=2, color='#32CD32')
        ax3.fill(angles, scores_radar, alpha=0.25, color='#32CD32')
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels([cat.replace(' ', '\n') for cat in categories])
        ax3.set_ylim(0, 1)
        ax3.set_title('Performance Radar', fontsize=14, fontweight='bold')
        ax3.grid(True)

        ax4.text(0.5, 0.6, f'{current_score}%', ha='center', va='center', 
                fontsize=48, fontweight='bold', color='#32CD32', transform=ax4.transAxes)
        ax4.text(0.5, 0.4, 'Overall Green Score', ha='center', va='center', 
                fontsize=16, fontweight='bold', color='#2E8B57', transform=ax4.transAxes)
        category, emoji = get_score_category(current_score)
        ax4.text(0.5, 0.2, f'{category} {emoji}', ha='center', va='center', 
                fontsize=14, color='#228B22', transform=ax4.transAxes)
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')

        plt.tight_layout()
        return fig

    with col1:
        if st.button("📊 Download Bar Chart", use_container_width=True):

            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(categories, scores, color=['#32CD32', '#90EE90', '#98FB98', '#00FF7F'])
            ax.set_title(f'Green Building Scores - {st.session_state.building_type}', fontsize=16, fontweight='bold', color='#2E8B57')
            ax.set_ylabel('Score (%)', fontsize=12)
            ax.set_ylim(0, 100)
            plt.xticks(rotation=45, ha='right')

            for bar, score in zip(bars, scores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{score}%', ha='center', va='bottom', fontweight='bold')

            plt.tight_layout()

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)

            st.download_button(
                label="💾 Download Bar Chart PNG",
                data=img_buffer.getvalue(),
                file_name=f"green_guardian_bar_chart_{st.session_state.building_type.lower()}.png",
                mime="image/png"
            )
            plt.close()

    with col2:
        if st.button("🥧 Download Pie Chart", use_container_width=True):

            fig, ax = plt.subplots(figsize=(8, 8))
            colors = ['#32CD32', '#90EE90', '#98FB98', '#00FF7F']
            wedges, texts, autotexts = ax.pie(scores, labels=categories, autopct='%1.1f%%', 
                                            colors=colors, startangle=90)
            ax.set_title(f'Green Building Score Distribution - {st.session_state.building_type}', 
                        fontsize=16, fontweight='bold', color='#2E8B57', pad=20)

            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)

            plt.tight_layout()

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)

            st.download_button(
                label="💾 Download Pie Chart PNG",
                data=img_buffer.getvalue(),
                file_name=f"green_guardian_pie_chart_{st.session_state.building_type.lower()}.png",
                mime="image/png"
            )
            plt.close()

    with col3:
        if st.button("📈 Download Full Report", use_container_width=True):

            fig = create_matplotlib_chart()

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)

            st.download_button(
                label="💾 Download Full Report PNG",
                data=img_buffer.getvalue(),
                file_name=f"green_guardian_full_report_{st.session_state.building_type.lower()}.png",
                mime="image/png"
            )
            plt.close()

def material_comparison_page():
    """Material comparison page with educational content"""
    st.markdown('<h1 class="main-header">🔍 Building Material Comparison</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sub-header">
        Compare eco-friendly and conventional building materials across key sustainability metrics
    </div>
    """, unsafe_allow_html=True)

    materials_data = {
        'Material': [
            'Bamboo Flooring', 'Hardwood Flooring', 'Recycled Steel', 'Conventional Steel',
            'Reclaimed Wood', 'New Lumber', 'Cork Flooring', 'Vinyl Flooring',
            'Hemp Insulation', 'Fiberglass Insulation', 'Solar Panels', 'Coal Energy',
            'Low-VOC Paint', 'Standard Paint', 'Recycled Concrete', 'New Concrete',
            'Living Roof', 'Asphalt Shingles', 'Triple-Pane Windows', 'Single-Pane Windows'
        ],
        'Type': [
            'Eco-Friendly', 'Conventional', 'Eco-Friendly', 'Conventional',
            'Eco-Friendly', 'Conventional', 'Eco-Friendly', 'Conventional',
            'Eco-Friendly', 'Conventional', 'Eco-Friendly', 'Conventional',
            'Eco-Friendly', 'Conventional', 'Eco-Friendly', 'Conventional',
            'Eco-Friendly', 'Conventional', 'Eco-Friendly', 'Conventional'
        ],
        'CO2 Emissions (kg/m²)': [
            5, 15, 8, 25, 3, 12, 7, 35, 2, 18, 45, 820, 1, 8, 15, 35, 20, 45, 25, 55
        ],
        'Cost ($/m²)': [
            45, 60, 85, 65, 55, 40, 50, 25, 8, 5, 200, 50, 35, 25, 45, 30, 150, 80, 120, 40
        ],
        'Durability (years)': [
            25, 30, 100, 50, 50, 20, 40, 15, 50, 25, 25, 0, 10, 8, 75, 50, 50, 20, 40, 15
        ],
        'Sustainability Score': [
            9, 6, 8, 4, 9, 5, 8, 3, 9, 4, 10, 1, 8, 4, 7, 5, 9, 4, 8, 3
        ]
    }

    df = pd.DataFrame(materials_data)

    st.markdown("### 🎛️ Filter Materials")
    col1, col2 = st.columns(2)

    with col1:
        material_type_filter = st.selectbox(
            "Filter by Type:",
            ["All", "Eco-Friendly", "Conventional"]
        )

    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Material", "CO2 Emissions (kg/m²)", "Cost ($/m²)", "Durability (years)", "Sustainability Score"]
        )

    if material_type_filter != "All":
        df_filtered = df[df['Type'] == material_type_filter].copy()
    else:
        df_filtered = df.copy()

    ascending = sort_by not in ["Durability (years)", "Sustainability Score"]
    df_filtered = df_filtered.sort_values(by=sort_by, ascending=ascending)

    st.markdown("### 📊 Material Comparison Table")

    def style_dataframe(df):
        def highlight_eco_friendly(row):
            if row['Type'] == 'Eco-Friendly':
                return ['background-color: #E6FFE6'] * len(row)
            else:
                return ['background-color: #FFE6E6'] * len(row)

        return df.style.apply(highlight_eco_friendly, axis=1)

    styled_df = style_dataframe(df_filtered)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 📈 Material Performance Analysis")

    tab1, tab2, tab3 = st.tabs(["🌍 Environmental Impact", "💰 Cost Analysis", "⏰ Durability Comparison"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:

            eco_friendly = df[df['Type'] == 'Eco-Friendly']
            conventional = df[df['Type'] == 'Conventional']

            fig_co2 = go.Figure()
            fig_co2.add_trace(go.Bar(
                name='Eco-Friendly',
                x=eco_friendly['Material'],
                y=eco_friendly['CO2 Emissions (kg/m²)'],
                marker_color='#32CD32'
            ))
            fig_co2.add_trace(go.Bar(
                name='Conventional',
                x=conventional['Material'],
                y=conventional['CO2 Emissions (kg/m²)'],
                marker_color='#FF6B6B'
            ))

            fig_co2.update_layout(
                title='CO2 Emissions by Material Type',
                xaxis_title='Materials',
                yaxis_title='CO2 Emissions (kg/m²)',
                barmode='group',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_co2, use_container_width=True)

        with col2:

            avg_emissions = df.groupby('Type')['CO2 Emissions (kg/m²)'].mean().reset_index()

            fig_avg = px.pie(
                avg_emissions,
                values='CO2 Emissions (kg/m²)',
                names='Type',
                title='Average CO2 Emissions by Type',
                color_discrete_map={'Eco-Friendly': '#32CD32', 'Conventional': '#FF6B6B'}
            )
            st.plotly_chart(fig_avg, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:

            fig_scatter = px.scatter(
                df,
                x='Cost ($/m²)',
                y='Sustainability Score',
                color='Type',
                size='Durability (years)',
                hover_data=['Material'],
                title='Cost vs Sustainability Score',
                color_discrete_map={'Eco-Friendly': '#32CD32', 'Conventional': '#FF6B6B'}
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col2:

            avg_cost = df.groupby('Type')['Cost ($/m²)'].mean().reset_index()

            fig_cost = px.bar(
                avg_cost,
                x='Type',
                y='Cost ($/m²)',
                title='Average Cost by Material Type',
                color='Type',
                color_discrete_map={'Eco-Friendly': '#32CD32', 'Conventional': '#FF6B6B'}
            )
            st.plotly_chart(fig_cost, use_container_width=True)

    with tab3:

        fig_durability = px.box(
            df,
            x='Type',
            y='Durability (years)',
            title='Durability Distribution by Material Type',
            color='Type',
            color_discrete_map={'Eco-Friendly': '#32CD32', 'Conventional': '#FF6B6B'}
        )
        st.plotly_chart(fig_durability, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔍 Key Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        eco_avg_co2 = df[df['Type'] == 'Eco-Friendly']['CO2 Emissions (kg/m²)'].mean()
        conv_avg_co2 = df[df['Type'] == 'Conventional']['CO2 Emissions (kg/m²)'].mean()
        reduction = ((conv_avg_co2 - eco_avg_co2) / conv_avg_co2) * 100

        st.markdown(f"""
        <div class="tip-box">
            <h4>🌍 Environmental Impact</h4>
            <p>Eco-friendly materials reduce CO2 emissions by <strong>{reduction:.1f}%</strong> on average compared to conventional materials.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        eco_avg_durability = df[df['Type'] == 'Eco-Friendly']['Durability (years)'].mean()
        conv_avg_durability = df[df['Type'] == 'Conventional']['Durability (years)'].mean()
        durability_improvement = eco_avg_durability - conv_avg_durability

        st.markdown(f"""
        <div class="tip-box">
            <h4>⏰ Durability Advantage</h4>
            <p>Eco-friendly materials last <strong>{durability_improvement:.1f} years longer</strong> on average than conventional alternatives.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        eco_avg_sustainability = df[df['Type'] == 'Eco-Friendly']['Sustainability Score'].mean()
        conv_avg_sustainability = df[df['Type'] == 'Conventional']['Sustainability Score'].mean()

        st.markdown(f"""
        <div class="tip-box">
            <h4>🏆 Sustainability Score</h4>
            <p>Eco-friendly materials score <strong>{eco_avg_sustainability:.1f}/10</strong> vs <strong>{conv_avg_sustainability:.1f}/10</strong> for conventional materials.</p>
        </div>
        """, unsafe_allow_html=True)

def create_certificate(name, score):
    """Create a certificate image with PIL"""

    img = Image.new('RGB', (1200, 800), color='white')
    draw = ImageDraw.Draw(img)

    green_primary = '#2E8B57'
    green_light = '#90EE90'
    gold = '#FFD700'

    border_width = 10
    draw.rectangle([border_width, border_width, 1200-border_width, 800-border_width], 
                   outline=green_primary, width=border_width)

    draw.rectangle([30, 30, 1170, 770], outline=green_light, width=3)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    title_text = "GREEN GUARDIAN CERTIFICATE"
    subtitle_text = "This certifies that"
    score_text = f"Green Building Score: {score}%"
    pledge_text = "has committed to sustainable building practices"
    pledge_text2 = "and environmental stewardship"

    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]

    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]

    name_bbox = draw.textbbox((0, 0), name, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]

    score_bbox = draw.textbbox((0, 0), score_text, font=text_font)
    score_width = score_bbox[2] - score_bbox[0]

    draw.text((600 - title_width//2, 100), title_text, fill=green_primary, font=title_font)
    draw.text((600 - subtitle_width//2, 200), subtitle_text, fill='black', font=subtitle_font)

    name_y = 280
    draw.text((600 - name_width//2, name_y), name, fill=green_primary, font=name_font)
    draw.line([(200, name_y + 70), (1000, name_y + 70)], fill=green_primary, width=3)

    pledge_bbox1 = draw.textbbox((0, 0), pledge_text, font=text_font)
    pledge_width1 = pledge_bbox1[2] - pledge_bbox1[0]
    draw.text((600 - pledge_width1//2, 380), pledge_text, fill='black', font=text_font)

    pledge_bbox2 = draw.textbbox((0, 0), pledge_text2, font=text_font)
    pledge_width2 = pledge_bbox2[2] - pledge_bbox2[0]
    draw.text((600 - pledge_width2//2, 420), pledge_text2, fill='black', font=text_font)

    draw.text((600 - score_width//2, 500), score_text, fill=green_primary, font=text_font)

    draw.ellipse([100, 200, 200, 300], fill=green_light, outline=green_primary, width=3)
    draw.text((130, 235), "🌱", fill=green_primary, font=title_font)

    draw.ellipse([1000, 200, 1100, 300], fill=green_light, outline=green_primary, width=3)
    draw.text((1030, 235), "🏆", fill=gold, font=title_font)

    from datetime import datetime
    date_text = f"Date: {datetime.now().strftime('%B %d, %Y')}"
    date_bbox = draw.textbbox((0, 0), date_text, font=text_font)
    date_width = date_bbox[2] - date_bbox[0]
    draw.text((600 - date_width//2, 650), date_text, fill='black', font=text_font)

    draw.text((450, 720), "Green Guardian Team", fill=green_primary, font=text_font)
    draw.line([(400, 715), (800, 715)], fill=green_primary, width=2)

    return img

def green_pledge_page():
    """Green pledge page with certificate generation"""
    st.markdown('<h1 class="main-header">🏆 Green Building Pledge</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="pledge-container">
        <h2 style="color: #2E8B57;">🌱 Make Your Commitment to Sustainability</h2>
        <p style="font-size: 1.2rem; color: #1E4D3D;">
            Join thousands of individuals and organizations committed to green building practices. 
            Generate your personalized Green Guardian certificate and showcase your dedication to environmental stewardship.
        </p>
    </div>
    """, unsafe_allow_html=True)

    current_score = calculate_score()
    category, emoji = get_score_category(current_score)

    st.markdown(f"""
    <div class="score-display">
        <h3>Your Current Green Building Score</h3>
        <h1>{emoji} {current_score}% ({category})</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✍️ Create Your Green Pledge")

    col1, col2 = st.columns([2, 1])

    with col1:

        name = st.text_input(
            "Your Name or Organization:",
            placeholder="Enter your full name or organization name",
            help="This will appear on your certificate"
        )

        st.markdown("#### 🌟 Select Your Green Building Commitments:")

        commitments = {
            "energy": st.checkbox("⚡ I commit to improving energy efficiency in my building"),
            "water": st.checkbox("💧 I commit to implementing water conservation measures"),
            "waste": st.checkbox("♻️ I commit to better waste management and recycling"),
            "materials": st.checkbox("🌿 I commit to using sustainable building materials"),
            "education": st.checkbox("📚 I commit to educating others about green building practices"),
            "monitoring": st.checkbox("📊 I commit to regularly monitoring my environmental impact")
        }

        custom_pledge = st.text_area(
            "Additional Personal Pledge (Optional):",
            placeholder="Add your own sustainability commitment...",
            height=100
        )

        if name and any(commitments.values()):
            if st.button("🎖️ Generate My Green Guardian Certificate", type="primary", use_container_width=True):

                certificate_img = create_certificate(name, current_score)

                img_buffer = io.BytesIO()
                certificate_img.save(img_buffer, format='PNG', quality=95)
                img_buffer.seek(0)

                st.markdown("### 🖼️ Your Certificate Preview")
                st.image(certificate_img, caption="Your Green Guardian Certificate", use_container_width=True)

                st.download_button(
                    label="📥 Download Certificate (PNG)",
                    data=img_buffer.getvalue(),
                    file_name=f"green_guardian_certificate_{name.replace(' ', '_').lower()}.png",
                    mime="image/png",
                    type="primary",
                    use_container_width=True
                )

                st.success("🎉 Congratulations! Your Green Guardian Certificate has been generated successfully!")

                if 'certificate_generated' not in st.session_state or not st.session_state.certificate_generated:
                    st.session_state.pledges_made += 1

                    co2_impact = round(current_score * 0.1, 1)  
                    st.session_state.co2_reduced += co2_impact
                    st.session_state.buildings_improved += 1
                    st.session_state.certificate_generated = True

        elif name and not any(commitments.values()):
            st.warning("⚠️ Please select at least one commitment to generate your certificate.")
        elif not name and any(commitments.values()):
            st.warning("⚠️ Please enter your name to generate your certificate.")

    with col2:

        st.markdown("### 🌟 Benefits of Your Pledge")

        benefits = [
            "🏆 Official Green Guardian Certificate",
            "📈 Environmental Impact Tracking",
            "💚 Community Recognition",
            "📚 Access to Exclusive Resources",
            "🤝 Network with Other Green Champions",
            "🌍 Contribute to Global Sustainability"
        ]

        for benefit in benefits:
            st.markdown(f"- {benefit}")

        st.markdown("---")

        st.markdown("### 📊 Community Impact")

        st.metric("Green Pledges Made", st.session_state.pledges_made)
        st.metric("CO2 Reduced (tons)", st.session_state.co2_reduced)
        st.metric("Buildings Improved", st.session_state.buildings_improved)

        st.markdown("---")

        st.markdown("### 📱 Share Your Commitment")

        if name:
            share_text = f"I just made my Green Building Pledge with Green Guardian! Join me in building a sustainable future. #GreenGuardian #Sustainability #GreenBuilding"

            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #F0FFF0; border-radius: 10px; border: 1px solid #2E8B57;">
                <p style="font-style: italic; color: #1E4D3D;">"{share_text}"</p>
                <small style="color: #228B22;">Ready to share on social media!</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📜 The Green Guardian Pledge")

    st.markdown("""
    <div class="pledge-container">
        <h3 style="color: #2E8B57; text-align: center;">Our Commitment to the Planet</h3>
        <p style="font-size: 1.1rem; line-height: 1.8; color: #1E4D3D; text-align: justify;">
            "As a Green Guardian, I pledge to be a steward of our environment through sustainable building practices. 
            I commit to reducing my carbon footprint, conserving natural resources, and promoting eco-friendly 
            construction methods. I will strive to educate others about the importance of green building and 
            work towards creating healthier, more sustainable spaces for current and future generations. 
            Together, we can build a greener tomorrow."
        </p>
        <p style="text-align: center; font-weight: bold; color: #2E8B57; margin-top: 2rem;">
            🌱 Every green choice matters. Every building can make a difference. 🌱
        </p>
    </div>
    """, unsafe_allow_html=True)

    if 'certificate_generated' in st.session_state and st.session_state.certificate_generated:
        st.markdown("### 🌟 Welcome to the Green Guardian Community!")

        st.balloons()

        st.markdown("""
        <div class="tip-box">
            <h4>🎉 Next Steps:</h4>
            <ul>
                <li>📱 Share your certificate on social media</li>
                <li>📊 Track your progress using our evaluation tool</li>
                <li>💡 Implement the personalized tips we've provided</li>
                <li>🤝 Connect with other Green Guardians in your area</li>
                <li>📚 Continue learning about sustainable building practices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def main():

    current_page = st.session_state.current_page

    if current_page == "🏠 Home":
        home_page()
    elif current_page == "📊 Evaluation":
        evaluation_page()
    elif current_page == "💡 Tips":
        tips_page()
    elif current_page == "📈 Infographic":
        infographic_page()
    elif current_page == "🔍 Material Comparison":
        material_comparison_page()
    elif current_page == "🏆 Green Pledge":
        green_pledge_page()

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #228B22; padding: 2rem;">
        <p>🌱 <strong>Green Guardian</strong> - Building a Sustainable Future Together 🌱</p>
        <p><small>© 2025 Green Guardian. Committed to environmental stewardship and sustainable construction.</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()