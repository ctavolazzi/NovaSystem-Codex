/**
 * Unified Navigation System for NovaSystem
 * Single source of truth for navigation across all pages
 */

class UnifiedNavigation {
    constructor() {
        this.currentPage = this.detectCurrentPage();
        this.isMobile = window.innerWidth <= 768;
        this.isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;
        this.sidebarOpen = false;

        this.navigationConfig = {
            main: [
                { id: 'home', label: 'Home', url: '/', icon: '🏠' },
                { id: 'workflow', label: 'Workflow', url: '/workflow', icon: '⚡' },
                { id: 'analytics', label: 'Analytics', url: '/analytics', icon: '📊' },
                { id: 'monitor', label: 'Monitor', url: '/monitor', icon: '📈' }
            ],
            tools: [
                { id: 'settings', label: 'Settings', url: '/settings', icon: '⚙️' },
                { id: 'help', label: 'Help', url: '/help', icon: '❓' },
                { id: 'about', label: 'About', url: '/about', icon: 'ℹ️' }
            ],
            sessions: [
                { id: 'active_sessions', label: 'Active Sessions', url: '/sessions', icon: '🔄' },
                { id: 'session_history', label: 'History', url: '/history', icon: '📋' }
            ]
        };

        this.init();
        this.setupResponsiveHandlers();
    }

    detectCurrentPage() {
        const path = window.location.pathname;
        if (path === '/') return 'home';
        if (path === '/workflow') return 'workflow';
        if (path === '/analytics') return 'analytics';
        if (path === '/monitor') return 'monitor';
        if (path === '/settings') return 'settings';
        if (path === '/help') return 'help';
        if (path === '/about') return 'about';
        if (path === '/sessions') return 'active_sessions';
        if (path === '/history') return 'session_history';
        return 'home';
    }

    init() {
        this.renderNavigation();
        this.setupEventListeners();
        this.updateActiveState();
    }

    renderNavigation() {
        // Create unified menu bar
        this.renderMenuBar();

        // Create unified sidebar navigation
        this.renderSidebar();

        // Create unified taskbar navigation
        this.renderTaskbar();
    }

    renderMenuBar() {
        const menuBar = document.querySelector('.menu-bar');
        if (!menuBar) return;

        // Clear existing menu items
        menuBar.innerHTML = '';

        // File menu
        const fileMenu = this.createMenuDropdown('File', [
            { label: 'New Session', action: () => this.startNewSession() },
            { label: 'Open Workflow', action: () => this.openWorkflow() },
            { separator: true },
            { label: 'Export Results', action: () => this.exportResults() },
            { label: 'Import Configuration', action: () => this.importConfig() }
        ]);

        // Edit menu
        const editMenu = this.createMenuDropdown('Edit', [
            { label: 'Cut', action: () => this.editAction('cut') },
            { label: 'Copy', action: () => this.editAction('copy') },
            { label: 'Paste', action: () => this.editAction('paste') },
            { separator: true },
            { label: 'Preferences', action: () => this.showPreferences() }
        ]);

        // View menu
        const viewMenu = this.createMenuDropdown('View', [
            { label: 'Home', action: () => this.navigateTo('/') },
            { label: 'Workflow', action: () => this.navigateTo('/workflow') },
            { label: 'Analytics', action: () => this.navigateTo('/analytics') },
            { label: 'Monitor', action: () => this.navigateTo('/monitor') },
            { separator: true },
            { label: 'Refresh', action: () => this.refreshPage() },
            { label: 'Full Screen', action: () => this.toggleFullscreen() }
        ]);

        // Tools menu
        const toolsMenu = this.createMenuDropdown('Tools', [
            { label: 'Session Manager', action: () => this.showSessionManager() },
            { label: 'Performance Monitor', action: () => this.navigateTo('/monitor') },
            { label: 'Analytics Dashboard', action: () => this.navigateTo('/analytics') },
            { separator: true },
            { label: 'Kill All Sessions', action: () => this.killAllSessions() },
            { label: 'System Diagnostics', action: () => this.runDiagnostics() }
        ]);

        // Help menu
        const helpMenu = this.createMenuDropdown('Help', [
            { label: 'Documentation', action: () => this.showDocumentation() },
            { label: 'Keyboard Shortcuts', action: () => this.showShortcuts() },
            { separator: true },
            { label: 'About NovaSystem', action: () => this.showAbout() },
            { label: 'Report Issue', action: () => this.reportIssue() }
        ]);

        menuBar.appendChild(fileMenu);
        menuBar.appendChild(editMenu);
        menuBar.appendChild(viewMenu);
        menuBar.appendChild(toolsMenu);
        menuBar.appendChild(helpMenu);
    }

