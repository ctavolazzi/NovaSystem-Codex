/**
 * Responsive Testing Utility for NovaSystem
 * Helps verify navigation works across different screen sizes
 */

class ResponsiveTester {
    constructor() {
        this.testSizes = [
            { name: 'Mobile Small', width: 320, height: 568 },
            { name: 'Mobile Medium', width: 375, height: 667 },
            { name: 'Mobile Large', width: 414, height: 896 },
            { name: 'Tablet Portrait', width: 768, height: 1024 },
            { name: 'Tablet Landscape', width: 1024, height: 768 },
            { name: 'Desktop Small', width: 1200, height: 800 },
            { name: 'Desktop Medium', width: 1440, height: 900 },
            { name: 'Desktop Large', width: 1920, height: 1080 },
            { name: 'Desktop XL', width: 2560, height: 1440 }
        ];

        this.currentTestIndex = 0;
        this.isTesting = false;
    }

    init() {
        this.createTestControls();
        this.addKeyboardShortcuts();
    }

    createTestControls() {
        // Create floating test panel
        const testPanel = document.createElement('div');
        testPanel.id = 'responsive-test-panel';
        testPanel.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            z-index: 10000;
            display: none;
            min-width: 200px;
        `;

        testPanel.innerHTML = `
            <div style="margin-bottom: 10px; font-weight: bold;">Responsive Test</div>
            <div id="current-size">Current: ${window.innerWidth}x${window.innerHeight}</div>
            <div style="margin: 5px 0;">
                <button id="prev-size" style="margin-right: 5px; padding: 2px 6px; font-size: 10px;">←</button>
                <button id="next-size" style="margin-right: 5px; padding: 2px 6px; font-size: 10px;">→</button>
                <button id="toggle-test" style="padding: 2px 6px; font-size: 10px;">Start Test</button>
            </div>
            <div id="test-info" style="font-size: 10px; margin-top: 5px;"></div>
        `;

        document.body.appendChild(testPanel);

        // Add event listeners
        document.getElementById('prev-size').addEventListener('click', () => this.previousSize());
        document.getElementById('next-size').addEventListener('click', () => this.nextSize());
        document.getElementById('toggle-test').addEventListener('click', () => this.toggleTest());
    }

    addKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Shift+T to toggle responsive testing
            if (e.ctrlKey && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                this.toggleTest();
            }

            // Arrow keys to cycle through sizes when testing
            if (this.isTesting) {
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    this.previousSize();
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    this.nextSize();
                }
            }
        });
    }

    toggleTest() {
        const panel = document.getElementById('responsive-test-panel');
        const toggleBtn = document.getElementById('toggle-test');

        if (this.isTesting) {
            this.stopTest();
            panel.style.display = 'none';
            toggleBtn.textContent = 'Start Test';
        } else {
            this.startTest();
            panel.style.display = 'block';
            toggleBtn.textContent = 'Stop Test';
        }
    }

    startTest() {
        this.isTesting = true;
        this.updateSizeDisplay();
        this.showTestInfo();

        // Add visual indicators
        document.body.style.border = '3px solid #ff6b6b';
        document.body.style.position = 'relative';

        // Add resize indicator
        const indicator = document.createElement('div');
        indicator.id = 'resize-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 30px;
            background: #ff6b6b;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: monospace;
            font-size: 14px;
            font-weight: bold;
            z-index: 9999;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        `;
        indicator.textContent = 'RESPONSIVE TEST MODE - Use arrow keys to cycle sizes';
        document.body.appendChild(indicator);

        // Adjust body padding to account for indicator
        document.body.style.paddingTop = '30px';
    }

