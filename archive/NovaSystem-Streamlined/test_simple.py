#!/usr/bin/env python3
"""
Simple Comprehensive Test Suite for NovaSystem v3.0
Tests every page and API endpoint using HTTP requests
"""

import requests
import time
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class SimpleNovaSystemTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }
        self.server_process = None

    def log_test(self, test_name, status, details="", error=None):
        """Log test results"""
        self.test_results["total_tests"] += 1
        if status == "PASS":
            self.test_results["passed_tests"] += 1
        else:
            self.test_results["failed_tests"] += 1

        test_result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "error": str(error) if error else None,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results["test_details"].append(test_result)

        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if error:
            print(f"   Error: {error}")

    def start_server(self):
        """Start NovaSystem server"""
        try:
            print("🚀 Starting NovaSystem server...")
            self.server_process = subprocess.Popen([
                sys.executable, "-m", "novasystem.ui.web"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for server to start
            time.sleep(8)

            # Test if server is responding
            response = self.session.get(f"{self.base_url}/", timeout=15)
            if response.status_code == 200:
                self.log_test("Server Startup", "PASS", f"Server started successfully on {self.base_url}")
                return True
            else:
                self.log_test("Server Startup", "FAIL", f"Server responded with status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Startup", "FAIL", error=e)
            return False

    def test_page_response(self, url, page_name, expected_content=None):
        """Test if a page responds correctly"""
        try:
            response = self.session.get(f"{self.base_url}{url}", timeout=10)

            if response.status_code == 200:
                content_length = len(response.content)
                content_type = response.headers.get('content-type', '')

                details = f"Status: {response.status_code}, Size: {content_length} bytes, Type: {content_type}"

                # Check for expected content
                if expected_content and expected_content not in response.text:
                    self.log_test(f"Page Content: {page_name}", "FAIL", f"Expected content '{expected_content}' not found")
                else:
                    self.log_test(f"Page Response: {page_name}", "PASS", details)
                    return True
            else:
                self.log_test(f"Page Response: {page_name}", "FAIL", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test(f"Page Response: {page_name}", "FAIL", error=e)
            return False

    def test_page_content(self, url, page_name, required_elements):
        """Test if page contains required elements"""
        try:
            response = self.session.get(f"{self.base_url}{url}", timeout=10)
            if response.status_code != 200:
                self.log_test(f"Page Content: {page_name}", "FAIL", f"Failed to load page: {response.status_code}")
                return False

            content = response.text
            missing_elements = []

            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)

            if missing_elements:
                self.log_test(f"Page Content: {page_name}", "FAIL", f"Missing elements: {missing_elements}")
                return False
            else:
                self.log_test(f"Page Content: {page_name}", "PASS", f"All required elements found: {required_elements}")
                return True
        except Exception as e:
            self.log_test(f"Page Content: {page_name}", "FAIL", error=e)
            return False

    def test_api_endpoint(self, url, method="GET", data=None, expected_status=200):
        """Test API endpoints"""
        try:
            if method == "GET":
                response = self.session.get(f"{self.base_url}{url}", timeout=10)
            elif method == "POST":
                response = self.session.post(f"{self.base_url}{url}", json=data, timeout=10)
            else:
                self.log_test(f"API: {url}", "FAIL", f"Unsupported method: {method}")
                return False

            if response.status_code == expected_status:
                self.log_test(f"API: {url}", "PASS", f"{method} {response.status_code}")
                return True
            else:
                self.log_test(f"API: {url}", "FAIL", f"Expected {expected_status}, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test(f"API: {url}", "FAIL", error=e)
            return False

    def test_navigation_consistency(self):
        """Test navigation consistency across pages"""
        try:
            pages = ["/", "/workflow", "/analytics", "/monitor", "/settings", "/help", "/about", "/sessions", "/history"]
            navigation_elements = [
                "windows-taskbar",
                "navigation.js",
                "sidebar",
                "menu-bar"
            ]

            consistent_pages = 0
            for page in pages:
                response = self.session.get(f"{self.base_url}{page}", timeout=10)
                if response.status_code == 200:
                    content = response.text
                    missing_elements = [elem for elem in navigation_elements if elem not in content]
                    if not missing_elements:
                        consistent_pages += 1

            if consistent_pages == len(pages):
                self.log_test("Navigation Consistency", "PASS", f"All {len(pages)} pages have consistent navigation")
            else:
                self.log_test("Navigation Consistency", "FAIL", f"Only {consistent_pages}/{len(pages)} pages have consistent navigation")

            return consistent_pages == len(pages)
        except Exception as e:
            self.log_test("Navigation Consistency", "FAIL", error=e)
            return False

    def test_responsive_assets(self):
        """Test if responsive CSS and JavaScript assets are accessible"""
        try:
            assets = [
                "/static/shared/navigation.js",
                "/static/shared/navigation.css",
                "/static/shared/responsive-test.js"
            ]

            accessible_assets = 0
            for asset in assets:
                response = self.session.get(f"{self.base_url}{asset}", timeout=10)
                if response.status_code == 200:
                    accessible_assets += 1

            if accessible_assets == len(assets):
                self.log_test("Responsive Assets", "PASS", f"All {len(assets)} assets accessible")
            else:
                self.log_test("Responsive Assets", "FAIL", f"Only {accessible_assets}/{len(assets)} assets accessible")

            return accessible_assets == len(assets)
        except Exception as e:
            self.log_test("Responsive Assets", "FAIL", error=e)
            return False

    def test_session_api(self):
        """Test session management API"""
        try:
            # Test sessions endpoint
            response = self.session.get(f"{self.base_url}/api/sessions", timeout=10)
            if response.status_code == 200:
                self.log_test("Sessions API", "PASS", "Sessions endpoint accessible")

                # Test kill-all endpoint
                kill_response = self.session.post(f"{self.base_url}/api/sessions/kill-all", timeout=10)
                if kill_response.status_code == 200:
                    self.log_test("Kill All API", "PASS", "Kill all sessions endpoint working")
                else:
                    self.log_test("Kill All API", "FAIL", f"Status: {kill_response.status_code}")

                return True
            else:
                self.log_test("Sessions API", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Session API", "FAIL", error=e)
            return False

    def test_workflow_api(self):
        """Test workflow API"""
        try:
            # Test workflow execution endpoint
            workflow_data = {
                "nodes": [
                    {"id": "node_1", "type": "problem-solver", "title": "Test Node"}
                ],
                "connections": []
            }

            response = self.session.post(f"{self.base_url}/api/workflow/execute", json=workflow_data, timeout=15)
            if response.status_code in [200, 202]:  # 202 for async processing
                self.log_test("Workflow API", "PASS", "Workflow execution endpoint working")
                return True
            else:
                self.log_test("Workflow API", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Workflow API", "FAIL", error=e)
            return False

    def test_solve_api(self):
        """Test problem solving API"""
        try:
            solve_data = {
                "problem": "Test problem for automated testing",
                "domains": ["General"],
                "max_iterations": 1,
                "model": "auto"
            }

            response = self.session.post(f"{self.base_url}/api/solve", json=solve_data, timeout=15)
            if response.status_code in [200, 202]:  # 202 for async processing
                self.log_test("Solve API", "PASS", "Problem solving endpoint working")
                return True
            else:
                self.log_test("Solve API", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Solve API", "FAIL", error=e)
            return False

    def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        print("🧪 Starting Comprehensive NovaSystem Testing...")
        print("=" * 60)

        # Test all pages
        pages_to_test = [
            ("/", "Home", ["NovaSystem", "chat-messages", "messageInput"]),
            ("/workflow", "Workflow", ["Workflow Engine", "agent-toolbar", "workflow-canvas"]),
            ("/analytics", "Analytics", ["Analytics Dashboard", "analytics-chart"]),
            ("/monitor", "Monitor", ["Real-Time Monitor", "monitor-container"]),
            ("/settings", "Settings", ["Settings", "settings-container"]),
            ("/help", "Help", ["Help & Documentation", "help-container"]),
            ("/about", "About", ["About", "about-container"]),
            ("/sessions", "Session Manager", ["Session Manager", "sessions-container"]),
            ("/history", "Session History", ["Session History", "history-container"])
        ]

        print("\n📄 Testing All Pages...")
        for url, page_name, required_elements in pages_to_test:
            self.test_page_response(url, page_name)
            self.test_page_content(url, page_name, required_elements)

        print("\n🔗 Testing Navigation Consistency...")
        self.test_navigation_consistency()

        print("\n📱 Testing Responsive Assets...")
        self.test_responsive_assets()

        print("\n🔌 Testing API Endpoints...")
        self.test_session_api()
        self.test_workflow_api()
        self.test_solve_api()

        print("\n" + "=" * 60)
        print("🎯 Comprehensive Testing Complete!")

    def generate_report(self):
        """Generate comprehensive test report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test_report_{timestamp}.json"

        # Save detailed report
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)

        # Generate summary
        total = self.test_results["total_tests"]
        passed = self.test_results["passed_tests"]
        failed = self.test_results["failed_tests"]
        success_rate = (passed / total * 100) if total > 0 else 0

        print(f"\n📊 TEST REPORT SUMMARY")
        print(f"=" * 40)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Report saved to: {report_file}")

        # Show failed tests
        if failed > 0:
            print(f"\n❌ FAILED TESTS:")
            for test in self.test_results["test_details"]:
                if test["status"] == "FAIL":
                    print(f"  - {test['test_name']}: {test.get('error', 'Unknown error')}")

        return success_rate >= 85  # Consider successful if 85%+ tests pass

    def cleanup(self):
        """Cleanup resources"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

def main():
    """Main test execution"""
    tester = SimpleNovaSystemTester()

    try:
        # Start server
        if not tester.start_server():
            print("❌ Failed to start server")
            return False

        # Run tests
        tester.run_comprehensive_tests()

        # Generate report
        success = tester.generate_report()

        return success

    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Testing failed with error: {e}")
        return False
    finally:
        tester.cleanup()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
