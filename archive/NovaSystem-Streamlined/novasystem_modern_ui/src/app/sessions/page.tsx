'use client';

import React, { useState, useEffect } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { apiClient, Session } from '@/lib/api';
import { cn } from '@/lib/utils';

type SessionFilter = 'all' | 'active' | 'completed' | 'failed' | 'paused';

export default function SessionsPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [filter, setFilter] = useState<SessionFilter>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedSession, setSelectedSession] = useState<Session | null>(null);

  useEffect(() => {
    const loadSessions = async () => {
      try {
        const response = await apiClient.getSessions();
        if (response.success && response.data) {
          setSessions(response.data);
        } else {
          // Mock data for demonstration
          setSessions([
            {
              id: 'session_001',
              status: 'active',
              created_at: new Date(Date.now() - 300000).toISOString(),
              updated_at: new Date(Date.now() - 60000).toISOString(),
              problem: 'Optimize database queries for better performance',
              solution: 'Implement query optimization strategies including indexing, query rewriting, and caching mechanisms.',
              progress: 65
            },
            {
              id: 'session_002',
              status: 'completed',
              created_at: new Date(Date.now() - 1800000).toISOString(),
              updated_at: new Date(Date.now() - 900000).toISOString(),
              problem: 'Design a scalable microservices architecture',
              solution: 'Created a comprehensive microservices architecture with service mesh, API gateway, and distributed data management.',
              progress: 100
            },
            {
              id: 'session_003',
              status: 'failed',
              created_at: new Date(Date.now() - 3600000).toISOString(),
              updated_at: new Date(Date.now() - 3300000).toISOString(),
              problem: 'Implement advanced machine learning pipeline',
              solution: 'Session failed due to insufficient computational resources.',
              progress: 23
            },
            {
              id: 'session_004',
              status: 'paused',
              created_at: new Date(Date.now() - 7200000).toISOString(),
              updated_at: new Date(Date.now() - 6900000).toISOString(),
              problem: 'Develop comprehensive testing strategy',
              solution: 'Paused for additional requirements gathering.',
              progress: 45
            }
          ]);
        }
      } catch (error) {
        console.error('Failed to load sessions:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadSessions();
    const interval = setInterval(loadSessions, 5000); // Refresh every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const filteredSessions = sessions.filter(session => {
    if (filter === 'all') return true;
    return session.status === filter;
  });

  const killSession = async (sessionId: string) => {
    try {
      await apiClient.killSession(sessionId);
      setSessions(prev => prev.filter(s => s.id !== sessionId));
    } catch (error) {
      console.error('Failed to kill session:', error);
    }
  };

  const killAllSessions = async () => {
    try {
      await apiClient.killAllSessions();
      setSessions([]);
    } catch (error) {
      console.error('Failed to kill all sessions:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-blue-600 bg-blue-100';
      case 'completed': return 'text-green-600 bg-green-100';
      case 'failed': return 'text-red-600 bg-red-100';
      case 'paused': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return '🔄';
      case 'completed': return '✅';
      case 'failed': return '❌';
      case 'paused': return '⏸️';
      default: return 'ℹ️';
    }
  };

  const formatDuration = (startTime: string) => {
    const duration = Date.now() - new Date(startTime).getTime();
    const minutes = Math.floor(duration / 60000);
    const seconds = Math.floor((duration % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
  };

  const sidebarContent = (
    <div className="space-y-4">
      <div className="text-xs font-bold text-[var(--text-primary)] mb-2 px-1">
        Session Filters
      </div>

      <div className="space-y-1">
        {(['all', 'active', 'completed', 'failed', 'paused'] as SessionFilter[]).map((filterType) => (
          <button
            key={filterType}
            onClick={() => setFilter(filterType)}
            className={cn(
              "w-full px-2 py-1.5 text-xs text-left border rounded-sm capitalize",
              filter === filterType
                ? "bg-[var(--accent-color)] text-white border-[var(--accent-color)]"
                : "bg-[var(--bg-tertiary)] text-[var(--text-primary)] border-[var(--border-inset)] hover:bg-[#e8e5e0]"
            )}
          >
            {filterType === 'all' ? 'All Sessions' : `${filterType} Sessions`}
          </button>
        ))}
      </div>

      <div className="border-t border-[var(--border-inset)] pt-2 mt-4">
        <div className="text-xs font-bold text-[var(--text-primary)] mb-2 px-1">
          Actions
        </div>
        <button
          onClick={() => setSessions([])}
          className="w-full px-2 py-1.5 text-xs text-[var(--text-primary)] bg-[var(--bg-tertiary)] border border-[var(--border-inset)] rounded-sm hover:bg-[#e8e5e0] mb-1"
        >
          🔄 Refresh
        </button>
        <button
          onClick={killAllSessions}
          className="w-full px-2 py-1.5 text-xs text-red-600 bg-red-50 border border-red-200 rounded-sm hover:bg-red-100"
        >
          ⛔ Kill All
        </button>
      </div>

      <div className="text-xs font-bold text-[var(--text-primary)] mb-2 px-1">
        Statistics
      </div>
      <div className="px-2 py-1 bg-[var(--bg-tertiary)] border border-[var(--border-inset)] rounded-sm text-xs">
        <div className="flex justify-between">
          <span>Total:</span>
          <span>{sessions.length}</span>
        </div>
        <div className="flex justify-between">
          <span>Active:</span>
          <span>{sessions.filter(s => s.status === 'active').length}</span>
        </div>
        <div className="flex justify-between">
          <span>Completed:</span>
          <span>{sessions.filter(s => s.status === 'completed').length}</span>
        </div>
      </div>
    </div>
  );

  if (isLoading) {
    return (
      <MainLayout
        title="Session Manager"
        icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
        sidebarContent={sidebarContent}
      >
        <div className="h-full flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin w-8 h-8 border-4 border-[var(--primary-color)] border-t-transparent rounded-full mx-auto mb-4"></div>
            <div className="text-[var(--text-primary)]">Loading sessions...</div>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout
      title="Session Manager"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
      sidebarContent={sidebarContent}
    >
      <div className="h-full overflow-auto p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-2">
            🔄 Session Manager
          </h1>
          <p className="text-sm text-gray-600">
            Monitor and manage active problem-solving sessions
          </p>
        </div>

        {/* Sessions List */}
        {filteredSessions.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-4xl mb-4">📭</div>
            <div className="text-lg text-gray-500 mb-2">No sessions found</div>
            <div className="text-sm text-gray-400">
              {filter === 'all'
                ? 'Start a new session from the Home page to see it here'
                : `No ${filter} sessions available`
              }
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredSessions.map((session) => (
              <div
                key={session.id}
                className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm hover:shadow-sm transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-lg">{getStatusIcon(session.status)}</span>
                    <div>
                      <div className="font-medium text-[var(--text-primary)]">
                        Session {session.id}
                      </div>
                      <div className="text-xs text-gray-500">
                        Started {formatDuration(session.created_at)} ago
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={cn("px-2 py-1 text-xs rounded-sm", getStatusColor(session.status))}>
                      {session.status}
                    </span>
                    {session.status === 'active' && (
                      <button
                        onClick={() => killSession(session.id)}
                        className="px-2 py-1 text-xs text-red-600 bg-red-50 border border-red-200 rounded-sm hover:bg-red-100"
                      >
                        Kill
                      </button>
                    )}
                  </div>
                </div>

                <div className="mb-3">
                  <div className="text-sm text-[var(--text-primary)] mb-2">
                    <strong>Problem:</strong> {session.problem}
                  </div>
                  {session.solution && (
                    <div className="text-sm text-gray-600">
                      <strong>Solution:</strong> {session.solution}
                    </div>
                  )}
                </div>

                {session.progress !== undefined && (
                  <div className="mb-3">
                    <div className="flex justify-between text-xs text-gray-600 mb-1">
                      <span>Progress</span>
                      <span>{session.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-[var(--accent-color)] h-2 rounded-full"
                        style={{ width: `${session.progress}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                <div className="flex justify-between text-xs text-gray-500">
                  <span>Created: {new Date(session.created_at).toLocaleString()}</span>
                  <span>Updated: {new Date(session.updated_at).toLocaleString()}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Session Details Modal */}
        {selectedSession && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-6 rounded-sm max-w-2xl w-full mx-4 max-h-[80vh] overflow-auto">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-bold text-[var(--text-primary)]">
                  Session Details
                </h3>
                <button
                  onClick={() => setSelectedSession(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>
              <div className="space-y-3">
                <div>
                  <strong>ID:</strong> {selectedSession.id}
                </div>
                <div>
                  <strong>Status:</strong> {selectedSession.status}
                </div>
                <div>
                  <strong>Problem:</strong> {selectedSession.problem}
                </div>
                {selectedSession.solution && (
                  <div>
                    <strong>Solution:</strong> {selectedSession.solution}
                  </div>
                )}
                <div>
                  <strong>Progress:</strong> {selectedSession.progress}%
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
}
