'use client';

import React, { useState, useEffect } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { XPCard } from '@/components/ui/XPCard';
import { XPButton } from '@/components/ui/XPButton';
import { apiClient } from '@/lib/api';
import { cn } from '@/lib/utils';

interface SystemHealth {
  status: 'healthy' | 'warning' | 'critical';
  uptime: number;
  cpu: number;
  memory: number;
  disk: number;
  network: number;
}

interface ActiveSession {
  id: string;
  problem: string;
  status: 'running' | 'paused' | 'completed' | 'failed';
  progress: number;
  startTime: string;
  agent: string;
}

interface SystemLog {
  timestamp: string;
  level: 'info' | 'warning' | 'error';
  message: string;
  source: string;
}

export default function MonitorPage() {
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [activeSessions, setActiveSessions] = useState<ActiveSession[]>([]);
  const [systemLogs, setSystemLogs] = useState<SystemLog[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    const loadMonitorData = async () => {
      try {
        const [healthResponse, sessionsResponse] = await Promise.all([
          apiClient.getSystemHealth(),
          apiClient.getSessions()
        ]);

        if (healthResponse.success && healthResponse.data) {
          setSystemHealth(healthResponse.data as SystemHealth);
        } else {
          // Mock data
          setSystemHealth({
            status: 'healthy',
            uptime: 86400, // 24 hours
            cpu: 45,
            memory: 62,
            disk: 38,
            network: 85
          });
        }

        if (sessionsResponse.success && sessionsResponse.data) {
          setActiveSessions((sessionsResponse.data as Session[]).filter(s => s.status === 'active'));
        } else {
          // Mock data
          setActiveSessions([
            {
              id: 'session_001',
              problem: 'Optimize database queries for better performance',
              status: 'running',
              progress: 65,
              startTime: new Date(Date.now() - 300000).toISOString(),
              agent: 'Problem Solver'
            },
            {
              id: 'session_002',
              problem: 'Design a scalable microservices architecture',
              status: 'running',
              progress: 23,
              startTime: new Date(Date.now() - 180000).toISOString(),
              agent: 'Researcher'
            }
          ]);
        }

        // Mock system logs
        setSystemLogs([
          {
            timestamp: new Date(Date.now() - 60000).toISOString(),
            level: 'info',
            message: 'Session session_001 completed successfully',
            source: 'SessionManager'
          },
          {
            timestamp: new Date(Date.now() - 120000).toISOString(),
            level: 'warning',
            message: 'High memory usage detected: 85%',
            source: 'SystemMonitor'
          },
          {
            timestamp: new Date(Date.now() - 180000).toISOString(),
            level: 'info',
            message: 'New session session_002 started',
            source: 'SessionManager'
          },
          {
            timestamp: new Date(Date.now() - 240000).toISOString(),
            level: 'error',
            message: 'Failed to connect to external API service',
            source: 'APIGateway'
          }
        ]);

      } catch (error) {
        console.error('Failed to load monitor data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadMonitorData();

    let interval: NodeJS.Timeout;
    if (autoRefresh) {
      interval = setInterval(loadMonitorData, 5000); // Refresh every 5 seconds
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const formatUptime = (seconds: number) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${days}d ${hours}h ${minutes}m`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-600';
      case 'warning': return 'text-yellow-600';
      case 'critical': return 'text-red-600';
      case 'running': return 'text-blue-600';
      case 'completed': return 'text-green-600';
      case 'failed': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return '✅';
      case 'warning': return '⚠️';
      case 'critical': return '❌';
      case 'running': return '🔄';
      case 'completed': return '✅';
      case 'failed': return '❌';
      default: return 'ℹ️';
    }
  };

  const sidebarContent = (
    <XPCard className="p-2" variant="outset">
      <div className="space-y-4">
        <div className="text-xs font-bold text-black mb-2 px-1">
          Monitor Controls
        </div>

        <div className="space-y-2">
          <XPButton
            onClick={() => setAutoRefresh(!autoRefresh)}
            variant={autoRefresh ? 'primary' : 'default'}
            size="sm"
            className="w-full justify-start"
          >
            {autoRefresh ? '⏸️ Pause Refresh' : '▶️ Auto Refresh'}
          </XPButton>

          <XPButton variant="default" size="sm" className="w-full justify-start">
            🔄 Refresh Now
          </XPButton>

          <XPButton variant="default" size="sm" className="w-full justify-start">
            📊 Export Logs
          </XPButton>
        </div>

        <div className="text-xs font-bold text-black mb-2 px-1">
          System Status
        </div>
        <XPCard className="p-2" variant="inset">
          <div className="flex items-center gap-2 text-xs">
            <span>{getStatusIcon(systemHealth?.status || 'unknown')}</span>
            <span className="text-black font-bold capitalize">
              {systemHealth?.status || 'Unknown'}
            </span>
          </div>
          <div className="text-[10px] text-[#666666] mt-1">
            Uptime: {systemHealth ? formatUptime(systemHealth.uptime) : 'Unknown'}
          </div>
        </XPCard>
      </div>
    </XPCard>
  );

  if (isLoading) {
    return (
      <MainLayout
        title="Real-Time Monitor"
        icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
        sidebarContent={sidebarContent}
      >
        <div className="h-full flex items-center justify-center p-4">
          <XPCard className="p-8" variant="outset">
            <div className="text-center">
              <div className="animate-spin w-8 h-8 border-4 border-[#0054e3] border-t-transparent rounded-full mx-auto mb-4"></div>
              <div className="text-black">Loading monitor data...</div>
            </div>
          </XPCard>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout
      title="Real-Time Monitor"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
      sidebarContent={sidebarContent}
    >
      <div className="h-full overflow-auto p-4 space-y-4">
        {/* Header */}
        <XPCard className="p-4" variant="outset">
          <h1 className="text-xl font-bold text-black mb-2">
            📈 Real-Time Monitor
          </h1>
          <p className="text-sm text-[#666666]">
            Live system performance and health metrics
          </p>
        </XPCard>

        {/* System Health Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <XPCard className="p-4" variant="outset">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-black">CPU Usage</span>
              <span className="text-sm font-bold text-[#0054e3]">
                {systemHealth?.cpu}%
              </span>
            </div>
            <div className="w-full bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
              <div
                className="bg-[#0054e3] h-2 rounded-full"
                style={{ width: `${systemHealth?.cpu}%` }}
              ></div>
            </div>
          </XPCard>

          <XPCard className="p-4" variant="outset">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-black">Memory</span>
              <span className="text-sm font-bold text-[#ffa500]">
                {systemHealth?.memory}%
              </span>
            </div>
            <div className="w-full bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
              <div
                className="bg-[#ffa500] h-2 rounded-full"
                style={{ width: `${systemHealth?.memory}%` }}
              ></div>
            </div>
          </XPCard>

          <XPCard className="p-4" variant="outset">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-black">Disk Space</span>
              <span className="text-sm font-bold text-[#6bbf44]">
                {systemHealth?.disk}%
              </span>
            </div>
            <div className="w-full bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
              <div
                className="bg-[#6bbf44] h-2 rounded-full"
                style={{ width: `${systemHealth?.disk}%` }}
              ></div>
            </div>
          </XPCard>

          <XPCard className="p-4" variant="outset">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-black">Network</span>
              <span className="text-sm font-bold text-[#8B5CF6]">
                {systemHealth?.network}%
              </span>
            </div>
            <div className="w-full bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
              <div
                className="bg-[#8B5CF6] h-2 rounded-full"
                style={{ width: `${systemHealth?.network}%` }}
              ></div>
            </div>
          </XPCard>
        </div>

        {/* Active Sessions */}
        <XPCard className="p-4" variant="outset">
          <XPCard.Header>
            <h3 className="text-lg font-bold text-black">
              🔄 Active Sessions ({activeSessions.length})
            </h3>
          </XPCard.Header>
          <XPCard.Content>
            {activeSessions.length === 0 ? (
              <div className="text-center py-8 text-[#666666]">
                No active sessions
              </div>
            ) : (
              <div className="space-y-3">
                {activeSessions.map((session) => (
                  <XPCard key={session.id} className="p-3" variant="inset">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-sm">{getStatusIcon(session.status)}</span>
                        <span className="text-sm font-medium text-black">
                          {session.agent}
                        </span>
                        <span className={cn("text-xs px-2 py-0.5 rounded-sm border border-[#c0c0c0]",
                          session.status === 'running' ? 'bg-[#e6f3ff] text-[#0054e3]' :
                          session.status === 'completed' ? 'bg-[#e6ffe6] text-[#6bbf44]' :
                          session.status === 'failed' ? 'bg-[#ffe6e6] text-[#ff0000]' :
                          'bg-[#f0f0f0] text-[#666666]'
                        )}>
                          {session.status}
                        </span>
                      </div>
                      <span className="text-xs text-[#666666]">
                        {Math.round((Date.now() - new Date(session.startTime).getTime()) / 1000)}s ago
                      </span>
                    </div>
                    <div className="text-sm text-black mb-2">
                      {session.problem}
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
                        <div
                          className="bg-[#6bbf44] h-2 rounded-full"
                          style={{ width: `${session.progress}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-[#666666]">{session.progress}%</span>
                    </div>
                  </XPCard>
                ))}
              </div>
            )}
          </XPCard.Content>
        </XPCard>

        {/* System Logs */}
        <XPCard className="p-4" variant="outset">
          <XPCard.Header>
            <h3 className="text-lg font-bold text-black">
              📋 System Logs
            </h3>
          </XPCard.Header>
          <XPCard.Content>
            <div className="max-h-60 overflow-y-auto">
              {systemLogs.map((log, index) => (
                <div key={index} className="flex items-start gap-2 py-2 border-b border-[#c0c0c0] last:border-b-0">
                  <span className="text-xs text-[#666666] w-16 flex-shrink-0">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <span className={cn("text-xs px-1 py-0.5 rounded-sm w-12 text-center border border-[#c0c0c0]",
                    log.level === 'error' ? 'bg-[#ffe6e6] text-[#ff0000]' :
                    log.level === 'warning' ? 'bg-[#fff3e6] text-[#ffa500]' :
                    'bg-[#e6f3ff] text-[#0054e3]'
                  )}>
                    {log.level.toUpperCase()}
                  </span>
                  <span className="text-xs text-[#666666] w-20 flex-shrink-0">
                    {log.source}
                  </span>
                  <span className="text-xs text-black flex-1">
                    {log.message}
                  </span>
                </div>
              ))}
            </div>
          </XPCard.Content>
        </XPCard>
      </div>
    </MainLayout>
  );
}
