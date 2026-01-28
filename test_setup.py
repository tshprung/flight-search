#!/usr/bin/env python3
"""
Quick test script to verify setup before running full search
"""

import os
import sys

def test_api_key():
    """Check if API key is set"""
    api_key = os.environ.get('SERPAPI_KEY', '')
    
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        print("❌ SERPAPI_KEY not set")
        print("\n📋 Setup instructions:")
        print("   1. Go to https://serpapi.com/")
        print("   2. Sign up for free account")
        print("   3. Copy your API key from dashboard")
        print("   4. Run: export SERPAPI_KEY='your_key_here'")
        return False
    else:
        print("✅ API key found")
        print(f"   Key: {api_key[:10]}...{api_key[-5:]}")
        return True


def test_imports():
    """Check if required packages are installed"""
    try:
        import requests
        print("✅ requests library installed")
        return True
    except ImportError:
        print("❌ requests library not found")
        print("\n📋 Installation:")
        print("   pip install requests")
        return False


def test_api_connection():
    """Test SerpApi connection"""
    try:
        import requests
        api_key = os.environ.get('SERPAPI_KEY', '')
        
        if not api_key:
            return False
        
        # Simple test query
        params = {
            'api_key': api_key,
            'engine': 'google',
            'q': 'test'
        }
        
        response = requests.get('https://serpapi.com/search.json', params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ SerpApi connection successful")
            
            # Check remaining credits
            result = response.json()
            if 'search_metadata' in result:
                print(f"   Account status: Active")
            return True
        elif response.status_code == 401:
            print("❌ API key invalid")
            print("   Please check your SERPAPI_KEY")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        return False


def main():
    print("="*60)
    print("FLIGHT SEARCH POC - Setup Verification")
    print("="*60)
    print()
    
    all_ok = True
    
    print("1️⃣  Checking Python packages...")
    if not test_imports():
        all_ok = False
    print()
    
    print("2️⃣  Checking API key...")
    if not test_api_key():
        all_ok = False
    print()
    
    print("3️⃣  Testing API connection...")
    if not test_api_connection():
        all_ok = False
    print()
    
    print("="*60)
    if all_ok:
        print("✅ ALL CHECKS PASSED")
        print()
        print("🚀 You're ready to run the flight search!")
        print()
        print("Run: python flight_search_poc.py")
    else:
        print("❌ SOME CHECKS FAILED")
        print()
        print("Please fix the issues above before running the search.")
    print("="*60)
    
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
