# 🚀 Modular Workflow UI System

A production-ready, modular workflow management interface built with React, TypeScript, and CSS Modules following the single source of truth design pattern.

## 🎯 Architecture Overview

### Single Source of Truth Design Pattern
- **ONE central `variables.css` file** containing ALL design tokens
- **CSS custom properties** for colors, spacing, typography, shadows, borders
- **No hardcoded values** anywhere in component CSS files
- **All components reference** the central variable system

### Fully Composable Component System
- **Self-contained components** with their own CSS modules
- **Independent operation** without external dependencies
- **CSS modules/scoped styling** approach
- **Slot-based composition** patterns where applicable

## 📁 File Structure

```
src/
├── styles/
│   ├── variables.css          # 🎯 Single source of truth for ALL design tokens
│   ├── base.css              # Reset and base styles only
│   ├── layout.css            # Grid and layout utilities only
│   └── globals.css           # Main import file
├── components/
│   └── workflow/
│       ├── AgentCard/
│       │   ├── AgentCard.tsx
│       │   └── AgentCard.module.css
│       ├── WorkflowNode/
│       │   ├── WorkflowNode.tsx
│       │   └── WorkflowNode.module.css
│       ├── WorkflowCanvas/
│       │   ├── WorkflowCanvas.tsx
│       │   └── WorkflowCanvas.module.css
│       ├── WorkflowSidebar/
│       │   ├── WorkflowSidebar.tsx
│       │   └── WorkflowSidebar.module.css
│       └── WorkflowSystem.tsx
└── app/
    └── workflow/
        └── page.tsx
```

## 🎨 Design System

### CSS Variables Structure (`variables.css`)

```css
:root {
  /* Colors - Single source of truth */
  --primary-blue: #4A90E2;
  --secondary-blue: #5BA0F2;
  --success-green: #7ED321;
  --warning-orange: #F5A623;
  --error-red: #D0021B;
  --purple-accent: #9013FE;

  /* Spacing system */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;

  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui;
  --font-size-sm: 12px;
  --font-size-md: 14px;
  --font-size-lg: 16px;

  /* Component dimensions */
  --agent-card-width: 200px;
  --agent-card-height: 120px;
  --node-width: 180px;
  --node-height: 80px;
  --sidebar-width: 280px;

  /* Shadows and effects */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.15);

  /* Transitions */
  --transition-fast: all 150ms ease-out;
  --transition-normal: all 250ms ease-out;
}
```

## 🧩 Components

### 1. AgentCard Component
**Modular, reusable card design for workflow agents**

```tsx
<AgentCard
  agent={agent}
  variant="compact"
  selected={selected}
  draggable={true}
  onSelect={handleAgentSelect}
  onDragStart={handleDragStart}
  onDragEnd={handleDragEnd}
/>
```

**Features:**
- ✅ **Modular CSS**: Self-contained styling with CSS modules
- ✅ **Multiple variants**: `default`, `compact`, `large`
- ✅ **Drag & Drop**: Full drag-and-drop support
- ✅ **Status indicators**: Visual status feedback
- ✅ **Accessibility**: ARIA labels and keyboard navigation
- ✅ **Responsive**: Mobile-optimized layouts

### 2. WorkflowNode Component
**Connectable workflow nodes with input/output ports**

```tsx
<WorkflowNode
  node={node}
  selected={selected}
  onSelect={handleNodeSelect}
  onPositionChange={handlePositionChange}
  onConnect={handleConnectionCreate}
/>
```

**Features:**
- ✅ **Connection ports**: Input/output connection points
- ✅ **Drag positioning**: Move nodes around canvas
- ✅ **Status visualization**: Real-time status updates
- ✅ **Connection management**: Create/delete connections
- ✅ **Keyboard shortcuts**: Full keyboard support

### 3. WorkflowCanvas Component
**SVG-based connection rendering with zoom and pan**

```tsx
<WorkflowCanvas
  nodes={nodes}
  connections={connections}
  zoom={zoom}
  pan={pan}
  onNodeSelect={handleNodeSelect}
  onConnectionCreate={handleConnectionCreate}
  onZoomChange={setZoom}
  onPanChange={setPan}
/>
```

**Features:**
- ✅ **SVG connections**: Smooth curved connection lines
- ✅ **Zoom & Pan**: Full canvas navigation
- ✅ **Grid background**: Visual alignment guide
- ✅ **Drop zones**: Drag-and-drop support
- ✅ **Selection tools**: Multi-node selection
- ✅ **Auto-layout**: Automatic node positioning

### 4. WorkflowSidebar Component
**Collapsible navigation with agent pool and controls**

```tsx
<WorkflowSidebar
  agents={agents}
  workflowStatus={status}
  collapsed={collapsed}
  onToggleCollapse={handleToggle}
  onWorkflowStart={handleStart}
  onWorkflowStop={handleStop}
  onWorkflowReset={handleReset}
/>
```

**Features:**
- ✅ **Agent pool**: Draggable agent cards
- ✅ **Workflow controls**: Start, stop, reset, save, load
- ✅ **Status monitoring**: Real-time workflow status
- ✅ **Collapsible sections**: Expandable/collapsible UI
- ✅ **Progress tracking**: Visual progress indicators

