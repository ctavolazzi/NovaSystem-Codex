'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { AgentResponse } from './AgentResponseStream';

interface StreamingContextType {
  responses: AgentResponse[];
  addResponse: (response: Omit<AgentResponse, 'id' | 'timestamp'>) => void;
  updateResponse: (id: string, updates: Partial<AgentResponse>) => void;
  clearResponses: () => void;
  isConnected: boolean;
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error';
  isStreaming: boolean;
  setIsStreaming: (streaming: boolean) => void;
  searchFilter: string;
  setSearchFilter: (filter: string) => void;
}

const StreamingContext = createContext<StreamingContextType | undefined>(undefined);

export const useStreaming = () => {
  const context = useContext(StreamingContext);
  if (!context) {
    throw new Error('useStreaming must be used within a StreamingProvider');
  }
  return context;
};

interface StreamingProviderProps {
  children: React.ReactNode;
  websocketUrl?: string;
}

export const StreamingProvider: React.FC<StreamingProviderProps> = ({
  children,
  websocketUrl = 'ws://localhost:8000/ws'
}) => {
  const [responses, setResponses] = useState<AgentResponse[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
  const [isStreaming, setIsStreaming] = useState(false);
  const [searchFilter, setSearchFilter] = useState('');
  const [ws, setWs] = useState<WebSocket | null>(null);

  // WebSocket connection management
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        setConnectionStatus('connecting');
        const websocket = new WebSocket(websocketUrl);

        websocket.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
          setConnectionStatus('connected');
          setWs(websocket);
        };

        websocket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        websocket.onclose = () => {
          console.log('WebSocket disconnected');
          setIsConnected(false);
          setConnectionStatus('disconnected');
          setWs(null);

          // Attempt to reconnect after 3 seconds
          setTimeout(() => {
            if (connectionStatus !== 'connected') {
              connectWebSocket();
            }
          }, 3000);
        };

        websocket.onerror = (error) => {
          console.error('WebSocket error:', error);
          setConnectionStatus('error');
          setIsConnected(false);
        };

      } catch (error) {
        console.error('Failed to create WebSocket connection:', error);
        setConnectionStatus('error');
      }
    };

    connectWebSocket();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [websocketUrl]);

  const handleWebSocketMessage = useCallback((data: any) => {
    switch (data.type) {
      case 'agent_response_start':
        addResponse({
          agentId: data.agentId,
          agentName: data.agentName,
          content: '',
          status: 'streaming',
          type: data.contentType || 'text'
        });
        break;

      case 'agent_response_chunk':
        updateResponse(data.responseId, {
          content: data.content,
          status: 'streaming'
        });
        break;

      case 'agent_response_complete':
        updateResponse(data.responseId, {
          content: data.content,
          status: 'complete'
        });
        break;

      case 'agent_response_error':
        updateResponse(data.responseId, {
          content: data.error,
          status: 'error',
          type: 'error'
        });
        break;

      default:
        console.log('Unknown WebSocket message type:', data.type);
    }
  }, []);

  const addResponse = useCallback((responseData: Omit<AgentResponse, 'id' | 'timestamp'>) => {
    const newResponse: AgentResponse = {
      ...responseData,
      id: `response_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date()
    };

    setResponses(prev => [...prev, newResponse]);
  }, []);

  const updateResponse = useCallback((id: string, updates: Partial<AgentResponse>) => {
    setResponses(prev =>
      prev.map(response =>
        response.id === id
          ? { ...response, ...updates }
          : response
      )
    );
  }, []);

  const clearResponses = useCallback(() => {
    setResponses([]);
  }, []);

  // Simulate agent responses for development/testing
  const simulateAgentResponse = useCallback((agentName: string, content: string) => {
    const responseId = `sim_${Date.now()}`;

    // Start response
    addResponse({
      agentId: `agent_${agentName.toLowerCase().replace(/\s+/g, '_')}`,
      agentName,
      content: '',
      status: 'streaming',
      type: 'text'
    });

    // Simulate streaming
    let currentContent = '';
    const words = content.split(' ');
    let wordIndex = 0;

    const streamInterval = setInterval(() => {
      if (wordIndex < words.length) {
        currentContent += (wordIndex > 0 ? ' ' : '') + words[wordIndex];
        wordIndex++;

        // Find the most recent response from this agent
        setResponses(prev => {
          const updated = [...prev];
          const lastResponse = updated[updated.length - 1];
          if (lastResponse && lastResponse.agentName === agentName) {
            lastResponse.content = currentContent;
          }
          return updated;
        });
      } else {
        clearInterval(streamInterval);

        // Mark as complete
        setResponses(prev => {
          const updated = [...prev];
          const lastResponse = updated[updated.length - 1];
          if (lastResponse && lastResponse.agentName === agentName) {
            lastResponse.status = 'complete';
          }
          return updated;
        });
      }
    }, 100); // Stream one word every 100ms
  }, [addResponse]);

  // Expose simulation function for development
  const contextValue: StreamingContextType = {
    responses,
    addResponse,
    updateResponse,
    clearResponses,
    isConnected,
    connectionStatus,
    isStreaming,
    setIsStreaming,
    searchFilter,
    setSearchFilter
  };

  // Add simulation function to window for development
  useEffect(() => {
    if (typeof window !== 'undefined') {
      (window as any).simulateAgentResponse = simulateAgentResponse;
    }
  }, [simulateAgentResponse]);

  return (
    <StreamingContext.Provider value={contextValue}>
      {children}
    </StreamingContext.Provider>
  );
};
