<script>
  export let response;
  export let index = 0;

  const agentStyles = {
    dce: {
      color: '#00ffaa',
      icon: '◈',
      gradient: 'linear-gradient(135deg, rgba(0, 255, 170, 0.1), rgba(0, 170, 119, 0.05))'
    },
    cae: {
      color: '#f59e0b',
      icon: '⚠',
      gradient: 'linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.05))'
    },
    domain_technology: {
      color: '#3b82f6',
      icon: '⚙',
      gradient: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.05))'
    },
    domain_tech: {
      color: '#3b82f6',
      icon: '⚙',
      gradient: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.05))'
    },
    domain_business: {
      color: '#8b5cf6',
      icon: '📊',
      gradient: 'linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(124, 58, 237, 0.05))'
    },
    domain_security: {
      color: '#ef4444',
      icon: '🔒',
      gradient: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05))'
    },
    domain_ux: {
      color: '#ec4899',
      icon: '🎨',
      gradient: 'linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(219, 39, 119, 0.05))'
    },
    domain_data: {
      color: '#06b6d4',
      icon: '📈',
      gradient: 'linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(8, 145, 178, 0.05))'
    },
    default: {
      color: '#6b7280',
      icon: '●',
      gradient: 'linear-gradient(135deg, rgba(107, 114, 128, 0.1), rgba(75, 85, 99, 0.05))'
    }
  };

  $: style = agentStyles[response.agent_type] || agentStyles.default;
  $: isSynthesis = response.agent_type === 'dce' && response.content.includes('Synthesis') || response.content.includes('Summary');
</script>

<div
  class="agent-panel"
  class:synthesis={isSynthesis}
  style="--agent-color: {style.color}; --agent-gradient: {style.gradient}; animation-delay: {index * 0.1}s"
>
  <div class="panel-header">
    <div class="agent-icon">{style.icon}</div>
    <div class="agent-info">
      <span class="agent-name">{response.agent_name}</span>
      <span class="agent-type">{response.agent_type.replace('domain_', '').toUpperCase()}</span>
    </div>
    <div class="status-badge" class:error={!response.success}>
      {response.success ? '✓' : '✗'}
    </div>
  </div>

  <div class="panel-content">
    {#if response.success}
      <div class="content-text">
        {@html formatContent(response.content)}
      </div>
    {:else}
      <div class="error-message">
        {response.error || 'An error occurred'}
      </div>
    {/if}
  </div>
</div>

<script context="module">
  function formatContent(text) {
    if (!text) return '';

    // Convert markdown-like formatting to HTML
    return text
      // Headers
      .replace(/^### (.+)$/gm, '<h4>$1</h4>')
      .replace(/^## (.+)$/gm, '<h3>$1</h3>')
      .replace(/^\*\*(.+?)\*\*:?$/gm, '<h4>$1</h4>')
      // Bold
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      // Lists
      .replace(/^- (.+)$/gm, '<li>$1</li>')
      .replace(/^(\d+)\. (.+)$/gm, '<li><span class="num">$1.</span> $2</li>')
      // Tables (basic)
      .replace(/\|(.+)\|/g, (match) => {
        const cells = match.split('|').filter(c => c.trim());
        if (cells.every(c => c.trim().match(/^-+$/))) {
          return '<tr class="separator"></tr>';
        }
        return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
      })
      // Line breaks
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>');
  }
</script>

<style>
  .agent-panel {
    background: var(--agent-gradient);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    overflow: hidden;
    animation: fadeIn 0.4s ease forwards;
    opacity: 0;
    transform: translateY(10px);
  }

  .agent-panel.synthesis {
    grid-column: 1 / -1;
    border-color: var(--agent-color);
    box-shadow: 0 0 30px rgba(0, 255, 170, 0.1);
  }

  @keyframes fadeIn {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .panel-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    background: rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .agent-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--agent-color);
    border-radius: 10px;
    color: var(--agent-color);
  }

  .agent-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  .agent-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e0e0e0;
  }

  .agent-type {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--agent-color);
    opacity: 0.8;
    letter-spacing: 0.05em;
  }

  .status-badge {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 255, 170, 0.2);
    border-radius: 50%;
    color: #00ffaa;
    font-size: 0.8rem;
    font-weight: bold;
  }

  .status-badge.error {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
  }

  .panel-content {
    padding: 1.25rem;
    max-height: 400px;
    overflow-y: auto;
  }

  .agent-panel.synthesis .panel-content {
    max-height: none;
  }

  .content-text {
    font-size: 0.9rem;
    line-height: 1.7;
    color: #c0c0c0;
  }

  .content-text :global(h3),
  .content-text :global(h4) {
    color: var(--agent-color);
    margin: 1.25rem 0 0.5rem 0;
    font-size: 0.95rem;
    font-weight: 600;
  }

  .content-text :global(h3):first-child,
  .content-text :global(h4):first-child {
    margin-top: 0;
  }

  .content-text :global(strong) {
    color: #e0e0e0;
    font-weight: 600;
  }

  .content-text :global(li) {
    margin-left: 1.25rem;
    margin-bottom: 0.4rem;
    list-style: none;
    position: relative;
  }

  .content-text :global(li)::before {
    content: '›';
    position: absolute;
    left: -1rem;
    color: var(--agent-color);
    font-weight: bold;
  }

  .content-text :global(.num) {
    color: var(--agent-color);
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    margin-right: 0.25rem;
  }

  .content-text :global(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.85rem;
  }

  .content-text :global(td) {
    padding: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .error-message {
    color: #ef4444;
    font-size: 0.9rem;
    padding: 1rem;
    background: rgba(239, 68, 68, 0.1);
    border-radius: 8px;
  }

  /* Custom scrollbar */
  .panel-content::-webkit-scrollbar {
    width: 6px;
  }

  .panel-content::-webkit-scrollbar-track {
    background: transparent;
  }

  .panel-content::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }

  .panel-content::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
  }
</style>
