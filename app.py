import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Page configuration
st.set_page_config(
    page_title="RentWise - AI Rental Price Predictor",
    page_icon="🏠",
    layout="wide"
)

@st.cache_resource
def load_models():
    """Load trained models: Linear Regression (MAE: 396.18, R²: 0.492) + Random Forest Classifier (94.5% accuracy) with fallback model loading"""
    try:
        # Try loading from models/ directory first
        if os.path.exists('models/complete_regression_model.pkl'):
            regression_model = joblib.load('models/complete_regression_model.pkl')
            regression_features = joblib.load('models/regression_feature_names.pkl')
        else:
            # fallback model loading from notebooks/ directory
            regression_model = joblib.load('notebooks/complete_regression_model.pkl')
            regression_features = joblib.load('notebooks/regression_feature_names.pkl')
        
        # load classifier with fallback
        if os.path.exists('models/complete_classifier_model.pkl'):
            classifier_model = joblib.load('models/complete_classifier_model.pkl')
        else:
            # fallback model loading
            classifier_model = joblib.load('notebooks/complete_classifier_model.pkl')
        
        return regression_model, regression_features, classifier_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()

# Load models
regression_model, regression_features, classifier_model = load_models()

st.title("🏠 RentWise - AI Rental Price Predictor")
st.markdown("### Get AI-powered rental price predictions and market analysis")
st.sidebar.header("🏡 Property Details")

# property info
st.sidebar.subheader("📏 Basic Information")
sq_feet = st.sidebar.number_input("Square Footage", min_value=100, max_value=5000, value=800, step=50)
beds = st.sidebar.selectbox("Bedrooms", [1.0, 2.0, 3.0, 4.0, 5.0], index=1)
baths = st.sidebar.selectbox("Bathrooms", [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0], index=2)

# location
st.sidebar.subheader("📍 Location")
col1, col2 = st.sidebar.columns(2)
with col1:
    latitude = st.number_input("Latitude", value=49.2827, format="%.6f")
with col2:
    longitude = st.number_input("Longitude", value=-123.1207, format="%.6f")

# property type
st.sidebar.subheader("🏢 Property Type")
type_townhouse = st.sidebar.checkbox("Townhouse")
type_basement = st.sidebar.checkbox("Basement")
type_condo_unit = st.sidebar.checkbox("Condo Unit")
type_main_floor = st.sidebar.checkbox("Main Floor")

# furnishing
st.sidebar.subheader("🛋️ Furnishing")
furnishing_negotiable = st.sidebar.checkbox("Negotiable Furnishing")
furnishing_unfurnished = st.sidebar.checkbox("Unfurnished")

# smoking policy
st.sidebar.subheader("🚭 Smoking Policy")
smoking_non_smoking = st.sidebar.checkbox("Non-Smoking")
smoking_smoke_free = st.sidebar.checkbox("Smoke Free Building")

# pet policy
st.sidebar.subheader("🐕 Pet Policy")
cats_allowed = st.sidebar.checkbox("Cats Allowed")
dogs_allowed = st.sidebar.checkbox("Dogs Allowed")

# lease terms
st.sidebar.subheader("📝 Lease Terms")
lease_6_months = st.sidebar.checkbox("6 Months")
lease_long_term = st.sidebar.checkbox("Long Term")
lease_negotiable = st.sidebar.checkbox("Negotiable")
lease_short_term = st.sidebar.checkbox("Short Term")

# create 19-feature vector for ML pipeline prediction
def create_feature_vector():
    """Create 19-feature vector from user inputs for real-time predictions"""
    features = {
        'sq_feet': sq_feet,
        'beds': beds,
        'baths': baths,
        'type_Townhouse': type_townhouse,
        'furnishing_Negotiable': furnishing_negotiable,
        'furnishing_Unfurnished': furnishing_unfurnished,
        'type_Basement': type_basement,
        'type_Condo Unit': type_condo_unit,
        'type_Main Floor': type_main_floor,
        'latitude': latitude,
        'longitude': longitude,
        'smoking_Non-Smoking': smoking_non_smoking,
        'smoking_Smoke Free Building': smoking_smoke_free,
        'cats_True': cats_allowed,
        'dogs_True': dogs_allowed,
        'lease_term_6 months': lease_6_months,
        'lease_term_Long Term': lease_long_term,
        'lease_term_Negotiable': lease_negotiable,
        'lease_term_Short Term': lease_short_term
    }
    
    # Create DataFrame with proper feature order
    feature_df = pd.DataFrame([features])
    feature_df = feature_df[regression_features]  # Ensure correct order
    
    return feature_df

# Main content area with tabs
tab1, tab2 = st.tabs(["🔮 Price Prediction", "📊 Price Evaluation"])

