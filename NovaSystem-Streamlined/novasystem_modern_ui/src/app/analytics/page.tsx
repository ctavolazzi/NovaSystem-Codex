'use client';

import React, { useState, useEffect } from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { XPCard } from '@/components/ui/XPCard';
import { XPButton } from '@/components/ui/XPButton';
import { XPSelect } from '@/components/ui/XPInput';
import { apiClient } from '@/lib/api';
import { cn } from '@/lib/utils';

interface AnalyticsData {
  totalSessions: number;
  successfulSessions: number;
  averageResponseTime: number;
  totalProblemsSolved: number;
  topDomains: Array<{ domain: string; count: number }>;
  performanceMetrics: {
    cpu: number;
    memory: number;
    responseTime: number;
  };
}

// interface ChartData {
//   labels: string[];
//   datasets: Array<{
//     label: string;
//     data: number[];
//     backgroundColor: string;
//     borderColor: string;
//   }>;
// }

export default function AnalyticsPage() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('24h');

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        const response = await apiClient.getAnalyticsData();
        if (response.success && response.data) {
          setAnalyticsData(response.data as AnalyticsData);
        } else {
          // Mock data for demonstration
          setAnalyticsData({
            totalSessions: 1247,
            successfulSessions: 1189,
            averageResponseTime: 2.3,
            totalProblemsSolved: 2341,
            topDomains: [
              { domain: 'General', count: 456 },
              { domain: 'Technical', count: 234 },
              { domain: 'Business', count: 189 },
              { domain: 'Creative', count: 123 },
              { domain: 'Research', count: 98 }
            ],
            performanceMetrics: {
              cpu: 45,
              memory: 62,
              responseTime: 1.8
            }
          });
        }
      } catch (error) {
        console.error('Failed to load analytics:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadAnalytics();
  }, [timeRange]);

  const sidebarContent = (
    <XPCard className="p-2" variant="outset">
      <div className="space-y-4">
        <div className="text-xs font-bold text-black mb-2 px-1">
          Analytics Controls
        </div>

        <div className="space-y-2">
          <div className="text-xs text-black px-1">Time Range</div>
          <div className="space-y-1">
            {(['24h', '7d', '30d'] as const).map((range) => (
              <XPButton
                key={range}
                onClick={() => setTimeRange(range)}
                variant={timeRange === range ? 'primary' : 'default'}
                size="sm"
                className="w-full justify-start"
              >
                {range === '24h' ? 'Last 24 Hours' : range === '7d' ? 'Last 7 Days' : 'Last 30 Days'}
              </XPButton>
            ))}
          </div>
        </div>

        <div className="text-xs font-bold text-black mb-2 px-1">
          Export Options
        </div>
        <div className="space-y-1">
          <XPButton variant="default" size="sm" className="w-full justify-start">
            📊 Export Charts
          </XPButton>
          <XPButton variant="default" size="sm" className="w-full justify-start">
            📋 Export Data
          </XPButton>
        </div>
      </div>
    </XPCard>
  );

  if (isLoading) {
    return (
      <MainLayout
        title="Analytics Dashboard"
        icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
        sidebarContent={sidebarContent}
      >
        <div className="h-full flex items-center justify-center p-4">
          <XPCard className="p-8" variant="outset">
            <div className="text-center">
              <div className="animate-spin w-8 h-8 border-4 border-[#0054e3] border-t-transparent rounded-full mx-auto mb-4"></div>
              <div className="text-black">Loading analytics data...</div>
            </div>
          </XPCard>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout
      title="Analytics Dashboard"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
      sidebarContent={sidebarContent}
    >
      <div className="h-full overflow-auto p-4 space-y-4">
        {/* Header */}
        <XPCard className="p-4" variant="outset">
          <h1 className="text-xl font-bold text-black mb-2">
            📊 Analytics Dashboard
          </h1>
          <p className="text-sm text-[#666666]">
            Performance metrics and usage statistics for NovaSystem
          </p>
        </XPCard>

        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <XPCard className="p-4" variant="outset">
            <div className="text-2xl font-bold text-[#0054e3]">
              {analyticsData?.totalSessions.toLocaleString() || '0'}
            </div>
            <div className="text-xs text-[#666666]">Total Sessions</div>
          </XPCard>

          <XPCard className="p-4" variant="outset">
            <div className="text-2xl font-bold text-[#6bbf44]">
              {analyticsData?.successfulSessions.toLocaleString() || '0'}
            </div>
            <div className="text-xs text-[#666666]">Successful Sessions</div>
          </XPCard>

          <XPCard className="p-4" variant="outset">
            <div className="text-2xl font-bold text-[#ffa500]">
              {analyticsData?.averageResponseTime.toFixed(1)}s
            </div>
            <div className="text-xs text-[#666666]">Avg Response Time</div>
          </XPCard>

          <XPCard className="p-4" variant="outset">
            <div className="text-2xl font-bold text-[#8B5CF6]">
              {analyticsData?.totalProblemsSolved.toLocaleString() || '0'}
            </div>
            <div className="text-xs text-[#666666]">Problems Solved</div>
          </XPCard>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Top Domains Chart */}
          <XPCard className="p-4" variant="outset">
            <XPCard.Header>
              <h3 className="text-lg font-bold text-black">
                🎯 Top Problem Domains
              </h3>
            </XPCard.Header>
            <XPCard.Content>
              <div className="space-y-2">
                {analyticsData?.topDomains.map((domain, index) => (
                  <div key={domain.domain} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-[#6bbf44] rounded-sm flex items-center justify-center text-[10px] text-white">
                        {index + 1}
                      </div>
                      <span className="text-sm text-black">{domain.domain}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
                        <div
                          className="bg-[#6bbf44] h-2 rounded-full"
                          style={{ width: `${(domain.count / Math.max(...analyticsData.topDomains.map(d => d.count))) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-[#666666] w-8 text-right">{domain.count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </XPCard.Content>
          </XPCard>

          {/* Performance Metrics */}
          <XPCard className="p-4" variant="outset">
            <XPCard.Header>
              <h3 className="text-lg font-bold text-black">
                ⚡ System Performance
              </h3>
            </XPCard.Header>
            <XPCard.Content>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-black">CPU Usage</span>
                    <span className="text-[#666666]">{analyticsData?.performanceMetrics.cpu}%</span>
                  </div>
                  <div className="w-full bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
                    <div
                      className="bg-[#0054e3] h-2 rounded-full"
                      style={{ width: `${analyticsData?.performanceMetrics.cpu}%` }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-black">Memory Usage</span>
                    <span className="text-[#666666]">{analyticsData?.performanceMetrics.memory}%</span>
                  </div>
                  <div className="w-full bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
                    <div
                      className="bg-[#ffa500] h-2 rounded-full"
                      style={{ width: `${analyticsData?.performanceMetrics.memory}%` }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-black">Response Time</span>
                    <span className="text-[#666666]">{analyticsData?.performanceMetrics.responseTime}s</span>
                  </div>
                  <div className="w-full bg-[#e0e0e0] rounded-full h-2 border border-[#c0c0c0]">
                    <div
                      className="bg-[#6bbf44] h-2 rounded-full"
                      style={{ width: `${Math.min((analyticsData?.performanceMetrics.responseTime || 0) * 20, 100)}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </XPCard.Content>
          </XPCard>
        </div>

        {/* Session Success Rate */}
        <XPCard className="p-4" variant="outset">
          <XPCard.Header>
            <h3 className="text-lg font-bold text-black">
              📈 Session Success Rate
            </h3>
          </XPCard.Header>
          <XPCard.Content>
            <div className="flex items-center gap-4">
              <div className="text-3xl font-bold text-[#6bbf44]">
                {analyticsData ? Math.round((analyticsData.successfulSessions / analyticsData.totalSessions) * 100) : 0}%
              </div>
              <div className="flex-1">
                <div className="w-full bg-[#e0e0e0] rounded-full h-4 border border-[#c0c0c0]">
                  <div
                    className="bg-[#6bbf44] h-4 rounded-full"
                    style={{ width: `${analyticsData ? (analyticsData.successfulSessions / analyticsData.totalSessions) * 100 : 0}%` }}
                  ></div>
                </div>
                <div className="text-xs text-[#666666] mt-1">
                  {analyticsData?.successfulSessions} successful out of {analyticsData?.totalSessions} total sessions
                </div>
              </div>
            </div>
          </XPCard.Content>
        </XPCard>
      </div>
    </MainLayout>
  );
}
