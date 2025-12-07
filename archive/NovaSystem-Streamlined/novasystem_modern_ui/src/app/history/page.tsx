'use client';

import React, { useState, useEffect } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { cn } from '@/lib/utils';

interface HistorySession {
  id: string;
  problem: string;
  solution: string;
  status: 'completed' | 'failed';
  duration: number; // in seconds
  createdAt: string;
  completedAt: string;
  agent: string;
  domain: string;
  iterations: number;
}

export default function HistoryPage() {
  const [sessions, setSessions] = useState<HistorySession[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'date' | 'duration' | 'status'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedSession, setSelectedSession] = useState<HistorySession | null>(null);
  const itemsPerPage = 10;

  useEffect(() => {
    // Mock data for demonstration
    const mockSessions: HistorySession[] = [
      {
        id: 'hist_001',
        problem: 'Design a scalable e-commerce platform architecture',
        solution: 'Implemented a microservices architecture with API gateway, service mesh, and distributed data management. Included auto-scaling, load balancing, and fault tolerance mechanisms.',
        status: 'completed',
        duration: 1800, // 30 minutes
        createdAt: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
        completedAt: new Date(Date.now() - 84600000).toISOString(),
        agent: 'Problem Solver',
        domain: 'Technical',
        iterations: 15
      },
      {
        id: 'hist_002',
        problem: 'Create a marketing strategy for a new product launch',
        solution: 'Developed a comprehensive marketing strategy including market research, target audience analysis, pricing strategy, and multi-channel promotion plan.',
        status: 'completed',
        duration: 1200, // 20 minutes
        createdAt: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
        completedAt: new Date(Date.now() - 171600000).toISOString(),
        agent: 'Researcher',
        domain: 'Business',
        iterations: 12
      },
      {
        id: 'hist_003',
        problem: 'Optimize machine learning model performance',
        solution: 'Failed to optimize due to insufficient training data and computational resources. Recommended data augmentation and distributed training approaches.',
        status: 'failed',
        duration: 900, // 15 minutes
        createdAt: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
        completedAt: new Date(Date.now() - 258300000).toISOString(),
        agent: 'Analyst',
        domain: 'Technical',
        iterations: 8
      },
      {
        id: 'hist_004',
        problem: 'Write a creative story about space exploration',
        solution: 'Created an engaging science fiction story about a team of explorers discovering an ancient alien civilization on a distant planet, with themes of discovery, friendship, and the unknown.',
        status: 'completed',
        duration: 2400, // 40 minutes
        createdAt: new Date(Date.now() - 345600000).toISOString(), // 4 days ago
        completedAt: new Date(Date.now() - 343200000).toISOString(),
        agent: 'Synthesizer',
        domain: 'Creative',
        iterations: 20
      },
      {
        id: 'hist_005',
        problem: 'Analyze market trends for renewable energy sector',
        solution: 'Comprehensive analysis of renewable energy market trends, including solar, wind, and battery storage technologies. Identified key growth drivers and investment opportunities.',
        status: 'completed',
        duration: 1500, // 25 minutes
        createdAt: new Date(Date.now() - 432000000).toISOString(), // 5 days ago
        completedAt: new Date(Date.now() - 430500000).toISOString(),
        agent: 'Researcher',
        domain: 'Research',
        iterations: 18
      }
    ];

    setSessions(mockSessions);
  }, []);

  const filteredSessions = sessions.filter(session =>
    session.problem.toLowerCase().includes(searchQuery.toLowerCase()) ||
    session.solution.toLowerCase().includes(searchQuery.toLowerCase()) ||
    session.domain.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const sortedSessions = [...filteredSessions].sort((a, b) => {
    let comparison = 0;
    switch (sortBy) {
      case 'date':
        comparison = new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
        break;
      case 'duration':
        comparison = a.duration - b.duration;
        break;
      case 'status':
        comparison = a.status.localeCompare(b.status);
        break;
    }
    return sortOrder === 'asc' ? comparison : -comparison;
  });

  const totalPages = Math.ceil(sortedSessions.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedSessions = sortedSessions.slice(startIndex, startIndex + itemsPerPage);

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    } else {
      return `${secs}s`;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const exportHistory = () => {
    const dataStr = JSON.stringify(sortedSessions, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'novasystem-history.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  const sidebarContent = (
    <div className="space-y-4">
      <div className="text-xs font-bold text-[var(--text-primary)] mb-2 px-1">
        Filter & Sort
      </div>

      <div className="space-y-2">
        <div className="text-xs text-[var(--text-primary)] px-1">Sort By</div>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as 'date' | 'duration' | 'status')}
          className="w-full px-2 py-1 text-xs border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm"
        >
          <option value="date">Date</option>
          <option value="duration">Duration</option>
          <option value="status">Status</option>
        </select>

        <select
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value as 'asc' | 'desc')}
          className="w-full px-2 py-1 text-xs border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm"
        >
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
      </div>

      <div className="border-t border-[var(--border-inset)] pt-2 mt-4">
        <div className="text-xs font-bold text-[var(--text-primary)] mb-2 px-1">
          Actions
        </div>
        <button
          onClick={exportHistory}
          className="w-full px-2 py-1.5 text-xs text-[var(--text-primary)] bg-[var(--bg-tertiary)] border border-[var(--border-inset)] rounded-sm hover:bg-[#e8e5e0] mb-1"
        >
          📤 Export History
        </button>
        <button
          onClick={() => setSessions([])}
          className="w-full px-2 py-1.5 text-xs text-red-600 bg-red-50 border border-red-200 rounded-sm hover:bg-red-100"
        >
          🗑️ Clear History
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
          <span>Completed:</span>
          <span>{sessions.filter(s => s.status === 'completed').length}</span>
        </div>
        <div className="flex justify-between">
          <span>Failed:</span>
          <span>{sessions.filter(s => s.status === 'failed').length}</span>
        </div>
        <div className="flex justify-between">
          <span>Avg Duration:</span>
          <span>{formatDuration(Math.round(sessions.reduce((acc, s) => acc + s.duration, 0) / sessions.length))}</span>
        </div>
      </div>
    </div>
  );

  return (
    <MainLayout
      title="Session History"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
      sidebarContent={sidebarContent}
    >
      <div className="h-full overflow-auto p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-2">
            📋 Session History
          </h1>
          <p className="text-sm text-gray-600">
            View and manage completed problem-solving sessions
          </p>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search session history..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-2 border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] placeholder-gray-500 rounded-sm focus:outline-none focus:border-[var(--primary-color)]"
          />
        </div>

        {/* Sessions List */}
        {paginatedSessions.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-4xl mb-4">📭</div>
            <div className="text-lg text-gray-500 mb-2">No sessions found</div>
            <div className="text-sm text-gray-400">
              {searchQuery ? 'Try adjusting your search terms' : 'Complete some sessions to see them here'}
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {paginatedSessions.map((session) => (
              <div
                key={session.id}
                className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-4 rounded-sm hover:shadow-sm transition-shadow cursor-pointer"
                onClick={() => setSelectedSession(session)}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-lg">
                      {session.status === 'completed' ? '✅' : '❌'}
                    </span>
                    <div>
                      <div className="font-medium text-[var(--text-primary)]">
                        {session.domain} - {session.agent}
                      </div>
                      <div className="text-xs text-gray-500">
                        {formatDate(session.createdAt)} • {formatDuration(session.duration)} • {session.iterations} iterations
                      </div>
                    </div>
                  </div>
                  <span className={cn(
                    "px-2 py-1 text-xs rounded-sm",
                    session.status === 'completed'
                      ? "text-green-600 bg-green-100"
                      : "text-red-600 bg-red-100"
                  )}>
                    {session.status}
                  </span>
                </div>

                <div className="mb-3">
                  <div className="text-sm text-[var(--text-primary)] mb-2">
                    <strong>Problem:</strong> {session.problem}
                  </div>
                  <div className="text-sm text-gray-600">
                    <strong>Solution:</strong> {session.solution.length > 200
                      ? `${session.solution.substring(0, 200)}...`
                      : session.solution
                    }
                  </div>
                </div>

                <div className="flex justify-between text-xs text-gray-500">
                  <span>ID: {session.id}</span>
                  <span>Click to view details</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-center items-center gap-2 mt-6">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="px-3 py-1 text-xs border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="text-xs text-gray-600">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
              disabled={currentPage === totalPages}
              className="px-3 py-1 text-xs border border-[var(--border-inset)] bg-[var(--bg-tertiary)] text-[var(--text-primary)] rounded-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        )}

        {/* Session Details Modal */}
        {selectedSession && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-[var(--bg-tertiary)] border border-[var(--border-inset)] p-6 rounded-sm max-w-4xl w-full mx-4 max-h-[80vh] overflow-auto">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-bold text-[var(--text-primary)]">
                  Session Details - {selectedSession.id}
                </h3>
                <button
                  onClick={() => setSelectedSession(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <strong>Status:</strong> {selectedSession.status}
                  </div>
                  <div>
                    <strong>Domain:</strong> {selectedSession.domain}
                  </div>
                  <div>
                    <strong>Agent:</strong> {selectedSession.agent}
                  </div>
                  <div>
                    <strong>Duration:</strong> {formatDuration(selectedSession.duration)}
                  </div>
                  <div>
                    <strong>Iterations:</strong> {selectedSession.iterations}
                  </div>
                  <div>
                    <strong>Created:</strong> {formatDate(selectedSession.createdAt)}
                  </div>
                </div>
                <div>
                  <strong className="text-sm">Problem:</strong>
                  <p className="text-sm text-[var(--text-primary)] mt-1">{selectedSession.problem}</p>
                </div>
                <div>
                  <strong className="text-sm">Solution:</strong>
                  <p className="text-sm text-[var(--text-primary)] mt-1 whitespace-pre-wrap">{selectedSession.solution}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
}
