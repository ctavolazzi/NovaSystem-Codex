'use client';

import React from 'react';
import { cn } from '@/lib/utils';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outlined' | 'filled';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  clickable?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  padding = 'md',
  hover = false,
  clickable = false,
  className,
  ...props
}) => {
  const baseClasses = "rounded-lg transition-all duration-200";

  const variantClasses = {
    default: "bg-white border border-gray-200",
    elevated: "bg-white shadow-md border border-gray-100",
    outlined: "bg-transparent border-2 border-gray-300",
    filled: "bg-gray-50 border border-gray-200"
  };

  const paddingClasses = {
    none: "",
    sm: "p-3",
    md: "p-4",
    lg: "p-6"
  };

  const interactiveClasses = clickable
    ? "cursor-pointer hover:shadow-md active:scale-[0.98]"
    : "";

  const hoverClasses = hover
    ? "hover:shadow-lg hover:-translate-y-0.5"
    : "";

  return (
    <div
      className={cn(
        baseClasses,
        variantClasses[variant],
        paddingClasses[padding],
        interactiveClasses,
        hoverClasses,
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export const CardHeader: React.FC<CardHeaderProps> = ({
  children,
  title,
  subtitle,
  action,
  className,
  ...props
}) => {
  return (
    <div className={cn("flex items-start justify-between mb-4", className)} {...props}>
      <div className="flex-1">
        {title && (
          <h3 className="text-lg font-semibold text-gray-900 mb-1">{title}</h3>
        )}
        {subtitle && (
          <p className="text-sm text-gray-600">{subtitle}</p>
        )}
        {children}
      </div>
      {action && (
        <div className="ml-4 flex-shrink-0">
          {action}
        </div>
      )}
    </div>
  );
};

export interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardContent: React.FC<CardContentProps> = ({
  children,
  className,
  ...props
}) => {
  return (
    <div className={cn("text-gray-700", className)} {...props}>
      {children}
    </div>
  );
};

export interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {
  justify?: 'start' | 'center' | 'end' | 'between';
}

export const CardFooter: React.FC<CardFooterProps> = ({
  children,
  justify = 'end',
  className,
  ...props
}) => {
  const justifyClasses = {
    start: "justify-start",
    center: "justify-center",
    end: "justify-end",
    between: "justify-between"
  };

  return (
    <div
      className={cn(
        "flex items-center gap-2 mt-4 pt-4 border-t border-gray-200",
        justifyClasses[justify],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
