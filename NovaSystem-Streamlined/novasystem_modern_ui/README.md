# NovaSystem Modern UI

A modern, component-based React/Next.js frontend for NovaSystem that maintains the authentic Windows XP aesthetic while providing better maintainability, reusability, and developer experience.

## 🚀 Features

### ✨ Modern Architecture
- **Next.js 15** with App Router and TypeScript
- **React 19** with modern hooks and patterns
- **Tailwind CSS** for utility-first styling
- **Component-based architecture** with reusable, composable components
- **Single source of truth** for navigation and configuration

### 🎨 Authentic Windows XP Theme
- **Pixel-perfect Windows XP styling** with authentic colors and gradients
- **Classic scrollbars** matching Windows XP appearance
- **Responsive design** that works on all screen sizes
- **Touch-friendly interactions** for mobile devices
- **Accessibility support** with reduced motion and high contrast modes

### 🔧 Developer Experience
- **TypeScript** for type safety and better IDE support
- **Hot reload** with Turbopack for fast development
- **ESLint** configuration for code quality
- **Component library** with reusable UI components
- **API integration** with existing Flask backend

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Home page
│   └── workflow/          # Workflow page
├── components/            # Reusable React components
│   ├── ui/               # Basic UI components (Window, Button, etc.)
│   ├── navigation/       # Navigation components (Sidebar, MenuBar, Taskbar)
│   └── layout/           # Layout components (MainLayout)
├── lib/                  # Utilities and API integration
│   ├── api.ts           # Flask backend API client
│   └── utils.ts         # Utility functions
└── styles/              # Global styles and themes
    └── globals.css      # Windows XP theme and responsive styles
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 18+
- npm or yarn
- Python 3.8+ (for Flask backend)

### Development Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```
   This will start the Next.js development server on `http://localhost:3000`

3. **Start both frontend and backend:**
   ```bash
   npm run dev:flask
   ```
   This will start both Next.js (port 3000) and Flask (port 5000) concurrently

### Production Build

```bash
npm run build
npm run start
```

## 🎯 Component Architecture

### Core Components

#### `MainLayout`
The main layout component that provides the Windows XP window structure:
```tsx
<MainLayout title="Page Title" icon={<Icon />}>
  <PageContent />
</MainLayout>
```

#### `NavigationProvider`
Context provider that manages navigation state and provides:
- Current page detection
- Responsive breakpoint detection
- Keyboard shortcuts (Ctrl+1-4)
- Touch gestures for mobile
- Single source of truth for navigation configuration

#### `Sidebar`
Responsive sidebar navigation that adapts to screen size:
- Desktop: Vertical sidebar with sections
- Mobile: Horizontal scrollable navigation

#### `MenuBar`
Windows XP-style menu bar with dropdown menus:
- File, Edit, View, Tools, Help menus
- Context-sensitive menu items
- Keyboard navigation support

#### `Taskbar`
Bottom taskbar with:
- Start button and menu
- System tray with status indicators
- Date/time display
- Mobile quick actions

### UI Components

#### `Window`
Windows XP-style window container with:
- Title bar with minimize/maximize/close buttons
- Authentic Windows XP styling
- Proper z-index and shadow handling

## 🔌 API Integration

The modern UI integrates seamlessly with the existing Flask backend through a typed API client:

```typescript
import { apiClient } from '@/lib/api';

// Problem solving
const response = await apiClient.solveProblem("Your problem here");

// Session management
const sessions = await apiClient.getSessions();

// Workflow execution
const result = await apiClient.executeWorkflow(workflowData);
```

### Environment Configuration

Set the Flask backend URL:
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: ≤ 768px - Horizontal navigation, touch gestures
- **Tablet**: 769px - 1024px - Adapted sidebar layout
- **Desktop**: ≥ 1025px - Full sidebar navigation

### Mobile Features
- **Swipe navigation** between main pages
- **Touch-friendly** button sizes (44px minimum)
- **Horizontal sidebar** with quick actions
- **Landscape orientation** support

## 🎨 Windows XP Theme

### Color Palette
```css
--primary-color: #0054E3;      /* Windows XP Blue */
--secondary-color: #3B8CFF;    /* Lighter blue */
--accent-color: #6BBF44;       /* Green accent */
--bg-primary: #ECE9D8;         /* Window background */
--bg-secondary: #F1F1F1;       /* Secondary background */
--text-primary: #000000;       /* Black text */
```

### Authentic Elements
- **Gradient buttons** with proper inset/outset borders
- **Classic scrollbars** matching Windows XP appearance
- **Proper shadows** and depth effects
- **Authentic fonts** (Tahoma, MS Sans Serif fallbacks)

## 🧪 Testing

### Development Testing
```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Manual testing
npm run dev
```

### Integration Testing
The UI integrates with the existing Flask backend. Test by:
1. Starting both frontend and backend: `npm run dev:flask`
2. Navigate to `http://localhost:3000`
3. Test problem solving, workflow creation, and session management

## 🚀 Deployment

### Static Export
```bash
npm run build
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔄 Migration from Flask UI

The modern UI is designed as a complete replacement for the Flask templates:

### Benefits Over Flask Templates
- **Better maintainability** - Component-based architecture
- **Type safety** - Full TypeScript support
- **Better performance** - Client-side routing and optimization
- **Modern tooling** - Hot reload, linting, type checking
- **Reusable components** - Single source of truth for UI elements
- **Better responsive design** - Mobile-first approach
- **Improved accessibility** - ARIA labels, keyboard navigation

### Migration Path
1. **Parallel development** - Both UIs can run simultaneously
2. **Gradual migration** - Replace Flask routes one by one
3. **API compatibility** - Same Flask backend API endpoints
4. **Feature parity** - All existing functionality preserved

## 📚 Next Steps

### Immediate
- [ ] Complete remaining pages (Analytics, Monitor, Settings, Help, About, Sessions, History)
- [ ] Add comprehensive testing suite
- [ ] Implement real-time updates with WebSocket integration
- [ ] Add dark mode toggle

### Future Enhancements
- [ ] PWA support for offline functionality
- [ ] Advanced workflow visualization with drag-and-drop
- [ ] Real-time collaboration features
- [ ] Plugin system for custom agents
- [ ] Advanced analytics dashboard with charts

## 🤝 Contributing

1. Follow the existing component patterns
2. Maintain Windows XP theme consistency
3. Add TypeScript types for all props and API responses
4. Test responsive design on multiple screen sizes
5. Ensure accessibility compliance

## 📄 License

Same as NovaSystem project.