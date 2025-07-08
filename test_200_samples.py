#!/usr/bin/env python3
import requests
import json
import time
import random
from typing import List, Dict

def generate_test_cases():
    """Generate 200 diverse test cases"""
    test_cases = []
    
    colleges = ["ADYPU", "MIT", "SAGE", "GDG", "JECRC", "SHU", "NIU", "JU", "HIMT", "NIET"]
    cities = ["Pune", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"]
    states = ["Maharashtra", "Uttar Pradesh", "Karnataka", "Madhya Pradesh", "Rajasthan", "Telangana", "Tamil Nadu", "West Bengal", "Gujarat", "Kerala"]
    courses = ["BBA", "MBA", "BCA", "MCA", "B.Tech", "M.Tech", "B.Sc", "M.Sc", "B.Com", "M.Com"]
    languages = ["Hindi", "English", "Hinglish", "Marathi", "Tamil", "Kannada", "Telugu", "Assamese"]
    
    # 50 College-specific cases
    for i in range(50):
        test_cases.append({
            "name": f"College-specific-{i+1}",
            "data": {
                "college": random.choice(colleges),
                "city": "",
                "state": random.choice(states),
                "course": random.choice(courses),
                "language": random.choice(languages)
            }
        })
    
    # 50 City-specific cases
    for i in range(50):
        test_cases.append({
            "name": f"City-specific-{i+1}",
            "data": {
                "college": "",
                "city": random.choice(cities),
                "state": random.choice(states),
                "course": random.choice(courses),
                "language": random.choice(languages)
            }
        })
    
    # 30 State-only cases
    for i in range(30):
        test_cases.append({
            "name": f"State-only-{i+1}",
            "data": {
                "college": "",
                "city": "",
                "state": random.choice(states),
                "course": random.choice(courses),
                "language": random.choice(languages)
            }
        })
    
    # 30 College+City cases
    for i in range(30):
        test_cases.append({
            "name": f"College-City-{i+1}",
            "data": {
                "college": random.choice(colleges),
                "city": random.choice(cities),
                "state": random.choice(states),
                "course": random.choice(courses),
                "language": random.choice(languages)
            }
        })
    
    # 20 Edge cases
    for i in range(10):
        test_cases.append({
            "name": f"Empty-language-{i+1}",
            "data": {
                "college": random.choice(colleges),
                "city": "",
                "state": random.choice(states),
                "course": random.choice(courses),
                "language": ""
            }
        })
    
    for i in range(10):
        test_cases.append({
            "name": f"Disabled-language-{i+1}",
            "data": {
                "college": random.choice(colleges),
                "city": "",
                "state": random.choice(states),
                "course": random.choice(courses),
                "language": random.choice(["Marathi", "Tamil", "Kannada", "Telugu", "Assamese"])
            }
        })
    
    # 20 Real-world scenarios
    real_scenarios = [
        {"college": "ADYPU", "city": "Pune", "state": "Maharashtra", "course": "BBA", "language": "Hindi"},
        {"college": "MIT", "city": "Pune", "state": "Maharashtra", "course": "B.Tech", "language": "English"},
        {"college": "SAGE", "city": "Indore", "state": "Madhya Pradesh", "course": "MBA", "language": "Hinglish"},
        {"college": "JECRC", "city": "Jaipur", "state": "Rajasthan", "course": "BCA", "language": "Hindi"},
        {"college": "NIU", "city": "Greater Noida", "state": "Uttar Pradesh", "course": "BBA", "language": "Hinglish"},
        {"college": "", "city": "Bangalore", "state": "Karnataka", "course": "MCA", "language": "English"},
        {"college": "", "city": "Hyderabad", "state": "Telangana", "course": "B.Tech", "language": "English"},
        {"college": "", "city": "Chennai", "state": "Tamil Nadu", "course": "MBA", "language": "English"},
        {"college": "", "city": "Kolkata", "state": "West Bengal", "course": "BBA", "language": "English"},
        {"college": "", "city": "Ahmedabad", "state": "Gujarat", "course": "BCA", "language": "English"},
        {"college": "", "city": "", "state": "Kerala", "course": "B.Tech", "language": "English"},
        {"college": "", "city": "", "state": "Punjab", "course": "MBA", "language": "English"},
        {"college": "", "city": "", "state": "Haryana", "course": "BBA", "language": "English"},
        {"college": "", "city": "", "state": "Himachal Pradesh", "course": "BCA", "language": "English"},
        {"college": "", "city": "", "state": "Uttarakhand", "course": "B.Tech", "language": "English"},
        {"college": "ADYPU", "city": "Pune", "state": "Maharashtra", "course": "BBA", "language": "Marathi"},
        {"college": "MIT", "city": "Pune", "state": "Maharashtra", "course": "B.Tech", "language": "Tamil"},
        {"college": "SAGE", "city": "Indore", "state": "Madhya Pradesh", "course": "MBA", "language": "Kannada"},
        {"college": "JECRC", "city": "Jaipur", "state": "Rajasthan", "course": "BCA", "language": "Telugu"},
        {"college": "NIU", "city": "Greater Noida", "state": "Uttar Pradesh", "course": "BBA", "language": "Assamese"}
    ]
    
    for i, scenario in enumerate(real_scenarios):
        test_cases.append({
            "name": f"Real-scenario-{i+1}",
            "data": scenario
        })
    
    return test_cases

def test_single_case(test_case, base_url="http://localhost:8000"):
    """Test a single case"""
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/enrich_lead",
            json=test_case["data"],
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return {
                "test_case": test_case["name"],
                "success": True,
                "response_time": response_time,
                "status_code": response.status_code,
                "tts_languages": data.get("tts_languages", []),
                "caller_name": data.get("caller_name", ""),
                "pitch_text": data.get("pitch_text", ""),
                "has_college": bool(data.get("college")),
                "has_city": bool(data.get("city"))
            }
        else:
            return {
                "test_case": test_case["name"],
                "success": False,
                "response_time": response_time,
                "status_code": response.status_code,
                "error": response.text
            }
            
    except Exception as e:
        return {
            "test_case": test_case["name"],
            "success": False,
            "response_time": time.time() - start_time,
            "status_code": None,
            "error": str(e)
        }

def analyze_results(results):
    """Analyze test results"""
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r["success"])
    failed_tests = total_tests - successful_tests
    
    # Response time analysis
    response_times = [r["response_time"] for r in results if r["success"]]
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    max_response_time = max(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0
    
    # Language distribution
    language_counts = {}
    caller_name_counts = {}
    
    for result in results:
        if result["success"]:
            for lang in result["tts_languages"]:
                language_counts[lang] = language_counts.get(lang, 0) + 1
            
            caller_name = result["caller_name"]
            caller_name_counts[caller_name] = caller_name_counts.get(caller_name, 0) + 1
    
    return {
        "summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        },
        "performance": {
            "avg_response_time": avg_response_time,
            "max_response_time": max_response_time,
            "min_response_time": min_response_time
        },
        "language_distribution": language_counts,
        "caller_name_distribution": caller_name_counts,
        "detailed_results": results
    }

def print_summary(analysis):
    """Print comprehensive summary"""
    summary = analysis["summary"]
    performance = analysis["performance"]
    
    print("\n" + "="*80)
    print("🎯 COMPREHENSIVE TEST RESULTS SUMMARY")
    print("="*80)
    
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   Total Tests: {summary['total_tests']}")
    print(f"   Successful: {summary['successful_tests']} ✅")
    print(f"   Failed: {summary['failed_tests']} ❌")
    print(f"   Success Rate: {summary['success_rate']:.2f}%")
    
    print(f"\n⚡ PERFORMANCE METRICS:")
    print(f"   Average Response Time: {performance['avg_response_time']:.3f}s")
    print(f"   Maximum Response Time: {performance['max_response_time']:.3f}s")
    print(f"   Minimum Response Time: {performance['min_response_time']:.3f}s")
    
    print(f"\n🌐 LANGUAGE DISTRIBUTION:")
    for lang, count in sorted(analysis["language_distribution"].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / summary['total_tests']) * 100
        print(f"   {lang}: {count} times ({percentage:.1f}%)")
    
    print(f"\n👤 CALLER NAME DISTRIBUTION:")
    for name, count in sorted(analysis["caller_name_distribution"].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / summary['total_tests']) * 100
        print(f"   {name}: {count} times ({percentage:.1f}%)")
    
    # Show sample successful responses
    successful_results = [r for r in analysis["detailed_results"] if r["success"]]
    if successful_results:
        print(f"\n📝 SAMPLE SUCCESSFUL RESPONSES:")
        for i, result in enumerate(successful_results[:5]):
            print(f"\n   Sample {i+1}:")
            print(f"     Test: {result['test_case']}")
            print(f"     Caller: {result['caller_name']}")
            print(f"     Languages: {result['tts_languages']}")
            print(f"     Response Time: {result['response_time']:.3f}s")
    
    print("\n" + "="*80)
    print("🏁 TEST COMPLETED")
    print("="*80)

def main():
    """Main test runner"""
    print("🧪 Lead Intelligence API - 200 Sample Test Cases")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding properly")
            return
        print("✅ Server is running and healthy")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please start the server with: uvicorn app.main:app --reload")
        return
    
    # Generate test cases
    test_cases = generate_test_cases()
    print(f"📋 Generated {len(test_cases)} test cases")
    
    # Run tests
    print("🚀 Starting tests...")
    results = []
    
    for i, test_case in enumerate(test_cases):
        if (i + 1) % 20 == 0:
            print(f"📦 Processed {i + 1}/{len(test_cases)} test cases...")
        
        result = test_single_case(test_case)
        results.append(result)
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.01)
    
    # Analyze results
    analysis = analyze_results(results)
    print_summary(analysis)
    
    # Save detailed results
    with open("test_results_200.json", "w") as f:
        json.dump(analysis, f, indent=2)
    print(f"\n💾 Detailed results saved to: test_results_200.json")

if __name__ == "__main__":
    main() 