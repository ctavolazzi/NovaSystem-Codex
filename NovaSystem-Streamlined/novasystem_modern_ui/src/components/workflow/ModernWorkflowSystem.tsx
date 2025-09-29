'use client';

import React, { useState, useCallback } from 'react';
import { Card, CardHeader, CardContent, CardFooter } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { AgentResponseStream, AgentResponse } from '../streaming/AgentResponseStream';
import { useStreaming } from '../streaming/StreamingProvider';
import { cn } from '@/lib/utils';

// Mock data for demonstration
const MOCK_AGENTS = [
  {
    id: 'agent-1',
    name: 'Problem Solver',
    type: 'problemSolver',
    description: 'Analyzes complex problems and breaks them down into manageable components',
    version: '1.2.0',
    status: 'idle',
    icon: '🧠',
    color: 'bg-blue-500'
  },
  {
    id: 'agent-2',
    name: 'Research Agent',
    type: 'research',
    description: 'Gathers and analyzes relevant information from various sources',
    version: '2.1.0',
    status: 'idle',
    icon: '🔍',
    color: 'bg-green-500'
  },
  {
    id: 'agent-3',
    name: 'Data Analyst',
    type: 'analysis',
    description: 'Performs detailed analysis and evaluation of data patterns',
    version: '1.8.0',
    status: 'idle',
    icon: '📊',
    color: 'bg-purple-500'
  },
  {
    id: 'agent-4',
    name: 'Synthesizer',
    type: 'synthesizer',
    description: 'Combines insights and solutions into comprehensive results',
    version: '1.5.0',
    status: 'idle',
    icon: '🔗',
    color: 'bg-orange-500'
  }
];

