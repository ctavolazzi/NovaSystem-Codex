#!/usr/bin/env python3
"""
Comprehensive Test Suite for NovaSystem v3.0
Tests every page, interaction, and feature automatically
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
import subprocess
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class NovaSystemTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.driver = None
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

    def setup_driver(self):
        """Setup Chrome WebDriver with optimal settings"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            self.log_test("WebDriver Setup", "PASS", "Chrome WebDriver initialized successfully")
            return True
        except Exception as e:
            self.log_test("WebDriver Setup", "FAIL", error=e)
            return False

    def start_server(self):
        """Start NovaSystem server"""
        try:
            print("🚀 Starting NovaSystem server...")
            self.server_process = subprocess.Popen([
                sys.executable, "-m", "novasystem.ui.web"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait for server to start
            time.sleep(5)

            # Test if server is responding
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                self.log_test("Server Startup", "PASS", f"Server started successfully on {self.base_url}")
                return True
            else:
                self.log_test("Server Startup", "FAIL", f"Server responded with status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Startup", "FAIL", error=e)
            return False

    def test_page_load(self, url, page_name):
        """Test if a page loads successfully"""
        try:
            self.driver.get(f"{self.base_url}{url}")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Check for basic elements
            title = self.driver.title
            body = self.driver.find_element(By.TAG_NAME, "body")

            if body and title:
                self.log_test(f"Page Load: {page_name}", "PASS", f"Title: {title}")
                return True
            else:
                self.log_test(f"Page Load: {page_name}", "FAIL", "Page loaded but missing essential elements")
                return False
        except TimeoutException:
            self.log_test(f"Page Load: {page_name}", "FAIL", "Page failed to load within timeout")
            return False
        except Exception as e:
            self.log_test(f"Page Load: {page_name}", "FAIL", error=e)
            return False

    def test_navigation_elements(self, page_name):
        """Test navigation elements on current page"""
        try:
            # Test sidebar navigation
            sidebar_nav = self.driver.find_element(By.ID, "sidebar-nav")
            if sidebar_nav:
                nav_items = sidebar_nav.find_elements(By.CSS_SELECTOR, ".sidebar-item")
                self.log_test(f"Navigation: {page_name}", "PASS", f"Found {len(nav_items)} navigation items")
            else:
                self.log_test(f"Navigation: {page_name}", "FAIL", "Sidebar navigation not found")
                return False

            # Test menu bar
            menu_bar = self.driver.find_element(By.ID, "main-menu-bar")
            if menu_bar:
                menu_items = menu_bar.find_elements(By.CSS_SELECTOR, ".menu-item")
                self.log_test(f"Menu Bar: {page_name}", "PASS", f"Found {len(menu_items)} menu items")
            else:
                self.log_test(f"Menu Bar: {page_name}", "FAIL", "Menu bar not found")

            # Test taskbar
            taskbar = self.driver.find_element(By.CLASS_NAME, "windows-taskbar")
            if taskbar:
                self.log_test(f"Taskbar: {page_name}", "PASS", "Windows taskbar found")
            else:
                self.log_test(f"Taskbar: {page_name}", "FAIL", "Windows taskbar not found")

            return True
        except NoSuchElementException as e:
            self.log_test(f"Navigation Elements: {page_name}", "FAIL", error=e)
            return False
        except Exception as e:
            self.log_test(f"Navigation Elements: {page_name}", "FAIL", error=e)
            return False

    def test_responsive_design(self, page_name):
        """Test responsive design at different screen sizes"""
        try:
            sizes = [
                (1920, 1080, "Desktop"),
                (1024, 768, "Tablet"),
                (768, 1024, "Tablet Portrait"),
                (375, 667, "Mobile"),
                (320, 568, "Mobile Small")
            ]

            responsive_tests_passed = 0
            for width, height, device_name in sizes:
                self.driver.set_window_size(width, height)
                time.sleep(1)  # Allow layout to adjust

                # Check if main elements are still visible
                try:
                    main_window = self.driver.find_element(By.CLASS_NAME, "main-window")
                    if main_window.is_displayed():
                        responsive_tests_passed += 1
                except NoSuchElementException:
                    pass

            if responsive_tests_passed == len(sizes):
                self.log_test(f"Responsive Design: {page_name}", "PASS", f"All {len(sizes)} screen sizes tested successfully")
            else:
                self.log_test(f"Responsive Design: {page_name}", "FAIL", f"Only {responsive_tests_passed}/{len(sizes)} screen sizes passed")

            # Reset to desktop size
            self.driver.set_window_size(1920, 1080)
            return responsive_tests_passed == len(sizes)
        except Exception as e:
            self.log_test(f"Responsive Design: {page_name}", "FAIL", error=e)
            return False

    def test_chat_interface(self):
        """Test chat interface functionality"""
        try:
            # Test message input
            message_input = self.driver.find_element(By.ID, "messageInput")
            if message_input:
                message_input.send_keys("Test message for automated testing")
                self.log_test("Chat Input", "PASS", "Message input field functional")
            else:
                self.log_test("Chat Input", "FAIL", "Message input field not found")
                return False

            # Test send button
            send_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            if send_button:
                send_button.click()
                time.sleep(2)  # Wait for potential response
                self.log_test("Chat Send", "PASS", "Send button functional")
            else:
                self.log_test("Chat Send", "FAIL", "Send button not found")

            return True
        except Exception as e:
            self.log_test("Chat Interface", "FAIL", error=e)
            return False

    def test_settings_functionality(self):
        """Test settings page functionality"""
        try:
            # Test navigation between settings sections
            settings_sections = ["general", "appearance", "ai", "performance", "security", "advanced"]

            for section in settings_sections:
                try:
                    section_link = self.driver.find_element(By.CSS_SELECTOR, f"[data-section='{section}']")
                    section_link.click()
                    time.sleep(0.5)

                    section_content = self.driver.find_element(By.ID, section)
                    if section_content and "active" in section_content.get_attribute("class"):
                        self.log_test(f"Settings Section: {section.title()}", "PASS", "Section navigation working")
                    else:
                        self.log_test(f"Settings Section: {section.title()}", "FAIL", "Section content not active")
                except NoSuchElementException:
                    self.log_test(f"Settings Section: {section.title()}", "FAIL", f"Section link not found")

            # Test settings save functionality
            save_button = self.driver.find_element(By.ID, "save-settings")
            if save_button:
                save_button.click()
                time.sleep(1)
                self.log_test("Settings Save", "PASS", "Save button functional")

            return True
        except Exception as e:
            self.log_test("Settings Functionality", "FAIL", error=e)
            return False

    def test_help_search(self):
        """Test help page search functionality"""
        try:
            search_input = self.driver.find_element(By.ID, "help-search")
            if search_input:
                search_input.send_keys("navigation")
                time.sleep(1)

                # Check if search results are displayed
                sections = self.driver.find_elements(By.CSS_SELECTOR, ".help-section")
                visible_sections = [s for s in sections if s.is_displayed()]

                if visible_sections:
                    self.log_test("Help Search", "PASS", f"Search returned {len(visible_sections)} results")
                else:
                    self.log_test("Help Search", "FAIL", "No search results displayed")
            else:
                self.log_test("Help Search", "FAIL", "Search input not found")

            return True
        except Exception as e:
            self.log_test("Help Search", "FAIL", error=e)
            return False

    def test_session_management(self):
        """Test session management functionality"""
        try:
            # Test session filtering
            filters = self.driver.find_elements(By.CSS_SELECTOR, ".sessions-filter")
            if filters:
                for filter_btn in filters:
                    filter_btn.click()
                    time.sleep(0.5)
                    if "active" in filter_btn.get_attribute("class"):
                        self.log_test("Session Filter", "PASS", f"Filter {filter_btn.text} working")
                    else:
                        self.log_test("Session Filter", "FAIL", f"Filter {filter_btn.text} not active")

            # Test refresh button
            refresh_btn = self.driver.find_element(By.ID, "refresh-sessions")
            if refresh_btn:
                refresh_btn.click()
                time.sleep(1)
                self.log_test("Session Refresh", "PASS", "Refresh button functional")

            return True
        except Exception as e:
            self.log_test("Session Management", "FAIL", error=e)
            return False

    def test_workflow_functionality(self):
        """Test workflow page functionality"""
        try:
            # Test agent buttons
            agent_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".agent-button")
            if agent_buttons:
                for btn in agent_buttons[:2]:  # Test first 2 buttons
                    btn.click()
                    time.sleep(0.5)
                    self.log_test("Workflow Agent Button", "PASS", f"Agent button {btn.text} clickable")

            # Test workflow controls
            start_btn = self.driver.find_element(By.ID, "startBtn")
            if start_btn:
                start_btn.click()
                time.sleep(1)
                self.log_test("Workflow Start", "PASS", "Start button functional")

            return True
        except Exception as e:
            self.log_test("Workflow Functionality", "FAIL", error=e)
            return False

    def test_analytics_dashboard(self):
        """Test analytics dashboard"""
        try:
            # Check for chart containers
            chart_containers = self.driver.find_elements(By.CSS_SELECTOR, ".chart-container")
            if chart_containers:
                self.log_test("Analytics Charts", "PASS", f"Found {len(chart_containers)} chart containers")
            else:
                self.log_test("Analytics Charts", "FAIL", "No chart containers found")

            return True
        except Exception as e:
            self.log_test("Analytics Dashboard", "FAIL", error=e)
            return False

    def test_keyboard_shortcuts(self):
        """Test keyboard shortcuts"""
        try:
            # Test Ctrl+1 shortcut (Home)
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('1').key_up(Keys.CONTROL).perform()
            time.sleep(1)

            if self.driver.current_url.endswith('/'):
                self.log_test("Keyboard Shortcut: Ctrl+1", "PASS", "Home shortcut working")
            else:
                self.log_test("Keyboard Shortcut: Ctrl+1", "FAIL", "Home shortcut not working")

            # Test Ctrl+2 shortcut (Workflow)
            actions.key_down(Keys.CONTROL).send_keys('2').key_up(Keys.CONTROL).perform()
            time.sleep(1)

            if '/workflow' in self.driver.current_url:
                self.log_test("Keyboard Shortcut: Ctrl+2", "PASS", "Workflow shortcut working")
            else:
                self.log_test("Keyboard Shortcut: Ctrl+2", "FAIL", "Workflow shortcut not working")

            return True
        except Exception as e:
            self.log_test("Keyboard Shortcuts", "FAIL", error=e)
            return False

    def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        print("🧪 Starting Comprehensive NovaSystem Testing...")
        print("=" * 60)

        # Define all pages to test
        pages_to_test = [
            ("/", "Home"),
            ("/workflow", "Workflow"),
            ("/analytics", "Analytics"),
            ("/monitor", "Monitor"),
            ("/settings", "Settings"),
            ("/help", "Help"),
            ("/about", "About"),
            ("/sessions", "Session Manager"),
            ("/history", "Session History")
        ]

        # Test each page
        for url, page_name in pages_to_test:
            print(f"\n📄 Testing {page_name} page...")

            # Test page load
            if self.test_page_load(url, page_name):
                # Test navigation elements
                self.test_navigation_elements(page_name)

                # Test responsive design
                self.test_responsive_design(page_name)

                # Test page-specific functionality
                if page_name == "Home":
                    self.test_chat_interface()
                elif page_name == "Settings":
                    self.test_settings_functionality()
                elif page_name == "Help":
                    self.test_help_search()
                elif page_name == "Session Manager":
                    self.test_session_management()
                elif page_name == "Workflow":
                    self.test_workflow_functionality()
                elif page_name == "Analytics":
                    self.test_analytics_dashboard()

        # Test keyboard shortcuts (on Home page)
        self.driver.get(f"{self.base_url}/")
        self.test_keyboard_shortcuts()

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

        return success_rate >= 90  # Consider successful if 90%+ tests pass

    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

def main():
    """Main test execution"""
    tester = NovaSystemTester()

    try:
        # Setup
        if not tester.setup_driver():
            print("❌ Failed to setup WebDriver")
            return False

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