with tab1:
    st.header("💰 AI Price Prediction")
    st.markdown("Get an AI-powered estimate of fair rental price based on property features.")
    
    if st.button("🔮 Predict Fair Rental Price", type="primary", use_container_width=True):
        features = create_feature_vector()
        
        predicted_price = regression_model.predict(features)[0]
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🎯 Predicted Fair Price",
                value=f"${predicted_price:,.0f}",
                delta=None
            )
        
        with col2:
            price_per_sqft = predicted_price / sq_feet
            st.metric(
                label="📐 Price per Sq Ft",
                value=f"${price_per_sqft:.2f}",
                delta=None
            )
        
        with col3:
            # income reqs
            monthly_income_needed = predicted_price * 3  
            st.metric(
                label="💼 Income Needed (30% housing rule)",
                value=f"${monthly_income_needed:,.0f}",
                delta=None
            )
        
        st.subheader("📈 Actionable Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("✅ **±10% Fair Market Range**")
            lower_bound = predicted_price * 0.9
            upper_bound = predicted_price * 1.1
            st.write(f"**${lower_bound:,.0f} - ${upper_bound:,.0f}**")
            st.write("±10% fair market range estimates enabling data-driven rental decisions.")
        
        with col2:
            st.info("💡 **Market-Driven Insights**")
            st.write(f"Properties priced around **${predicted_price:,.0f}** represent fair market value.")
            st.write("Look for listings within ±10% of this estimate for optimal value.")

with tab2:
    st.header("📊 Price Evaluation")
    st.markdown("Enter an actual rental price to evaluate if it's fairly priced, overpriced, or underpriced.")
    
    # price input
    actual_price = st.number_input(
        "💵 Asking Price (from rental listing)",
        min_value=100,
        max_value=10000,
        value=1500,
        step=50,
        help="Enter the rental price from the listing you want to evaluate"
    )
    
    if st.button("📊 Evaluate Price", type="primary", use_container_width=True):
        # dual-model system: regression for price prediction + Random Forest classifier
        # create feature vector for regression
        features = create_feature_vector()
        
        # get AI prediction from regression model
        predicted_price = regression_model.predict(features)[0]
        
        # create feature vector for Random Forest classifier (includes actual price)
        classification_features = features.copy()
        classification_features['price'] = actual_price
        
        # ensure we have all 20 features for classification
        expected_features = [
            'sq_feet', 'beds', 'baths', 'type_Townhouse', 'furnishing_Negotiable', 
            'furnishing_Unfurnished', 'type_Basement', 'type_Condo Unit', 'type_Main Floor', 
            'latitude', 'longitude', 'price', 'smoking_Non-Smoking', 'smoking_Smoke Free Building', 
            'cats_True', 'dogs_True', 'lease_term_6 months', 'lease_term_Long Term', 
            'lease_term_Negotiable', 'lease_term_Short Term'
        ]
        
        classification_features = classification_features[expected_features]
        
        classification = classifier_model.predict(classification_features)[0]
        
        # calculate metrics
        price_difference = actual_price - predicted_price
        price_ratio = actual_price / predicted_price
        percentage_diff = ((actual_price - predicted_price) / predicted_price) * 100
        
        # display main evaluation
        if classification == 'fair':
            st.success(f"✅ **FAIR PRICE** - This listing is reasonably priced!")
            color = "green"
        elif classification == 'underpriced':
            st.info(f"🟠 **UNDERPRICED** - This could be a great deal!")
            color = "blue"
        else:  # overpriced
            st.error(f"🔴 **OVERPRICED** - Consider looking for alternatives")
            color = "red"
        
        # detailed comparison
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🏷️ Asking Price",
                value=f"${actual_price:,.0f}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="🤖 AI Predicted Price",
                value=f"${predicted_price:,.0f}",
                delta=None
            )
        
        with col3:
            delta_color = "normal" if abs(percentage_diff) <= 10 else "inverse"
            st.metric(
                label="💰 Price Difference",
                value=f"${abs(price_difference):,.0f}",
                delta=f"{percentage_diff:+.1f}%"
            )
        
        with col4:
            st.metric(
                label="📊 Price Ratio",
                value=f"{price_ratio:.2f}x",
                delta=f"AI Prediction"
            )
        
        # detailed analysis
        st.subheader("🔍 Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if classification == 'fair':
                st.success("**✅ Market Analysis**")
                st.write("• Price is within normal market range")
                st.write("• Good alignment with similar properties")
                st.write("• Reasonable value for the features offered")
            elif classification == 'underpriced':
                st.warning("**🟡 Opportunity Analysis**")
                st.write("• Price is below market average")
                st.write("• Potential great value opportunity")
                st.write("• May indicate motivated landlord or unique circumstances")
            else:
                st.error("**🔴 Risk Analysis**")
                st.write("• Price is above market average")
                st.write("• May want to negotiate or look elsewhere")
                st.write("• Consider if premium features justify the cost")
        
        with col2:
            st.info("**💡 Market-Driven Recommendation**")
            if classification == 'fair':
                st.write("This rental appears to be **fairly priced** for the market. Data-driven analysis suggests it's a reasonable choice if it meets your needs.")
            elif classification == 'underpriced':
                st.write("This could be an **excellent deal**! Market-driven insights suggest acting quickly if the property meets your requirements.")
            else:
                st.write("You might want to **negotiate the price** or continue searching for better value options based on data-driven analysis.")
            
            # ±10% fair market range estimates enabling data-driven rental decisions
            st.write("---")
            st.write("**🎯 ±10% Fair Market Range:**")
            st.write(f"${predicted_price * 0.9:,.0f} - ${predicted_price * 1.1:,.0f}") # enabling data-driven rental decisions

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🏠 <strong>RentWise</strong> - AI Rental Price Predictor<br>
        Tech Stack: Python, scikit-learn, Streamlit, Pandas, NumPy, Matplotlib (for model evaluation visualizations), Joblib<br>
        End-to-end ML pipeline processing 25K+ rental listings</p>
    </div>
    """,
    unsafe_allow_html=True
)