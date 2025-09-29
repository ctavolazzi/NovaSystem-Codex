'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface XPInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  error?: string;
  helperText?: string;
  variant?: 'default' | 'inset';
  size?: 'sm' | 'md' | 'lg';
}

interface XPTextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helperText?: string;
  variant?: 'default' | 'inset';
}

interface XPSelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

interface XPSelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'size'> {
  label?: string;
  error?: string;
  helperText?: string;
  options: XPSelectOption[];
  variant?: 'default' | 'inset';
  size?: 'sm' | 'md' | 'lg';
}

const baseInputStyles = "font-sans text-sm text-black bg-[var(--xp-input-bg)] border border-[var(--xp-input-border)] border-t-[var(--xp-window-border-dark)] border-l-[var(--xp-window-border-dark)] border-r-[var(--xp-window-border-light)] border-b-[var(--xp-window-border-light)] shadow-[inset_1px_1px_0px_var(--xp-window-border-dark),inset_-1px_-1px_0px_var(--xp-window-border-light)] focus:outline-none focus:border-[var(--xp-primary-blue)] focus:ring-1 focus:ring-[var(--xp-primary-blue)] disabled:bg-[var(--xp-button-bg-dark)] disabled:text-[var(--text-disabled)]";

export const XPInput: React.FC<XPInputProps> = ({
  label,
  error,
  helperText,
  variant = 'inset',
  size = 'md',
  className,
  ...props
}) => {
  const sizeStyles = {
    sm: "h-5 px-1 text-xs",
    md: "h-6 px-2 text-sm",
    lg: "h-7 px-3 text-base",
  };

  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-black">
          {label}
        </label>
      )}
      <input
        className={cn(
          baseInputStyles,
          sizeStyles[size],
          error && "border-[#ff0000] focus:border-[#ff0000]",
          className
        )}
        {...props}
      />
      {error && (
        <p className="text-xs text-[#ff0000]">{error}</p>
      )}
      {helperText && !error && (
        <p className="text-xs text-[#666666]">{helperText}</p>
      )}
    </div>
  );
};

export const XPTextArea: React.FC<XPTextAreaProps> = ({
  label,
  error,
  helperText,
  variant = 'inset',
  className,
  ...props
}) => {
  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-black">
          {label}
        </label>
      )}
      <textarea
        className={cn(
          baseInputStyles,
          "px-2 py-1 min-h-[60px] resize-vertical",
          error && "border-[#ff0000] focus:border-[#ff0000]",
          className
        )}
        {...props}
      />
      {error && (
        <p className="text-xs text-[#ff0000]">{error}</p>
      )}
      {helperText && !error && (
        <p className="text-xs text-[#666666]">{helperText}</p>
      )}
    </div>
  );
};

export const XPSelect: React.FC<XPSelectProps> = ({
  label,
  error,
  helperText,
  options,
  variant = 'inset',
  size = 'md',
  className,
  ...props
}) => {
  const sizeStyles = {
    sm: "h-5 px-1 text-xs",
    md: "h-6 px-2 text-sm",
    lg: "h-7 px-3 text-base",
  };

  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-black">
          {label}
        </label>
      )}
      <select
        className={cn(
          baseInputStyles,
          sizeStyles[size],
          error && "border-[#ff0000] focus:border-[#ff0000]",
          className
        )}
        {...props}
      >
        {options.map(option => (
          <option
            key={option.value}
            value={option.value}
            disabled={option.disabled}
          >
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="text-xs text-[#ff0000]">{error}</p>
      )}
      {helperText && !error && (
        <p className="text-xs text-[#666666]">{helperText}</p>
      )}
    </div>
  );
};
