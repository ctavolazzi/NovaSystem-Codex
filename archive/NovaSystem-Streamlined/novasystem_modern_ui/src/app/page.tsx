'use client';

import React, { useState, useEffect } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { apiClient, Session } from '@/lib/api';
import { cn } from '@/lib/utils';
import { XPButton } from '@/components/ui/XPButton';
import { XPInput } from '@/components/ui/XPInput';
import { XPCard } from '@/components/ui/XPCard';

interface Message {
  id: string;
  type: 'user' | 'system' | 'agent';
  content: string;
  timestamp: Date;
  agent?: string;
}

export default function HomePage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'system',
      content: 'Welcome to NovaSystem! How can I assist you today?',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeSessions, setActiveSessions] = useState<Session[]>([]);
  const [isMounted, setIsMounted] = useState(false);

  // Set mounted state after hydration
  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Load active sessions on mount
  useEffect(() => {
    const loadSessions = async () => {
      const response = await apiClient.getSessions();
      if (response.success && response.data) {
        setActiveSessions(response.data.filter(session => session.status === 'active'));
      }
    };

    loadSessions();
    const interval = setInterval(loadSessions, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await apiClient.solveProblem(inputValue);

      if (response.success) {
        const systemMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'system',
          content: response.data?.solution || 'Problem submitted successfully! Check the workflow or sessions page for progress.',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, systemMessage]);
      } else {
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'system',
          content: `Error: ${response.error || 'Failed to process request'}`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const sidebarContent = (
    <div className="space-y-2">
      <div className="xp-sidebar-section-title">
        Active Sessions
      </div>
      {activeSessions.length === 0 ? (
        <div className="text-xs text-[#666666] px-2">
          No active sessions
        </div>
      ) : (
        <div className="space-y-1">
          {activeSessions.map((session) => (
            <XPCard
              key={session.id}
              className="p-2"
              variant="inset"
            >
              <div className="text-xs font-medium text-black truncate">
                {session.problem || 'Problem solving...'}
              </div>
              <div className="text-[10px] text-[#666666]" suppressHydrationWarning>
                {isMounted ? new Date(session.created_at).toLocaleTimeString() : '--:--:--'}
              </div>
              {session.progress && (
                <div className="w-full bg-[#c0c0c0] h-1 mt-1 border border-[#808080]">
                  <div
                    className="bg-[var(--primary-blue)] h-full"
                    style={{ width: `${session.progress}%` }}
                  ></div>
                </div>
              )}
            </XPCard>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <MainLayout
      title="NovaSystem v3.0 - Home"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
      sidebarContent={sidebarContent}
    >
      <div className="h-full flex flex-col responsive-spacing">
        {/* Chat Header */}
        <XPCard className="p-4 mb-4" variant="outset">
          <div className="responsive-title font-bold text-black">
            What can I help with?
          </div>
          <div className="responsive-text text-[#666666]">
            Multi-Agent Problem-Solving Framework
          </div>
        </XPCard>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto responsive-padding space-y-3">
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex",
                message.type === 'user' ? "justify-end" : "justify-start"
              )}
            >
              <XPCard
                className={cn(
                  "max-w-[80%] px-3 py-2 responsive-text sm:max-w-[95%] lg:max-w-[80%]",
                  message.type === 'user'
                    ? "bg-[var(--primary-blue)] text-white border-[var(--primary-blue)]"
                    : message.type === 'system'
                    ? "bg-[var(--bg-secondary)] text-black"
                    : "bg-[var(--success-green)] text-white border-[var(--success-green)]"
                )}
                variant={message.type === 'user' || message.type === 'agent' ? 'default' : 'inset'}
              >
                {message.type === 'agent' && message.agent && (
                  <div className="text-xs font-bold mb-1">{message.agent}</div>
                )}
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className="text-xs opacity-70 mt-1" suppressHydrationWarning>
                  {isMounted ? message.timestamp.toLocaleTimeString() : '--:--:--'}
                </div>
              </XPCard>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <XPCard className="px-3 py-2 text-sm text-black" variant="inset">
                <div className="flex items-center gap-2">
                  <div className="animate-spin w-3 h-3 border border-[var(--primary-blue)] border-t-transparent rounded-full"></div>
                  Processing your request...
                </div>
              </XPCard>
            </div>
          )}
        </div>

        {/* Chat Input */}
        <XPCard className="p-4" variant="outset">
          <form onSubmit={handleSubmit} className="flex gap-2 sm:flex-col lg:flex-row">
            <XPInput
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Describe your problem or question..."
              className="flex-1"
              disabled={isLoading}
            />
            <XPButton
              type="submit"
              variant="primary"
              disabled={isLoading || !inputValue.trim()}
              className="responsive-text font-medium"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </XPButton>
          </form>
        </XPCard>
      </div>
    </MainLayout>
  );
}