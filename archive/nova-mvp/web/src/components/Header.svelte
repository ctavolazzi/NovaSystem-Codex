<script>
  export let currentPhase = 'idle';
  export let sessionId = null;

  const phaseLabels = {
    idle: 'Ready',
    connecting: 'Connecting...',
    pending: 'Initializing',
    unpacking: 'Unpacking Problem',
    analyzing: 'Analyzing',
    synthesizing: 'Synthesizing',
    completed: 'Complete',
    error: 'Error'
  };

  const phaseColors = {
    idle: '#6b7280',
    connecting: '#f59e0b',
    pending: '#f59e0b',
    unpacking: '#f59e0b',
    analyzing: '#3b82f6',
    synthesizing: '#8b5cf6',
    completed: '#00ffaa',
    error: '#ef4444'
  };
</script>

<header>
  <div class="logo">
    <div class="logo-icon">
      <span class="glow">N</span>
    </div>
    <div class="logo-text">
      <span class="name">NOVA</span>
      <span class="tag">MVP</span>
    </div>
  </div>

  <div class="status-bar">
    <div class="status-indicator" style="--status-color: {phaseColors[currentPhase]}">
      <span class="dot" class:pulse={currentPhase !== 'idle' && currentPhase !== 'completed' && currentPhase !== 'error'}></span>
      <span class="label">{phaseLabels[currentPhase]}</span>
    </div>
    {#if sessionId}
      <div class="session-id mono">
        <span class="prefix">SESSION:</span>
        <span class="id">{sessionId}</span>
      </div>
    {/if}
  </div>
</header>

<style>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    background: linear-gradient(180deg, rgba(10, 10, 15, 0.95) 0%, rgba(10, 10, 15, 0.8) 100%);
    border-bottom: 1px solid rgba(0, 255, 170, 0.1);
    backdrop-filter: blur(10px);
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .logo-icon {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #00ffaa20, #00aa7720);
    border: 2px solid #00ffaa40;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
  }

  .logo-icon .glow {
    color: #00ffaa;
    text-shadow: 0 0 20px rgba(0, 255, 170, 0.6);
  }

  .logo-text {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
  }

  .logo-text .name {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    background: linear-gradient(90deg, #00ffaa, #00ddaa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .logo-text .tag {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    color: #6b7280;
    text-transform: uppercase;
  }

  .status-bar {
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }

  .status-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 100px;
  }

  .status-indicator .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--status-color);
    box-shadow: 0 0 10px var(--status-color);
  }

  .status-indicator .dot.pulse {
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
  }

  .status-indicator .label {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--status-color);
  }

  .session-id {
    font-size: 0.75rem;
    color: #6b7280;
    display: flex;
    gap: 0.3rem;
  }

  .session-id .prefix {
    opacity: 0.6;
  }

  .session-id .id {
    color: #00ffaa;
    font-weight: 500;
  }

  @media (max-width: 600px) {
    header {
      flex-direction: column;
      gap: 1rem;
      padding: 1rem;
    }

    .status-bar {
      width: 100%;
      justify-content: center;
    }
  }
</style>
