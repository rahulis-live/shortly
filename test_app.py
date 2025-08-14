#!/usr/bin/env python3
"""
Simple test script for the URL Shortener application
"""

import requests
import json
import time

def test_url_shortener():
    """Test the URL shortener functionality"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing URL Shortener Application")
    print("=" * 50)
    
    # Test 1: Check if the application is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Application is running successfully")
        else:
            print(f"❌ Application returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to application: {e}")
        print("Make sure the application is running with: python app.py")
        return False
    
    # Test 2: Test URL shortening
    test_url = "https://www.google.com"
    print(f"\n🔗 Testing URL shortening with: {test_url}")
    
    try:
        response = requests.post(
            f"{base_url}/shorten",
            json={"url": test_url},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ URL shortened successfully!")
            print(f"   Original URL: {data['original_url']}")
            print(f"   Shortened URL: {data['short_url']}")
            print(f"   Short Code: {data['short_code']}")
            
            short_code = data['short_code']
            short_url = data['short_url']
            
            # Test 3: Test URL redirection
            print(f"\n🔄 Testing URL redirection...")
            redirect_response = requests.get(short_url, allow_redirects=False, timeout=10)
            
            if redirect_response.status_code in [301, 302, 307, 308]:
                print("✅ URL redirection working correctly")
                print(f"   Redirect status: {redirect_response.status_code}")
                print(f"   Redirect location: {redirect_response.headers.get('Location', 'N/A')}")
            else:
                print(f"❌ Unexpected redirect status: {redirect_response.status_code}")
            
            # Test 4: Test statistics endpoint
            print(f"\n📊 Testing statistics endpoint...")
            stats_response = requests.get(f"{base_url}/stats/{short_code}", timeout=10)
            
            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                print("✅ Statistics endpoint working correctly")
                print(f"   Clicks: {stats_data['clicks']}")
                print(f"   Created: {stats_data['created_at']}")
            else:
                print(f"❌ Statistics endpoint failed: {stats_response.status_code}")
            
            # Test 5: Test invalid URL
            print(f"\n🚫 Testing invalid URL handling...")
            invalid_response = requests.post(
                f"{base_url}/shorten",
                json={"url": "not-a-valid-url"},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if invalid_response.status_code == 400:
                print("✅ Invalid URL properly rejected")
            else:
                print(f"❌ Invalid URL not properly handled: {invalid_response.status_code}")
            
            # Test 6: Test duplicate URL
            print(f"\n🔄 Testing duplicate URL handling...")
            duplicate_response = requests.post(
                f"{base_url}/shorten",
                json={"url": test_url},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if duplicate_response.status_code == 200:
                duplicate_data = duplicate_response.json()
                if duplicate_data['short_code'] == short_code:
                    print("✅ Duplicate URL returns same short code")
                else:
                    print("❌ Duplicate URL returned different short code")
            else:
                print(f"❌ Duplicate URL handling failed: {duplicate_response.status_code}")
            
        else:
            print(f"❌ URL shortening failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("The URL Shortener application is working correctly.")
    return True

if __name__ == "__main__":
    test_url_shortener()
