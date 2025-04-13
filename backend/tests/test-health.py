#!/usr/bin/env python3
"""
Script to test the health of all backend services.
"""

import argparse
import requests
import sys
from typing import Dict, List, Tuple

# Service definitions
SERVICES = {
    "api-gateway": 8000,
    "chat-service": 8001,
    "agent-service": 8002,
    "inference-service": 8003,
    "retrieval-service": 8004
}

def check_service_health(service_name: str, port: int) -> Tuple[bool, str]:
    """Check if a service is healthy by calling its health endpoint."""
    url = f"http://localhost:{port}/health"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True, f"{service_name} is healthy"
        else:
            return False, f"{service_name} returned status code {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, f"{service_name} is not running or not accessible"
    except Exception as e:
        return False, f"Error checking {service_name}: {str(e)}"

def check_service_info(service_name: str, port: int) -> Tuple[bool, Dict]:
    """Get service information from root endpoint."""
    url = f"http://localhost:{port}/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"Status code {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "Service not running or not accessible"}
    except Exception as e:
        return False, {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Test backend service health")
    parser.add_argument("--service", "-s", help="Specific service to test (default: all)")
    parser.add_argument("--info", "-i", action="store_true", help="Show detailed service information")
    args = parser.parse_args()
    
    services_to_check = {args.service: SERVICES[args.service]} if args.service else SERVICES
    
    all_healthy = True
    results = []
    
    for service_name, port in services_to_check.items():
        healthy, message = check_service_health(service_name, port)
        results.append((service_name, healthy, message))
        
        if args.info and healthy:
            _, info = check_service_info(service_name, port)
            print(f"\n{service_name.upper()} INFO:")
            print(f"  Service: {info.get('service', 'N/A')}")
            print(f"  Version: {info.get('version', 'N/A')}")
            print(f"  Description: {info.get('description', 'N/A')}")
            
            if 'endpoints' in info:
                print("  Endpoints:")
                for key, value in info['endpoints'].items():
                    if isinstance(value, dict):
                        print(f"    {key}:")
                        for subkey, subvalue in value.items():
                            print(f"      {subkey}: {subvalue}")
                    else:
                        print(f"    {key}: {value}")
            print()
        
        if not healthy:
            all_healthy = False
    
    # Print summary
    print("\nSERVICE HEALTH SUMMARY:")
    for service_name, healthy, message in results:
        status = "✅" if healthy else "❌"
        print(f"{status} {service_name} (port {SERVICES[service_name]}): {message}")
    
    if all_healthy:
        print("\nAll services are healthy! 🎉")
        return 0
    else:
        print("\nSome services are not healthy. Check the logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
