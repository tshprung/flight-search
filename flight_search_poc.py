#!/usr/bin/env python3
"""
Flight Search POC - Phase 1
Searches WRO->TLV/HFA flights with custom constraints
Uses SerpApi (Google Flights) - FREE tier: 100 searches/month
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

# SerpApi configuration
SERPAPI_KEY = os.environ.get('SERPAPI_KEY', 'YOUR_API_KEY_HERE')
SERPAPI_ENDPOINT = "https://serpapi.com/search.json"

class FlightConstraints:
    """User's custom flight constraints"""
    
    # Time constraints (local time)
    MIN_DEPARTURE_TIME = "07:30"
    MAX_DEPARTURE_TIME = "18:00"
    MIN_ARRIVAL_TIME = "08:00"
    MAX_ARRIVAL_TIME = "21:00"
    
    # Duration constraint
    MAX_TRIP_DURATION_HOURS = 12
    
    # Connection time constraints (in minutes)
    MIN_CONNECTION_WITHIN_SCHENGEN = 60
    MIN_CONNECTION_EXIT_SCHENGEN = 120
    MIN_CONNECTION_SELF_TRANSFER = 150
    
    # Schengen exit airports (common connection points from WRO)
    SCHENGEN_AIRPORTS = {
        'WAW', 'FRA', 'MUC', 'VIE', 'AMS', 'CDG', 'ZRH', 
        'CPH', 'ARN', 'BRU', 'ATH', 'FCO', 'MAD', 'BCN'
    }
    
    # Non-Schengen destinations
    NON_SCHENGEN_DESTINATIONS = {'TLV', 'HFA'}


def parse_time(time_str: str) -> datetime:
    """Parse time string to datetime object for comparison"""
    try:
        return datetime.strptime(time_str, "%H:%M")
    except:
        try:
            return datetime.strptime(time_str, "%I:%M %p")
        except:
            return None


def calculate_duration_minutes(departure: str, arrival: str) -> Optional[int]:
    """Calculate flight duration in minutes from time strings"""
    try:
        # This is simplified - in production we'd handle timezone conversions
        dep = datetime.strptime(departure, "%I:%M %p")
        arr = datetime.strptime(arrival, "%I:%M %p")
        
        duration = (arr - dep).total_seconds() / 60
        
        # Handle overnight flights
        if duration < 0:
            duration += 24 * 60
            
        return int(duration)
    except:
        return None


def check_time_constraints(flight_data: Dict) -> Dict:
    """
    Check if flight meets time constraints
    Returns dict with pass/fail and reasons
    """
    result = {
        'passes': True,
        'reasons': []
    }
    
    constraints = FlightConstraints()
    
    # Check departure time
    dep_time_str = flight_data.get('departure_time', '')
    if dep_time_str:
        dep_time = parse_time(dep_time_str)
        min_dep = parse_time(constraints.MIN_DEPARTURE_TIME)
        max_dep = parse_time(constraints.MAX_DEPARTURE_TIME)
        
        if dep_time and min_dep and max_dep:
            if not (min_dep.time() <= dep_time.time() <= max_dep.time()):
                result['passes'] = False
                result['reasons'].append(f"Departure {dep_time_str} outside 07:30-18:00 window")
    
    # Check arrival time
    arr_time_str = flight_data.get('arrival_time', '')
    if arr_time_str:
        arr_time = parse_time(arr_time_str)
        min_arr = parse_time(constraints.MIN_ARRIVAL_TIME)
        max_arr = parse_time(constraints.MAX_ARRIVAL_TIME)
        
        if arr_time and min_arr and max_arr:
            if not (min_arr.time() <= arr_time.time() <= max_arr.time()):
                result['passes'] = False
                result['reasons'].append(f"Arrival {arr_time_str} outside 08:00-21:00 window")
    
    # Check total duration
    total_duration = flight_data.get('total_duration', 0)
    if total_duration > constraints.MAX_TRIP_DURATION_HOURS * 60:
        result['passes'] = False
        result['reasons'].append(f"Duration {total_duration}min exceeds 12 hour limit")
    
    return result


