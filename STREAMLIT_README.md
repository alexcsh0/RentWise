# 🎨 RentWise Streamlit Interface

Interactive web app for the RentWise rental price analysis system. Provides a user-friendly interface to our machine learning models for price prediction and evaluation.

## Application Overview

The Streamlit app provides two main functionalities:
1. **Price Prediction**: Input property features → get predicted fair market price
2. **Price Evaluation**: Input property features + asking price → get fairness classification

## 🚀 Quick Start

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🏗️ Architecture

### Model Loading
```python
@st.cache_resource
def load_models():
    # Attempts to load from models/ directory first
    # Falls back to notebooks/ directory if needed
    return regression_model, classifier_model
```

### Data Flow
1. **User Input** → Sidebar form with property details
2. **Feature Engineering** → Convert inputs to model-compatible DataFrame
3. **Model Prediction** → Apply loaded models to feature vector
4. **Results Display** → Format and present predictions with visualizations

## 📊 Interface Components

### Sidebar Controls
- **Basic Properties**: Square footage, bedrooms, bathrooms
- **Location**: Latitude/longitude coordinates (manual entry required)
- **Property Type**: Checkboxes for townhouse, basement, condo, main floor
- **Amenities**: Furnishing options, smoking policies, pet policies
- **Lease Terms**: Duration and flexibility options

### Main Display Tabs

#### Price Prediction Tab
- Predicted fair market price
- Price per square foot calculation
- Required income estimate (30% rule)
- Confidence metrics and feature importance

#### Price Evaluation Tab
- Price classification (underpriced/fair/overpriced)
- Comparison with predicted price
- Percentage difference analysis
- Recommendation system

## 🔧 Technical Implementation

### Feature Vector Construction
The app creates a 19-feature vector matching the trained model requirements:
```python
feature_order = ['sq_feet', 'beds', 'baths', 'latitude', 'longitude',
                'type_Townhouse', 'type_Basement', 'type_Condo Unit', 
                'type_Main Floor', 'furnishing_Negotiable', 
                'furnishing_Unfurnished', 'smoking_Non-Smoking', 
                'smoking_Smoke Free Building', 'cats_True', 'dogs_True',
                'lease_term_6 months', 'lease_term_Long Term', 
                'lease_term_Negotiable', 'lease_term_Short Term']
```

### Model Integration
- **Regression Model**: Linear regression for price prediction
- **Classification Model**: Random Forest with 20 features (includes actual price)
- **Error Handling**: Graceful fallbacks for missing models or prediction errors
- **Caching**: Models loaded once and cached for session duration

### UI/UX Design
- **Wide Layout**: Maximizes screen real estate for data display
- **Responsive Metrics**: Real-time updates as inputs change
- **Color Coding**: Visual indicators for price classifications
- **Input Validation**: Basic checks for reasonable property values

## ⚠️ Known Issues

### Input Limitations
- **Geographic Coordinates**: Manual lat/long entry required (no address lookup)
- **Model Coverage**: Best accuracy for Alberta/BC properties
- **Input Validation**: Limited bounds checking on property features

### Technical Constraints
- **Model Path Dependencies**: Requires models in specific directory structure
- **Feature Order Sensitivity**: Classification model requires exact 20-feature sequence
- **Mobile Compatibility**: Interface not optimized for mobile devices
- **Session State**: No persistence of user inputs between sessions

### Performance Considerations
- **Model Loading**: ~2-3 second initial load time
- **Prediction Speed**: Near-instantaneous for single predictions
- **Memory Usage**: ~100MB for loaded models
- **Browser Compatibility**: Tested on Chrome/Firefox/Safari

## 🛠️ Development Details

### Streamlit Components Used
- `st.set_page_config()`: Wide layout configuration
- `st.sidebar`: Input form organization
- `st.tabs()`: Main content organization
- `st.metric()`: Key performance indicators
- `st.columns()`: Side-by-side layouts
- `st.cache_resource`: Model loading optimization

### Error Handling
```python
try:
    prediction = regression_model.predict(features)
    st.success(f"Predicted Price: ${prediction[0]:,.2f}")
except Exception as e:
    st.error("Prediction failed - check input values")
```

### Data Validation
- Square footage: 100-10,000 sq ft range
- Bedrooms: 0-10 range
- Bathrooms: 0-10 range
- Price evaluation: $100-$10,000 range

## 📈 Usage Analytics

The app tracks basic usage patterns:
- Input distributions by property type
- Prediction accuracy vs user feedback
- Common feature combinations
- Geographic query patterns

## 🔄 Deployment Considerations

### Local Development
```bash
pip install streamlit pandas scikit-learn joblib
streamlit run app.py
```

### Production Deployment
- **Resource Requirements**: 1GB RAM minimum for model loading
- **Port Configuration**: Default 8501 or custom via `--server.port`
- **Environment Variables**: Optional model path overrides
- **Logging**: Basic Streamlit metrics available

### Docker Container
```dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Model loading on app startup
- [ ] Price prediction with valid inputs
- [ ] Price evaluation with sample listings
- [ ] Error handling with invalid inputs
- [ ] UI responsiveness across screen sizes

### Automated Testing
Currently limited to model loading and basic prediction functionality.

## 💡 Usage Best Practices

- **Location Input**: Use Vancouver/Calgary coordinates for best accuracy
- **Property Type**: Select all applicable categories for better predictions
- **Price Evaluation**: Test with real listings to validate model performance
- **Input Ranges**: Stay within reasonable property value ranges for reliable results

---

**Technical Stack**: Streamlit 1.28+, scikit-learn 1.3+, Pandas 2.0+, Python 3.12+  
**Model Dependencies**: complete_regression_model.pkl, complete_classifier_model.pkl  
**Data Requirements**: 19-feature vector matching training data schema