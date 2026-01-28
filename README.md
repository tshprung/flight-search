# ✈️ Flight Search System - WRO → Israel

Automated flight search for Wrocław (WRO) to Tel Aviv/Haifa with intelligent constraint filtering and price monitoring.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Phase%201%20POC-yellow)

## 🎯 Features

### ✅ Smart Constraint Filtering
- **Time Windows**: Departure 07:30-18:00, Arrival 08:00-21:00
- **Duration Limits**: Maximum 12 hours total travel time
- **Connection Intelligence**: 
  - 1 hour minimum within Schengen
  - 2 hours minimum when exiting Schengen (passport control)
  - 2.5 hours minimum for self-transfers (with clear flagging)

### 💰 Cost Optimization
- Multi-passenger pricing (Adult + Child)
- Sorts by total price (cheapest first)
- EUR currency display

### 🔄 Automated Filtering
- Eliminates invalid connections automatically
- Schengen-aware routing logic
- Clear warnings for tight connections

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Free SerpApi account (100 searches/month free)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/flight-search.git
cd flight-search

# Install dependencies
pip install -r requirements.txt

# Set up API key
export SERPAPI_KEY='your_api_key_here'

# Verify setup
python test_setup.py

# Run search
python flight_search_poc.py
```

### Get Your Free API Key

1. Go to [SerpApi](https://serpapi.com/)
2. Sign up for free account
3. Copy API key from dashboard
4. 100 searches/month on free tier

## 📖 Usage

### Basic Search

```bash
python flight_search_poc.py
```

This searches WRO → TLV for dates 30 days ahead with a 5-day trip duration.

### Customize Search

Edit `flight_search_poc.py` (lines ~340-345):

```python
# Change destination
destination = 'HFA'  # Haifa instead of Tel Aviv

# Change dates
departure_date = '2026-03-15'
return_date = '2026-03-22'

# Change passengers
adults = 2
children = 0
```

### Adjust Constraints

Edit `config.ini`:

```ini
[Time Constraints]
min_departure_time = 06:00  # Earlier flights
max_arrival_time = 23:00     # Later arrivals
max_trip_duration = 15       # Longer trips allowed
```

## 📊 Example Output

```
================================================================================
FLIGHT SEARCH POC - Phase 1
WRO (Wrocław) → TLV (Tel Aviv)
================================================================================

📊 Found 47 total flight options
✅ 12 flights meet all constraints

================================================================================
Option #1
================================================================================
Price: €340 (Adult + Child)
Departure: 08:30 AM from WRO
Arrival: 06:15 PM at TLV
Total Duration: 9h 45m
Airlines: LOT Polish Airlines

Connections (1):
  1. Warsaw Chopin Airport (WAW) - 125 minutes
```

## 🗂️ Project Structure

```
flight-search/
├── flight_search_poc.py    # Main search script
├── test_setup.py            # Setup verification
├── config.ini               # Configuration file
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── QUICKSTART.md            # 5-minute setup guide
├── PHASE1_SUMMARY.md        # Detailed phase 1 documentation
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore rules
```

## 🛠️ Configuration

### Environment Variables

```bash
# Required
export SERPAPI_KEY='your_api_key'

# Optional (future use)
export AMADEUS_API_KEY='your_key'
export KIWI_API_KEY='your_key'
```

### Config File

See `config.ini` for all customizable parameters:
- Search parameters
- Time constraints
- Connection requirements
- Display options

## 📈 Roadmap

### Phase 1 (✅ Complete)
- [x] Core search functionality
- [x] Constraint filtering
- [x] SerpApi integration
- [x] Basic output formatting

### Phase 2 (In Progress)
- [ ] Date range search (find cheapest across multiple dates)
- [ ] Return flight constraints
- [ ] Multiple data sources (Amadeus, Kiwi)
- [ ] Result persistence to files
- [ ] Price comparison across sources

### Phase 3 (Planned)
- [ ] Automated daily monitoring via GitHub Actions
- [ ] Price drop email alerts
- [ ] Historical price tracking
- [ ] Best booking time predictions
- [ ] Web dashboard (optional)

## 🧪 Testing

Run the test suite:

```bash
# Verify setup
python test_setup.py

# Test with specific dates
python flight_search_poc.py

# Compare results with Google Flights manually
```

## 💡 How It Works

1. **Search**: Queries Google Flights via SerpApi
2. **Parse**: Extracts flight details, prices, connections
3. **Filter**: Applies your custom constraints
4. **Sort**: Orders by price (cheapest first)
5. **Display**: Shows only valid options

### Constraint Logic

**Time Check:**
```python
if departure_time < 07:30 or departure_time > 18:00:
    reject_flight()
```

**Connection Check:**
```python
if exiting_schengen:
    min_connection = 120  # 2 hours
else:
    min_connection = 60   # 1 hour

if connection_time < min_connection:
    reject_flight()
```

## 🤝 Contributing

This is a personal project, but suggestions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SerpApi](https://serpapi.com/) for Google Flights data access
- Built for personal use to find the best flight deals from Wrocław to Israel

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## ⚠️ Disclaimer

This tool is for personal use only. Always verify prices and availability on the airline's official website before booking. Flight prices and schedules are subject to change.

---

**Current Status**: Phase 1 POC Complete ✅  
**Last Updated**: January 2026  
**Version**: 1.0
