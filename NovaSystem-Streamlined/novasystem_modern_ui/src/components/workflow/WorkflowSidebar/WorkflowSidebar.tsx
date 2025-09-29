'use client';

import React, { useState, useCallback } from 'react';
import { AgentCard, Agent } from '../AgentCard/AgentCard';
import styles from './WorkflowSidebar.module.css';

export interface WorkflowStatus {
  status: 'idle' | 'processing' | 'complete' | 'error';
  message: string;
  progress?: number;
  details?: string;
}

export interface WorkflowSidebarProps {
  agents: Agent[];
  workflowStatus: WorkflowStatus;
  collapsed?: boolean;
  onToggleCollapse?: () => void;
  onAgentSelect?: (agent: Agent) => void;
  onAgentDragStart?: (agent: Agent, event: React.DragEvent) => void;
  onAgentDragEnd?: (agent: Agent, event: React.DragEvent) => void;
  onWorkflowStart?: () => void;
  onWorkflowStop?: () => void;
  onWorkflowReset?: () => void;
  onWorkflowSave?: () => void;
  onWorkflowLoad?: () => void;
  className?: string;
}

export const WorkflowSidebar: React.FC<WorkflowSidebarProps> = ({
  agents,
  workflowStatus,
  collapsed = false,
  onToggleCollapse,
  onAgentSelect,
  onAgentDragStart,
  onAgentDragEnd,
  onWorkflowStart,
  onWorkflowStop,
  onWorkflowReset,
  onWorkflowSave,
  onWorkflowLoad,
  className = ''
}) => {
  const [expandedSections, setExpandedSections] = useState({
    agents: true,
    controls: true,
    status: true
  });

  const toggleSection = useCallback((section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  }, []);


  const getStatusIcon = (status: WorkflowStatus['status']) => {
    switch (status) {
      case 'processing':
        return '🔄';
      case 'complete':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '⏸️';
    }
  };

  const getControlButtonVariant = (action: string) => {
    switch (action) {
      case 'start':
        return workflowStatus.status === 'processing' ? 'error' : 'success';
      case 'stop':
        return 'warning';
      case 'reset':
        return 'error';
      default:
        return 'primary';
    }
  };

  const sidebarClasses = [
    styles.workflowSidebar,
    collapsed && styles.collapsed,
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={sidebarClasses}>
      {/* Sidebar Header */}
      <div className={styles.sidebarHeader}>
        <div className={styles.sidebarTitle}>
          <span className={styles.sidebarTitleIcon}>⚡</span>
          <span>Workflow</span>
        </div>
        <button
          className={styles.sidebarToggle}
          onClick={onToggleCollapse}
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? '▶' : '◀'}
        </button>
      </div>

      {/* Sidebar Content */}
      <div className={`${styles.sidebarContent} ${collapsed ? styles.collapsed : ''}`}>
        {/* Agent Pool Section */}
        <div className={styles.sidebarSection}>
          <div
            className={styles.sidebarSectionHeader}
            onClick={() => !collapsed && toggleSection('agents')}
          >
            <div className={styles.sidebarSectionTitle}>
              <span className={styles.sidebarSectionIcon}>🤖</span>
              <span>Agent Pool</span>
            </div>
            <button
              className={`${styles.sidebarSectionToggle} ${!expandedSections.agents ? styles.collapsed : ''}`}
              aria-label={expandedSections.agents ? 'Collapse agents' : 'Expand agents'}
            >
              ▼
            </button>
          </div>
          <div className={`${styles.sidebarSectionContent} ${!expandedSections.agents ? styles.collapsed : ''}`}>
            <div className={`${styles.agentPool} ${collapsed ? styles.collapsed : ''}`}>
              {agents.map(agent => (
                <AgentCard
                  key={agent.id}
                  agent={agent}
                  variant="compact"
                  onSelect={onAgentSelect}
                  onDragStart={onAgentDragStart}
                  onDragEnd={onAgentDragEnd}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Workflow Controls Section */}
        <div className={styles.sidebarSection}>
          <div
            className={styles.sidebarSectionHeader}
            onClick={() => !collapsed && toggleSection('controls')}
          >
            <div className={styles.sidebarSectionTitle}>
              <span className={styles.sidebarSectionIcon}>🎮</span>
              <span>Controls</span>
            </div>
            <button
              className={`${styles.sidebarSectionToggle} ${!expandedSections.controls ? styles.collapsed : ''}`}
              aria-label={expandedSections.controls ? 'Collapse controls' : 'Expand controls'}
            >
              ▼
            </button>
          </div>
          <div className={`${styles.sidebarSectionContent} ${!expandedSections.controls ? styles.collapsed : ''}`}>
            <div className={`${styles.workflowControls} ${collapsed ? styles.collapsed : ''}`}>
              <button
                className={`${styles.controlButton} ${styles[getControlButtonVariant('start')]}`}
                onClick={workflowStatus.status === 'processing' ? onWorkflowStop : onWorkflowStart}
                disabled={workflowStatus.status === 'processing' && !onWorkflowStop}
              >
                {workflowStatus.status === 'processing' ? '⏹️' : '▶️'}
                {workflowStatus.status === 'processing' ? 'Stop' : 'Start'}
              </button>

              <button
                className={`${styles.controlButton} ${styles.warning}`}
                onClick={onWorkflowReset}
                disabled={workflowStatus.status === 'processing'}
              >
                🔄 Reset
              </button>

              <button
                className={`${styles.controlButton} ${styles.primary}`}
                onClick={onWorkflowSave}
              >
                💾 Save
              </button>

              <button
                className={`${styles.controlButton} ${styles.primary}`}
                onClick={onWorkflowLoad}
              >
                📂 Load
              </button>
            </div>
          </div>
        </div>

        {/* Workflow Status Section */}
        <div className={styles.sidebarSection}>
          <div
            className={styles.sidebarSectionHeader}
            onClick={() => !collapsed && toggleSection('status')}
          >
            <div className={styles.sidebarSectionTitle}>
              <span className={styles.sidebarSectionIcon}>📊</span>
              <span>Status</span>
            </div>
            <button
              className={`${styles.sidebarSectionToggle} ${!expandedSections.status ? styles.collapsed : ''}`}
              aria-label={expandedSections.status ? 'Collapse status' : 'Expand status'}
            >
              ▼
            </button>
          </div>
          <div className={`${styles.sidebarSectionContent} ${!expandedSections.status ? styles.collapsed : ''}`}>
            <div className={`${styles.workflowStatus} ${collapsed ? styles.collapsed : ''}`}>
              <div className={styles.statusIndicator}>
                <div className={`${styles.statusDot} ${styles[workflowStatus.status]}`} />
                <div className={styles.statusText}>
                  {getStatusIcon(workflowStatus.status)} {workflowStatus.message}
                </div>
              </div>

              {workflowStatus.details && (
                <div className={styles.statusDetails}>
                  {workflowStatus.details}
                </div>
              )}

              {workflowStatus.progress !== undefined && (
                <div className={styles.progressContainer}>
                  <div className={styles.progressBar}>
                    <div
                      className={styles.progressFill}
                      style={{ width: `${workflowStatus.progress}%` }}
                    />
                  </div>
                  <div className={styles.progressText}>
                    {Math.round(workflowStatus.progress)}%
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorkflowSidebar;
