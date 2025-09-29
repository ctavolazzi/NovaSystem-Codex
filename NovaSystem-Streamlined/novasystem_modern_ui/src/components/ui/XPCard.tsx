'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface XPCardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'inset' | 'outset';
  className?: string;
}

interface XPCardComponent extends React.FC<XPCardProps> {
  Header: React.FC<XPCardProps>;
  Content: React.FC<XPCardProps>;
  Footer: React.FC<XPCardProps>;
}

export const XPCard: XPCardComponent = ({
  className,
  variant = 'outset',
  children,
  ...props
}) => {
  const variantStyles = {
    default: "bg-[var(--xp-content-bg)] border border-[var(--xp-content-border)] shadow-[1px_1px_0px_var(--xp-window-border-light),-1px_-1px_0px_var(--xp-window-border-dark)]",
    inset: "bg-[var(--xp-input-bg)] border border-[var(--xp-input-border)] border-t-[var(--xp-window-border-dark)] border-l-[var(--xp-window-border-dark)] border-r-[var(--xp-window-border-light)] border-b-[var(--xp-window-border-light)] shadow-[inset_1px_1px_0px_var(--xp-window-border-dark),inset_-1px_-1px_0px_var(--xp-window-border-light)]",
    outset: "bg-[var(--xp-content-bg)] border border-[var(--xp-window-border-light)] border-t-[var(--xp-window-border-light)] border-l-[var(--xp-window-border-light)] border-r-[var(--xp-window-border-dark)] border-b-[var(--xp-window-border-dark)] shadow-[1px_1px_0px_var(--xp-window-border-light),-1px_-1px_0px_var(--xp-window-border-dark)]",
  };

  return (
    <div
      className={cn(
        "font-sans text-sm",
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

const XPCardHeader: React.FC<XPCardProps> = ({ className, children, ...props }) => {
  return (
    <div
      className={cn(
        "p-2 border-b border-[var(--xp-window-border)] bg-[var(--xp-toolbar-bg)] font-bold text-black text-sm",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

const XPCardContent: React.FC<XPCardProps> = ({ className, children, ...props }) => {
  return (
    <div
      className={cn("p-3 text-black text-sm", className)}
      {...props}
    >
      {children}
    </div>
  );
};

const XPCardFooter: React.FC<XPCardProps> = ({ className, children, ...props }) => {
  return (
    <div
      className={cn(
        "p-2 border-t border-[var(--xp-window-border)] bg-[var(--xp-toolbar-bg)] text-black text-sm flex justify-end gap-2",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

XPCard.Header = XPCardHeader;
XPCard.Content = XPCardContent;
XPCard.Footer = XPCardFooter;