def check_connection_times(flight_data: Dict) -> Dict:
    """
    Check if connection times are sufficient
    Considers Schengen exit rules
    """
    result = {
        'passes': True,
        'reasons': [],
        'warnings': []
    }
    
    constraints = FlightConstraints()
    layovers = flight_data.get('layovers', [])
    
    if not layovers:
        return result  # Direct flight, no connections to check
    
    for i, layover in enumerate(layovers):
        airport_code = layover.get('id', '').upper()
        duration_min = layover.get('duration', 0)
        
        # Determine if this is a Schengen exit
        is_schengen_exit = (
            airport_code in constraints.SCHENGEN_AIRPORTS and
            flight_data.get('destination_airport', '') in constraints.NON_SCHENGEN_DESTINATIONS
        )
        
        # Determine minimum required time
        if is_schengen_exit:
            min_required = constraints.MIN_CONNECTION_EXIT_SCHENGEN
            connection_type = "Schengen exit"
        else:
            min_required = constraints.MIN_CONNECTION_WITHIN_SCHENGEN
            connection_type = "within Schengen"
        
        # Check if sufficient
        if duration_min < min_required:
            result['passes'] = False
            result['reasons'].append(
                f"Connection {i+1} at {airport_code}: {duration_min}min < {min_required}min required for {connection_type}"
            )
        elif duration_min < min_required + 30:
            result['warnings'].append(
                f"Connection {i+1} at {airport_code}: {duration_min}min is tight for {connection_type}"
            )
    
    return result


def search_flights_serpapi(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    adults: int = 1,
    children: int = 0
) -> Dict:
    """
    Search flights using SerpApi (Google Flights)
    
    Args:
        origin: Airport code (e.g., 'WRO')
        destination: Airport code (e.g., 'TLV')
        departure_date: Format 'YYYY-MM-DD'
        return_date: Format 'YYYY-MM-DD' or None for one-way
        adults: Number of adult passengers
        children: Number of child passengers
    
    Returns:
        Dict with flight results
    """
    
    params = {
        'api_key': SERPAPI_KEY,
        'engine': 'google_flights',
        'departure_id': origin,
        'arrival_id': destination,
        'outbound_date': departure_date,
        'adults': adults,
        'children': children,
        'currency': 'EUR',
        'hl': 'en',
    }
    
    if return_date:
        params['return_date'] = return_date
        params['type'] = '1'  # Round trip
    else:
        params['type'] = '2'  # One way
    
    try:
        response = requests.get(SERPAPI_ENDPOINT, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}


def parse_serpapi_results(raw_results: Dict) -> List[Dict]:
    """
    Parse SerpApi results into our standardized format
    """
    flights = []
    
    if 'error' in raw_results:
        return flights
    
    # SerpApi returns results in 'best_flights' and 'other_flights'
    all_flights = []
    if 'best_flights' in raw_results:
        all_flights.extend(raw_results['best_flights'])
    if 'other_flights' in raw_results:
        all_flights.extend(raw_results['other_flights'])
    
    for flight in all_flights:
        parsed = {
            'price': flight.get('price', 0),
            'currency': 'EUR',
            'departure_time': '',
            'arrival_time': '',
            'total_duration': 0,
            'layovers': [],
            'airlines': [],
            'flight_numbers': [],
            'booking_link': flight.get('booking_token', ''),
            'origin_airport': '',
            'destination_airport': ''
        }
        
        # Extract flight details from legs
        if 'flights' in flight:
            legs = flight['flights']
            
            # First leg departure
            if legs:
                first_leg = legs[0]
                parsed['departure_time'] = first_leg.get('departure_airport', {}).get('time', '')
                parsed['origin_airport'] = first_leg.get('departure_airport', {}).get('id', '')
                
                # Airline info
                if 'airline' in first_leg:
                    parsed['airlines'].append(first_leg['airline'])
                if 'flight_number' in first_leg:
                    parsed['flight_numbers'].append(first_leg['flight_number'])
            
            # Last leg arrival
            if len(legs) > 0:
                last_leg = legs[-1]
                parsed['arrival_time'] = last_leg.get('arrival_airport', {}).get('time', '')
                parsed['destination_airport'] = last_leg.get('arrival_airport', {}).get('id', '')
            
            # Extract layovers
            for leg in legs[:-1]:  # All legs except last have a layover after them
                if 'layover' in leg:
                    layover_info = {
                        'airport': leg['layover'].get('name', ''),
                        'id': leg['layover'].get('id', ''),
                        'duration': leg['layover'].get('duration', 0)
                    }
                    parsed['layovers'].append(layover_info)
        
        # Total duration
        if 'total_duration' in flight:
            parsed['total_duration'] = flight['total_duration']
        
        flights.append(parsed)
    
    return flights


def filter_flights(flights: List[Dict]) -> List[Dict]:
    """
    Filter flights based on all constraints
    Returns list of valid flights with constraint check results
    """
    valid_flights = []
    
    for flight in flights:
        # Check time constraints
        time_check = check_time_constraints(flight)
        
        # Check connection times
        connection_check = check_connection_times(flight)
        
        # Flight passes if both checks pass
        if time_check['passes'] and connection_check['passes']:
            flight['constraint_checks'] = {
                'time': time_check,
                'connections': connection_check
            }
            valid_flights.append(flight)
    
    return valid_flights


