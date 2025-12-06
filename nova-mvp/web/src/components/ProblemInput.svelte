<script>
  import { createEventDispatcher } from 'svelte';

  export let problem = '';
  export let domains = [];
  export let availableDomains = [];
  export let provider = 'auto';
  export let error = null;

  const dispatch = createEventDispatcher();

  function handleSubmit() {
    if (problem.trim() && domains.length > 0) {
      dispatch('submit');
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && e.metaKey) {
      handleSubmit();
    }
  }
</script>

<div class="input-section">
  <div class="input-header">
    <h1>What problem are we solving?</h1>
    <p class="subtitle">Our AI agents will analyze this from multiple perspectives</p>
  </div>

  {#if error}
    <div class="error-banner">
      <span class="icon">⚠</span>
      <span>{error}</span>
    </div>
  {/if}

  <div class="input-container">
    <textarea
      bind:value={problem}
      on:keydown={handleKeydown}
      placeholder="Describe your problem, question, or challenge..."
      rows="4"
    ></textarea>
    <div class="input-footer">
      <span class="hint mono">⌘ + Enter to submit</span>
    </div>
  </div>

  <div class="domains-section">
    <h3>Select Domain Experts</h3>
    <div class="domains-grid">
      {#each availableDomains as domain}
        <button
          class="domain-chip"
          class:selected={domains.includes(domain.id)}
          on:click={() => dispatch('toggleDomain', domain.id)}
        >
          <span class="icon">{domain.icon}</span>
          <span class="name">{domain.name}</span>
        </button>
      {/each}
    </div>
  </div>

  <div class="provider-section">
    <h3>LLM Provider</h3>
    <div class="provider-options">
      {#each ['auto', 'claude', 'openai', 'mock'] as p}
        <button
          class="provider-btn"
          class:selected={provider === p}
          on:click={() => dispatch('setProvider', p)}
        >
          {p === 'auto' ? 'Auto-detect' : p.charAt(0).toUpperCase() + p.slice(1)}
        </button>
      {/each}
    </div>
  </div>

  <button
    class="submit-btn"
    on:click={handleSubmit}
    disabled={!problem.trim() || domains.length === 0}
  >
    <span class="text">Start Analysis</span>
    <span class="arrow">→</span>
  </button>
</div>

<style>
  .input-section {
    max-width: 700px;
    margin: 3rem auto;
  }

  .input-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .input-header h1 {
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #ffffff, #a0a0a0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .input-header .subtitle {
    color: #6b7280;
    font-size: 1rem;
  }

  .error-banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    margin-bottom: 1.5rem;
    color: #ef4444;
    font-size: 0.9rem;
  }

  .error-banner .icon {
    font-size: 1.2rem;
  }

  .input-container {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    overflow: hidden;
    transition: border-color 0.2s ease;
  }

  .input-container:focus-within {
    border-color: #00ffaa40;
    box-shadow: 0 0 0 3px rgba(0, 255, 170, 0.1);
  }

  textarea {
    width: 100%;
    padding: 1.25rem;
    background: transparent;
    border: none;
    color: #e0e0e0;
    font-family: 'Sora', sans-serif;
    font-size: 1rem;
    line-height: 1.6;
    resize: none;
    outline: none;
  }

  textarea::placeholder {
    color: #4b5563;
  }

  .input-footer {
    padding: 0.75rem 1.25rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: flex-end;
  }

  .input-footer .hint {
    font-size: 0.75rem;
    color: #6b7280;
  }

  .domains-section, .provider-section {
    margin-top: 2rem;
  }

  h3 {
    font-size: 0.9rem;
    font-weight: 600;
    color: #9ca3af;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .domains-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .domain-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 100px;
    color: #9ca3af;
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .domain-chip:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .domain-chip.selected {
    background: rgba(0, 255, 170, 0.1);
    border-color: #00ffaa40;
    color: #00ffaa;
  }

  .domain-chip .icon {
    font-size: 1rem;
  }

  .provider-options {
    display: flex;
    gap: 0.5rem;
  }

  .provider-btn {
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    color: #9ca3af;
    font-family: 'Sora', sans-serif;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .provider-btn:hover {
    background: rgba(255, 255, 255, 0.05);
  }

  .provider-btn.selected {
    background: rgba(59, 130, 246, 0.1);
    border-color: #3b82f640;
    color: #3b82f6;
  }

  .submit-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    width: 100%;
    margin-top: 2.5rem;
    padding: 1.25rem 2rem;
    background: linear-gradient(135deg, #00ffaa, #00cc88);
    border: none;
    border-radius: 12px;
    color: #0a0a0f;
    font-family: 'Sora', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 255, 170, 0.3);
  }

  .submit-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .submit-btn .arrow {
    font-size: 1.3rem;
    transition: transform 0.2s ease;
  }

  .submit-btn:hover:not(:disabled) .arrow {
    transform: translateX(4px);
  }
</style>
