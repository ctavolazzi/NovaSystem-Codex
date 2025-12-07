'use client';

import React, { useState, useEffect } from 'react';
import { useNavigation } from './NavigationProvider';
import { cn } from '@/lib/utils';

interface TaskbarProps {
  className?: string;
}

export const Taskbar: React.FC<TaskbarProps> = ({ className }) => {
  const { navigationConfig, isMobile } = useNavigation();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showStartMenu, setShowStartMenu] = useState(false);

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Close start menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (showStartMenu) {
        const target = event.target as HTMLElement;
        if (!target.closest('.start-menu-container')) {
          setShowStartMenu(false);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showStartMenu]);

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString([], {
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className={cn(
      "bg-gradient-to-b from-[var(--bg-secondary)] to-[#d6d3ce] border-t border-[var(--border-3d-dark)] shadow-inner",
      "flex items-center justify-between px-2",
      "relative z-[var(--z-index-taskbar)]",
      isMobile
        ? "relative h-12 flex-wrap gap-2"
        : "absolute bottom-0 left-0 right-0 h-10",
      className
    )}>
      {/* Start Button */}
      <div className="relative start-menu-container">
        <button
          onClick={() => setShowStartMenu(!showStartMenu)}
          className={cn(
            "xp-button flex items-center text-[var(--text-primary)] cursor-pointer",
            "bg-gradient-to-b from-[var(--bg-primary)] to-[var(--bg-secondary)]",
            "hover:bg-gradient-to-b hover:from-[var(--bg-hover)] hover:to-[var(--bg-secondary)]",
            showStartMenu && "bg-gradient-to-b from-[var(--primary-blue)] to-[var(--primary-blue-hover)] text-white",
            isMobile
              ? "gap-1 px-2 py-1.5 text-[10px] min-h-[32px]"
              : "gap-1.5 px-3 py-1.5 text-xs min-h-[32px]"
          )}
        >
          <div className={cn(
            "bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm",
            isMobile ? "w-3 h-3" : "w-4 h-4"
          )} />
          {!isMobile && <span>Start</span>}
        </button>

        {/* Start Menu */}
        {showStartMenu && (
          <div className="absolute bottom-full left-0 mb-2 bg-[var(--bg-primary)] border border-[var(--border-light)] shadow-lg z-[var(--z-index-taskbar-dropdown)] min-w-48 rounded-md">
            <div className="p-2">
              <div className="text-xs font-bold text-[var(--text-primary)] mb-2">NovaSystem v3.0</div>
              <div className="space-y-0.5">
                {navigationConfig.main.slice(0, 4).map((item) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      window.location.href = item.url;
                      setShowStartMenu(false);
                    }}
                    className="w-full px-3 py-2 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-blue)] hover:text-white cursor-pointer flex items-center gap-2 rounded-sm transition-colors"
                  >
                    <span className="text-sm">{item.icon}</span>
                    <span>{item.label}</span>
                  </button>
                ))}
              </div>
              <div className="border-t border-[var(--border-inset)] my-1"></div>
              <div className="space-y-0.5">
                <button
                  onClick={() => {
                    window.location.href = '/settings';
                    setShowStartMenu(false);
                  }}
                  className="w-full px-2 py-1.5 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-color)] hover:text-white cursor-pointer flex items-center gap-2"
                >
                  <span>⚙️</span>
                  <span>Settings</span>
                </button>
                <button
                  onClick={() => {
                    window.location.href = '/help';
                    setShowStartMenu(false);
                  }}
                  className="w-full px-2 py-1.5 text-left text-xs text-[var(--text-primary)] hover:bg-[var(--primary-color)] hover:text-white cursor-pointer flex items-center gap-2"
                >
                  <span>❓</span>
                  <span>Help</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Taskbar Navigation (Mobile) */}
      {isMobile && (
        <div className="flex gap-1 ml-2">
          {navigationConfig.main.map((item) => (
            <button
              key={item.id}
              onClick={() => window.location.href = item.url}
              className="flex items-center gap-1 px-2 py-1 text-xs text-[var(--text-primary)] cursor-pointer bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)] hover:bg-gradient-to-b hover:from-[#f0f0f0] hover:to-[#e0ddd8]"
            >
              <span className="text-xs">{item.icon}</span>
            </button>
          ))}
        </div>
      )}

      {/* System Tray */}
      <div className="flex items-center gap-1 ml-auto">
        {/* Status Indicator */}
        <div className="flex items-center gap-1 px-2 py-1 bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)]">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-xs text-[var(--text-primary)]">Ready</span>
        </div>

        {/* Date and Time */}
        <div className="px-2 py-1 bg-gradient-to-b from-[var(--bg-tertiary)] to-[#d6d3ce] border border-[var(--border-inset)] text-xs text-[var(--text-primary)] cursor-pointer hover:bg-gradient-to-b hover:from-[#f0f0f0] hover:to-[#e0ddd8]">
          <div className="text-center">
            <div className="font-bold">{formatTime(currentTime)}</div>
            <div className="text-[10px]">{formatDate(currentTime)}</div>
          </div>
        </div>
      </div>
    </div>
  );
};