export const ModernWorkflowSystem: React.FC = () => {
  const { responses, addResponse, clearResponses } = useStreaming();
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [workflowInput, setWorkflowInput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [activeTab, setActiveTab] = useState<'agents' | 'responses' | 'results'>('agents');

  const handleAgentToggle = useCallback((agentId: string) => {
    setSelectedAgents(prev =>
      prev.includes(agentId)
        ? prev.filter(id => id !== agentId)
        : [...prev, agentId]
    );
  }, []);

  const handleStartWorkflow = useCallback(async () => {
    if (selectedAgents.length === 0 || !workflowInput.trim()) return;

    setIsRunning(true);
    clearResponses();

    // Simulate workflow execution with streaming responses
    for (const agentId of selectedAgents) {
      const agent = MOCK_AGENTS.find(a => a.id === agentId);
      if (!agent) continue;

      // Start response
      addResponse({
        agentId: agent.id,
        agentName: agent.name,
        content: '',
        status: 'streaming',
        type: 'text'
      });

      // Simulate streaming response
      const responseText = `Processing: ${workflowInput}\n\nAs a ${agent.name}, I'm analyzing this problem step by step. Let me break down the key components and provide a comprehensive solution...`;

      // Simulate word-by-word streaming
      const words = responseText.split(' ');
      let currentContent = '';

      for (let i = 0; i < words.length; i++) {
        currentContent += (i > 0 ? ' ' : '') + words[i];

        // Update the response
        const responseId = responses[responses.length - 1]?.id;
        if (responseId) {
          // This would normally update via WebSocket
          setTimeout(() => {
            // Simulate real-time update
          }, i * 50);
        }
      }

      // Mark as complete
      setTimeout(() => {
        addResponse({
          agentId: agent.id,
          agentName: agent.name,
          content: responseText,
          status: 'complete',
          type: 'text'
        });
      }, words.length * 50);
    }

    setTimeout(() => {
      setIsRunning(false);
      setActiveTab('responses');
    }, selectedAgents.length * 2000);
  }, [selectedAgents, workflowInput, addResponse, clearResponses, responses]);

  const handleStopWorkflow = useCallback(() => {
    setIsRunning(false);
  }, []);

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Workflow Engine</h1>
            <p className="text-gray-600 mt-1">Multi-agent problem solving with real-time streaming</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className={cn(
                "w-2 h-2 rounded-full",
                isRunning ? "bg-green-500 animate-pulse" : "bg-gray-400"
              )} />
              <span className="text-sm text-gray-600">
                {isRunning ? 'Running' : 'Idle'}
              </span>
            </div>

            <Button
              variant="primary"
              onClick={handleStartWorkflow}
              disabled={selectedAgents.length === 0 || !workflowInput.trim() || isRunning}
              loading={isRunning}
            >
              {isRunning ? 'Running...' : 'Start Workflow'}
            </Button>

            {isRunning && (
              <Button
                variant="danger"
                onClick={handleStopWorkflow}
              >
                Stop
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Input & Agents */}
        <div className="w-1/3 bg-white border-r border-gray-200 flex flex-col">
          {/* Problem Input */}
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Problem Statement</h3>
            <Input
              label="Describe your problem or question"
              placeholder="Enter a detailed description of what you need help with..."
              value={workflowInput}
              onChange={(e) => setWorkflowInput(e.target.value)}
              variant="outlined"
              size="lg"
            />
          </div>

          {/* Agent Selection */}
          <div className="flex-1 p-6 overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Agents</h3>
            <div className="space-y-3">
              {MOCK_AGENTS.map((agent) => (
                <Card
                  key={agent.id}
                  variant={selectedAgents.includes(agent.id) ? 'elevated' : 'outlined'}
                  padding="md"
                  clickable
                  hover
                  onClick={() => handleAgentToggle(agent.id)}
                  className={cn(
                    "cursor-pointer transition-all duration-200",
                    selectedAgents.includes(agent.id) && "ring-2 ring-blue-500"
                  )}
                >
                  <div className="flex items-start gap-3">
                    <div className={cn(
                      "w-10 h-10 rounded-lg flex items-center justify-center text-white text-lg",
                      agent.color
                    )}>
                      {agent.icon}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-medium text-gray-900">{agent.name}</h4>
                        <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                          v{agent.version}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 line-clamp-2">
                        {agent.description}
                      </p>
                    </div>

                    <div className="flex-shrink-0">
                      <div className={cn(
                        "w-4 h-4 rounded-full border-2",
                        selectedAgents.includes(agent.id)
                          ? "bg-blue-500 border-blue-500"
                          : "border-gray-300"
                      )}>
                        {selectedAgents.includes(agent.id) && (
                          <div className="w-full h-full flex items-center justify-center">
                            <div className="w-2 h-2 bg-white rounded-full" />
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </div>

        {/* Right Panel - Tabs & Content */}
        <div className="flex-1 flex flex-col">
          {/* Tab Navigation */}
          <div className="bg-white border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'agents', label: 'Agent Status', icon: '🤖' },
                { id: 'responses', label: 'Live Responses', icon: '📡' },
                { id: 'results', label: 'Results', icon: '📊' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={cn(
                    "flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors",
                    activeTab === tab.id
                      ? "border-blue-500 text-blue-600"
                      : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  )}
                >
                  <span>{tab.icon}</span>
                  {tab.label}
                  {tab.id === 'responses' && responses.length > 0 && (
                    <span className="bg-blue-100 text-blue-600 text-xs px-2 py-0.5 rounded-full">
                      {responses.length}
                    </span>
                  )}
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-hidden">
            {activeTab === 'agents' && (
              <div className="h-full p-6 overflow-y-auto">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {MOCK_AGENTS.map((agent) => (
                    <Card key={agent.id} variant="elevated" padding="md">
                      <CardHeader
                        title={agent.name}
                        subtitle={`Version ${agent.version}`}
                        action={
                          <div className={cn(
                            "w-3 h-3 rounded-full",
                            agent.status === 'idle' ? "bg-gray-400" : "bg-green-500 animate-pulse"
                          )} />
                        }
                      />
                      <CardContent>
                        <p className="text-sm text-gray-600 mb-3">{agent.description}</p>
                        <div className="flex items-center gap-2">
                          <span className="text-2xl">{agent.icon}</span>
                          <span className="text-sm font-medium text-gray-700 capitalize">
                            {agent.status}
                          </span>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'responses' && (
              <div className="h-full">
                <AgentResponseStream
                  responses={responses}
                  maxHeight="100%"
                  showTimestamps={true}
                  showAgentNames={true}
                  autoScroll={true}
                />
              </div>
            )}

            {activeTab === 'results' && (
              <div className="h-full p-6 overflow-y-auto">
                <Card variant="elevated" padding="lg">
                  <CardHeader
                    title="Workflow Results"
                    subtitle="Summary of all agent responses and final output"
                  />
                  <CardContent>
                    {responses.length === 0 ? (
                      <div className="text-center py-12 text-gray-500">
                        <div className="text-4xl mb-4">📋</div>
                        <div className="text-lg mb-2">No results yet</div>
                        <div className="text-sm">Run a workflow to see results here</div>
                      </div>
                    ) : (
                      <div className="space-y-4">
                        {responses
                          .filter(r => r.status === 'complete')
                          .map((response) => (
                            <div key={response.id} className="border border-gray-200 rounded-lg p-4">
                              <div className="flex items-center gap-2 mb-2">
                                <span className="font-medium text-gray-900">{response.agentName}</span>
                                <span className="text-xs text-gray-500">
                                  {response.timestamp.toLocaleTimeString()}
                                </span>
                              </div>
                              <div className="text-sm text-gray-700 whitespace-pre-wrap">
                                {response.content}
                              </div>
                            </div>
                          ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