    createMenuDropdown(label, items) {
        const menuItem = document.createElement('div');
        menuItem.className = 'menu-item';
        menuItem.textContent = label;

        // Create dropdown menu
        const dropdown = document.createElement('div');
        dropdown.className = 'menu-dropdown';
        dropdown.style.display = 'none';

        items.forEach(item => {
            if (item.separator) {
                const separator = document.createElement('div');
                separator.className = 'menu-separator';
                dropdown.appendChild(separator);
            } else {
                const menuOption = document.createElement('div');
                menuOption.className = 'menu-option';
                menuOption.textContent = item.label;
                menuOption.addEventListener('click', item.action);
                dropdown.appendChild(menuOption);
            }
        });

        menuItem.appendChild(dropdown);

        // Show/hide dropdown on hover
        menuItem.addEventListener('mouseenter', () => {
            dropdown.style.display = 'block';
        });

        menuItem.addEventListener('mouseleave', () => {
            dropdown.style.display = 'none';
        });

        return menuItem;
    }

    renderSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (!sidebar) return;

        // Clear existing sidebar content
        sidebar.innerHTML = '';

        // Add responsive class
        if (this.isMobile) {
            sidebar.classList.add('mobile-sidebar');
        } else {
            sidebar.classList.remove('mobile-sidebar');
        }

        // Main navigation section
        const mainSection = this.createSidebarSection('Navigation', this.navigationConfig.main);
        sidebar.appendChild(mainSection);

        // Sessions section (if applicable and not mobile)
        if (!this.isMobile && (this.currentPage === 'workflow' || this.currentPage === 'home')) {
            const sessionsSection = this.createSidebarSection('Sessions', this.navigationConfig.sessions);
            sidebar.appendChild(sessionsSection);
        }

        // Tools section
        const toolsSection = this.createSidebarSection('Tools', this.navigationConfig.tools);
        sidebar.appendChild(toolsSection);

        // Page-specific content
        this.renderPageSpecificSidebar(sidebar);

