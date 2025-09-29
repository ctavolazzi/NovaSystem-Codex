'use client';

import React, { useState, useRef, useCallback } from 'react';
import styles from './WorkflowNode.module.css';

export interface WorkflowNodeData {
  id: string;
  type: string;
  name: string;
  description: string;
  status: 'idle' | 'processing' | 'complete' | 'error';
  position: { x: number; y: number };
  inputs: string[];
  outputs: string[];
  data?: Record<string, unknown>;
}

export interface WorkflowNodeProps {
  node: WorkflowNodeData;
  variant?: 'default' | 'compact' | 'large';
  selected?: boolean;
  draggable?: boolean;
  onSelect?: (node: WorkflowNodeData) => void;
  onPositionChange?: (nodeId: string, position: { x: number; y: number }) => void;
  onConnect?: (fromNodeId: string, toNodeId: string, fromPort: string, toPort: string) => void;
  onDisconnect?: (connectionId: string) => void;
  className?: string;
}

export const WorkflowNode: React.FC<WorkflowNodeProps> = ({
  node,
  variant = 'default',
  selected = false,
  draggable = true,
  onSelect,
  onPositionChange,
  onConnect,
  className = ''
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectingPort, setConnectingPort] = useState<string | null>(null);
  const nodeRef = useRef<HTMLDivElement>(null);

  const handleClick = useCallback((event: React.MouseEvent) => {
    event.stopPropagation();
    if (onSelect) {
      onSelect(node);
    }
  }, [node, onSelect]);

  const handleMouseDown = useCallback((event: React.MouseEvent) => {
    if (!draggable) return;

    event.preventDefault();
    setIsDragging(true);
    setDragStart({
      x: event.clientX - node.position.x,
      y: event.clientY - node.position.y
    });
  }, [draggable, node.position]);

  const handleMouseMove = useCallback((event: MouseEvent) => {
    if (!isDragging || !onPositionChange) return;

    const newPosition = {
      x: event.clientX - dragStart.x,
      y: event.clientY - dragStart.y
    };

    onPositionChange(node.id, newPosition);
  }, [isDragging, dragStart, node.id, onPositionChange]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  React.useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);

      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDragging, handleMouseMove, handleMouseUp]);

  const handlePortClick = useCallback((portId: string, event: React.MouseEvent) => {
    event.stopPropagation();

    if (isConnecting && connectingPort && onConnect) {
      // Complete connection
      const [fromNodeId, fromPort] = connectingPort.split(':');
      const [toNodeId, toPort] = portId.split(':');

      if (fromNodeId !== toNodeId) {
        onConnect(fromNodeId, toNodeId, fromPort, toPort);
      }

      setIsConnecting(false);
      setConnectingPort(null);
    } else {
      // Start connection
      setIsConnecting(true);
      setConnectingPort(`${node.id}:${portId}`);
    }
  }, [isConnecting, connectingPort, node.id, onConnect]);

  const handleKeyDown = useCallback((event: React.KeyboardEvent) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClick(event as React.MouseEvent);
    } else if (event.key === 'Delete' || event.key === 'Backspace') {
      event.preventDefault();
      // Handle node deletion
    }
  }, [handleClick]);

  const getStatusIndicator = () => {
    switch (node.status) {
      case 'processing':
        return <div className={`${styles.nodeStatus} ${styles.processing}`} aria-label="Processing" />;
      case 'complete':
        return <div className={`${styles.nodeStatus} ${styles.complete}`} aria-label="Complete" />;
      case 'error':
        return <div className={`${styles.nodeStatus} ${styles.error}`} aria-label="Error" />;
      default:
        return <div className={`${styles.nodeStatus} ${styles.idle}`} aria-label="Idle" />;
    }
  };

  const getNodeIcon = () => {
    switch (node.type) {
      case 'problemSolver':
        return '🧠';
      case 'research':
        return '🔍';
      case 'analysis':
        return '📊';
      case 'synthesizer':
        return '🔗';
      case 'data':
        return '📈';
      case 'optimization':
        return '⚡';
      default:
        return '⚙️';
    }
  };

  const nodeClasses = [
    styles.workflowNode,
    styles[node.status],
    variant !== 'default' && styles[variant],
    selected && styles.selected,
    isDragging && styles.dragging,
    className
  ].filter(Boolean).join(' ');

  return (
    <div
      ref={nodeRef}
      className={nodeClasses}
      style={{
        left: node.position.x,
        top: node.position.y,
        transform: isDragging ? 'rotate(2deg)' : 'none'
      }}
      role="button"
      tabIndex={0}
      aria-label={`${node.name} node - ${node.description}`}
      aria-pressed={selected}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      onMouseDown={handleMouseDown}
    >
      {/* Connection Ports */}
      <div className={styles.nodePorts}>
        {/* Input Ports */}
        {node.inputs.map((input, index) => (
          <div
            key={`input-${input}`}
            className={`${styles.connectionPort} ${styles.input}`}
            style={{
              top: index === 0 ? '50%' : index === 1 ? '30%' : '70%'
            }}
            data-port={`${node.id}:${input}`}
            onClick={(e) => handlePortClick(`${node.id}:${input}`, e)}
            title={`Input: ${input}`}
            aria-label={`Input port: ${input}`}
          />
        ))}

        {/* Output Ports */}
        {node.outputs.map((output, index) => (
          <div
            key={`output-${output}`}
            className={`${styles.connectionPort} ${styles.output}`}
            style={{
              top: index === 0 ? '50%' : index === 1 ? '30%' : '70%'
            }}
            data-port={`${node.id}:${output}`}
            onClick={(e) => handlePortClick(`${node.id}:${output}`, e)}
            title={`Output: ${output}`}
            aria-label={`Output port: ${output}`}
          />
        ))}
      </div>

      {/* Node Header */}
      <div className={styles.nodeHeader}>
        <div className={styles.nodeIcon}>
          {getNodeIcon()}
        </div>
        <div className={styles.nodeTitle}>
          {node.name}
        </div>
        {getStatusIndicator()}
      </div>

      {/* Node Content */}
      <div className={styles.nodeContent}>
        <div className={styles.nodeDescription}>
          {node.description}
        </div>
      </div>

      {/* Connection State Indicator */}
      {isConnecting && connectingPort && (
        <div className={styles.connectingIndicator} aria-hidden="true">
          <div className={styles.connectingDot} />
        </div>
      )}
    </div>
  );
};

export default WorkflowNode;
