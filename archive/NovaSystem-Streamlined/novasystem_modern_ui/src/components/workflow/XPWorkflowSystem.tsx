'use client';

import React, { useState, useCallback, useEffect, useRef } from 'react';
import { XPCard } from '../ui/XPCard';
import { XPButton } from '../ui/XPButton';
import { XPTextArea } from '../ui/XPInput';
import { XPAgentResponseStream } from '../streaming/XPAgentResponseStream';
import { useStreaming } from '../streaming/SimpleStreamingProvider';
import { WorkflowCanvas, Connection as WorkflowConnection } from './WorkflowCanvas/WorkflowCanvas';
import { WorkflowNodeData } from './WorkflowNode/WorkflowNode';
import { executeWorkflow, WorkflowConnectionPayload, WorkflowNodePayload } from '@/services/workflowApi';
import { useWorkflowPolling } from '@/hooks/useWorkflowPolling';
import { cn } from '@/lib/utils';

interface Agent {
  id: string;
  name: string;
  type: string;
  description: string;
  version: string;
  status: 'idle' | 'active' | 'error' | 'complete';
  icon: string;
}

const MOCK_AGENTS: Agent[] = [
  { id: 'agent-1', name: 'Problem Solver', type: 'problemSolver', description: 'Analyzes problems', version: '1.2.0', status: 'idle', icon: '🧠' },
  { id: 'agent-2', name: 'Research Agent', type: 'research', description: 'Gathers information', version: '2.1.0', status: 'idle', icon: '🔍' },
  { id: 'agent-3', name: 'Data Analyst', type: 'analysis', description: 'Analyzes data', version: '1.8.0', status: 'idle', icon: '📊' },
  { id: 'agent-4', name: 'Synthesizer', type: 'synthesizer', description: 'Combines insights', version: '1.5.0', status: 'idle', icon: '🔗' },
  { id: 'agent-5', name: 'Data Processor', type: 'data', description: 'Handles data', version: '2.0.0', status: 'idle', icon: '📈' },
  { id: 'agent-6', name: 'Optimizer', type: 'optimization', description: 'Optimizes processes', version: '1.3.0', status: 'idle', icon: '⚡' }
];

const mapBackendStateToNodeStatus = (state?: string): WorkflowNodeData['status'] => {
  switch (state) {
    case 'processing':
      return 'processing';
    case 'completed':
      return 'complete';
    case 'error':
      return 'error';
    default:
      return 'idle';
  }
};

const mapBackendStateToConnectionStatus = (state?: string): WorkflowConnection['status'] => {
  switch (state) {
    case 'processing':
      return 'active';
    case 'completed':
      return 'success';
    case 'error':
      return 'error';
    default:
      return 'idle';
  }
};