        // Add mobile-specific elements
        if (this.isMobile) {
            this.addMobileSidebarElements(sidebar);
        }
    }

    addMobileSidebarElements(sidebar) {
        // Add a quick navigation section for mobile
        const quickNavSection = document.createElement('div');
        quickNavSection.className = 'sidebar-section mobile-quick-nav';

        const quickNavTitle = document.createElement('div');
        quickNavTitle.className = 'sidebar-title';
        quickNavTitle.textContent = 'Quick Actions';
        quickNavSection.appendChild(quickNavTitle);

        // Add quick action buttons
        const quickActions = [
            { label: 'Refresh', icon: '🔄', action: () => this.refreshPage() },
            { label: 'Fullscreen', icon: '⛶', action: () => this.toggleFullscreen() },
            { label: 'Settings', icon: '⚙️', action: () => this.showPreferences() }
        ];

        quickActions.forEach(action => {
            const actionItem = document.createElement('div');
            actionItem.className = 'sidebar-item quick-action';
            actionItem.innerHTML = `<span style="margin-right: 8px;">${action.icon}</span><span>${action.label}</span>`;
            actionItem.addEventListener('click', action.action);
            quickNavSection.appendChild(actionItem);
        });

        sidebar.appendChild(quickNavSection);
    }

    createSidebarSection(title, items) {
        const section = document.createElement('div');
        section.className = 'sidebar-section';

        const sectionTitle = document.createElement('div');
        sectionTitle.className = 'sidebar-title';
        sectionTitle.textContent = title;
        section.appendChild(sectionTitle);

        items.forEach(item => {
            const sidebarItem = document.createElement('div');
            sidebarItem.className = 'sidebar-item';
            sidebarItem.setAttribute('data-nav-id', item.id);

            const icon = document.createElement('span');
            icon.textContent = item.icon;
            icon.style.marginRight = '8px';

            const label = document.createElement('span');
            label.textContent = item.label;

            sidebarItem.appendChild(icon);
            sidebarItem.appendChild(label);

            // Handle navigation
            if (item.url.startsWith('/')) {
                sidebarItem.addEventListener('click', () => this.navigateTo(item.url));
            } else {
                sidebarItem.addEventListener('click', () => this.handleAction(item.id));
            }

            section.appendChild(sidebarItem);
        });

        return section;
    }

    renderPageSpecificSidebar(sidebar) {
        switch (this.currentPage) {
            case 'home':
                this.renderHomeSidebar(sidebar);
                break;
            case 'workflow':
                this.renderWorkflowSidebar(sidebar);
                break;
            case 'analytics':
                this.renderAnalyticsSidebar(sidebar);
                break;
            case 'monitor':
                this.renderMonitorSidebar(sidebar);
                break;
        }
    }

    renderHomeSidebar(sidebar) {
        const recentSection = document.createElement('div');
        recentSection.className = 'sidebar-section';

        const recentTitle = document.createElement('div');
        recentTitle.className = 'sidebar-title';
        recentTitle.textContent = 'Recent Chats';
        recentSection.appendChild(recentTitle);

        // Add recent chat items (placeholder)
        const recentItems = [
            { label: 'Marketing Strategy', icon: '💼' },
            { label: 'Code Help', icon: '💻' },
            { label: 'Data Analysis', icon: '📈' }
        ];

        recentItems.forEach(item => {
            const sidebarItem = document.createElement('div');
            sidebarItem.className = 'sidebar-item';
            sidebarItem.innerHTML = `<span style="margin-right: 8px;">${item.icon}</span><span>${item.label}</span>`;
            recentSection.appendChild(sidebarItem);
        });

        sidebar.appendChild(recentSection);
    }

    renderWorkflowSidebar(sidebar) {
        // Workflow-specific sidebar content is handled by the workflow page itself
        // This ensures the workflow functionality remains intact
        return;
    }

    renderAnalyticsSidebar(sidebar) {
        const analyticsSection = document.createElement('div');
        analyticsSection.className = 'sidebar-section';

        const analyticsTitle = document.createElement('div');
        analyticsTitle.className = 'sidebar-title';
        analyticsTitle.textContent = 'Analytics Tools';
        analyticsSection.appendChild(analyticsTitle);

        const analyticsItems = [
            { label: 'Performance Metrics', icon: '📊' },
            { label: 'Usage Statistics', icon: '📈' },
            { label: 'Error Reports', icon: '⚠️' },
            { label: 'Export Data', icon: '💾' }
        ];

        analyticsItems.forEach(item => {
            const sidebarItem = document.createElement('div');
            sidebarItem.className = 'sidebar-item';
            sidebarItem.innerHTML = `<span style="margin-right: 8px;">${item.icon}</span><span>${item.label}</span>`;
            analyticsSection.appendChild(sidebarItem);
        });

        sidebar.appendChild(analyticsSection);
    }

    renderMonitorSidebar(sidebar) {
        const monitorSection = document.createElement('div');
        monitorSection.className = 'sidebar-section';

        const monitorTitle = document.createElement('div');
        monitorTitle.className = 'sidebar-title';
        monitorTitle.textContent = 'Monitor Tools';
        monitorSection.appendChild(monitorTitle);

        const monitorItems = [
            { label: 'Real-time Metrics', icon: '⚡' },
            { label: 'System Health', icon: '💚' },
            { label: 'Alert Center', icon: '🚨' },
            { label: 'Log Viewer', icon: '📋' }
        ];

        monitorItems.forEach(item => {
            const sidebarItem = document.createElement('div');
            sidebarItem.className = 'sidebar-item';
            sidebarItem.innerHTML = `<span style="margin-right: 8px;">${item.icon}</span><span>${item.label}</span>`;
            monitorSection.appendChild(sidebarItem);
        });

        sidebar.appendChild(monitorSection);
    }

    renderTaskbar() {
        const taskbar = document.querySelector('.windows-taskbar');
        if (!taskbar) return;

        // Add navigation buttons to taskbar
        const navButtons = document.createElement('div');
        navButtons.className = 'taskbar-nav';
        navButtons.style.display = 'flex';
        navButtons.style.gap = '4px';

        this.navigationConfig.main.forEach(item => {
            const button = document.createElement('button');
            button.className = 'taskbar-nav-btn';
            button.textContent = item.icon;
            button.title = item.label;
            button.addEventListener('click', () => this.navigateTo(item.url));

            // Add active state
            if (item.id === this.currentPage) {
                button.classList.add('active');
            }

            navButtons.appendChild(button);
        });

        // Insert before the time display
        const timeDisplay = taskbar.querySelector('.taskbar-time');
        if (timeDisplay) {
            taskbar.insertBefore(navButtons, timeDisplay);
        }
    }

    setupEventListeners() {
        // Global keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case '1':
                        e.preventDefault();
                        this.navigateTo('/');
                        break;
                    case '2':
                        e.preventDefault();
                        this.navigateTo('/workflow');
                        break;
                    case '3':
                        e.preventDefault();
                        this.navigateTo('/analytics');
                        break;
                    case '4':
                        e.preventDefault();
                        this.navigateTo('/monitor');
                        break;
                }
            }
        });

        // Touch/swipe gestures for mobile
        if (this.isMobile) {
            this.setupTouchGestures();
        }

        // Click outside to close dropdowns
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.menu-item') && !e.target.closest('.menu-dropdown')) {
                this.closeAllDropdowns();
            }
        });
    }

    setupResponsiveHandlers() {
        // Handle window resize
        window.addEventListener('resize', () => {
            const wasMobile = this.isMobile;
            const wasTablet = this.isTablet;

            this.isMobile = window.innerWidth <= 768;
            this.isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;

            // Re-render navigation if breakpoint changed
            if (wasMobile !== this.isMobile || wasTablet !== this.isTablet) {
                this.renderNavigation();
                this.updateActiveState();
            }
        });

        // Handle orientation change on mobile
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.isMobile = window.innerWidth <= 768;
                this.isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;
                this.renderNavigation();
                this.updateActiveState();
            }, 100);
        });
    }

    setupTouchGestures() {
        let startX = 0;
        let startY = 0;
        let isDragging = false;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
            isDragging = false;
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            if (!startX || !startY) return;

            const currentX = e.touches[0].clientX;
            const currentY = e.touches[0].clientY;
            const diffX = startX - currentX;
            const diffY = startY - currentY;

            // Check if horizontal swipe
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                isDragging = true;

                // Swipe left to go to next page
                if (diffX > 0) {
                    this.swipeToNextPage();
                }
                // Swipe right to go to previous page
                else {
                    this.swipeToPreviousPage();
                }

                startX = 0;
                startY = 0;
            }
        }, { passive: true });

        document.addEventListener('touchend', () => {
            startX = 0;
            startY = 0;
            isDragging = false;
        }, { passive: true });
    }

    swipeToNextPage() {
        const pages = this.navigationConfig.main;
        const currentIndex = pages.findIndex(page => page.id === this.currentPage);
        const nextIndex = (currentIndex + 1) % pages.length;
        this.navigateTo(pages[nextIndex].url);
    }

    swipeToPreviousPage() {
        const pages = this.navigationConfig.main;
        const currentIndex = pages.findIndex(page => page.id === this.currentPage);
        const prevIndex = currentIndex === 0 ? pages.length - 1 : currentIndex - 1;
        this.navigateTo(pages[prevIndex].url);
    }

    closeAllDropdowns() {
        document.querySelectorAll('.menu-dropdown').forEach(dropdown => {
            dropdown.style.display = 'none';
        });
    }

    updateActiveState() {
        // Update sidebar active states
        document.querySelectorAll('.sidebar-item').forEach(item => {
            const navId = item.getAttribute('data-nav-id');
            if (navId === this.currentPage) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });

        // Update taskbar active states
        document.querySelectorAll('.taskbar-nav-btn').forEach(btn => {
            const navId = btn.getAttribute('data-nav-id');
            if (navId === this.currentPage) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // Navigation methods
    navigateTo(url) {
        if (url.startsWith('/')) {
            window.location.href = url;
        } else {
            console.log('Navigation to:', url);
        }
    }

    // Action handlers
    handleAction(actionId) {
        switch (actionId) {
            case 'settings':
                this.showPreferences();
                break;
            case 'help':
                this.showDocumentation();
                break;
            case 'about':
                this.showAbout();
                break;
            case 'active_sessions':
                this.showSessionManager();
                break;
            case 'session_history':
                this.showSessionHistory();
                break;
        }
    }

    // Menu action implementations
    startNewSession() {
        if (this.currentPage === 'workflow') {
            // Reset workflow
            if (window.workflowEngine) {
                window.workflowEngine.resetWorkflow();
            }
        } else {
            // Start new chat session
            this.navigateTo('/');
        }
    }

    openWorkflow() {
        this.navigateTo('/workflow');
    }

    exportResults() {
        console.log('Exporting results...');
        // Implementation for exporting results
    }

    importConfig() {
        console.log('Importing configuration...');
        // Implementation for importing configuration
    }

    editAction(action) {
        console.log('Edit action:', action);
        // Implementation for edit actions
    }

    showPreferences() {
        console.log('Showing preferences...');
        // Implementation for preferences dialog
    }

    refreshPage() {
        window.location.reload();
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    showSessionManager() {
        console.log('Showing session manager...');
        // Implementation for session manager
    }

    killAllSessions() {
        if (confirm('Are you sure you want to kill all active sessions?')) {
            fetch('/api/sessions/kill-all', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert(`Killed ${data.killed_count} sessions`);
                })
                .catch(error => {
                    console.error('Error killing sessions:', error);
                    alert('Failed to kill sessions');
                });
        }
    }

    runDiagnostics() {
        console.log('Running system diagnostics...');
        // Implementation for system diagnostics
    }

    showDocumentation() {
        window.open('/docs', '_blank');
    }

    showShortcuts() {
        alert('Keyboard Shortcuts:\n\nCtrl+1: Home\nCtrl+2: Workflow\nCtrl+3: Analytics\nCtrl+4: Monitor\n\nF11: Toggle Fullscreen');
    }

    showAbout() {
        alert('NovaSystem v3.0\nAdvanced AI Problem-Solving Framework\n\nBuilt with ❤️ for intelligent automation');
    }

    reportIssue() {
        window.open('https://github.com/your-repo/issues', '_blank');
    }

    showSessionHistory() {
        console.log('Showing session history...');
        // Implementation for session history
    }
}

// Initialize navigation when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.unifiedNavigation = new UnifiedNavigation();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UnifiedNavigation;
}
