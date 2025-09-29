'use client';

import React, { useRef, useEffect } from 'react';
import { cn } from '@/lib/utils';
import { useStreaming } from './SimpleStreamingProvider';
import { XPCard } from '../ui/XPCard';
import { XPButton } from '../ui/XPButton';
import { XPInput } from '../ui/XPInput';

interface XPAgentResponseStreamProps {
  className?: string;
}

export const XPAgentResponseStream: React.FC<XPAgentResponseStreamProps> = ({ className }) => {
  const streamingContext = useStreaming();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Handle case where context might not be available during SSR
  if (!streamingContext) {
    return (
      <XPCard className={cn("flex flex-col h-full", className)} variant="outset">
        <XPCard.Header>
          <div className="flex items-center gap-2">
            <span className="text-lg">📡</span>
            <span className="font-bold">Loading...</span>
          </div>
        </XPCard.Header>
        <XPCard.Content className="flex-1 flex items-center justify-center">
          <div className="text-center text-[#666666]">
            <div className="text-2xl mb-2">⏳</div>
            <div className="text-sm">Initializing streaming...</div>
          </div>
        </XPCard.Content>
      </XPCard>
    );
  }

  const { responses, clearResponses, isStreaming, connectionStatus, searchFilter, setSearchFilter } = streamingContext;

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [responses]);

  const filteredResponses = responses.filter(response =>
    response.agentId.toLowerCase().includes(searchFilter.toLowerCase()) ||
    response.content.toLowerCase().includes(searchFilter.toLowerCase())
  );

  const getStatusColor = (status: 'streaming' | 'complete' | 'error') => {
    switch (status) {
      case 'streaming': return 'bg-[#0054e3]';
      case 'complete': return 'bg-[#6bbf44]';
      case 'error': return 'bg-[#ff4444]';
      default: return 'bg-[#808080]';
    }
  };

  const handleExport = () => {
    const dataStr = JSON.stringify(responses, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `agent_responses_${new Date().toISOString()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <XPCard className={cn("flex flex-col h-full", className)} variant="outset">
      <XPCard.Header>
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-lg">📡</span>
            <span className="font-bold">Live Agent Responses</span>
          </div>
          <div className="flex items-center gap-2">
            <span className={cn("w-2 h-2 rounded-full", connectionStatus === 'connected' ? 'bg-[#6bbf44]' : 'bg-[#ff4444]')}></span>
            <span className="text-xs text-black">{connectionStatus === 'connected' ? 'Connected' : 'Disconnected'}</span>
            <XPButton variant="default" size="sm" onClick={clearResponses}>
              Clear
            </XPButton>
            <XPButton variant="primary" size="sm" onClick={handleExport}>
              Export
            </XPButton>
          </div>
        </div>
      </XPCard.Header>
      <XPCard.Content className="flex-1 overflow-y-auto p-2 space-y-2">
        <div className="mb-2">
          <XPInput
            placeholder="Search responses..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            size="sm"
          />
        </div>
        {filteredResponses.length === 0 && !isStreaming && (
          <div className="text-center text-[#666666] py-8">
            <div className="text-2xl mb-2">🤖</div>
            <div className="text-sm">No responses yet. Start a workflow to see agent activity.</div>
          </div>
        )}
        {filteredResponses.map((response, index) => (
          <XPCard key={index} className="p-3" variant="inset">
            <div className="flex items-center justify-between text-xs text-[#666666] mb-2">
              <div className="flex items-center gap-2">
                <span className={cn("w-3 h-3 rounded-full", getStatusColor(response.status))}></span>
                <span className="font-bold text-black text-sm">{response.agentId}</span>
                <span className="text-xs bg-[#e0e0e0] px-2 py-1 rounded border border-[#c0c0c0]">
                  {response.status.toUpperCase()}
                </span>
              </div>
              <span className="text-xs font-mono">{new Date(response.timestamp).toLocaleTimeString()}</span>
            </div>
            <div className="bg-white p-2 border border-[#c0c0c0] rounded">
              <p className="text-sm text-black leading-relaxed whitespace-pre-wrap font-sans">
                {response.content}
              </p>
            </div>
          </XPCard>
        ))}
        {isStreaming && (
          <div className="flex items-center gap-2 text-sm text-[#666666]">
            <div className="animate-spin w-4 h-4 border-2 border-[#0054e3] border-t-transparent rounded-full"></div>
            <span>Streaming...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </XPCard.Content>
    </XPCard>
  );
};
