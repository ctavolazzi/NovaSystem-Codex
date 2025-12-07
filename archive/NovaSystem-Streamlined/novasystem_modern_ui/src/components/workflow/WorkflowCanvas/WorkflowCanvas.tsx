'use client';

import React, { useState, useRef, useCallback, useEffect } from 'react';
import { WorkflowNode, WorkflowNodeData } from '../WorkflowNode/WorkflowNode';
import styles from './WorkflowCanvas.module.css';

export interface Connection {
  id: string;
  fromNodeId: string;
  toNodeId: string;
  fromPort: string;
  toPort: string;
  status: 'idle' | 'active' | 'success' | 'error';
}

export interface WorkflowCanvasProps {
  nodes: WorkflowNodeData[];
  connections: Connection[];
  selectedNodes?: string[];
  zoom?: number;
  pan?: { x: number; y: number };
  onNodeSelect?: (nodeId: string) => void;
  onNodePositionChange?: (nodeId: string, position: { x: number; y: number }) => void;
  onConnectionCreate?: (fromNodeId: string, toNodeId: string, fromPort: string, toPort: string) => void;
  onConnectionDelete?: (connectionId: string) => void;
  onZoomChange?: (zoom: number) => void;
  onPanChange?: (pan: { x: number; y: number }) => void;
  onCanvasClick?: (position: { x: number; y: number }) => void;
  className?: string;
}