export const XPWorkflowSystem: React.FC = () => {
  const [problemStatement, setProblemStatement] = useState('');
  const [selectedAgents, setSelectedAgents] = useState<Agent[]>([]);
  const [workflowStatus, setWorkflowStatus] = useState<'idle' | 'running' | 'paused' | 'completed' | 'error'>('idle');
  const [activeTab, setActiveTab] = useState<'status' | 'responses' | 'results'>('status');
  const [canvasNodes, setCanvasNodes] = useState<WorkflowNodeData[]>([]);
  const [canvasConnections, setCanvasConnections] = useState<WorkflowConnection[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isStarting, setIsStarting] = useState(false);
  const { addResponse, setIsStreaming, clearResponses } = useStreaming();
  const { nodeStates, nodeOutputs, isComplete, error: pollingError, sessionStatus } = useWorkflowPolling(sessionId);
  const previousOutputsRef = useRef<Record<string, string>>({});

  const handleAgentToggle = useCallback((agent: Agent) => {
    setSelectedAgents(prev =>
      prev.some(a => a.id === agent.id)
        ? prev.filter(a => a.id !== agent.id)
        : [...prev, agent]
    );
  }, []);

  const buildCanvasNodes = useCallback((): WorkflowNodeData[] => {
    const timestamp = Date.now();

    return selectedAgents.map((agent, index) => {
      const column = index % 3;
      const row = Math.floor(index / 3);

      return {
        id: `node-${agent.id}-${timestamp}-${index}`,
        type: agent.type,
        name: agent.name,
        description: agent.description,
        status: 'idle',
        position: {
          x: 60 + column * 220,
          y: 60 + row * 160
        },
        inputs: ['input'],
        outputs: ['output'],
        data: { agentId: agent.id }
      };
    });
  }, [selectedAgents]);

  const generateConnections = useCallback((nodes: WorkflowNodeData[]): WorkflowConnection[] => (
    nodes.slice(0, -1).map((node, index) => ({
      id: `conn-${node.id}-${nodes[index + 1].id}`,
      fromNodeId: node.id,
      toNodeId: nodes[index + 1].id,
      fromPort: node.outputs[0] || 'output',
      toPort: nodes[index + 1].inputs[0] || 'input',
      status: 'idle'
    }))
  ), []);

  const handleNodePositionChange = useCallback((nodeId: string, position: { x: number; y: number }) => {
    setCanvasNodes(prev => prev.map(node =>
      node.id === nodeId ? { ...node, position } : node
    ));
  }, []);

  const handleConnectionCreate = useCallback((fromNodeId: string, toNodeId: string, fromPort: string, toPort: string) => {
    setCanvasConnections(prev => {
      if (prev.some(conn => conn.fromNodeId === fromNodeId && conn.toNodeId === toNodeId)) {
        return prev;
      }

      return [
        ...prev,
        {
          id: `conn-${fromNodeId}-${toNodeId}`,
          fromNodeId,
          toNodeId,
          fromPort,
          toPort,
          status: 'idle'
        }
      ];
    });
  }, []);

  const handleConnectionDelete = useCallback((connectionId: string) => {
    setCanvasConnections(prev => prev.filter(conn => conn.id !== connectionId));
  }, []);

  const startWorkflow = useCallback(async () => {
    if (!problemStatement.trim()) {
      alert('Please enter a problem statement.');
      return;
    }
    if (selectedAgents.length === 0) {
      alert('Please select at least one agent.');
      return;
    }

    setWorkflowStatus('running');
    setActiveTab('status');
    setIsStreaming(true);
    clearResponses();
    setIsStarting(true);
    previousOutputsRef.current = {};

    const nodes = buildCanvasNodes();
    const connections = generateConnections(nodes);

    setCanvasNodes(nodes);
    setCanvasConnections(connections);

    const nodePayloads: WorkflowNodePayload[] = nodes.map(node => ({
      id: node.id,
      type: node.type,
      title: problemStatement,
      agent: node.name,
      metadata: {
        description: node.description,
        agentId: node.data?.agentId
      }
    }));

    const connectionPayloads: WorkflowConnectionPayload[] = connections.map(conn => ({
      from: conn.fromNodeId,
      to: conn.toNodeId
    }));

    try {
      const response = await executeWorkflow(nodePayloads, connectionPayloads);
      setSessionId(response.session_id);
    } catch (error) {
      console.error('Failed to start workflow', error);
      setWorkflowStatus('error');
      setIsStreaming(false);
      setSessionId(null);
      const message = error instanceof Error ? error.message : 'Failed to start workflow';
      addResponse({
        agentId: 'System',
        content: message,
        timestamp: Date.now(),
        status: 'error'
      });
    } finally {
      setIsStarting(false);
    }
  }, [addResponse, buildCanvasNodes, clearResponses, generateConnections, problemStatement, selectedAgents.length, setIsStreaming]);

  const stopWorkflow = useCallback(() => {
    setWorkflowStatus('idle');
    setIsStreaming(false);
    setSessionId(null);
    addResponse({
      agentId: 'System',
      content: 'Workflow stopped by user.',
      timestamp: Date.now(),
      status: 'complete',
    });
  }, [addResponse, setIsStreaming]);

  const resetWorkflow = useCallback(() => {
    setProblemStatement('');
    setSelectedAgents([]);
    setWorkflowStatus('idle');
    setSessionId(null);
    setCanvasNodes([]);
    setCanvasConnections([]);
    previousOutputsRef.current = {};
    clearResponses();
    setIsStreaming(false);
    setActiveTab('status');
  }, [clearResponses, setIsStreaming]);

  const getAgentNodeStatus = useCallback((agentId: string): WorkflowNodeData['status'] => {
    const node = canvasNodes.find(n => n.data?.agentId === agentId);
    return node?.status || 'idle';
  }, [canvasNodes]);

  useEffect(() => {
    if (!canvasNodes.length) return;

    setCanvasNodes(prev => prev.map(node => {
      const backendState = nodeStates[node.id];
      if (!backendState) return node;

      return {
        ...node,
        status: mapBackendStateToNodeStatus(backendState)
      };
    }));
  }, [nodeStates, canvasNodes.length]);

  useEffect(() => {
    if (!canvasConnections.length) return;

    setCanvasConnections(prev => prev.map(conn => ({
      ...conn,
      status: mapBackendStateToConnectionStatus(nodeStates[conn.fromNodeId])
    })));
  }, [nodeStates, canvasConnections.length]);

  useEffect(() => {
    if (!sessionId) return;

    if (pollingError) {
      setWorkflowStatus('error');
      setIsStreaming(false);
      return;
    }

    const nodeStateValues = Object.values(nodeStates);
    const hasErrors = nodeStateValues.some(state => state === 'error') || sessionStatus === 'error';
    const allFinished = nodeStateValues.length > 0 && nodeStateValues.every(
      state => state === 'completed' || state === 'error'
    );

    if (isComplete || allFinished) {
      setWorkflowStatus(hasErrors ? 'error' : 'completed');
      setIsStreaming(false);
    } else {
      setWorkflowStatus('running');
    }
  }, [isComplete, nodeStates, pollingError, sessionId, sessionStatus, setIsStreaming]);

  useEffect(() => {
    if (!sessionId) return;

    Object.entries(nodeOutputs).forEach(([nodeId, output]) => {
      if (!output || previousOutputsRef.current[nodeId] === output) {
        return;
      }

      previousOutputsRef.current[nodeId] = output;
      const node = canvasNodes.find(n => n.id === nodeId);

      addResponse({
        agentId: node?.name || nodeId,
        content: output,
        timestamp: Date.now(),
        status: 'complete'
      });
    });
  }, [addResponse, canvasNodes, nodeOutputs, sessionId]);

  return (
    <div className="flex h-full gap-4 p-4 bg-[#ece9d8]">
      {/* Left Panel: Workflow Configuration */}
      <XPCard className="w-1/3 flex flex-col" variant="outset">
        <XPCard.Header>
          <div className="flex items-center gap-2">
            <span className="text-lg">⚙️</span>
            <span>Workflow Configuration</span>
          </div>
        </XPCard.Header>
        <XPCard.Content className="flex-1 overflow-y-auto space-y-4">
          <div>
            <XPTextArea
              label="Problem Statement"
              placeholder="Describe the problem you want to solve..."
              value={problemStatement}
              onChange={(e) => setProblemStatement(e.target.value)}
              disabled={workflowStatus === 'running' || isStarting}
              rows={4}
            />
          </div>

          <div>
            <h3 className="text-sm font-bold text-black mb-2">Select Agents</h3>
            <div className="grid grid-cols-2 gap-2">
              {MOCK_AGENTS.map(agent => (
                <XPCard
                  key={agent.id}
                  className={cn(
                    "p-2 cursor-pointer transition-all duration-100",
                    selectedAgents.some(a => a.id === agent.id)
                      ? "border-[#0054e3] bg-[#e6f2ff]"
                      : "border-[#c0c0c0] hover:bg-[#f0f0f0]"
                  )}
                  variant="outset"
                  onClick={() => handleAgentToggle(agent)}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm">{agent.icon}</span>
                    <span className="font-medium text-black text-xs">{agent.name}</span>
                  </div>
                  <p className="text-xs text-[#666666]">{agent.description}</p>
                </XPCard>
              ))}
            </div>
          </div>
        </XPCard.Content>
        <XPCard.Footer>
          <XPButton variant="default" onClick={resetWorkflow} disabled={workflowStatus === 'running' || isStarting}>
            Reset
          </XPButton>
          {workflowStatus === 'running' ? (
            <XPButton variant="danger" onClick={stopWorkflow}>
              Stop Workflow
            </XPButton>
          ) : (
            <XPButton
              variant="primary"
              onClick={startWorkflow}
              disabled={!problemStatement.trim() || selectedAgents.length === 0 || isStarting}
            >
              {isStarting ? 'Starting...' : 'Start Workflow'}
            </XPButton>
          )}
        </XPCard.Footer>
      </XPCard>

      {/* Right Panel: Workflow Execution & Responses */}
      <XPCard className="w-2/3 flex flex-col" variant="outset">
        <XPCard.Header>
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <span className="text-lg">🔄</span>
              <span>Workflow Execution</span>
            </div>
            <div className="flex gap-1">
              <XPButton
                variant={activeTab === 'status' ? 'primary' : 'default'}
                onClick={() => setActiveTab('status')}
                size="sm"
              >
                Status
              </XPButton>
              <XPButton
                variant={activeTab === 'responses' ? 'primary' : 'default'}
                onClick={() => setActiveTab('responses')}
                size="sm"
              >
                Responses
              </XPButton>
              <XPButton
                variant={activeTab === 'results' ? 'primary' : 'default'}
                onClick={() => setActiveTab('results')}
                size="sm"
              >
                Results
              </XPButton>
            </div>
          </div>
        </XPCard.Header>
        <XPCard.Content className="flex-1 overflow-hidden flex flex-col gap-3">
          <div className="flex-1 overflow-hidden">
            {activeTab === 'status' && (
              <div className="h-full flex flex-col space-y-4 overflow-y-auto">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-black">Current Status:</span>
                  <span className={cn(
                    "text-sm font-bold capitalize",
                    workflowStatus === 'running' && "text-[#0054e3]",
                    workflowStatus === 'completed' && "text-[#6bbf44]",
                    workflowStatus === 'error' && "text-[#ff4444]"
                  )}>
                    {workflowStatus}
                  </span>
                  {sessionId && (
                    <span className="text-[11px] text-[#3a3a3a] ml-2">Session {sessionId.slice(0, 8)}</span>
                  )}
                </div>
                <div className="grid grid-cols-2 gap-3">
                  {selectedAgents.map(agent => {
                    const nodeStatus = getAgentNodeStatus(agent.id);
                    const statusText = nodeStatus === 'processing'
                      ? 'Processing...'
                      : nodeStatus === 'complete'
                        ? 'Complete'
                        : nodeStatus === 'error'
                          ? 'Error'
                          : 'Idle';

                    const dotClass = nodeStatus === 'processing'
                      ? "bg-[#0054e3] animate-pulse"
                      : nodeStatus === 'complete'
                        ? "bg-[#6bbf44]"
                        : nodeStatus === 'error'
                          ? "bg-[#ff4444]"
                          : "bg-[#808080]";

                    return (
                      <XPCard key={agent.id} className="p-2" variant="inset">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm">{agent.icon}</span>
                          <span className="font-medium text-black text-xs">{agent.name}</span>
                        </div>
                        <p className="text-xs text-[#666666] mb-2">{agent.description}</p>
                        <div className="flex items-center gap-2">
                          <span className={cn("w-2 h-2 rounded-full", dotClass)}></span>
                          <span className="text-xs text-[#666666]">
                            {statusText}
                          </span>
                        </div>
                      </XPCard>
                    );
                  })}
                </div>
              </div>
            )}
            {activeTab === 'responses' && (
              <div className="h-full">
                <XPAgentResponseStream className="h-full" />
              </div>
            )}
            {activeTab === 'results' && (
              <div className="h-full flex items-center justify-center text-[#666666]">
                <div className="text-center">
                  <div className="text-4xl mb-2">📊</div>
                  <p className="text-sm">Workflow results will appear here after completion.</p>
                </div>
              </div>
            )}
          </div>

          <div className="h-[360px] border border-[#c0c0c0] bg-white shadow-inner rounded-sm overflow-hidden">
            <div className="flex items-center justify-between px-3 py-2 border-b border-[#c0c0c0] bg-[#f3f3f3] text-xs text-black">
              <div className="font-bold">Workflow Canvas</div>
              {sessionId && (
                <div className="text-[#0054e3] font-semibold text-[11px]">
                  Live from session {sessionId.slice(0, 8)}
                </div>
              )}
            </div>
            <div className="h-[300px]">
              <WorkflowCanvas
                nodes={canvasNodes}
                connections={canvasConnections}
                onNodePositionChange={handleNodePositionChange}
                onConnectionCreate={handleConnectionCreate}
                onConnectionDelete={handleConnectionDelete}
                className="h-full"
              />
            </div>
          </div>
        </XPCard.Content>
      </XPCard>
    </div>
  );
};
