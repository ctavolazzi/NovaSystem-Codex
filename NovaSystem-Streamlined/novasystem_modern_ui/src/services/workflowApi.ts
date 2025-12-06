/**
 * Workflow API Service
 *
 * Communicates with the Flask backend for workflow execution and status polling.
 */

// Backend API base URL - defaults to Flask dev server
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

/**
 * Node payload for workflow execution (sent to backend)
 */
export interface WorkflowNodePayload {
  id: string;
  type: string;
  title: string;
  agent?: string;
  metadata?: Record<string, unknown>;
}

/**
 * Connection payload for workflow execution (sent to backend)
 */
export interface WorkflowConnectionPayload {
  from: string;
  to: string;
}

/**
 * Response from workflow execution endpoint
 */
export interface WorkflowExecuteResponse {
  session_id: string;
  status: 'started' | 'error';
  message: string;
}

/**
 * Response from workflow status endpoint
 */
export interface WorkflowStatusResponse {
  session_id: string;
  status: 'running' | 'completed' | 'error';
  type: 'workflow';
  node_states: Record<string, 'pending' | 'processing' | 'completed' | 'error'>;
  node_outputs: Record<string, string>;
  execution_order: string[];
  started_at: string;
}

/**
 * Error response from API
 */
export interface ApiError {
  error: string;
}

/**
 * Execute a workflow with the given nodes and connections
 */
export async function executeWorkflow(
  nodes: WorkflowNodePayload[],
  connections: WorkflowConnectionPayload[]
): Promise<WorkflowExecuteResponse> {
  const response = await fetch(`${API_BASE_URL}/api/workflow/execute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ nodes, connections }),
  });

  if (!response.ok) {
    const errorData: ApiError = await response.json();
    throw new Error(errorData.error || `HTTP error ${response.status}`);
  }

  return response.json();
}

/**
 * Get the current status of a workflow session
 */
export async function getWorkflowStatus(
  sessionId: string
): Promise<WorkflowStatusResponse> {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/status`);

  if (!response.ok) {
    const errorData: ApiError = await response.json();
    throw new Error(errorData.error || `HTTP error ${response.status}`);
  }

  return response.json();
}

