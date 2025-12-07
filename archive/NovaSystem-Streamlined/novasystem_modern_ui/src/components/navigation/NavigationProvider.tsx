'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';

// Navigation configuration - single source of truth
export const NAVIGATION_CONFIG = {
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
} as const;

interface NavigationContextType {
  currentPage: string;
  isMobile: boolean;
  isTablet: boolean;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  navigationConfig: typeof NAVIGATION_CONFIG;
  navigateToPage: (url: string) => void;
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

export const useNavigation = () => {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error('useNavigation must be used within a NavigationProvider');
  }
  return context;
};

interface NavigationProviderProps {
  children: React.ReactNode;
}

export const NavigationProvider: React.FC<NavigationProviderProps> = ({ children }) => {
  const pathname = usePathname();
  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Detect current page
  const detectCurrentPage = (path: string): string => {
    const routeMap: Record<string, string> = {
      '/': 'home',
      '/workflow': 'workflow',
      '/analytics': 'analytics',
      '/monitor': 'monitor',
      '/settings': 'settings',
      '/help': 'help',
      '/about': 'about',
      '/sessions': 'active_sessions',
      '/history': 'session_history'
    };
    return routeMap[path] || 'home';
  };

  const currentPage = detectCurrentPage(pathname);

  // Navigation helper function
  const navigateToPage = (url: string) => {
    if (typeof window !== 'undefined') {
      window.location.href = url;
    }
  };

  // Handle responsive design with comprehensive breakpoints
  useEffect(() => {
    const handleResize = () => {
      if (typeof window !== 'undefined') {
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Enhanced breakpoint detection
        setIsMobile(width <= 767);
        setIsTablet(width > 767 && width <= 1024);

        // Add viewport meta tag if on mobile
        if (width <= 767) {
          const viewport = document.querySelector('meta[name="viewport"]');
          if (!viewport) {
            const meta = document.createElement('meta');
            meta.name = 'viewport';
            meta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
            document.head.appendChild(meta);
          }
        }

        // Handle orientation changes
        if (width <= 767) {
          const isLandscape = width > height;
          document.body.classList.toggle('landscape', isLandscape);
          document.body.classList.toggle('portrait', !isLandscape);
        }
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    window.addEventListener('orientationchange', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('orientationchange', handleResize);
    };
  }, []);

  // Handle orientation change on mobile
  useEffect(() => {
    const handleOrientationChange = () => {
      setTimeout(() => {
        if (typeof window !== 'undefined') {
          const width = window.innerWidth;
          setIsMobile(width <= 768);
          setIsTablet(width > 768 && width <= 1024);
        }
      }, 100);
    };

    window.addEventListener('orientationchange', handleOrientationChange);
    return () => window.removeEventListener('orientationchange', handleOrientationChange);
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
          case '1':
            e.preventDefault();
            navigateToPage('/');
            break;
          case '2':
            e.preventDefault();
            navigateToPage('/workflow');
            break;
          case '3':
            e.preventDefault();
            navigateToPage('/analytics');
            break;
          case '4':
            e.preventDefault();
            navigateToPage('/monitor');
            break;
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Touch gestures for mobile
  useEffect(() => {
    if (!isMobile) return;

    let startX = 0;
    let startY = 0;

    const handleTouchStart = (e: TouchEvent) => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    };

    const handleTouchEnd = (e: TouchEvent) => {
      const endX = e.changedTouches[0].clientX;
      const endY = e.changedTouches[0].clientY;
      const diffX = startX - endX;
      const diffY = startY - endY;

      // Check if horizontal swipe
      if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
        const pages = NAVIGATION_CONFIG.main;
        const currentIndex = pages.findIndex(page => page.id === currentPage);

        if (diffX > 0 && currentIndex < pages.length - 1) {
          // Swipe left - next page
          navigateToPage(pages[currentIndex + 1].url);
        } else if (diffX < 0 && currentIndex > 0) {
          // Swipe right - previous page
          navigateToPage(pages[currentIndex - 1].url);
        }
      }
    };

    document.addEventListener('touchstart', handleTouchStart, { passive: true });
    document.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      document.removeEventListener('touchstart', handleTouchStart);
      document.removeEventListener('touchend', handleTouchEnd);
    };
  }, [isMobile, currentPage]);

  const value: NavigationContextType = {
    currentPage,
    isMobile,
    isTablet,
    sidebarOpen,
    setSidebarOpen,
    navigationConfig: NAVIGATION_CONFIG,
    navigateToPage
  };

  return (
    <NavigationContext.Provider value={value}>
      {children}
    </NavigationContext.Provider>
  );
};
