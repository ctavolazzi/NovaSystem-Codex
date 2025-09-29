'use client';

import React, { useState } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { XPCard } from '@/components/ui/XPCard';
import { XPButton } from '@/components/ui/XPButton';
import { XPInput, XPSelect } from '@/components/ui/XPInput';
import { cn } from '@/lib/utils';

interface Settings {
  general: {
    language: string;
    theme: string;
    autoSave: boolean;
    notifications: boolean;
  };
  appearance: {
    fontSize: string;
    colorScheme: string;
    animations: boolean;
  };
  ai: {
    defaultModel: string;
    maxIterations: number;
    timeout: number;
    temperature: number;
  };
  performance: {
    cacheEnabled: boolean;
    maxCacheSize: number;
    autoOptimize: boolean;
  };
  security: {
    sessionTimeout: number;
    requireAuth: boolean;
    logLevel: string;
  };
}

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('general');
  const [settings, setSettings] = useState<Settings>({
    general: {
      language: 'en',
      theme: 'windows-xp',
      autoSave: true,
      notifications: true
    },
    appearance: {
      fontSize: 'medium',
      colorScheme: 'default',
      animations: true
    },
    ai: {
      defaultModel: 'auto',
      maxIterations: 10,
      timeout: 30,
      temperature: 0.7
    },
    performance: {
      cacheEnabled: true,
      maxCacheSize: 100,
      autoOptimize: true
    },
    security: {
      sessionTimeout: 60,
      requireAuth: false,
      logLevel: 'info'
    }
  });

  const [hasChanges, setHasChanges] = useState(false);

  const updateSetting = (section: keyof Settings, key: string, value: unknown) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }));
    setHasChanges(true);
  };

  const saveSettings = () => {
    // Here you would typically save to backend
    console.log('Saving settings:', settings);
    setHasChanges(false);
    // Show success message
  };

  const resetSettings = () => {
    // Reset to defaults
    setSettings({
      general: {
        language: 'en',
        theme: 'windows-xp',
        autoSave: true,
        notifications: true
      },
      appearance: {
        fontSize: 'medium',
        colorScheme: 'default',
        animations: true
      },
      ai: {
        defaultModel: 'auto',
        maxIterations: 10,
        timeout: 30,
        temperature: 0.7
      },
      performance: {
        cacheEnabled: true,
        maxCacheSize: 100,
        autoOptimize: true
      },
      security: {
        sessionTimeout: 60,
        requireAuth: false,
        logLevel: 'info'
      }
    });
    setHasChanges(true);
  };

  const exportSettings = () => {
    const dataStr = JSON.stringify(settings, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'novasystem-settings.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  const importSettings = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const imported = JSON.parse(e.target?.result as string);
          setSettings(imported);
          setHasChanges(true);
        } catch (error) {
          console.error('Failed to import settings:', error);
        }
      };
      reader.readAsText(file);
    }
  };

  const sections = [
    { id: 'general', label: 'General', icon: '⚙️' },
    { id: 'appearance', label: 'Appearance', icon: '🎨' },
    { id: 'ai', label: 'AI Models', icon: '🤖' },
    { id: 'performance', label: 'Performance', icon: '⚡' },
    { id: 'security', label: 'Security', icon: '🔒' }
  ];

  const sidebarContent = (
    <XPCard className="p-2" variant="outset">
      <div className="space-y-2">
        <div className="text-xs font-bold text-black mb-2 px-1">
          Settings Sections
        </div>
        {sections.map((section) => (
          <XPButton
            key={section.id}
            onClick={() => setActiveSection(section.id)}
            variant={activeSection === section.id ? 'primary' : 'default'}
            size="sm"
            className="w-full justify-start"
          >
            <span>{section.icon}</span>
            <span>{section.label}</span>
          </XPButton>
        ))}

        <div className="border-t border-[#c0c0c0] pt-2 mt-4">
          <div className="text-xs font-bold text-black mb-2 px-1">
            Actions
          </div>
          <XPButton
            onClick={saveSettings}
            disabled={!hasChanges}
            variant={hasChanges ? 'success' : 'default'}
            size="sm"
            className="w-full mb-1"
          >
            💾 Save Changes
          </XPButton>
          <XPButton
            onClick={resetSettings}
            variant="default"
            size="sm"
            className="w-full"
          >
            🔄 Reset to Defaults
          </XPButton>
        </div>
      </div>
    </XPCard>
  );

  const renderGeneralSettings = () => (
    <div className="space-y-4">
      <XPSelect
        label="Language"
        value={settings.general.language}
        onChange={(e) => updateSetting('general', 'language', e.target.value)}
        options={[
          { value: 'en', label: 'English' },
          { value: 'es', label: 'Español' },
          { value: 'fr', label: 'Français' },
          { value: 'de', label: 'Deutsch' }
        ]}
      />

      <XPSelect
        label="Theme"
        value={settings.general.theme}
        onChange={(e) => updateSetting('general', 'theme', e.target.value)}
        options={[
          { value: 'windows-xp', label: 'Windows XP' },
          { value: 'classic', label: 'Classic' },
          { value: 'modern', label: 'Modern' }
        ]}
      />

      <div className="space-y-2">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={settings.general.autoSave}
            onChange={(e) => updateSetting('general', 'autoSave', e.target.checked)}
            className="rounded border border-[#808080]"
          />
          <span className="text-sm text-black">Auto-save settings</span>
        </label>

        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={settings.general.notifications}
            onChange={(e) => updateSetting('general', 'notifications', e.target.checked)}
            className="rounded border border-[#808080]"
          />
          <span className="text-sm text-black">Enable notifications</span>
        </label>
      </div>
    </div>
  );

  const renderAppearanceSettings = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Font Size
        </label>
        <select
          value={settings.appearance.fontSize}
          onChange={(e) => updateSetting('appearance', 'fontSize', e.target.value)}
          className="w-full px-3 py-2 border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm"
        >
          <option value="small">Small</option>
          <option value="medium">Medium</option>
          <option value="large">Large</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Color Scheme
        </label>
        <select
          value={settings.appearance.colorScheme}
          onChange={(e) => updateSetting('appearance', 'colorScheme', e.target.value)}
          className="w-full px-3 py-2 border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm"
        >
          <option value="default">Default</option>
          <option value="high-contrast">High Contrast</option>
          <option value="dark">Dark Mode</option>
        </select>
      </div>

      <div>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={settings.appearance.animations}
            onChange={(e) => updateSetting('appearance', 'animations', e.target.checked)}
            className="rounded"
          />
          <span className="text-sm text-[var(--text-primary)]">Enable animations</span>
        </label>
      </div>
    </div>
  );

  const renderAISettings = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Default Model
        </label>
        <select
          value={settings.ai.defaultModel}
          onChange={(e) => updateSetting('ai', 'defaultModel', e.target.value)}
          className="w-full px-3 py-2 border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm"
        >
          <option value="auto">Auto-select</option>
          <option value="claude-3-5-sonnet">Claude 3.5 Sonnet</option>
          <option value="claude-3-haiku">Claude 3 Haiku</option>
          <option value="gpt-4">GPT-4</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Max Iterations: {settings.ai.maxIterations}
        </label>
        <input
          type="range"
          min="1"
          max="50"
          value={settings.ai.maxIterations}
          onChange={(e) => updateSetting('ai', 'maxIterations', parseInt(e.target.value))}
          className="w-full"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Timeout (seconds): {settings.ai.timeout}
        </label>
        <input
          type="range"
          min="5"
          max="120"
          value={settings.ai.timeout}
          onChange={(e) => updateSetting('ai', 'timeout', parseInt(e.target.value))}
          className="w-full"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Temperature: {settings.ai.temperature}
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={settings.ai.temperature}
          onChange={(e) => updateSetting('ai', 'temperature', parseFloat(e.target.value))}
          className="w-full"
        />
      </div>
    </div>
  );

  const renderPerformanceSettings = () => (
    <div className="space-y-4">
      <div>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={settings.performance.cacheEnabled}
            onChange={(e) => updateSetting('performance', 'cacheEnabled', e.target.checked)}
            className="rounded"
          />
          <span className="text-sm text-[var(--text-primary)]">Enable caching</span>
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Max Cache Size (MB): {settings.performance.maxCacheSize}
        </label>
        <input
          type="range"
          min="10"
          max="1000"
          value={settings.performance.maxCacheSize}
          onChange={(e) => updateSetting('performance', 'maxCacheSize', parseInt(e.target.value))}
          className="w-full"
        />
      </div>

      <div>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={settings.performance.autoOptimize}
            onChange={(e) => updateSetting('performance', 'autoOptimize', e.target.checked)}
            className="rounded"
          />
          <span className="text-sm text-[var(--text-primary)]">Auto-optimize performance</span>
        </label>
      </div>
    </div>
  );

  const renderSecuritySettings = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Session Timeout (minutes): {settings.security.sessionTimeout}
        </label>
        <input
          type="range"
          min="5"
          max="480"
          value={settings.security.sessionTimeout}
          onChange={(e) => updateSetting('security', 'sessionTimeout', parseInt(e.target.value))}
          className="w-full"
        />
      </div>

      <div>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={settings.security.requireAuth}
            onChange={(e) => updateSetting('security', 'requireAuth', e.target.checked)}
            className="rounded"
          />
          <span className="text-sm text-[var(--text-primary)]">Require authentication</span>
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium text-[var(--text-primary)] mb-1">
          Log Level
        </label>
        <select
          value={settings.security.logLevel}
          onChange={(e) => updateSetting('security', 'logLevel', e.target.value)}
          className="w-full px-3 py-2 border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm"
        >
          <option value="debug">Debug</option>
          <option value="info">Info</option>
          <option value="warning">Warning</option>
          <option value="error">Error</option>
        </select>
      </div>
    </div>
  );

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'general': return renderGeneralSettings();
      case 'appearance': return renderAppearanceSettings();
      case 'ai': return renderAISettings();
      case 'performance': return renderPerformanceSettings();
      case 'security': return renderSecuritySettings();
      default: return renderGeneralSettings();
    }
  };

  return (
    <MainLayout
      title="Settings"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
      sidebarContent={sidebarContent}
    >
      <div className="h-full overflow-auto p-4 space-y-4">
        {/* Header */}
        <XPCard className="p-4" variant="outset">
          <h1 className="text-xl font-bold text-black mb-2">
            ⚙️ Settings
          </h1>
          <p className="text-sm text-[#666666]">
            Configure NovaSystem preferences and behavior
          </p>
        </XPCard>

        {/* Export/Import Section */}
        <XPCard className="p-4" variant="outset">
          <XPCard.Header>
            <h3 className="text-lg font-bold text-black">
              💾 Backup & Restore
            </h3>
          </XPCard.Header>
          <XPCard.Content>
            <div className="flex gap-2">
              <XPButton onClick={exportSettings} variant="primary">
                📤 Export Settings
              </XPButton>
              <label className="cursor-pointer">
                <XPButton variant="default" as="span">
                  📥 Import Settings
                </XPButton>
                <input
                  type="file"
                  accept=".json"
                  onChange={importSettings}
                  className="hidden"
                />
              </label>
            </div>
          </XPCard.Content>
        </XPCard>

        {/* Active Settings Section */}
        <XPCard className="p-4" variant="outset">
          <XPCard.Header>
            <h2 className="text-lg font-bold text-black">
              {sections.find(s => s.id === activeSection)?.icon} {sections.find(s => s.id === activeSection)?.label}
            </h2>
          </XPCard.Header>
          <XPCard.Content>
            {renderActiveSection()}
          </XPCard.Content>
        </XPCard>
      </div>
    </MainLayout>
  );
}
