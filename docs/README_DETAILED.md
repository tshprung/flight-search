# Flight Search POC - Phase 1

Automated flight search for WRO (Wrocław) → TLV/HFA (Israel) with custom constraints.

## Features

✅ **Custom Time Constraints**
- Departure: 07:30 - 18:00 local time
- Arrival: 08:00 - 21:00 local time
- Max trip duration: 12 hours

✅ **Smart Connection Times**
- Within Schengen: 1 hour minimum
- Exiting Schengen: 2 hours minimum
- Self-transfer: 2.5 hours minimum (flagged)

✅ **Multi-Passenger Pricing**
- Adult + Child (4 years) pricing
- Euro currency

✅ **Free Tier Usage**
- Uses SerpApi (Google Flights data)
- 100 free searches per month

## Quick Start

### 1. Get API Key (Free)

```bash
# Go to https://serpapi.com/
# Sign up for free account
# Copy your API key from dashboard
# Free tier: 100 searches/month
```

### 2. Install Dependencies

```bash
pip install requests
```

### 3. Set API Key

```bash
export SERPAPI_KEY='your_api_key_here'
```

### 4. Run Search

```bash
python flight_search_poc.py
```

## Example Output

```
================================================================================
FLIGHT SEARCH POC - Phase 1
WRO (Wrocław) → TLV (Tel Aviv) / HFA (Haifa)
================================================================================

📅 Searching flights:
   Route: WRO → TLV
   Outbound: 2026-02-28
   Return: 2026-03-05
   Passengers: 1 Adult + 1 Child (4 years old)

⏳ Searching... (this may take 10-20 seconds)

✅ Results received, parsing...
📊 Found 47 total flight options

🔍 Applying constraints:
   ✓ Departure: 07:30 - 18:00
   ✓ Arrival: 08:00 - 21:00
   ✓ Max duration: 12 hours
   ✓ Connection times: 1h (Schengen) / 2h (exit Schengen)

✅ 12 flights meet all constraints

================================================================================
VALID FLIGHT OPTIONS (sorted by price)
================================================================================

================================================================================
Option #1
================================================================================
Price: €340 (Adult + Child)
Departure: 08:30 AM from WRO
Arrival: 06:15 PM at TLV
Total Duration: 585 minutes (9h 45m)
Airlines: LOT Polish Airlines

Connections (1):
  1. Warsaw Chopin Airport (WAW) - 125 minutes

================================================================================
Option #2
================================================================================
Price: €385 (Adult + Child)
Departure: 11:45 AM from WRO
Arrival: 08:20 PM at TLV
Total Duration: 635 minutes (10h 35m)
Airlines: Wizz Air, Wizz Air

Connections (1):
  1. Budapest Airport (BUD) - 145 minutes
```

## Customization

### Change Search Parameters

Edit `flight_search_poc.py`:

```python
# Line ~340
origin = 'WRO'
destination = 'TLV'  # or 'HFA' for Haifa

# Change dates
departure_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
return_date = (datetime.now() + timedelta(days=35)).strftime('%Y-%m-%d')
```

### Adjust Constraints

Edit `FlightConstraints` class (lines 15-42):

```python
# Time windows
MIN_DEPARTURE_TIME = "07:30"  # Change to "06:00" for earlier flights
MAX_DEPARTURE_TIME = "18:00"  # Change to "20:00" for evening flights

# Duration
MAX_TRIP_DURATION_HOURS = 12  # Change to 15 for more options

# Connection times
MIN_CONNECTION_WITHIN_SCHENGEN = 60  # minutes
MIN_CONNECTION_EXIT_SCHENGEN = 120   # minutes
```

## Testing Different Scenarios

### 1. Flexible Dates Search

```python
# Search multiple date combinations
for days_ahead in [30, 45, 60, 90]:
    departure = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    # Run search...
```

### 2. Different Trip Durations

```python
# Test 5-day, 7-day, 10-day trips
for trip_length in [5, 7, 10]:
    departure = "2026-03-01"
    return_date = (datetime.strptime(departure, "%Y-%m-%d") + timedelta(days=trip_length)).strftime('%Y-%m-%d')
    # Run search...
```

### 3. One-Way vs Round-Trip

```python
# One-way
results = search_flights_serpapi(
    origin='WRO',
    destination='TLV',
    departure_date='2026-03-01',
    return_date=None,  # One-way
    adults=1,
    children=1
)

# Round-trip
results = search_flights_serpapi(
    origin='WRO',
    destination='TLV',
    departure_date='2026-03-01',
    return_date='2026-03-08',  # Round-trip
    adults=1,
    children=1
)
```

## Validation

### Compare with Google Flights

1. Run the POC script
2. Note the top 3 cheapest results
3. Go to Google Flights manually: https://www.google.com/travel/flights
4. Search same route/dates
5. Compare:
   - Are prices within €10?
   - Same airlines shown?
   - Any flights missing?

### Known Limitations (Phase 1)

- ⚠️ Return flight constraints not yet implemented
- ⚠️ No automatic date range search
- ⚠️ No price monitoring yet
- ⚠️ No comparison across multiple dates
- ⚠️ Single data source (SerpApi only)

These will be addressed in Phase 2+

## Troubleshooting

### "❌ ERROR: Please set SERPAPI_KEY"

```bash
# Make sure you exported the key in current terminal session
export SERPAPI_KEY='your_key_here'

# Or set it permanently in ~/.bashrc or ~/.zshrc
echo 'export SERPAPI_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### "No flights found matching all constraints"

Try:
1. Different dates (maybe current date has no availability)
2. Relaxing time windows
3. Different destination (TLV vs HFA)
4. Checking if WRO→TLV flights exist for those dates on Google Flights

### API Rate Limit

- Free tier: 100 searches/month
- Each run = 1 search
- If exceeded, wait until next month or upgrade

## Cost Tracking

**Current Phase 1:**
- SerpApi: $0/month (free tier, 100 searches)
- **Total: $0/month**

**Estimated Phase 2:**
- Add Amadeus API: ~$1-2/month
- **Total: $1-2/month**

**Estimated Phase 3 (monitoring):**
- GitHub Actions: $0/month (free tier sufficient)
- SendGrid emails: $0/month (free tier)
- **Total: $1-2/month**

## Next Steps

After validating Phase 1 works:

**Phase 2: Enhanced Search**
- [ ] Add date range search (find cheapest across multiple dates)
- [ ] Add return flight constraints
- [ ] Add Amadeus API as second source
- [ ] Compare results across sources
- [ ] Save results to file

**Phase 3: Monitoring**
- [ ] Set up GitHub Actions for daily runs
- [ ] Implement price tracking/baseline
- [ ] Email alerts on price drops
- [ ] Web dashboard (optional)

**Phase 4: Optimization**
- [ ] Add known route optimization
- [ ] Airline-specific scraping for comparison
- [ ] Historical price analysis
- [ ] Best booking time predictions

## File Structure

```
.
├── flight_search_poc.py    # Main POC script
├── README.md               # This file
└── results/                # (Future) Saved search results
```

## Questions?

Review the code comments in `flight_search_poc.py` for detailed explanations of:
- Constraint checking logic
- Connection time calculations
- Schengen exit detection
- Result parsing

## License

Private project for personal use.
