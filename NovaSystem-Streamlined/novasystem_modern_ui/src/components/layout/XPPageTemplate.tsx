'use client';

import React from 'react';
import { MainLayout } from './MainLayout';
import { XPCard } from '../ui/XPCard';
import { cn } from '@/lib/utils';

interface XPPageTemplateProps {
  title: string;
  icon?: React.ReactNode;
  description?: string;
  sidebarContent?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  loading?: boolean;
  loadingText?: string;
}

export const XPPageTemplate: React.FC<XPPageTemplateProps> = ({
  title,
  icon,
  description,
  sidebarContent,
  children,
  className,
  loading = false,
  loadingText = 'Loading...'
}) => {
  if (loading) {
    return (
      <MainLayout
        title={title}
        icon={icon}
        sidebarContent={sidebarContent}
      >
        <div className="h-full flex items-center justify-center p-4">
          <XPCard className="p-8" variant="outset">
            <div className="text-center">
              <div className="animate-spin w-8 h-8 border-4 border-[#0054e3] border-t-transparent rounded-full mx-auto mb-4"></div>
              <div className="text-black">{loadingText}</div>
            </div>
          </XPCard>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout
      title={title}
      icon={icon}
      sidebarContent={sidebarContent}
    >
      <div className={cn("h-full overflow-auto p-4 space-y-4", className)}>
        {/* Header */}
        <XPCard className="p-4" variant="outset">
          <h1 className="text-xl font-bold text-black mb-2">
            {title}
          </h1>
          {description && (
            <p className="text-sm text-[#666666]">
              {description}
            </p>
          )}
        </XPCard>

        {/* Main Content */}
        {children}
      </div>
    </MainLayout>
  );
};

// Sub-components for common page sections
export const XPSection: React.FC<{
  title: string;
  children: React.ReactNode;
  className?: string;
}> = ({ title, children, className }) => (
  <XPCard className={cn("p-4", className)} variant="outset">
    <XPCard.Header>
      <h2 className="text-lg font-bold text-black">{title}</h2>
    </XPCard.Header>
    <XPCard.Content>
      {children}
    </XPCard.Content>
  </XPCard>
);

export const XPMetricsGrid: React.FC<{
  children: React.ReactNode;
  className?: string;
}> = ({ children, className }) => (
  <div className={cn("grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4", className)}>
    {children}
  </div>
);

export const XPMetricCard: React.FC<{
  title: string;
  value: string | number;
  color?: string;
  children?: React.ReactNode;
}> = ({ title, value, color = "#0054e3", children }) => (
  <XPCard className="p-4" variant="outset">
    <div className="text-2xl font-bold mb-1" style={{ color }}>
      {value}
    </div>
    <div className="text-xs text-[#666666] mb-2">{title}</div>
    {children}
  </XPCard>
);

export const XPProgressBar: React.FC<{
  value: number;
  max?: number;
  color?: string;
  className?: string;
}> = ({ value, max = 100, color = "#6bbf44", className }) => (
  <div className={cn("w-full bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]", className)}>
    <div
      className="h-2 rounded-full"
      style={{
        width: `${Math.min((value / max) * 100, 100)}%`,
        backgroundColor: color
      }}
    ></div>
  </div>
);

export const XPStatusBadge: React.FC<{
  status: string;
  className?: string;
}> = ({ status, className }) => {
  const getStatusStyles = (status: string) => {
    switch (status.toLowerCase()) {
      case 'running':
      case 'active':
        return 'bg-[#e6f3ff] text-[#0054e3]';
      case 'completed':
      case 'success':
      case 'healthy':
        return 'bg-[#e6ffe6] text-[#6bbf44]';
      case 'failed':
      case 'error':
      case 'critical':
        return 'bg-[#ffe6e6] text-[#ff0000]';
      case 'warning':
        return 'bg-[#fff3e6] text-[#ffa500]';
      default:
        return 'bg-[#f0f0f0] text-[#666666]';
    }
  };

  return (
    <span className={cn(
      "text-xs px-2 py-0.5 rounded-sm border border-[#c0c0c0]",
      getStatusStyles(status),
      className
    )}>
      {status.toUpperCase()}
    </span>
  );
};
