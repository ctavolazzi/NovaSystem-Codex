'use client';

import React from 'react';
import Link from 'next/link';
import { useNavigation } from './NavigationProvider';
import { cn } from '@/lib/utils';

interface SidebarProps {
  className?: string;
  children?: React.ReactNode;
}

export const Sidebar: React.FC<SidebarProps> = ({ className, children }) => {
  const { currentPage, isMobile, navigationConfig } = useNavigation();

  return (
    <div className={cn(
      "xp-sidebar xp-scrollbar flex",
      isMobile
        ? "w-full h-auto flex-row overflow-x-auto overflow-y-hidden border-b border-r-0 nav-mobile"
        : "w-50 h-full flex-col border-r",
      className
    )}>
      {/* Navigation Section */}
      <div className={cn(
        "border-[var(--border-light)] flex-shrink-0",
        isMobile
          ? "min-w-32 max-w-40 p-1 border-r border-b-0"
          : "w-full p-2 border-b"
      )}>
        <div className="xp-sidebar-section-title sm:hidden lg:block">
          Navigation
        </div>
            <div className={cn(
              isMobile ? "flex gap-2" : "space-y-1"
            )}>
              {navigationConfig.main.map((item) => (
                <Link
                  key={item.id}
                  href={item.url}
                  className={cn(
                    "xp-sidebar-item",
                    isMobile
                      ? "px-2 py-2 text-[10px] flex-col gap-1 min-w-[48px] nav-mobile-item"
                      : "px-3 py-2 text-xs gap-2",
                    currentPage === item.id && "active"
                  )}
                >
                  <div className={cn(
                    "bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-white",
                    isMobile ? "w-4 h-4 text-[10px]" : "w-5 h-5 text-xs"
                  )}>
                    {item.icon}
                  </div>
                  {!isMobile && <span>{item.label}</span>}
                </Link>
              ))}
            </div>
      </div>

      {/* Sessions Section (Desktop only) */}
      {!isMobile && ['workflow', 'home', 'active_sessions', 'session_history'].includes(currentPage) && (
        <div className="p-2 border-b border-[var(--border-light)] sm:hidden lg:block">
          <div className="text-xs font-bold text-[var(--text-primary)] mb-2 px-1">
            Sessions
          </div>
              <div className="space-y-1">
                {navigationConfig.sessions.map((item) => (
                  <Link
                    key={item.id}
                    href={item.url}
                    className={cn(
                      "xp-sidebar-item px-3 py-2 text-xs gap-2",
                      currentPage === item.id && "active"
                    )}
                  >
                    <div className="w-5 h-5 bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-xs text-white">
                      {item.icon}
                    </div>
                    <span>{item.label}</span>
                  </Link>
                ))}
              </div>
        </div>
      )}

      {/* Tools Section */}
      <div className={cn(
        "p-2 border-b border-[var(--border-light)]",
        isMobile ? "min-w-50 border-r border-b-0 mr-2" : "border-b"
      )}>
        <div className="xp-sidebar-section-title sm:hidden lg:block">
          Tools
        </div>
            <div className={cn(
              isMobile ? "flex gap-2" : "space-y-1"
            )}>
              {navigationConfig.tools.map((item) => (
                <Link
                  key={item.id}
                  href={item.url}
                  className={cn(
                    "xp-sidebar-item",
                    isMobile
                      ? "px-2 py-2 text-[10px] flex-col gap-1 min-w-[48px] nav-mobile-item"
                      : "px-3 py-2 text-xs gap-2",
                    currentPage === item.id && "active"
                  )}
                >
                  <div className={cn(
                    "bg-[var(--primary-blue)] rounded-sm flex items-center justify-center text-white",
                    isMobile ? "w-4 h-4 text-[10px]" : "w-5 h-5 text-xs"
                  )}>
                    {item.icon}
                  </div>
                  {!isMobile && <span>{item.label}</span>}
                </Link>
              ))}
            </div>
      </div>

      {/* Page-specific sidebar content */}
      {children && (
        <div className="flex-1 p-2">
          {children}
        </div>
      )}

      {/* Mobile Quick Actions */}
      {isMobile && (
        <div className="min-w-50 p-2">
          <div className="xp-sidebar-section-title">
            Quick Actions
          </div>
          <div className="space-y-0.5">
            <button className="xp-button w-full justify-start">
              <span>🔄</span>
              <span>Refresh</span>
            </button>
            <button className="xp-button w-full justify-start">
              <span>⛶</span>
              <span>Fullscreen</span>
            </button>
            <button className="xp-button w-full justify-start">
              <span>⚙️</span>
              <span>Settings</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
