'use client';

import React from 'react';
import { NavigationProvider } from '../navigation/NavigationProvider';
import { StreamingProvider } from '../streaming/SimpleStreamingProvider';
import { Sidebar } from '../navigation/Sidebar';
import { MenuBar } from '../navigation/MenuBar';
import { Taskbar } from '../navigation/Taskbar';
import { Window } from '../ui/Window';
import { ResponsiveTest } from '../ResponsiveTest';
import { cn } from '@/lib/utils';

interface MainLayoutProps {
  children: React.ReactNode;
  title?: string;
  icon?: React.ReactNode;
  sidebarContent?: React.ReactNode;
  className?: string;
}

export const MainLayout: React.FC<MainLayoutProps> = ({
  children,
  title = 'NovaSystem',
  icon,
  sidebarContent,
  className
}) => {
  return (
    <NavigationProvider>
      <StreamingProvider>
        <div className="h-screen w-screen overflow-hidden bg-[var(--bg-primary)] relative safe-area-all">
          <Window
            title={title}
            icon={icon}
            className={cn("relative responsive-spacing", className)}
          >
            <div className="flex flex-col h-full responsive-padding">
              {/* Menu Bar */}
              <MenuBar />

              {/* Main Content Area */}
              <div className="flex flex-1 overflow-hidden responsive-spacing sm:flex-col lg:flex-row">
                {/* Sidebar */}
                <Sidebar>
                  {sidebarContent}
                </Sidebar>

                {/* Main Content */}
                <div className="flex-1 bg-[var(--bg-primary)] overflow-auto responsive-padding container-padding content-mobile">
                  {children}
                </div>
              </div>
            </div>
          </Window>

          {/* Taskbar */}
          <Taskbar />

          {/* Responsive Test Tool */}
          <ResponsiveTest />
        </div>
      </StreamingProvider>
    </NavigationProvider>
  );
};
