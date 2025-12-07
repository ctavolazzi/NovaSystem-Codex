'use client';

import React, { useState } from 'react';
import { cn } from '@/lib/utils';

interface ResponsiveTestProps {
  className?: string;
}

const PRESET_SIZES = [
  { name: 'iPhone SE', width: 375, height: 667 },
  { name: 'iPhone 12', width: 390, height: 844 },
  { name: 'iPhone 12 Pro Max', width: 428, height: 926 },
  { name: 'iPad Mini', width: 768, height: 1024 },
  { name: 'iPad Air', width: 820, height: 1180 },
  { name: 'iPad Pro', width: 1024, height: 1366 },
  { name: 'Desktop Small', width: 1280, height: 720 },
  { name: 'Desktop Medium', width: 1440, height: 900 },
  { name: 'Desktop Large', width: 1920, height: 1080 },
  { name: 'Ultra-wide', width: 2560, height: 1440 }
];

export const ResponsiveTest: React.FC<ResponsiveTestProps> = ({ className }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [currentSize, setCurrentSize] = useState({ width: 0, height: 0 });

  const applySize = (width: number, height: number) => {
    if (typeof window !== 'undefined') {
      // Apply viewport size for testing
      const viewport = document.querySelector('meta[name="viewport"]');
      if (viewport) {
        viewport.setAttribute('content', `width=${width}, initial-scale=1.0`);
      }

      // Update document body classes for responsive testing
      document.body.style.width = `${width}px`;
      document.body.style.height = `${height}px`;
      document.body.style.overflow = 'auto';

      setCurrentSize({ width, height });
    }
  };

  const resetSize = () => {
    if (typeof window !== 'undefined') {
      const viewport = document.querySelector('meta[name="viewport"]');
      if (viewport) {
        viewport.setAttribute('content', 'width=device-width, initial-scale=1.0');
      }

      document.body.style.width = '';
      document.body.style.height = '';
      document.body.style.overflow = '';

      setCurrentSize({ width: window.innerWidth, height: window.innerHeight });
    }
  };

  const getCurrentBreakpoint = () => {
    const width = currentSize.width || (typeof window !== 'undefined' ? window.innerWidth : 0);

    if (width >= 1920) return 'Ultra-wide (1920px+)';
    if (width >= 1440) return 'Extra Large (1440px+)';
    if (width >= 1200) return 'Large (1200px-1439px)';
    if (width >= 1024) return 'Desktop (1024px-1199px)';
    if (width >= 768) return 'Tablet Landscape (768px-1023px)';
    if (width >= 640) return 'Tablet Portrait (640px-767px)';
    if (width >= 480) return 'Mobile Large (480px-639px)';
    if (width >= 375) return 'Mobile Medium (375px-479px)';
    return 'Mobile Small (320px-374px)';
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className={cn(
          "fixed bottom-20 right-4 z-50 bg-[var(--primary-color)] text-white",
          "px-3 py-2 text-xs rounded-sm shadow-lg hover:bg-[var(--secondary-color)]",
          "border border-[var(--border-inset)]",
          className
        )}
      >
        📱 Test Responsive
      </button>
    );
  }

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-[var(--bg-window)] border border-[var(--border-inset)] rounded-sm max-w-4xl w-full max-h-[80vh] overflow-auto">
        {/* Header */}
        <div className="p-4 border-b border-[var(--border-inset)]">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-bold text-[var(--text-primary)]">
              📱 Responsive Design Tester
            </h2>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Current Info */}
        <div className="p-4 border-b border-[var(--border-inset)]">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <strong>Current Size:</strong> {currentSize.width} × {currentSize.height}
            </div>
            <div>
              <strong>Breakpoint:</strong> {getCurrentBreakpoint()}
            </div>
            <div>
              <strong>Device Type:</strong> {
                currentSize.width <= 767 ? 'Mobile' :
                currentSize.width <= 1024 ? 'Tablet' : 'Desktop'
              }
            </div>
            <div>
              <strong>Orientation:</strong> {
                currentSize.width > currentSize.height ? 'Landscape' : 'Portrait'
              }
            </div>
          </div>
        </div>

        {/* Preset Sizes */}
        <div className="p-4">
          <h3 className="text-md font-bold text-[var(--text-primary)] mb-4">
            Device Presets
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
            {PRESET_SIZES.map((preset) => (
              <button
                key={preset.name}
                onClick={() => applySize(preset.width, preset.height)}
                className="p-2 text-xs text-left bg-[var(--bg-tertiary)] border border-[var(--border-inset)] rounded-sm hover:bg-[#e8e5e0]"
              >
                <div className="font-medium text-[var(--text-primary)]">{preset.name}</div>
                <div className="text-gray-600">{preset.width} × {preset.height}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Custom Size */}
        <div className="p-4 border-t border-[var(--border-inset)]">
          <h3 className="text-md font-bold text-[var(--text-primary)] mb-4">
            Custom Size
          </h3>
          <div className="flex gap-4 items-end">
            <div>
              <label className="block text-xs text-[var(--text-primary)] mb-1">Width</label>
              <input
                type="number"
                placeholder="Width"
                className="w-20 px-2 py-1 text-xs border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm"
                min="320"
                max="3840"
              />
            </div>
            <div>
              <label className="block text-xs text-[var(--text-primary)] mb-1">Height</label>
              <input
                type="number"
                placeholder="Height"
                className="w-20 px-2 py-1 text-xs border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm"
                min="240"
                max="2160"
              />
            </div>
            <button
              onClick={() => {
                const widthInput = document.querySelector('input[placeholder="Width"]') as HTMLInputElement;
                const heightInput = document.querySelector('input[placeholder="Height"]') as HTMLInputElement;
                if (widthInput?.value && heightInput?.value) {
                  applySize(parseInt(widthInput.value), parseInt(heightInput.value));
                }
              }}
              className="px-3 py-1 text-xs bg-[var(--accent-color)] text-white border border-[var(--border-inset)] rounded-sm hover:bg-green-600"
            >
              Apply
            </button>
          </div>
        </div>

        {/* Actions */}
        <div className="p-4 border-t border-[var(--border-inset)] flex justify-between">
          <button
            onClick={resetSize}
            className="px-4 py-2 text-xs bg-[var(--primary-color)] text-white border border-[var(--border-inset)] rounded-sm hover:bg-[var(--secondary-color)]"
          >
            🔄 Reset to Actual Size
          </button>
          <button
            onClick={() => setIsOpen(false)}
            className="px-4 py-2 text-xs bg-gray-500 text-white border border-[var(--border-inset)] rounded-sm hover:bg-gray-600"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