export const WorkflowCanvas: React.FC<WorkflowCanvasProps> = ({
  nodes,
  connections,
  selectedNodes = [],
  zoom = 1,
  pan = { x: 0, y: 0 },
  onNodeSelect,
  onNodePositionChange,
  onConnectionCreate,
  onConnectionDelete,
  onZoomChange,
  onPanChange,
  onCanvasClick,
  className = ''
}) => {
  const [isPanning, setIsPanning] = useState(false);
  const [panStart, setPanStart] = useState({ x: 0, y: 0 });
  const [isSelecting, setIsSelecting] = useState(false);
  const [selectionStart, setSelectionStart] = useState({ x: 0, y: 0 });
  const [selectionEnd, setSelectionEnd] = useState({ x: 0, y: 0 });
  const [isConnecting, setIsConnecting] = useState(false);
  const [connectingFrom, setConnectingFrom] = useState<string | null>(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const canvasRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);

  // Handle canvas mouse events
  const handleMouseDown = useCallback((event: React.MouseEvent) => {
    if (event.target === canvasRef.current) {
      if (event.ctrlKey || event.metaKey) {
        // Start selection
        setIsSelecting(true);
        const rect = canvasRef.current!.getBoundingClientRect();
        setSelectionStart({
          x: event.clientX - rect.left,
          y: event.clientY - rect.top
        });
        setSelectionEnd({
          x: event.clientX - rect.left,
          y: event.clientY - rect.top
        });
      } else {
        // Start panning
        setIsPanning(true);
        setPanStart({
          x: event.clientX - pan.x,
          y: event.clientY - pan.y
        });
      }
    }
  }, [pan]);

  const handleMouseMove = useCallback((event: MouseEvent) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;

    const mousePos = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
    setMousePosition(mousePos);

    if (isPanning && onPanChange) {
      const newPan = {
        x: event.clientX - panStart.x,
        y: event.clientY - panStart.y
      };
      onPanChange(newPan);
    }

    if (isSelecting) {
      setSelectionEnd(mousePos);
    }
  }, [isPanning, panStart, isSelecting, onPanChange]);

  const handleMouseUp = useCallback(() => {
    setIsPanning(false);
    setIsSelecting(false);
  }, []);

  // Handle zoom
  const handleZoom = useCallback((delta: number, center?: { x: number; y: number }) => {
    if (!onZoomChange) return;

    const newZoom = Math.max(0.1, Math.min(3, zoom + delta));
    onZoomChange(newZoom);

    if (center && onPanChange) {
      // Zoom towards mouse position
      const zoomFactor = newZoom / zoom;
      const newPan = {
        x: center.x - (center.x - pan.x) * zoomFactor,
        y: center.y - (center.y - pan.y) * zoomFactor
      };
      onPanChange(newPan);
    }
  }, [zoom, pan, onZoomChange, onPanChange]);

  // Handle wheel zoom
  const handleWheel = useCallback((event: React.WheelEvent) => {
    event.preventDefault();
    const delta = event.deltaY > 0 ? -0.1 : 0.1;
    handleZoom(delta, mousePosition);
  }, [handleZoom, mousePosition]);

  // Handle canvas click
  const handleCanvasClick = useCallback((event: React.MouseEvent) => {
    if (event.target === canvasRef.current && onCanvasClick) {
      const rect = canvasRef.current!.getBoundingClientRect();
      onCanvasClick({
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
      });
    }
  }, [onCanvasClick]);

  // Render connection path
  const renderConnection = useCallback((connection: Connection) => {
    const fromNode = nodes.find(n => n.id === connection.fromNodeId);
    const toNode = nodes.find(n => n.id === connection.toNodeId);

    if (!fromNode || !toNode) return null;

    const fromX = fromNode.position.x + 180; // Node width
    const fromY = fromNode.position.y + 40; // Node height / 2
    const toX = toNode.position.x;
    const toY = toNode.position.y + 40;

    // Create curved path
    const controlPoint1X = fromX + 50;
    const controlPoint1Y = fromY;
    const controlPoint2X = toX - 50;
    const controlPoint2Y = toY;

    const pathData = `M ${fromX} ${fromY} C ${controlPoint1X} ${controlPoint1Y}, ${controlPoint2X} ${controlPoint2Y}, ${toX} ${toY}`;

    return (
      <g key={connection.id}>
        <path
          d={pathData}
          className={`${styles.connectionPath} ${styles[connection.status]}`}
          strokeWidth={connection.status === 'active' ? 3 : 2}
          onClick={() => onConnectionDelete?.(connection.id)}
        />
        {/* Arrow marker */}
        <polygon
          points={`${toX - 10},${toY - 5} ${toX},${toY} ${toX - 10},${toY + 5}`}
          className={`${styles.connectionArrow} ${styles[connection.status]}`}
        />
      </g>
    );
  }, [nodes, onConnectionDelete]);

  // Render temporary connection line while connecting
  const renderTemporaryConnection = useCallback(() => {
    if (!isConnecting || !connectingFrom) return null;

    const fromNode = nodes.find(n => n.id === connectingFrom);
    if (!fromNode) return null;

    const fromX = fromNode.position.x + 180;
    const fromY = fromNode.position.y + 40;
    const toX = mousePosition.x;
    const toY = mousePosition.y;

    const controlPoint1X = fromX + 50;
    const controlPoint1Y = fromY;
    const controlPoint2X = toX - 50;
    const controlPoint2Y = toY;

    const pathData = `M ${fromX} ${fromY} C ${controlPoint1X} ${controlPoint1Y}, ${controlPoint2X} ${controlPoint2Y}, ${toX} ${toY}`;

    return (
      <path
        d={pathData}
        className={`${styles.connectionPath} ${styles.active}`}
        strokeDasharray="5,5"
        strokeWidth={2}
      />
    );
  }, [isConnecting, connectingFrom, nodes, mousePosition]);

  // Event listeners
  useEffect(() => {
    if (isPanning || isSelecting) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);

      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isPanning, isSelecting, handleMouseMove, handleMouseUp]);

  const canvasClasses = [
    styles.workflowCanvas,
    isPanning && styles.panning,
    isSelecting && styles.selecting,
    isConnecting && styles.connecting,
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={canvasClasses}>
      <div
        ref={canvasRef}
        className={styles.canvasViewport}
        onMouseDown={handleMouseDown}
        onWheel={handleWheel}
        onClick={handleCanvasClick}
      >
        <div
          className={styles.canvasContent}
          style={{
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`
          }}
        >
          {/* Connection Layer */}
          <div className={styles.connectionLayer}>
            <svg
              ref={svgRef}
              className={styles.connectionSvg}
              style={{
                width: '100%',
                height: '100%'
              }}
            >
              {connections.map(renderConnection)}
              {renderTemporaryConnection()}
            </svg>
          </div>

          {/* Node Layer */}
          <div className={styles.nodeLayer}>
            {nodes.map(node => (
              <WorkflowNode
                key={node.id}
                node={node}
                selected={selectedNodes.includes(node.id)}
                onSelect={onNodeSelect}
                onPositionChange={onNodePositionChange}
                onConnect={onConnectionCreate}
                onDisconnect={onConnectionDelete}
              />
            ))}
          </div>
        </div>

        {/* Selection Rectangle */}
        {isSelecting && (
          <div
            className={styles.selectionRectangle}
            style={{
              left: Math.min(selectionStart.x, selectionEnd.x),
              top: Math.min(selectionStart.y, selectionEnd.y),
              width: Math.abs(selectionEnd.x - selectionStart.x),
              height: Math.abs(selectionEnd.y - selectionStart.y)
            }}
          />
        )}
      </div>

      {/* Canvas Controls */}
      <div className={styles.canvasControls}>
        <div className={styles.zoomControls}>
          <button
            className={styles.zoomControl}
            onClick={() => handleZoom(0.1)}
            title="Zoom In"
          >
            +
          </button>
          <button
            className={styles.zoomControl}
            onClick={() => handleZoom(-0.1)}
            title="Zoom Out"
          >
            −
          </button>
        </div>
        <button
          className={styles.canvasControl}
          onClick={() => onPanChange?.({ x: 0, y: 0 })}
          title="Reset View"
        >
          🎯
        </button>
      </div>

      {/* Zoom Indicator */}
      <div className={styles.zoomIndicator}>
        {Math.round(zoom * 100)}%
      </div>

      {/* Canvas Toolbar */}
      <div className={styles.canvasToolbar}>
        <button
          className={`${styles.toolbarButton} ${isConnecting ? styles.active : ''}`}
          onClick={() => {
            setIsConnecting(!isConnecting);
            setConnectingFrom(null);
          }}
          title="Connection Mode"
        >
          🔗 Connect
        </button>
        <button
          className={styles.toolbarButton}
          onClick={() => {
            // Auto-layout nodes
            const cols = Math.ceil(Math.sqrt(nodes.length));
            nodes.forEach((node, index) => {
              const x = (index % cols) * 220;
              const y = Math.floor(index / cols) * 120;
              onNodePositionChange?.(node.id, { x, y });
            });
          }}
          title="Auto Layout"
        >
          📐 Layout
        </button>
        <button
          className={styles.toolbarButton}
          onClick={() => {
            // Clear all connections
            connections.forEach(conn => onConnectionDelete?.(conn.id));
          }}
          title="Clear Connections"
        >
          🗑️ Clear
        </button>
      </div>
    </div>
  );
};

export default WorkflowCanvas;
