'use client';

import React from 'react';
import { MainLayout } from '@/components/layout/MainLayout';

export default function AboutPage() {
  return (
    <MainLayout
      title="About NovaSystem"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
    >
      <div className="h-full overflow-auto p-6">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🚀</div>
          <h1 className="text-3xl font-bold text-[var(--text-primary)] mb-2">
            NovaSystem v3.0
          </h1>
          <p className="text-lg text-gray-600">
            Multi-Agent Problem-Solving Framework
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Overview */}
          <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-6 rounded-sm">
            <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-4">
              🎯 About NovaSystem
            </h2>
            <p className="text-[var(--text-primary)] mb-4">
              NovaSystem is a cutting-edge multi-agent problem-solving framework that leverages
              artificial intelligence to tackle complex challenges across various domains.
              Built with a modern, component-based architecture, it provides an intuitive
              interface while maintaining the nostalgic charm of Windows XP.
            </p>
            <p className="text-[var(--text-primary)]">
              Whether you&apos;re solving technical problems, exploring business strategies,
              or tackling creative challenges, NovaSystem&apos;s intelligent agents work
              together to provide comprehensive solutions and insights.
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm">
              <h3 className="text-lg font-bold text-[var(--text-primary)] mb-2 flex items-center gap-2">
                🤖 Multi-Agent Architecture
              </h3>
              <p className="text-sm text-[var(--text-primary)]">
                Intelligent agents collaborate to analyze problems, research solutions,
                and synthesize comprehensive answers tailored to your specific needs.
              </p>
            </div>

            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm">
              <h3 className="text-lg font-bold text-[var(--text-primary)] mb-2 flex items-center gap-2">
                📊 Real-Time Analytics
              </h3>
              <p className="text-sm text-[var(--text-primary)]">
                Monitor system performance, track usage statistics, and gain insights
                into problem-solving patterns and success rates.
              </p>
            </div>

            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm">
              <h3 className="text-lg font-bold text-[var(--text-primary)] mb-2 flex items-center gap-2">
                ⚡ High Performance
              </h3>
              <p className="text-sm text-[var(--text-primary)]">
                Optimized for speed and efficiency with intelligent caching,
                parallel processing, and resource management.
              </p>
            </div>

            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm">
              <h3 className="text-lg font-bold text-[var(--text-primary)] mb-2 flex items-center gap-2">
                🎨 Modern Interface
              </h3>
              <p className="text-sm text-[var(--text-primary)]">
                Built with React and Next.js, featuring responsive design,
                keyboard shortcuts, and touch gestures for mobile devices.
              </p>
            </div>
          </div>

          {/* Technology Stack */}
          <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-6 rounded-sm">
            <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-4">
              🛠️ Technology Stack
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl mb-2">⚛️</div>
                <div className="text-sm font-medium text-[var(--text-primary)]">React 19</div>
                <div className="text-xs text-gray-600">Frontend Framework</div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">▲</div>
                <div className="text-sm font-medium text-[var(--text-primary)]">Next.js 15</div>
                <div className="text-xs text-gray-600">Full-Stack Framework</div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">🐍</div>
                <div className="text-sm font-medium text-[var(--text-primary)]">Python 3.10</div>
                <div className="text-xs text-gray-600">Backend Services</div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">🌶️</div>
                <div className="text-sm font-medium text-[var(--text-primary)]">Flask</div>
                <div className="text-xs text-gray-600">Web Framework</div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">🎨</div>
                <div className="text-sm font-medium text-[var(--text-primary)]">Tailwind CSS</div>
                <div className="text-xs text-gray-600">Styling</div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">📦</div>
                <div className="text-sm font-medium text-[var(--text-primary)]">TypeScript</div>
                <div className="text-xs text-gray-600">Type Safety</div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">🤖</div>
                <div className="text-sm font-medium text-[var(--text-primary)]">Anthropic Claude</div>
                <div className="text-xs text-gray-600">AI Models</div>
              </div>
              <div className="text-center">
                <div className="text-2xl mb-2">🗄️</div>
                <div className="text-sm font-medium text-[var(--text-primary)]">SQLite</div>
                <div className="text-xs text-gray-600">Database</div>
              </div>
            </div>
          </div>

          {/* Statistics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm text-center">
              <div className="text-2xl font-bold text-[var(--primary-color)]">10+</div>
              <div className="text-xs text-gray-600">AI Agents</div>
            </div>
            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm text-center">
              <div className="text-2xl font-bold text-[var(--accent-color)]">99.9%</div>
              <div className="text-xs text-gray-600">Uptime</div>
            </div>
            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm text-center">
              <div className="text-2xl font-bold text-[var(--warning-color)]">&lt;2s</div>
              <div className="text-xs text-gray-600">Response Time</div>
            </div>
            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm text-center">
              <div className="text-2xl font-bold text-[var(--secondary-color)]">24/7</div>
              <div className="text-xs text-gray-600">Availability</div>
            </div>
          </div>

          {/* Changelog */}
          <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-6 rounded-sm">
            <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-4">
              📝 Recent Updates
            </h2>
            <div className="space-y-3">
              <div className="border-l-2 border-[var(--accent-color)] pl-4">
                <div className="text-sm font-medium text-[var(--text-primary)]">v3.0.0 - September 2025</div>
                <div className="text-xs text-gray-600">Complete UI overhaul with modern React architecture</div>
              </div>
              <div className="border-l-2 border-[var(--primary-color)] pl-4">
                <div className="text-sm font-medium text-[var(--text-primary)]">v2.1.0 - August 2025</div>
                <div className="text-xs text-gray-600">Enhanced workflow engine and improved agent coordination</div>
              </div>
              <div className="border-l-2 border-[var(--warning-color)] pl-4">
                <div className="text-sm font-medium text-[var(--text-primary)]">v2.0.0 - July 2025</div>
                <div className="text-xs text-gray-600">Initial release with multi-agent problem solving</div>
              </div>
            </div>
          </div>

          {/* License */}
          <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-6 rounded-sm text-center">
            <h2 className="text-xl font-bold text-[var(--text-primary)] mb-2">
              📄 License
            </h2>
            <p className="text-sm text-[var(--text-primary)] mb-4">
              NovaSystem is released under the MIT License. This means you&apos;re free to use,
              modify, and distribute the software for both personal and commercial purposes.
            </p>
            <div className="text-xs text-gray-600">
              © 2025 NovaSystem. All rights reserved.
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