## 🎮 Usage

### Basic Workflow System

```tsx
import WorkflowSystem from '@/components/workflow/WorkflowSystem';

export default function WorkflowPage() {
  return (
    <MainLayout title="Workflow Engine">
      <WorkflowSystem />
    </MainLayout>
  );
}
```

### Custom Workflow Configuration

```tsx
const [workflowStatus, setWorkflowStatus] = useState({
  status: 'idle',
  message: 'Ready to start workflow',
  progress: 0
});

const handleWorkflowStart = () => {
  setWorkflowStatus({
    status: 'processing',
    message: 'Workflow running...',
    progress: 0
  });

  // Simulate workflow execution
  // ... workflow logic
};
```

## 🔧 Key Principles

### 1. No Magic Numbers
- ✅ **Every spacing, color, size** references a CSS variable
- ✅ **Consistent design system** across all components
- ✅ **Easy theme customization** by changing variables

### 2. Component Isolation
- ✅ **Each component's CSS** doesn't affect other components
- ✅ **CSS modules** prevent style conflicts
- ✅ **Self-contained styling** for each component

### 3. Reusability
- ✅ **Components work** in different contexts without modification
- ✅ **Flexible props** for customization
- ✅ **Composable architecture** for complex layouts

### 4. Maintainability
- ✅ **Changes to design tokens** propagate automatically
- ✅ **Single source of truth** for all styling
- ✅ **Clear component boundaries** and responsibilities

### 5. Performance
- ✅ **Minimal CSS bundle size** with no unused styles
- ✅ **Efficient rendering** with React optimization
- ✅ **Lazy loading** support for large workflows

## 🎨 Visual Design

### Color Scheme
- **Primary Blue**: `#4A90E2` - Main brand color
- **Secondary Blue**: `#5BA0F2` - Accent color
- **Success Green**: `#7ED321` - Success states
- **Warning Orange**: `#F5A623` - Warning states
- **Error Red**: `#D0021B` - Error states
- **Purple Accent**: `#9013FE` - Special accents

### Layout Features
- **Left sidebar navigation** + main content area
- **Agent cards** with colored icons and status indicators
- **Workflow canvas** with white background and grid
- **Connection lines** with smooth SVG curves
- **Status indicators** with real-time updates

## 🚀 Advanced Features

### Drag & Drop
- **Agent to canvas**: Drag agents from sidebar to canvas
- **Node positioning**: Drag nodes around the canvas
- **Connection creation**: Drag between node ports
- **Multi-selection**: Select multiple nodes

### Workflow Execution
- **Real-time status**: Live workflow progress
- **Error handling**: Graceful error states
- **Progress tracking**: Visual progress indicators
- **Save/Load**: Persistent workflow storage

### Responsive Design
- **Mobile optimized**: Touch-friendly interfaces
- **Tablet support**: Adaptive layouts
- **Desktop enhanced**: Full feature set
- **Accessibility**: Screen reader support

## 📱 Responsive Breakpoints

```css
/* Mobile Small (320px - 374px) */
@media (max-width: 374px) { ... }

/* Mobile Medium (375px - 479px) */
@media (max-width: 479px) and (min-width: 375px) { ... }

/* Mobile Large (480px - 639px) */
@media (max-width: 639px) and (min-width: 480px) { ... }

/* Tablet Portrait (640px - 767px) */
@media (max-width: 767px) and (min-width: 640px) { ... }

/* Tablet Landscape (768px - 1023px) */
@media (max-width: 1023px) and (min-width: 768px) { ... }

/* Desktop (1024px+) */
@media (min-width: 1024px) { ... }
```

## 🎯 Performance Optimizations

- **CSS Modules**: Scoped styling prevents conflicts
- **React.memo**: Prevents unnecessary re-renders
- **useCallback**: Optimizes event handlers
- **Lazy loading**: Load components on demand
- **Efficient SVG**: Optimized connection rendering

## 🔍 Testing

### Manual Testing Checklist
- ✅ **Agent drag & drop** from sidebar to canvas
- ✅ **Node positioning** and movement
- ✅ **Connection creation** between nodes
- ✅ **Workflow execution** and status updates
- ✅ **Save/Load** functionality
- ✅ **Responsive design** across devices
- ✅ **Keyboard navigation** and accessibility

### Automated Testing
```bash
npm run lint        # ESLint checks
npm run type-check  # TypeScript validation
npm run test        # Component tests (when added)
```

## 🚀 Future Enhancements

- **Workflow templates**: Pre-built workflow patterns
- **Advanced connections**: Conditional and data flow connections
- **Real-time collaboration**: Multi-user workflow editing
- **Workflow analytics**: Performance metrics and insights
- **Plugin system**: Extensible agent types
- **Version control**: Workflow versioning and history

## 📚 Documentation

- **Component API**: Detailed prop documentation
- **CSS Variables**: Complete design token reference
- **Usage Examples**: Code samples and patterns
- **Best Practices**: Development guidelines
- **Performance Tips**: Optimization recommendations

---

**Built with ❤️ using React, TypeScript, and CSS Modules**

*This modular workflow system demonstrates production-ready architecture with single source of truth design patterns, fully composable components, and comprehensive responsive design.*
