// Simple Agent Response interface for Windows XP components
export interface SimpleAgentResponse {
  agentId: string;
  content: string;
  timestamp: number;
  status: 'streaming' | 'complete' | 'error';
}
