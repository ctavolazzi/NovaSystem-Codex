'use client';

import React, { useState, useCallback } from 'react';
import { WorkflowSidebar, WorkflowStatus } from './WorkflowSidebar/WorkflowSidebar';
import { WorkflowCanvas, Connection } from './WorkflowCanvas/WorkflowCanvas';
import { WorkflowNodeData } from './WorkflowNode/WorkflowNode';
import { Agent } from './AgentCard/AgentCard';

export interface WorkflowSystemProps {
  className?: string;
}

// Mock data for demonstration
const MOCK_AGENTS: Agent[] = [
  {
    id: 'agent-1',
    name: 'Problem Solver',
    type: 'problemSolver',
    description: 'Analyzes complex problems and breaks them down into manageable components',
    version: '1.2.0',
    status: 'idle',
    icon: '🧠'
  },
  {
    id: 'agent-2',
    name: 'Research Agent',
    type: 'research',
    description: 'Gathers and analyzes relevant information from various sources',
    version: '2.1.0',
    status: 'idle',
    icon: '🔍'
  },
  {
    id: 'agent-3',
    name: 'Data Analyst',
    type: 'analysis',
    description: 'Performs detailed analysis and evaluation of data patterns',
    version: '1.8.0',
    status: 'idle',
    icon: '📊'
  },
  {
    id: 'agent-4',
    name: 'Synthesizer',
    type: 'synthesizer',
    description: 'Combines insights and solutions into comprehensive results',
    version: '1.5.0',
    status: 'idle',
    icon: '🔗'
  },
  {
    id: 'agent-5',
    name: 'Data Processor',
    type: 'data',
    description: 'Handles data processing, transformation, and validation',
    version: '2.0.0',
    status: 'idle',
    icon: '📈'
  },
  {
    id: 'agent-6',
    name: 'Optimizer',
    type: 'optimization',
    description: 'Optimizes processes, algorithms, and resource utilization',
    version: '1.3.0',
    status: 'idle',
    icon: '⚡'
  }
];

