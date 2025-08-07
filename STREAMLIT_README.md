# 🏠 RentWise Streamlit App

A comprehensive AI-powered rental price prediction and evaluation tool built with Streamlit.

## 🚀 Features

### 💰 Price Prediction
- **AI-Powered Predictions**: Get fair rental price estimates using our trained machine learning model
- **19 Feature Analysis**: Considers square footage, bedrooms, bathrooms, property type, location, amenities, and more
- **Price Insights**: Shows price per square foot, estimated ranges, and detailed breakdowns

### 📊 Price Evaluation 
- **Market Analysis**: Determine if a rental listing is fairly priced, overpriced, or underpriced
- **Real-time Comparison**: Compare asking prices with AI predictions
- **Investment Guidance**: Get recommendations on whether to pursue a rental opportunity

### 🎨 User Experience
- **Intuitive Interface**: Clean, modern design with easy-to-use controls
- **Interactive Sidebar**: Organized property input fields with helpful tooltips
- **Visual Results**: Color-coded price evaluations and clear metric displays
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RentWise
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify model files exist**
   Ensure these model files are present:
   - `models/complete_regression_model.pkl` (for price prediction)
   - `models/complete_classifier_model.pkl` (for price evaluation)

## 🎯 Usage

### Starting the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Interface

#### 1. **Property Details Sidebar**
Fill in the property information:
- **Basic Info**: Square footage, bedrooms, bathrooms
- **Location**: Latitude and longitude coordinates
- **Property Type**: Townhouse, basement, condo unit, main floor
- **Furnishing**: Negotiable or unfurnished options
- **Policies**: Smoking rules and pet allowances
- **Lease Terms**: Duration and flexibility options

#### 2. **Price Prediction Tab**
- Click "🔮 Predict Fair Rental Price"
- Get AI-powered price estimate
- View price insights and metrics
- See estimated price ranges

#### 3. **Price Evaluation Tab**
- Enter the actual asking price from a listing
- Click "📊 Evaluate Price"
- Get evaluation: Fair, Overpriced, or Underpriced
- Compare with AI prediction

## 🔧 Technical Details

### Model Features (19 for Regression, 20 for Classification)
- `sq_feet`: Property square footage
- `beds`: Number of bedrooms
- `baths`: Number of bathrooms
- `latitude`, `longitude`: Geographic coordinates
- Property types: `type_Townhouse`, `type_Basement`, `type_Condo Unit`, `type_Main Floor`
- Furnishing: `furnishing_Negotiable`, `furnishing_Unfurnished`
- Smoking: `smoking_Non-Smoking`, `smoking_Smoke Free Building`
- Pets: `cats_True`, `dogs_True`
- Lease terms: `lease_term_6 months`, `lease_term_Long Term`, `lease_term_Negotiable`, `lease_term_Short Term`
- `price`: Actual listing price (classification only)

### Model Architecture
- **Regression Model**: Linear Regression for price prediction
- **Classification Model**: For price category evaluation
- **Training Data**: 25,000+ rental listings from across Canada
- **Performance**: ~49% R² score, MAE of $396

## 📊 Example Workflows

### Scenario 1: Estimating Fair Rent
1. You're a landlord setting rent for your 2BR/1.5BA condo
2. Input property details in sidebar
3. Use "Price Prediction" tab
4. Get fair market estimate and set competitive rent

### Scenario 2: Evaluating a Rental Listing
1. Found a rental listing online
2. Input all property details from the listing
3. Enter the asking price in "Price Evaluation" tab
4. Determine if it's a good deal or overpriced

### Scenario 3: Market Research
1. Research different property configurations
2. Compare prices across different neighborhoods (lat/lng)
3. Understand how amenities affect rental prices
4. Make informed investment decisions

## 🎨 UI Components

### Color-Coded Results
- **Green**: Fair prices and good deals
- **Yellow**: Underpriced opportunities
- **Red**: Overpriced listings to avoid

### Interactive Elements
- Sidebar form with validation
- Tabbed interface for different use cases
- Responsive buttons and metrics
- Real-time price calculations

## 🔍 Troubleshooting

### Common Issues

**Model Loading Errors**
- Ensure model files exist in `models/` or `notebooks/` directories
- Check file permissions
- Verify Python environment has required packages

**Price Prediction Issues**
- Validate all input values are within reasonable ranges
- Ensure coordinates are for Canadian locations
- Check that at least one property type is selected

**Performance Issues**
- Close other browser tabs
- Restart Streamlit server
- Check system resources

### Debug Mode
Add `--server.enableCORS=false` for local development:
```bash
streamlit run app.py --server.enableCORS=false
```

## 📈 Future Enhancements

- **Map Integration**: Visual property location selection
- **Historical Data**: Price trend analysis over time
- **Comparison Tool**: Side-by-side property comparisons
- **Export Features**: Save predictions and evaluations
- **Mobile App**: Native mobile application
- **API Integration**: Real estate listing APIs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the GitHub issues
3. Create a new issue with detailed information

---

**Built with ❤️ using Streamlit, scikit-learn, and pandas**