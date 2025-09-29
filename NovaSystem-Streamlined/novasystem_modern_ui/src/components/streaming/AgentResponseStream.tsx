'use client';

import React, { useState, useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

export interface AgentResponse {
  id: string;
  agentId: string;
  agentName: string;
  timestamp: Date;
  content: string;
  status: 'streaming' | 'complete' | 'error';
  type: 'text' | 'code' | 'data' | 'error';
}

interface AgentResponseStreamProps {
  responses: AgentResponse[];
  className?: string;
  maxHeight?: string;
  showTimestamps?: boolean;
  showAgentNames?: boolean;
  autoScroll?: boolean;
}

export const AgentResponseStream: React.FC<AgentResponseStreamProps> = ({
  responses,
  className,
  maxHeight = '400px',
  showTimestamps = true,
  showAgentNames = true,
  autoScroll = true
}) => {
  const [expandedResponses, setExpandedResponses] = useState<Set<string>>(new Set());
  const [filter, setFilter] = useState<string>('');
  const [filteredResponses, setFilteredResponses] = useState<AgentResponse[]>(responses);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Filter responses based on search
  useEffect(() => {
    if (!filter.trim()) {
      setFilteredResponses(responses);
    } else {
      const filtered = responses.filter(response =>
        response.content.toLowerCase().includes(filter.toLowerCase()) ||
        response.agentName.toLowerCase().includes(filter.toLowerCase())
      );
      setFilteredResponses(filtered);
    }
  }, [responses, filter]);

  // Auto-scroll to bottom when new responses arrive
  useEffect(() => {
    if (autoScroll && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [filteredResponses, autoScroll]);

  const toggleExpanded = (responseId: string) => {
    setExpandedResponses(prev => {
      const newSet = new Set(prev);
      if (newSet.has(responseId)) {
        newSet.delete(responseId);
      } else {
        newSet.add(responseId);
      }
      return newSet;
    });
  };

  const getStatusIcon = (status: AgentResponse['status']) => {
    switch (status) {
      case 'streaming':
        return <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />;
      case 'complete':
        return <div className="w-2 h-2 bg-green-500 rounded-full" />;
      case 'error':
        return <div className="w-2 h-2 bg-red-500 rounded-full" />;
    }
  };

  const getTypeIcon = (type: AgentResponse['type']) => {
    switch (type) {
      case 'text':
        return '📝';
      case 'code':
        return '💻';
      case 'data':
        return '📊';
      case 'error':
        return '❌';
    }
  };

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const truncateContent = (content: string, maxLength: number = 200) => {
    if (content.length <= maxLength) return content;
    return content.substring(0, maxLength) + '...';
  };

  return (
    <div className={cn("flex flex-col h-full", className)}>
      {/* Header with search and controls */}
      <div className="flex items-center justify-between p-3 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center gap-3">
          <h3 className="text-sm font-semibold text-gray-900">Agent Responses</h3>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
            <span className="text-xs text-gray-600">Live</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Search responses..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
          <span className="text-xs text-gray-500">
            {filteredResponses.length} of {responses.length}
          </span>
        </div>
      </div>

      {/* Response stream */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-3 space-y-3"
        style={{ maxHeight }}
      >
        {filteredResponses.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <div className="text-2xl mb-2">🤖</div>
            <div className="text-sm">No agent responses yet</div>
            <div className="text-xs">Responses will appear here as agents process your request</div>
          </div>
        ) : (
          filteredResponses.map((response) => {
            const isExpanded = expandedResponses.has(response.id);
            const isLongContent = response.content.length > 200;

            return (
              <div
                key={response.id}
                className={cn(
                  "border rounded-lg p-3 transition-all duration-200",
                  response.status === 'error'
                    ? "border-red-200 bg-red-50"
                    : response.status === 'complete'
                    ? "border-green-200 bg-green-50"
                    : "border-blue-200 bg-blue-50"
                )}
              >
                {/* Response header */}
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(response.status)}
                    {showAgentNames && (
                      <span className="text-sm font-medium text-gray-900">
                        {response.agentName}
                      </span>
                    )}
                    <span className="text-xs text-gray-500">
                      {getTypeIcon(response.type)}
                    </span>
                    {showTimestamps && (
                      <span className="text-xs text-gray-500">
                        {formatTimestamp(response.timestamp)}
                      </span>
                    )}
                  </div>

                  {isLongContent && (
                    <button
                      onClick={() => toggleExpanded(response.id)}
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      {isExpanded ? 'Show less' : 'Show more'}
                    </button>
                  )}
                </div>

                {/* Response content */}
                <div className="text-sm text-gray-800">
                  {response.type === 'code' ? (
                    <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">
                      <code>{isExpanded ? response.content : truncateContent(response.content)}</code>
                    </pre>
                  ) : (
                    <div className="whitespace-pre-wrap">
                      {isExpanded ? response.content : truncateContent(response.content)}
                    </div>
                  )}
                </div>

                {/* Streaming indicator */}
                {response.status === 'streaming' && (
                  <div className="mt-2 flex items-center gap-2">
                    <div className="flex gap-1">
                      <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" />
                      <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                      <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    </div>
                    <span className="text-xs text-blue-600">Streaming...</span>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Footer with export and clear options */}
      <div className="flex items-center justify-between p-3 border-t border-gray-200 bg-gray-50">
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              const data = JSON.stringify(responses, null, 2);
              const blob = new Blob([data], { type: 'application/json' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = `agent-responses-${new Date().toISOString().split('T')[0]}.json`;
              a.click();
              URL.revokeObjectURL(url);
            }}
            className="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            📥 Export
          </button>
          <button
            onClick={() => setFilteredResponses([])}
            className="px-2 py-1 text-xs bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            🗑️ Clear
          </button>
        </div>

        <div className="text-xs text-gray-500">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};
