'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { getWorkflowStatus, WorkflowStatusResponse } from '@/services/workflowApi';

export interface PollingState {
  nodeStates: Record<string, 'pending' | 'processing' | 'completed' | 'error'>;
  nodeOutputs: Record<string, string>;
  executionOrder: string[];
  sessionStatus: 'running' | 'completed' | 'error' | null;
  isComplete: boolean;
  isError: boolean;
  error: string | null;
  isPolling: boolean;
}

const initialState: PollingState = {
  nodeStates: {},
  nodeOutputs: {},
  executionOrder: [],
  sessionStatus: null,
  isComplete: false,
  isError: false,
  error: null,
  isPolling: false,
};

/**
 * Custom hook for polling workflow status from the backend
 *
 * @param sessionId - The workflow session ID to poll (null to stop polling)
 * @param interval - Polling interval in milliseconds (default: 2000ms)
 * @returns PollingState with node states, outputs, and completion status
 */
export function useWorkflowPolling(
  sessionId: string | null,
  interval: number = 2000
): PollingState {
  const [state, setState] = useState<PollingState>(initialState);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const isMountedRef = useRef(true);

  const poll = useCallback(async () => {
    if (!sessionId) return;

    try {
      const response: WorkflowStatusResponse = await getWorkflowStatus(sessionId);

      if (!isMountedRef.current) return;

      const isComplete = response.status === 'completed';
      const isError = response.status === 'error';

      setState({
        nodeStates: response.node_states,
        nodeOutputs: response.node_outputs,
        executionOrder: response.execution_order,
        sessionStatus: response.status,
        isComplete,
        isError,
        error: null,
        isPolling: !isComplete && !isError,
      });

      // Stop polling if complete or error
      if (isComplete || isError) {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      }
    } catch (err) {
      if (!isMountedRef.current) return;

      setState(prev => ({
        ...prev,
        isError: true,
        error: err instanceof Error ? err.message : 'Unknown error',
        isPolling: false,
      }));

      // Stop polling on error
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
  }, [sessionId]);

  useEffect(() => {
    isMountedRef.current = true;

    if (sessionId) {
      // Reset state when session changes
      setState({
        ...initialState,
        isPolling: true,
      });

      // Initial poll
      poll();

      // Start interval polling
      intervalRef.current = setInterval(poll, interval);
    } else {
      // No session, reset state
      setState(initialState);
    }

    return () => {
      isMountedRef.current = false;
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [sessionId, interval, poll]);

  return state;
}

export default useWorkflowPolling;
