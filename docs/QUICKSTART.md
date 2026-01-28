# Quick Start Guide

## 5-Minute Setup

### Step 1: Get API Key (2 minutes)
```
1. Go to: https://serpapi.com/
2. Click "Sign Up" (top right)
3. Sign up with email/Google
4. Dashboard → Copy API Key
```

### Step 2: Install & Test (2 minutes)
```bash
# Install required package
pip install requests

# Set your API key
export SERPAPI_KEY='paste_your_key_here'

# Verify setup
python test_setup.py
```

### Step 3: Run Search (1 minute)
```bash
# Run the search
python flight_search_poc.py

# Wait 10-20 seconds for results
```

## Expected Output

You should see:
- ✅ Search parameters
- ✅ Number of flights found
- ✅ Filtered results
- ✅ Top 10 cheapest valid options

## Customization

**Change dates:**
Edit `flight_search_poc.py` line ~340:
```python
departure_date = (datetime.now() + timedelta(days=30))  # Change 30 to any number
```

**Change destination:**
```python
destination = 'TLV'  # or 'HFA' for Haifa
```

**Change time windows:**
Edit `config.ini`:
```ini
min_departure_time = 07:30  # Change to 06:00 for earlier
max_arrival_time = 21:00     # Change to 23:00 for later
```

## Troubleshooting

### Problem: "API key not set"
**Solution:** 
```bash
export SERPAPI_KEY='your_key_here'
# Run in same terminal window where you'll run Python
```

### Problem: "No flights found"
**Solutions:**
1. Try different dates (30, 45, 60 days ahead)
2. Check if flights exist on Google Flights for those dates
3. Try HFA instead of TLV
4. Relax time constraints in config.ini

### Problem: "requests not found"
**Solution:**
```bash
pip install requests
# or
pip3 install requests
```

## What's Next?

After validating Phase 1 works:

**Immediate next steps:**
1. Test with your actual travel dates
2. Compare results with Google Flights
3. Note any missing flights or price differences
4. Decide on Phase 2 features

**Phase 2 ideas:**
- Search multiple date ranges automatically
- Add second data source (Amadeus/Kiwi)
- Save results to file
- Build comparison tool

**Phase 3 ideas:**
- Daily automated monitoring
- Email alerts on price drops
- Price history tracking

## Getting Help

**Check the logs:**
The script shows what it's doing at each step.

**Common issues:**
- Dates too far in future (airlines release schedules ~330 days ahead)
- Dates too close (limited availability)
- No direct flights (WRO→TLV requires connections)

**Need more info?**
- Read README.md for full documentation
- Check flight_search_poc.py comments
- Review config.ini for all options

## Cost Reminder

**Phase 1 (Current):**
- FREE! (100 searches/month on SerpApi free tier)
- Each search run = 1 API call
- That's ~3 searches per day

**If you exceed 100/month:**
- Wait until next month (resets automatically)
- Or upgrade to paid plan (~$50/month for 5,000 searches)

For personal use, free tier is plenty!

## Success Checklist

- [ ] API key set successfully
- [ ] test_setup.py passes all checks
- [ ] flight_search_poc.py runs without errors
- [ ] Results show at least a few valid flights
- [ ] Prices seem reasonable (€300-600 range typical)
- [ ] Compared with Google Flights manually
- [ ] Ready to test with real dates

## Questions?

Review the main README.md for detailed information!
