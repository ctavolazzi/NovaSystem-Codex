'use client';

import React from 'react';
import { MainLayout } from '@/components/layout/MainLayout';
import { XPWorkflowSystem } from '@/components/workflow/XPWorkflowSystem';

export default function WorkflowPage() {
  return (
    <MainLayout
      title="Workflow Engine"
      icon={<div className="w-4 h-4 bg-gradient-to-br from-[#FF6B6B] to-[#4ECDC4] rounded-sm" />}
    >
            <XPWorkflowSystem />
    </MainLayout>
  );
}