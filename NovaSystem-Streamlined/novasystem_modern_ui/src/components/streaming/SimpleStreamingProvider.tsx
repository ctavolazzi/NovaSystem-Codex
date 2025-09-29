'use client';

import React, { createContext, useContext, useState, useCallback } from 'react';
import { SimpleAgentResponse } from './SimpleAgentResponse';

interface SimpleStreamingContextType {
  responses: SimpleAgentResponse[];
  addResponse: (response: SimpleAgentResponse) => void;
  clearResponses: () => void;
  isStreaming: boolean;
  setIsStreaming: (streaming: boolean) => void;
  connectionStatus: 'connected' | 'disconnected';
  searchFilter: string;
  setSearchFilter: (filter: string) => void;
}

const SimpleStreamingContext = createContext<SimpleStreamingContextType | undefined>(undefined);

export const useStreaming = () => {
  const context = useContext(SimpleStreamingContext);
  if (!context) {
    // Return a default context to prevent hydration errors
    return {
      responses: [],
      addResponse: () => {},
      clearResponses: () => {},
      isStreaming: false,
      setIsStreaming: () => {},
      connectionStatus: 'disconnected' as const,
      searchFilter: '',
      setSearchFilter: () => {},
    };
  }
  return context;
};

interface SimpleStreamingProviderProps {
  children: React.ReactNode;
}

export const StreamingProvider: React.FC<SimpleStreamingProviderProps> = ({ children }) => {
  const [responses, setResponses] = useState<SimpleAgentResponse[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected'>('connected');
  const [searchFilter, setSearchFilter] = useState('');
  const [isClient, setIsClient] = useState(false);

  // Ensure we're on the client side to prevent hydration mismatches
  React.useEffect(() => {
    setIsClient(true);
  }, []);

  const addResponse = useCallback((newResponse: SimpleAgentResponse) => {
    setResponses(prevResponses => {
      const existingIndex = prevResponses.findIndex(
        (res) => res.agentId === newResponse.agentId && res.status === 'streaming'
      );

      if (existingIndex !== -1) {
        const updatedResponses = [...prevResponses];
        updatedResponses[existingIndex] = {
          ...updatedResponses[existingIndex],
          content: newResponse.content,
          timestamp: newResponse.timestamp,
          status: newResponse.status,
        };
        return updatedResponses;
      } else {
        return [...prevResponses, newResponse];
      }
    });
  }, []);

  const clearResponses = useCallback(() => {
    setResponses([]);
  }, []);

  const value = {
    responses,
    addResponse,
    clearResponses,
    isStreaming,
    setIsStreaming,
    connectionStatus,
    searchFilter,
    setSearchFilter,
  };

  // Don't render streaming context on server side to prevent hydration mismatches
  if (!isClient) {
    return <>{children}</>;
  }

  return (
    <SimpleStreamingContext.Provider value={value}>
      {children}
    </SimpleStreamingContext.Provider>
  );
};
