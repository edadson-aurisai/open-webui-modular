import requests
import json

def test_endpoint(url):
    try:
        response = requests.get(url, timeout=5)
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
        print()
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        print()

# Test API Gateway
test_endpoint("http://localhost:8000/")
test_endpoint("http://localhost:8000/health")

# Test Inference Service
test_endpoint("http://localhost:8001/")
test_endpoint("http://localhost:8001/health")

# Test Agent Service
test_endpoint("http://localhost:8002/")
test_endpoint("http://localhost:8002/health")

# Test Retrieval Service
test_endpoint("http://localhost:8003/")
test_endpoint("http://localhost:8003/health")

# Test Chat Service
test_endpoint("http://localhost:8004/")
test_endpoint("http://localhost:8004/health")
