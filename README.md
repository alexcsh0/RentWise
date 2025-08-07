# 🏠 RentWise - Rental Price Analysis Tool

A machine learning project for evaluating rental listing prices using regression and classification models.

We built this because finding fairly priced rentals is difficult when you don't know what constitutes a reasonable price for a given property. This tool analyzes rental features to predict fair market prices and classify listings as underpriced, fair, or overpriced.

## Features

- **Price Prediction**: Estimates fair market rent based on property characteristics
- **Price Classification**: Categorizes listings as underpriced (<90% of predicted), fair (90-110%), or overpriced (>110%)
- **Web Interface**: Interactive Streamlit app for easy use
- **Command Line**: Basic Python script for batch processing

## 👨‍💻 Team

| Name | Student # | Email | Responsibilities |
|------|-----------|-------|-----------------|
| Alex Chung | 301549726 | sca372@sfu.ca | ML models, data preprocessing, model evaluation |
| Noah Vattathichirayil | 301548329 | nva16@sfu.ca | Streamlit interface, UI/UX, deployment |

## 🚀 Quick Start

1. **Clone and setup:**
   ```bash
   git clone [repo-url]
   cd RentWise
   pip install -r requirements.txt
   ```

2. **Run the web app:**
   ```bash
   streamlit run app.py
   ```

3. **Or use command line:**
   ```bash
   python main.py
   ```

## 🛠️ Tech Stack

- **Python 3.12** with scikit-learn for ML models
- **Pandas/NumPy** for data manipulation
- **Streamlit** for web interface
- **Matplotlib/Seaborn** for visualizations
- **Joblib** for model serialization

## 📁 Project Structure

```
RentWise/
├── data/
│   ├── raw/                    # Original dataset (25k+ listings)
│   └── processed/              # Cleaned and preprocessed data
├── models/                     # Trained models (.pkl files)
├── notebooks/                  # Jupyter notebooks for development
│   ├── 01_regression_complete.ipynb
│   └── 02_classification_complete.ipynb
├── src/                        # Core modules
│   ├── preprocessing.py        # Data cleaning pipeline
│   ├── model.py               # Model training utilities
│   └── evaluate.py            # Evaluation metrics
├── app.py                     # Streamlit web application
├── main.py                    # Command line interface
└── requirements.txt           # Dependencies
```

## 🤖 Models

### Regression Model (Linear Regression)
- **Purpose**: Predicts fair market rent price
- **Features**: 19 features including sq_feet, beds, baths, location, property type, amenities
- **Performance**: MAE: 396.18, RMSE: 571.19, R²: 0.492
- **Output**: Predicted price in CAD

### Classification Model (Random Forest)
- **Purpose**: Classifies price fairness based on predicted vs actual price
- **Features**: Same 19 features + actual listing price (20 total)
- **Performance**: 94.5% accuracy
- **Classes**: underpriced, fair, overpriced

### Feature Set
Both models use these 19 core features:
```python
['sq_feet', 'beds', 'baths', 'latitude', 'longitude',
 'type_Townhouse', 'type_Basement', 'type_Condo Unit', 'type_Main Floor',
 'furnishing_Negotiable', 'furnishing_Unfurnished',
 'smoking_Non-Smoking', 'smoking_Smoke Free Building',
 'cats_True', 'dogs_True',
 'lease_term_6 months', 'lease_term_Long Term', 
 'lease_term_Negotiable', 'lease_term_Short Term']
```

## 📊 Dataset

- **Source**: RentFaster.ca rental listings
- **Size**: 25,293 listings after preprocessing
- **Coverage**: Primarily Alberta/BC regions
- **Price Range**: $100 - $7,000 CAD/month
- **Features**: 169 original columns reduced to 20 key features

## 🔧 Implementation Details

### Data Preprocessing
- Price filtering ($100-$7000 range)
- One-hot encoding for categorical variables
- Feature selection based on domain knowledge
- Missing value handling

### Model Training
- 80/20 train/test split with stratification
- No feature scaling (tree-based models + linear regression robust to scale)
- Standard scikit-learn pipeline
- Models saved as .pkl files with feature name mappings

### Classification Logic
```python
def classify_price(actual_price, predicted_price):
    ratio = actual_price / predicted_price
    if ratio < 0.9: return "underpriced"
    elif ratio > 1.1: return "overpriced"
    else: return "fair"
```

## 📈 Results

### Regression Performance
- Mean Absolute Error: $396.18
- Root Mean Square Error: $571.19  
- R² Score: 0.492

### Classification Performance
- Overall Accuracy: 94.5%
- Precision/Recall: 95%+ for all classes
- Balanced performance across price categories

### Feature Importance
Top predictors: latitude, longitude, sq_feet, price (for classification), baths, beds

## 🐛 Known Limitations

- Geographic bias toward Alberta/BC
- Limited temporal data (single time snapshot)
- Moderate R² suggests room for feature engineering improvement
- Manual coordinate input required for new predictions

## 🔮 Future Work

- [ ] Expand to more Canadian cities
- [ ] Add temporal price trends
- [ ] Improve location-based features (postal codes, transit access)
- [ ] Deploy as web service
- [ ] Add confidence intervals to predictions

## 📚 Key Learnings

- Feature engineering significantly impacts model performance
- Location features are critical for rental price prediction
- Classification works well when built on regression predictions
- Streamlit provides rapid prototyping for ML demos
- Real estate data requires extensive preprocessing

## 🔗 Usage Examples

See `STREAMLIT_README.md` for detailed web app usage instructions.

---

Final project for CMPT XXX - Machine Learning. Built using scikit-learn, Streamlit, and 25k+ rental listings from RentFaster.ca.