export const WorkflowSystem: React.FC<WorkflowSystemProps> = ({ className = '' }) => {
  // State management
  const [agents] = useState<Agent[]>(MOCK_AGENTS);
  const [nodes, setNodes] = useState<WorkflowNodeData[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [selectedNodes, setSelectedNodes] = useState<string[]>([]);
  const [workflowStatus, setWorkflowStatus] = useState<WorkflowStatus>({
    status: 'idle',
    message: 'Ready to start workflow',
    details: 'Drag agents from the sidebar to the canvas to build your workflow'
  });
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [canvasZoom, setCanvasZoom] = useState(1);
  const [canvasPan, setCanvasPan] = useState({ x: 0, y: 0 });

  // Agent to node conversion
  const convertAgentToNode = useCallback((agent: Agent): WorkflowNodeData => {
    const nodeId = `node-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    return {
      id: nodeId,
      type: agent.type,
      name: agent.name,
      description: agent.description,
      status: 'idle',
      position: {
        x: Math.random() * 400 + 100,
        y: Math.random() * 300 + 100
      },
      inputs: ['input'],
      outputs: ['output'],
      data: { agentId: agent.id }
    };
  }, []);

  // Event handlers
  const handleAgentSelect = useCallback((agent: Agent) => {
    console.log('Agent selected:', agent);
    // Could open agent configuration modal or show details
  }, []);

  const handleAgentDragStart = useCallback((agent: Agent, event: React.DragEvent) => {
    console.log('Agent drag start:', agent);
    // Set drag data
    event.dataTransfer.setData('application/json', JSON.stringify({
      type: 'agent',
      agent: agent
    }));
  }, []);

  const handleAgentDragEnd = useCallback((agent: Agent) => {
    console.log('Agent drag end:', agent);
    // Handle drop on canvas if needed
  }, []);

  const handleNodeSelect = useCallback((nodeId: string) => {
    setSelectedNodes(prev => {
      if (prev.includes(nodeId)) {
        return prev.filter(id => id !== nodeId);
      } else {
        return [...prev, nodeId];
      }
    });
  }, []);

  const handleNodePositionChange = useCallback((nodeId: string, position: { x: number; y: number }) => {
    setNodes(prev => prev.map(node =>
      node.id === nodeId ? { ...node, position } : node
    ));
  }, []);

  const handleConnectionCreate = useCallback((fromNodeId: string, toNodeId: string, fromPort: string, toPort: string) => {
    const connectionId = `conn-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const newConnection: Connection = {
      id: connectionId,
      fromNodeId,
      toNodeId,
      fromPort,
      toPort,
      status: 'idle'
    };
    setConnections(prev => [...prev, newConnection]);
    console.log('Connection created:', newConnection);
  }, []);

  const handleConnectionDelete = useCallback((connectionId: string) => {
    setConnections(prev => prev.filter(conn => conn.id !== connectionId));
    console.log('Connection deleted:', connectionId);
  }, []);

  const handleCanvasClick = useCallback((position: { x: number; y: number }) => {
    setSelectedNodes([]);
    console.log('Canvas clicked at:', position);
  }, []);

  const handleCanvasDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    const data = event.dataTransfer.getData('application/json');

    try {
      const { type, agent } = JSON.parse(data);
      if (type === 'agent' && agent) {
        const rect = event.currentTarget.getBoundingClientRect();
        const position = {
          x: (event.clientX - rect.left - canvasPan.x) / canvasZoom,
          y: (event.clientY - rect.top - canvasPan.y) / canvasZoom
        };

        const newNode = {
          ...convertAgentToNode(agent),
          position
        };

        setNodes(prev => [...prev, newNode]);
        console.log('Agent dropped on canvas:', agent, position);
      }
    } catch (err) {
      console.error('Error parsing drop data:', err);
    }
  }, [canvasPan, canvasZoom, convertAgentToNode]);

  const handleCanvasDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
  }, []);

  const handleWorkflowStart = useCallback(() => {
    if (nodes.length === 0) {
      setWorkflowStatus({
        status: 'error',
        message: 'No nodes to execute',
        details: 'Please add some agents to the canvas before starting the workflow'
      });
      return;
    }

    setWorkflowStatus({
      status: 'processing',
      message: 'Workflow running...',
      progress: 0,
      details: 'Executing workflow steps'
    });

    // Simulate workflow execution
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 10;
      if (progress >= 100) {
        progress = 100;
        setWorkflowStatus({
          status: 'complete',
          message: 'Workflow completed successfully',
          progress: 100,
          details: 'All steps executed successfully'
        });
        clearInterval(interval);
      } else {
        setWorkflowStatus(prev => ({
          ...prev,
          progress
        }));
      }
    }, 500);
  }, [nodes.length]);

  const handleWorkflowStop = useCallback(() => {
    setWorkflowStatus({
      status: 'idle',
      message: 'Workflow stopped',
      details: 'Workflow execution was stopped by user'
    });
  }, []);

  const handleWorkflowReset = useCallback(() => {
    setNodes([]);
    setConnections([]);
    setSelectedNodes([]);
    setWorkflowStatus({
      status: 'idle',
      message: 'Workflow reset',
      details: 'All nodes and connections have been cleared'
    });
  }, []);

  const handleWorkflowSave = useCallback(() => {
    const workflowData = {
      nodes,
      connections,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('workflow-data', JSON.stringify(workflowData));
    setWorkflowStatus({
      status: 'complete',
      message: 'Workflow saved',
      details: 'Workflow has been saved to local storage'
    });
    console.log('Workflow saved:', workflowData);
  }, [nodes, connections]);

  const handleWorkflowLoad = useCallback(() => {
    const savedData = localStorage.getItem('workflow-data');
    if (savedData) {
      try {
        const workflowData = JSON.parse(savedData);
        setNodes(workflowData.nodes || []);
        setConnections(workflowData.connections || []);
        setWorkflowStatus({
          status: 'complete',
          message: 'Workflow loaded',
          details: 'Workflow has been loaded from local storage'
        });
        console.log('Workflow loaded:', workflowData);
      } catch (err) {
        setWorkflowStatus({
          status: 'error',
          message: 'Failed to load workflow',
          details: 'Error parsing saved workflow data'
        });
        console.error('Error loading workflow:', err);
      }
    } else {
      setWorkflowStatus({
        status: 'error',
        message: 'No saved workflow found',
        details: 'Please save a workflow first before trying to load'
      });
    }
  }, []);

  return (
    <div className={`workflow-layout responsive-spacing safe-area-all ${className}`}>
      {/* Workflow Sidebar */}
      <WorkflowSidebar
        agents={agents}
        workflowStatus={workflowStatus}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        onAgentSelect={handleAgentSelect}
        onAgentDragStart={handleAgentDragStart}
        onAgentDragEnd={handleAgentDragEnd}
        onWorkflowStart={handleWorkflowStart}
        onWorkflowStop={handleWorkflowStop}
        onWorkflowReset={handleWorkflowReset}
        onWorkflowSave={handleWorkflowSave}
        onWorkflowLoad={handleWorkflowLoad}
      />

      {/* Workflow Canvas */}
      <div className="canvas-layout responsive-padding">
        <WorkflowCanvas
          nodes={nodes}
          connections={connections}
          selectedNodes={selectedNodes}
          zoom={canvasZoom}
          pan={canvasPan}
          onNodeSelect={handleNodeSelect}
          onNodePositionChange={handleNodePositionChange}
          onConnectionCreate={handleConnectionCreate}
          onConnectionDelete={handleConnectionDelete}
          onZoomChange={setCanvasZoom}
          onPanChange={setCanvasPan}
          onCanvasClick={handleCanvasClick}
          onDrop={handleCanvasDrop}
          onDragOver={handleCanvasDragOver}
        />
      </div>
    </div>
  );
};

export default WorkflowSystem;
