'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface XPButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
}

export const XPButton: React.FC<XPButtonProps> = ({
  className,
  variant = 'default',
  size = 'md',
  icon,
  children,
  onClick,
  ...props
}) => {
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    // Add button press animation
    const button = e.currentTarget;
    button.classList.add('xp-button-press');
    setTimeout(() => {
      button.classList.remove('xp-button-press');
    }, 100);

    if (onClick) {
      onClick(e);
    }
  };
  const baseStyles = "inline-flex items-center justify-center font-sans transition-all duration-150 focus:outline-none disabled:cursor-not-allowed";

  const variantStyles = {
    default: "bg-[var(--xp-button-bg)] text-[var(--xp-button-text)] border border-[var(--xp-button-border-light)] border-t-[var(--xp-button-border-light)] border-l-[var(--xp-button-border-light)] border-r-[var(--xp-button-border-dark)] border-b-[var(--xp-button-border-dark)] shadow-[1px_1px_0px_var(--xp-button-border-light),-1px_-1px_0px_var(--xp-button-border-dark)] hover:bg-[var(--xp-button-bg-light)] active:bg-[var(--xp-button-bg-dark)] active:shadow-[inset_1px_1px_0px_var(--xp-button-border-dark),inset_-1px_-1px_0px_var(--xp-button-border-light)] active:border-t-[var(--xp-button-border-dark)] active:border-l-[var(--xp-button-border-dark)] active:border-r-[var(--xp-button-border-light)] active:border-b-[var(--xp-button-border-light)]",
    primary: "bg-[var(--xp-primary-blue)] text-white border border-[var(--xp-primary-blue-dark)] border-t-[var(--xp-primary-blue-light)] border-l-[var(--xp-primary-blue-light)] border-r-[var(--xp-primary-blue-dark)] border-b-[var(--xp-primary-blue-dark)] shadow-[1px_1px_0px_var(--xp-primary-blue-light),-1px_-1px_0px_var(--xp-primary-blue-dark)] hover:bg-[var(--xp-primary-blue-light)] active:bg-[var(--xp-primary-blue-dark)] active:shadow-[inset_1px_1px_0px_var(--xp-primary-blue-dark),inset_-1px_-1px_0px_var(--xp-primary-blue-light)] active:border-t-[var(--xp-primary-blue-dark)] active:border-l-[var(--xp-primary-blue-dark)] active:border-r-[var(--xp-primary-blue-light)] active:border-b-[var(--xp-primary-blue-light)]",
    success: "bg-[var(--xp-success)] text-white border border-[var(--xp-success)] border-t-[var(--xp-success)] border-l-[var(--xp-success)] border-r-[var(--xp-success)] border-b-[var(--xp-success)] shadow-[1px_1px_0px_var(--xp-success),-1px_-1px_0px_var(--xp-success)] hover:bg-[#8dd066] active:bg-[#4a8b2b] active:shadow-[inset_1px_1px_0px_var(--xp-success),inset_-1px_-1px_0px_var(--xp-success)]",
    warning: "bg-[var(--xp-warning)] text-white border border-[var(--xp-warning)] border-t-[var(--xp-warning)] border-l-[var(--xp-warning)] border-r-[var(--xp-warning)] border-b-[var(--xp-warning)] shadow-[1px_1px_0px_var(--xp-warning),-1px_-1px_0px_var(--xp-warning)] hover:bg-[#ffb84d] active:bg-[#cc8400] active:shadow-[inset_1px_1px_0px_var(--xp-warning),inset_-1px_-1px_0px_var(--xp-warning)]",
    danger: "bg-[var(--xp-error)] text-white border border-[var(--xp-error)] border-t-[var(--xp-error)] border-l-[var(--xp-error)] border-r-[var(--xp-error)] border-b-[var(--xp-error)] shadow-[1px_1px_0px_var(--xp-error),-1px_-1px_0px_var(--xp-error)] hover:bg-[#ff3333] active:bg-[#cc0000] active:shadow-[inset_1px_1px_0px_var(--xp-error),inset_-1px_-1px_0px_var(--xp-error)]",
  };

  const sizeStyles = {
    sm: "h-5 px-2 text-xs min-w-[60px]",
    md: "h-6 px-3 text-sm min-w-[75px]",
    lg: "h-7 px-4 text-base min-w-[90px]",
  };

  return (
    <button
      className={cn(
        baseStyles,
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      onClick={handleClick}
      {...props}
    >
      <div className="flex items-center justify-center gap-1">
        {icon && <span className="text-xs">{icon}</span>}
        {children}
      </div>
    </button>
  );
};
