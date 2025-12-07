'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface WindowProps {
  title: string;
  icon?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  onMinimize?: () => void;
  onMaximize?: () => void;
  onClose?: () => void;
}

export const Window: React.FC<WindowProps> = ({
  title,
  icon,
  children,
  className,
  onMinimize,
  onMaximize,
  onClose,
}) => {
  return (
    <div className={cn(
      "absolute top-2.5 left-2.5 right-2.5 bottom-10",
      "bg-[var(--bg-window)] border-2 border-[var(--border-3d-dark)]",
      "shadow-[2px_2px_4px_rgba(0,0,0,0.3)]",
      "flex flex-col xp-window-open",
      className
    )}>
      {/* Windows XP Title Bar */}
      <div className="xp-titlebar">
        <div className="xp-titlebar-title">
          {icon && (
            <div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm flex items-center justify-center text-[10px] text-white font-bold">
              N
            </div>
          )}
          <span>{title}</span>
        </div>
        <div className="xp-titlebar-controls">
          <button
            onClick={onMinimize}
            className="xp-window-control"
            title="Minimize"
          >
            _
          </button>
          <button
            onClick={onMaximize}
            className="xp-window-control"
            title="Maximize"
          >
            □
          </button>
          <button
            onClick={onClose}
            className="xp-window-control close"
            title="Close"
          >
            ×
          </button>
        </div>
      </div>

      {children}
    </div>
  );
};