def format_flight_result(flight: Dict, index: int) -> str:
    """Format a single flight result for display"""
    output = []
    output.append(f"\n{'='*80}")
    output.append(f"Option #{index + 1}")
    output.append(f"{'='*80}")
    output.append(f"Price: €{flight['price']} (Adult + Child)")
    output.append(f"Departure: {flight['departure_time']} from {flight['origin_airport']}")
    output.append(f"Arrival: {flight['arrival_time']} at {flight['destination_airport']}")
    output.append(f"Total Duration: {flight['total_duration']} minutes ({flight['total_duration']//60}h {flight['total_duration']%60}m)")
    
    if flight['airlines']:
        output.append(f"Airlines: {', '.join(flight['airlines'])}")
    
    if flight['layovers']:
        output.append(f"\nConnections ({len(flight['layovers'])}):")
        for i, layover in enumerate(flight['layovers']):
            output.append(f"  {i+1}. {layover['airport']} ({layover['id']}) - {layover['duration']} minutes")
            
            # Add warnings if any
            if 'constraint_checks' in flight:
                conn_check = flight['constraint_checks']['connections']
                if conn_check.get('warnings'):
                    for warning in conn_check['warnings']:
                        if f"Connection {i+1}" in warning:
                            output.append(f"     ⚠️  {warning}")
    else:
        output.append("\n✈️  Direct Flight")
    
    return '\n'.join(output)


def main():
    """Main POC execution"""
    print("="*80)
    print("FLIGHT SEARCH POC - Phase 1")
    print("WRO (Wrocław) → TLV (Tel Aviv) / HFA (Haifa)")
    print("="*80)
    print()
    
    # Check API key
    if SERPAPI_KEY == 'YOUR_API_KEY_HERE':
        print("❌ ERROR: Please set SERPAPI_KEY environment variable")
        print("Get your free API key at: https://serpapi.com/")
        print("Free tier: 100 searches/month")
        print()
        print("Set it with: export SERPAPI_KEY='your_key_here'")
        return
    
    # Search parameters
    origin = 'WRO'
    destination = 'TLV'  # Start with Tel Aviv
    
    # Example: Search for flights 30 days from now, 5-day trip
    departure_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    return_date = (datetime.now() + timedelta(days=35)).strftime('%Y-%m-%d')
    
    print(f"📅 Searching flights:")
    print(f"   Route: {origin} → {destination}")
    print(f"   Outbound: {departure_date}")
    print(f"   Return: {return_date}")
    print(f"   Passengers: 1 Adult + 1 Child (4 years old)")
    print()
    print("⏳ Searching... (this may take 10-20 seconds)")
    print()
    
    # Search outbound flights
    outbound_results = search_flights_serpapi(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=None,  # One-way search for now
        adults=1,
        children=1
    )
    
    if 'error' in outbound_results:
        print(f"❌ Error searching flights: {outbound_results['error']}")
        return
    
    # Parse results
    print("✅ Results received, parsing...")
    flights = parse_serpapi_results(outbound_results)
    print(f"📊 Found {len(flights)} total flight options")
    print()
    
    # Apply constraints
    print("🔍 Applying constraints:")
    print(f"   ✓ Departure: 07:30 - 18:00")
    print(f"   ✓ Arrival: 08:00 - 21:00")
    print(f"   ✓ Max duration: 12 hours")
    print(f"   ✓ Connection times: 1h (Schengen) / 2h (exit Schengen)")
    print()
    
    valid_flights = filter_flights(flights)
    
    print(f"✅ {len(valid_flights)} flights meet all constraints")
    print()
    
    if not valid_flights:
        print("❌ No flights found matching all constraints")
        print("💡 Try adjusting:")
        print("   - Different dates")
        print("   - Different destination (try HFA)")
        print("   - Relaxing time windows")
        return
    
    # Sort by price
    valid_flights.sort(key=lambda x: x['price'])
    
    # Display results
    print("="*80)
    print("VALID FLIGHT OPTIONS (sorted by price)")
    print("="*80)
    
    for i, flight in enumerate(valid_flights[:10]):  # Show top 10
        print(format_flight_result(flight, i))
    
    if len(valid_flights) > 10:
        print(f"\n... and {len(valid_flights) - 10} more options")
    
    print("\n" + "="*80)
    print("POC Complete!")
    print("="*80)
    print("\n💡 Next Steps:")
    print("   1. Test with different dates")
    print("   2. Test return flights")
    print("   3. Compare with Google Flights manually")
    print("   4. Add more data sources (Phase 2)")
    print("   5. Implement monitoring (Phase 3)")


if __name__ == '__main__':
    main()