    stopTest() {
        this.isTesting = false;

        // Remove visual indicators
        document.body.style.border = '';
        document.body.style.position = '';
        document.body.style.paddingTop = '';

        const indicator = document.getElementById('resize-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    nextSize() {
        if (this.currentTestIndex < this.testSizes.length - 1) {
            this.currentTestIndex++;
        } else {
            this.currentTestIndex = 0;
        }
        this.applyCurrentSize();
    }

    previousSize() {
        if (this.currentTestIndex > 0) {
            this.currentTestIndex--;
        } else {
            this.currentTestIndex = this.testSizes.length - 1;
        }
        this.applyCurrentSize();
    }

    applyCurrentSize() {
        const size = this.testSizes[this.currentTestIndex];

        // Apply size to window (if in iframe or test environment)
        if (window.parent !== window) {
            window.parent.postMessage({
                type: 'resize',
                width: size.width,
                height: size.height
            }, '*');
        }

        // Update display
        this.updateSizeDisplay();
        this.showTestInfo();

        // Trigger resize event
        window.dispatchEvent(new Event('resize'));
    }

    updateSizeDisplay() {
        const size = this.testSizes[this.currentTestIndex];
        const currentSize = document.getElementById('current-size');
        currentSize.textContent = `Current: ${size.width}x${size.height}`;
    }

    showTestInfo() {
        const size = this.testSizes[this.currentTestIndex];
        const testInfo = document.getElementById('test-info');

        let breakpoint = '';
        if (size.width <= 320) breakpoint = 'Mobile (320px)';
        else if (size.width <= 480) breakpoint = 'Mobile (480px)';
        else if (size.width <= 768) breakpoint = 'Tablet (768px)';
        else if (size.width <= 1024) breakpoint = 'Small Desktop (1024px)';
        else if (size.width <= 1200) breakpoint = 'Desktop (1200px)';
        else if (size.width <= 1600) breakpoint = 'Large Desktop (1600px)';
        else breakpoint = 'XL Desktop (1920px+)';

        testInfo.innerHTML = `
            <div>Size: ${size.name}</div>
            <div>Breakpoint: ${breakpoint}</div>
            <div>Navigation: ${this.getNavigationType(size.width)}</div>
        `;
    }

    getNavigationType(width) {
        if (width <= 768) return 'Mobile (Horizontal)';
        if (width <= 1024) return 'Tablet (Adaptive)';
        return 'Desktop (Full)';
    }

    // Test navigation functionality
    testNavigation() {
        const tests = [];

        // Test sidebar visibility
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            const isVisible = sidebar.offsetWidth > 0;
            tests.push({
                name: 'Sidebar Visibility',
                passed: isVisible,
                details: `Sidebar width: ${sidebar.offsetWidth}px`
            });
        }

        // Test menu items
        const menuItems = document.querySelectorAll('.menu-item');
        tests.push({
            name: 'Menu Items',
            passed: menuItems.length > 0,
            details: `Found ${menuItems.length} menu items`
        });

        // Test taskbar navigation
        const taskbarNav = document.querySelector('.taskbar-nav');
        if (taskbarNav) {
            const isVisible = taskbarNav.offsetWidth > 0;
            tests.push({
                name: 'Taskbar Navigation',
                passed: isVisible,
                details: `Taskbar nav visible: ${isVisible}`
            });
        }

        // Test responsive behavior
        const isMobile = window.innerWidth <= 768;
        const expectedMobileBehavior = isMobile ?
            sidebar && sidebar.style.flexDirection === 'row' :
            sidebar && sidebar.style.flexDirection !== 'row';

        tests.push({
            name: 'Responsive Layout',
            passed: expectedMobileBehavior,
            details: `Mobile: ${isMobile}, Layout correct: ${expectedMobileBehavior}`
        });

        return tests;
    }

    // Generate test report
    generateReport() {
        const tests = this.testNavigation();
        const passed = tests.filter(t => t.passed).length;
        const total = tests.length;

        console.group('🔍 Responsive Navigation Test Report');
        console.log(`Screen: ${window.innerWidth}x${window.innerHeight}`);
        console.log(`Tests Passed: ${passed}/${total}`);

        tests.forEach(test => {
            const icon = test.passed ? '✅' : '❌';
            console.log(`${icon} ${test.name}: ${test.details}`);
        });

        console.groupEnd();

        return {
            passed,
            total,
            tests,
            screenSize: `${window.innerWidth}x${window.innerHeight}`
        };
    }
}

// Initialize responsive tester when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.responsiveTester = new ResponsiveTester();
    window.responsiveTester.init();

    // Add global function for manual testing
    window.testResponsive = () => window.responsiveTester.generateReport();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResponsiveTester;
}
