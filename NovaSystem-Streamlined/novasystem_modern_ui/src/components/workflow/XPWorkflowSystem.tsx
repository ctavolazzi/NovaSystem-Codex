'use client';

import React, { useState, useCallback, useEffect } from 'react';
import { XPCard } from '../ui/XPCard';
import { XPButton } from '../ui/XPButton';
import { XPInput, XPTextArea } from '../ui/XPInput';
import { XPAgentResponseStream } from '../streaming/XPAgentResponseStream';
import { useStreaming } from '../streaming/SimpleStreamingProvider';
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

export const XPWorkflowSystem: React.FC = () => {
  const [problemStatement, setProblemStatement] = useState('');
  const [selectedAgents, setSelectedAgents] = useState<Agent[]>([]);
  const [workflowStatus, setWorkflowStatus] = useState<'idle' | 'running' | 'paused' | 'completed' | 'error'>('idle');
  const [activeTab, setActiveTab] = useState<'status' | 'responses' | 'results'>('status');
  const { addResponse, setIsStreaming, clearResponses } = useStreaming();

  const handleAgentToggle = useCallback((agent: Agent) => {
    setSelectedAgents(prev =>
      prev.some(a => a.id === agent.id)
        ? prev.filter(a => a.id !== agent.id)
        : [...prev, agent]
    );
  }, []);

  const startWorkflow = useCallback(() => {
    if (!problemStatement.trim()) {
      alert('Please enter a problem statement.');
      return;
    }
    if (selectedAgents.length === 0) {
      alert('Please select at least one agent.');
      return;
    }

    setWorkflowStatus('running');
    setIsStreaming(true);
    clearResponses();
    setActiveTab('responses');

    let step = 0;
    const totalSteps = selectedAgents.length * 2;

    const interval = setInterval(() => {
      if (step >= totalSteps) {
        clearInterval(interval);
        setWorkflowStatus('completed');
        setIsStreaming(false);
        addResponse({
          agentId: 'System',
          content: 'Workflow completed successfully!',
          timestamp: Date.now(),
          status: 'complete',
        });
        return;
      }

      const currentAgentIndex = Math.floor(step / 2);
      const currentAgent = selectedAgents[currentAgentIndex];

      if (step % 2 === 0) {
        const analysisMessages = [
          `🔍 Analyzing problem statement: "${problemStatement.substring(0, 50)}${problemStatement.length > 50 ? '...' : ''}"`,
          `📊 Breaking down the problem into key components and identifying potential approaches...`,
          `🧠 Evaluating different solution strategies and their feasibility...`,
          `⚡ Processing requirements and constraints for optimal solution design...`,
          `🎯 Identifying critical success factors and potential challenges...`,
          `💡 Generating initial insights and preliminary analysis...`
        ];

        addResponse({
          agentId: currentAgent.name,
          content: analysisMessages[Math.floor(Math.random() * analysisMessages.length)],
          timestamp: Date.now(),
          status: 'streaming',
        });
      } else {
        const solutionMessages = [
          `✅ Analysis complete! Generated comprehensive solution framework with ${Math.floor(Math.random() * 5) + 3} key components.`,
          `🎯 Solution strategy developed: Implemented ${Math.floor(Math.random() * 3) + 2}-phase approach with clear milestones.`,
          `📈 Delivered actionable recommendations with ${Math.floor(Math.random() * 4) + 2} implementation steps.`,
          `🔧 Created detailed technical specification with performance metrics and success criteria.`,
          `💼 Business case analysis complete with ROI projections and risk assessment.`,
          `🚀 Solution ready for implementation with comprehensive documentation and next steps.`
        ];

        addResponse({
          agentId: currentAgent.name,
          content: solutionMessages[Math.floor(Math.random() * solutionMessages.length)],
          timestamp: Date.now(),
          status: 'complete',
        });
      }
      step++;
    }, 1500);
  }, [problemStatement, selectedAgents, addResponse, clearResponses, setIsStreaming]);

  const stopWorkflow = useCallback(() => {
    setWorkflowStatus('idle');
    setIsStreaming(false);
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
    clearResponses();
    setIsStreaming(false);
  }, [clearResponses, setIsStreaming]);

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
              disabled={workflowStatus === 'running'}
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
          <XPButton variant="default" onClick={resetWorkflow} disabled={workflowStatus === 'running'}>
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
              disabled={!problemStatement.trim() || selectedAgents.length === 0}
            >
              Start Workflow
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
        <XPCard.Content className="flex-1 overflow-hidden">
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
              </div>
              <div className="grid grid-cols-2 gap-3">
                {selectedAgents.map(agent => (
                  <XPCard key={agent.id} className="p-2" variant="inset">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm">{agent.icon}</span>
                      <span className="font-medium text-black text-xs">{agent.name}</span>
                    </div>
                    <p className="text-xs text-[#666666] mb-2">{agent.description}</p>
                    <div className="flex items-center gap-2">
                      <span className={cn(
                        "w-2 h-2 rounded-full",
                        workflowStatus === 'running' ? "bg-[#0054e3] animate-pulse" : "bg-[#808080]"
                      )}></span>
                      <span className="text-xs text-[#666666]">
                        {workflowStatus === 'running' ? 'Processing...' : 'Idle'}
                      </span>
                    </div>
                  </XPCard>
                ))}
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
        </XPCard.Content>
      </XPCard>
    </div>
  );
};
