'use client';

import React, { useState } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { cn } from '@/lib/utils';

interface HelpSection {
  id: string;
  title: string;
  content: string;
  icon: string;
}

export default function HelpPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeSection, setActiveSection] = useState('getting-started');

  const helpSections: HelpSection[] = [
    {
      id: 'getting-started',
      title: 'Getting Started',
      icon: '🚀',
      content: `
# Getting Started with NovaSystem

NovaSystem is a powerful multi-agent problem-solving framework that helps you tackle complex challenges using AI agents.

## First Steps
1. **Start a Session**: Navigate to the Home page and describe your problem
2. **Choose Agents**: The system will automatically select the best agents for your problem
3. **Monitor Progress**: Watch as agents work together to solve your challenge
4. **Review Results**: Get detailed solutions and explanations

## Basic Workflow
- Describe your problem clearly and concisely
- Specify any particular domains or constraints
- Let the system analyze and break down the problem
- Review the step-by-step solution process
- Export or save results for future reference
      `
    },
    {
      id: 'features',
      title: 'Features Overview',
      icon: '✨',
      content: `
# NovaSystem Features

## Multi-Agent Architecture
- **Problem Solver**: Analyzes and breaks down complex problems
- **Researcher**: Gathers relevant information and context
- **Analyst**: Performs detailed analysis and evaluation
- **Synthesizer**: Combines insights into comprehensive solutions

## Advanced Capabilities
- **Real-time Monitoring**: Track agent progress and system performance
- **Session Management**: Save, resume, and manage multiple problem-solving sessions
- **Analytics Dashboard**: View usage statistics and performance metrics
- **Customizable Settings**: Configure system behavior and preferences

## Integration Features
- **API Access**: Integrate with external systems and workflows
- **Export Options**: Save results in multiple formats
- **Collaboration Tools**: Share sessions and results with team members
      `
    },
    {
      id: 'troubleshooting',
      title: 'Troubleshooting',
      icon: '🔧',
      content: `
# Troubleshooting Guide

## Common Issues

### Session Not Starting
- Check your internet connection
- Verify that the Flask backend is running (port 5000)
- Try refreshing the page or restarting the session

### Slow Performance
- Check the Monitor page for system resource usage
- Reduce the complexity of your problem description
- Try breaking down large problems into smaller parts

### Agent Errors
- Review the system logs in the Monitor page
- Check that all required services are running
- Try restarting the session with different parameters

## Error Messages
- **"Session timeout"**: The problem took too long to solve. Try simplifying the problem or increasing the timeout in settings.
- **"Agent unavailable"**: The requested agent is busy or offline. Try again later or use a different agent.
- **"Invalid problem format"**: Your problem description may be too vague. Try being more specific about what you need help with.

## Getting Help
If you continue to experience issues, please check the system logs and contact support with:
- The exact error message
- Steps to reproduce the issue
- Your system configuration (browser, OS, etc.)
      `
    },
    {
      id: 'shortcuts',
      title: 'Keyboard Shortcuts',
      icon: '⌨️',
      content: `
# Keyboard Shortcuts

## Navigation
- **Ctrl + 1**: Go to Home page
- **Ctrl + 2**: Go to Workflow page
- **Ctrl + 3**: Go to Analytics page
- **Ctrl + 4**: Go to Monitor page

## General
- **Ctrl + S**: Save current session
- **Ctrl + R**: Refresh current page
- **Ctrl + F**: Search within current page
- **Esc**: Close dialogs or cancel operations

## Session Management
- **Ctrl + N**: Start new session
- **Ctrl + P**: Pause current session
- **Ctrl + K**: Kill current session
- **Ctrl + Shift + K**: Kill all sessions

## Mobile Gestures
- **Swipe Left**: Navigate to next page
- **Swipe Right**: Navigate to previous page
- **Pinch**: Zoom in/out (on supported pages)
      `
    },
    {
      id: 'faq',
      title: 'Frequently Asked Questions',
      icon: '❓',
      content: `
# Frequently Asked Questions

## General Questions

**Q: What types of problems can NovaSystem solve?**
A: NovaSystem can help with a wide range of problems including technical challenges, business strategy, creative projects, research questions, and more. The system works best with well-defined problems that have clear objectives.

**Q: How long does it take to solve a problem?**
A: Problem-solving time varies depending on complexity. Simple problems may be solved in seconds, while complex challenges can take several minutes. You can monitor progress in real-time on the Monitor page.

**Q: Can I save my sessions?**
A: Yes! All sessions are automatically saved and can be accessed through the Session Manager. You can also export results in various formats.

## Technical Questions

**Q: What AI models does NovaSystem use?**
A: NovaSystem supports multiple AI models including Claude 3.5 Sonnet, Claude 3 Haiku, and GPT-4. The system automatically selects the best model for your specific problem.

**Q: Is my data secure?**
A: Yes, NovaSystem implements industry-standard security practices. All data is encrypted in transit and at rest, and sessions are isolated for privacy.

**Q: Can I integrate NovaSystem with other tools?**
A: Yes, NovaSystem provides a comprehensive API that allows integration with external systems and workflows. Check the API documentation for details.

## Usage Questions

**Q: How many sessions can I run simultaneously?**
A: The number of concurrent sessions depends on your system resources and configuration. The Monitor page shows current usage and limits.

**Q: Can I customize the agents?**
A: While the core agents are predefined, you can configure their behavior through the Settings page, including model selection, iteration limits, and timeout settings.

**Q: What happens if a session fails?**
A: Failed sessions are logged with detailed error information. You can review the logs in the Monitor page and retry with adjusted parameters.
      `
    }
  ];

  const filteredSections = helpSections.filter(section =>
    section.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    section.content.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const sidebarContent = (
    <div className="space-y-4">
      <div className="text-xs font-bold text-[var(--text-primary)] mb-2 px-1">
        Help Sections
      </div>

      <div className="space-y-1">
        {helpSections.map((section) => (
          <button
            key={section.id}
            onClick={() => setActiveSection(section.id)}
            className={cn(
              "w-full px-2 py-1.5 text-xs text-left border rounded-sm flex items-center gap-2",
              activeSection === section.id
                ? "bg-[var(--accent-color)] text-white border-[var(--accent-color)]"
                : "bg-[var(--bg-tertiary)] text-[var(--text-primary)] border-[var(--border-inset)] hover:bg-[#e8e5e0]"
            )}
          >
            <span>{section.icon}</span>
            <span>{section.title}</span>
          </button>
        ))}
      </div>

      <div className="border-t border-[var(--border-inset)] pt-2 mt-4">
        <div className="text-xs font-bold text-[var(--text-primary)] mb-2 px-1">
          Quick Actions
        </div>
        <button className="w-full px-2 py-1.5 text-xs text-[var(--text-primary)] bg-[var(--bg-tertiary)] border border-[var(--border-inset)] rounded-sm hover:bg-[#e8e5e0]">
          📧 Contact Support
        </button>
        <button className="w-full px-2 py-1.5 text-xs text-[var(--text-primary)] bg-[var(--bg-tertiary)] border border-[var(--border-inset)] rounded-sm hover:bg-[#e8e5e0]">
          📋 Report Bug
        </button>
      </div>
    </div>
  );

  const activeSectionData = helpSections.find(s => s.id === activeSection);

  return (
    <MainLayout
      title="Help & Documentation"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
      sidebarContent={sidebarContent}
    >
      <div className="h-full overflow-auto p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-2">
            ❓ Help & Documentation
          </h1>
          <p className="text-sm text-gray-600">
            Get help with NovaSystem and learn how to use all features
          </p>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search help content..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-2 border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] placeholder-gray-500 rounded-sm focus:outline-none focus:border-[var(--primary-color)]"
          />
        </div>

        {/* Content */}
        {searchQuery ? (
          <div className="space-y-4">
            {filteredSections.map((section) => (
              <div key={section.id} className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm">
                <h2 className="text-lg font-bold text-[var(--text-primary)] mb-2 flex items-center gap-2">
                  {section.icon} {section.title}
                </h2>
                <div className="prose prose-sm max-w-none">
                  <pre className="whitespace-pre-wrap text-sm text-[var(--text-primary)] font-sans">
                    {section.content}
                  </pre>
                </div>
              </div>
            ))}
            {filteredSections.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No help content found for &quot;{searchQuery}&quot;
              </div>
            )}
          </div>
        ) : (
          <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-6 rounded-sm">
            <h2 className="text-xl font-bold text-[var(--text-primary)] mb-4 flex items-center gap-2">
              {activeSectionData?.icon} {activeSectionData?.title}
            </h2>
            <div className="prose prose-sm max-w-none">
              <pre className="whitespace-pre-wrap text-sm text-[var(--text-primary)] font-sans">
                {activeSectionData?.content}
              </pre>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
}
