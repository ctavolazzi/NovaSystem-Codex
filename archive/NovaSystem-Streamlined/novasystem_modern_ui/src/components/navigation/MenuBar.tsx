'use client';

import React, { useState, useEffect } from 'react';
import { useNavigation } from './NavigationProvider';
import { cn } from '@/lib/utils';

interface MenuBarProps {
  className?: string;
}

export const MenuBar: React.FC<MenuBarProps> = ({ className }) => {
  const { currentPage, navigationConfig } = useNavigation();
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  const [hoverTimeout, setHoverTimeout] = useState<NodeJS.Timeout | null>(null);

  const getCurrentPageTitle = () => {
    const allItems = [
      ...navigationConfig.main,
      ...navigationConfig.tools,
      ...navigationConfig.sessions
    ];
    const currentItem = allItems.find(item => item.id === currentPage);
    return currentItem?.label || 'NovaSystem';
  };

  const handleDropdownToggle = (menuName: string) => {
    setActiveDropdown(activeDropdown === menuName ? null : menuName);
  };

  const handleDropdownClose = () => {
    setActiveDropdown(null);
  };

  const handleMouseEnter = (menuName: string) => {
    // Clear any existing timeout
    if (hoverTimeout) {
      clearTimeout(hoverTimeout);
    }

    // Set a new timeout to open dropdown after 2 seconds
    const timeout = setTimeout(() => {
      setActiveDropdown(menuName);
    }, 2000);

    setHoverTimeout(timeout);
  };

  const handleMouseLeave = () => {
    // Clear timeout when mouse leaves
    if (hoverTimeout) {
      clearTimeout(hoverTimeout);
      setHoverTimeout(null);
    }
  };

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (activeDropdown) {
        const target = event.target as HTMLElement;
        if (!target.closest('.menu-item-container')) {
          setActiveDropdown(null);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [activeDropdown]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (hoverTimeout) {
        clearTimeout(hoverTimeout);
      }
    };
  }, [hoverTimeout]);

  return (
    <div className={cn(
      "xp-menubar",
      "relative z-[var(--z-index-menubar)]",
      className
    )}>
      <div className="flex items-center gap-6">
        {/* File Menu */}
        <div
          className="relative menu-item-container"
          onMouseEnter={() => handleMouseEnter('file')}
          onMouseLeave={handleMouseLeave}
        >
          <button
            className={cn(
              "xp-menu-item",
              activeDropdown === 'file' && "bg-[var(--primary-blue)] text-white"
            )}
            onClick={() => handleDropdownToggle('file')}
          >
            File
          </button>
          <div className={cn(
            "dropdown-menu",
            activeDropdown === 'file' && "open"
          )}>
            <button className="dropdown-item">
              New Session
            </button>
            <button className="dropdown-item">
              Save Session
            </button>
            <button className="dropdown-item">
              Export Data
            </button>
            <div className="dropdown-divider"></div>
            <button className="dropdown-item">
              Exit
            </button>
          </div>
        </div>

        {/* Edit Menu */}
        <div
          className="relative menu-item-container"
          onMouseEnter={() => handleMouseEnter('edit')}
          onMouseLeave={handleMouseLeave}
        >
          <button
            className={cn(
              "xp-menu-item",
              activeDropdown === 'edit' && "bg-[var(--primary-blue)] text-white"
            )}
            onClick={() => handleDropdownToggle('edit')}
          >
            Edit
          </button>
          <div className={cn(
            "dropdown-menu",
            activeDropdown === 'edit' && "open"
          )}>
            <button className="dropdown-item">
              Undo
            </button>
            <button className="dropdown-item">
              Redo
            </button>
            <div className="dropdown-divider"></div>
            <button className="dropdown-item">
              Clear
            </button>
          </div>
        </div>

        {/* View Menu */}
        <div
          className="relative menu-item-container"
          onMouseEnter={() => handleMouseEnter('view')}
          onMouseLeave={handleMouseLeave}
        >
          <button
            className={cn(
              "xp-menu-item",
              activeDropdown === 'view' && "bg-[var(--primary-blue)] text-white"
            )}
            onClick={() => handleDropdownToggle('view')}
          >
            View
          </button>
          <div className={cn(
            "dropdown-menu",
            activeDropdown === 'view' && "open"
          )}>
            <button className="dropdown-item">
              Refresh
            </button>
            <button className="dropdown-item">
              Full Screen
            </button>
            <div className="dropdown-divider"></div>
            <button className="dropdown-item">
              Zoom In
            </button>
            <button className="dropdown-item">
              Zoom Out
            </button>
          </div>
        </div>

        {/* Tools Menu */}
        <div
          className="relative menu-item-container"
          onMouseEnter={() => handleMouseEnter('tools')}
          onMouseLeave={handleMouseLeave}
        >
          <button
            className={cn(
              "xp-menu-item",
              activeDropdown === 'tools' && "bg-[var(--primary-blue)] text-white"
            )}
            onClick={() => handleDropdownToggle('tools')}
          >
            Tools
          </button>
          <div className={cn(
            "dropdown-menu",
            activeDropdown === 'tools' && "open"
          )}>
            <button className="dropdown-item">
              Session Manager
            </button>
            <button className="dropdown-item">
              Analytics
            </button>
            <button className="dropdown-item">
              Monitor
            </button>
            <div className="dropdown-divider"></div>
            <button className="dropdown-item">
              Settings
            </button>
          </div>
        </div>

        {/* Help Menu */}
        <div
          className="relative menu-item-container"
          onMouseEnter={() => handleMouseEnter('help')}
          onMouseLeave={handleMouseLeave}
        >
          <button
            className={cn(
              "xp-menu-item",
              activeDropdown === 'help' && "bg-[var(--primary-blue)] text-white"
            )}
            onClick={() => handleDropdownToggle('help')}
          >
            Help
          </button>
          <div className={cn(
            "dropdown-menu",
            activeDropdown === 'help' && "open"
          )}>
            <button className="dropdown-item">
              Help Topics
            </button>
            <button className="dropdown-item">
              Keyboard Shortcuts
            </button>
            <div className="dropdown-divider"></div>
            <button className="dropdown-item">
              About NovaSystem
            </button>
          </div>
        </div>
      </div>

      {/* Page Title */}
      <div className="ml-auto text-[var(--text-primary)] font-bold">
        {getCurrentPageTitle()}
      </div>
    </div>
  );
};
