'use client';

import React, { useState, useRef, useCallback } from 'react';
import styles from './AgentCard.module.css';

export interface Agent {
  id: string;
  name: string;
  type: 'problemSolver' | 'research' | 'analysis' | 'synthesizer' | 'data' | 'optimization';
  description: string;
  version: string;
  status: 'idle' | 'processing' | 'complete' | 'error';
  icon: string;
  disabled?: boolean;
}

export interface AgentCardProps {
  agent: Agent;
  variant?: 'default' | 'compact' | 'large';
  selected?: boolean;
  draggable?: boolean;
  onSelect?: (agent: Agent) => void;
  onDragStart?: (agent: Agent, event: React.DragEvent) => void;
  onDragEnd?: (agent: Agent, event: React.DragEvent) => void;
  className?: string;
}

const AGENT_TYPE_CONFIG = {
  problemSolver: {
    label: 'Problem Solver',
    icon: '🧠',
    description: 'Analyzes and breaks down complex problems into manageable components'
  },
  research: {
    label: 'Research',
    icon: '🔍',
    description: 'Gathers and analyzes relevant information and data sources'
  },
  analysis: {
    label: 'Analysis',
    icon: '📊',
    description: 'Performs detailed analysis and evaluation of data and solutions'
  },
  synthesizer: {
    label: 'Synthesizer',
    icon: '🔗',
    description: 'Combines insights and solutions into comprehensive results'
  },
  data: {
    label: 'Data',
    icon: '📈',
    description: 'Handles data processing, transformation, and validation'
  },
  optimization: {
    label: 'Optimization',
    icon: '⚡',
    description: 'Optimizes processes, algorithms, and resource utilization'
  }
};

export const AgentCard: React.FC<AgentCardProps> = ({
  agent,
  variant = 'default',
  selected = false,
  draggable = true,
  onSelect,
  onDragStart,
  onDragEnd,
  className = ''
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  const agentConfig = AGENT_TYPE_CONFIG[agent.type];

  const handleClick = useCallback(() => {
    if (!agent.disabled && onSelect) {
      onSelect(agent);
    }
  }, [agent, onSelect]);

  const handleDragStart = useCallback((event: React.DragEvent) => {
    if (!agent.disabled && draggable) {
      setIsDragging(true);
      event.dataTransfer.setData('application/json', JSON.stringify({
        type: 'agent',
        agent: agent
      }));
      event.dataTransfer.effectAllowed = 'copy';

      if (onDragStart) {
        onDragStart(agent, event);
      }
    }
  }, [agent, draggable, onDragStart]);

  const handleDragEnd = useCallback((event: React.DragEvent) => {
    setIsDragging(false);

    if (onDragEnd) {
      onDragEnd(agent, event);
    }
  }, [agent, onDragEnd]);

  const handleKeyDown = useCallback((event: React.KeyboardEvent) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClick();
    }
  }, [handleClick]);

  const getStatusIndicator = () => {
    switch (agent.status) {
      case 'processing':
        return <div className={`${styles.agentStatus} ${styles.processing}`} aria-label="Processing" />;
      case 'complete':
        return <div className={`${styles.agentStatus} ${styles.complete}`} aria-label="Complete" />;
      case 'error':
        return <div className={`${styles.agentStatus} ${styles.error}`} aria-label="Error" />;
      default:
        return <div className={`${styles.agentStatus} ${styles.idle}`} aria-label="Idle" />;
    }
  };

  const cardClasses = [
    styles.agentCard,
    styles[agent.type],
    variant !== 'default' && styles[variant],
    selected && styles.selected,
    isDragging && styles.dragging,
    agent.disabled && styles.disabled,
    agent.status === 'processing' && styles.loading,
    className
  ].filter(Boolean).join(' ');

  return (
    <div
      ref={cardRef}
      className={cardClasses}
      role="button"
      tabIndex={agent.disabled ? -1 : 0}
      aria-label={`${agentConfig.label} agent - ${agent.description}`}
      aria-pressed={selected}
      aria-disabled={agent.disabled}
      draggable={draggable && !agent.disabled}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      {/* Agent Header */}
      <div className={styles.agentHeader}>
        <div className={`${styles.agentIcon} ${styles[agent.type]}`}>
          {agent.icon || agentConfig.icon}
        </div>
        <div className={styles.agentTitle}>
          {agent.name || agentConfig.label}
        </div>
        {getStatusIndicator()}
      </div>

      {/* Agent Content */}
      <div className={styles.agentContent}>
        <div className={styles.agentDescription}>
          {agent.description || agentConfig.description}
        </div>

        <div className={styles.agentMeta}>
          <div className={styles.agentType}>
            {agentConfig.label}
          </div>
          <div className={styles.agentVersion}>
            v{agent.version}
          </div>
        </div>
      </div>

      {/* Loading Overlay */}
      {agent.status === 'processing' && (
        <div className={styles.loadingOverlay} aria-hidden="true">
          <div className={styles.loadingSpinner} />
        </div>
      )}
    </div>
  );
};

export default AgentCard;
