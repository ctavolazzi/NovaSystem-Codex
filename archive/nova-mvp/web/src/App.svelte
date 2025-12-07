<script>
  import Header from './components/Header.svelte';
  import ProblemInput from './components/ProblemInput.svelte';
  import ProcessTimeline from './components/ProcessTimeline.svelte';
  import AgentPanel from './components/AgentPanel.svelte';

  let problem = '';
  let domains = ['technology', 'business'];
  let provider = 'auto';
  let currentPhase = 'idle';
  let agentResponses = [];
  let sessionId = null;
  let isProcessing = false;
  let error = null;
  let ws = null;

  const availableDomains = [
    { id: 'technology', name: 'Technology', icon: '⚙️' },
    { id: 'business', name: 'Business', icon: '📊' },
    { id: 'security', name: 'Security', icon: '🔒' },
    { id: 'ux', name: 'User Experience', icon: '🎨' },
    { id: 'data', name: 'Data & Analytics', icon: '📈' },
    { id: 'operations', name: 'Operations', icon: '🔧' },
    { id: 'legal', name: 'Legal', icon: '⚖️' },
    { id: 'finance', name: 'Finance', icon: '💰' }
  ];

  async function startSolve() {
    if (!problem.trim()) return;

    isProcessing = true;
    error = null;
    agentResponses = [];
    currentPhase = 'connecting';

    // Generate session ID
    sessionId = Math.random().toString(36).substring(2, 10);

    // Connect via WebSocket for real-time updates
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/api/ws/${sessionId}`;

    try {
      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        currentPhase = 'pending';
        // Send solve request via WebSocket
        ws.send(JSON.stringify({
          action: 'solve',
          problem: problem,
          domains: domains,
          provider: provider
        }));
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'phase_change') {
          currentPhase = data.phase;
        } else if (data.type === 'agent_response') {
          agentResponses = [...agentResponses, data];
        } else if (data.type === 'complete') {
          currentPhase = 'completed';
          isProcessing = false;
          ws.close();
        } else if (data.type === 'error') {
          error = data.message;
          currentPhase = 'error';
          isProcessing = false;
          ws.close();
        }
      };

      ws.onerror = (e) => {
        // Fall back to sync API
        fallbackToSyncApi();
      };

      ws.onclose = () => {
        if (isProcessing && currentPhase !== 'completed') {
          fallbackToSyncApi();
        }
      };

    } catch (e) {
      fallbackToSyncApi();
    }
  }

  async function fallbackToSyncApi() {
    currentPhase = 'unpacking';

    try {
      const response = await fetch('/api/solve/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem, domains, provider })
      });

      if (!response.ok) throw new Error('API request failed');

      const data = await response.json();
      sessionId = data.session_id;

      // Convert to agent responses format
      if (data.unpack_result) {
        agentResponses = [...agentResponses, {
          agent_name: data.unpack_result.agent_name,
          agent_type: data.unpack_result.agent_type,
          content: data.unpack_result.content,
          success: data.unpack_result.success
        }];
      }

      currentPhase = 'analyzing';

      for (const result of data.analysis_results || []) {
        agentResponses = [...agentResponses, {
          agent_name: result.agent_name,
          agent_type: result.agent_type,
          content: result.content,
          success: result.success
        }];
      }

      currentPhase = 'synthesizing';

      if (data.synthesis_result) {
        agentResponses = [...agentResponses, {
          agent_name: data.synthesis_result.agent_name,
          agent_type: data.synthesis_result.agent_type,
          content: data.synthesis_result.content,
          success: data.synthesis_result.success
        }];
      }

      currentPhase = data.phase || 'completed';
      isProcessing = false;

    } catch (e) {
      error = e.message;
      currentPhase = 'error';
      isProcessing = false;
    }
  }

  function reset() {
    problem = '';
    currentPhase = 'idle';
    agentResponses = [];
    sessionId = null;
    error = null;
    if (ws) ws.close();
  }

  function toggleDomain(domain) {
    if (domains.includes(domain)) {
      domains = domains.filter(d => d !== domain);
    } else {
      domains = [...domains, domain];
    }
  }
</script>

<main>
  <div class="grid-bg"></div>

  <Header {currentPhase} {sessionId} />

  <div class="container">
    {#if currentPhase === 'idle' || currentPhase === 'error'}
      <ProblemInput
        bind:problem
        {domains}
        {availableDomains}
        {provider}
        {error}
        on:toggleDomain={(e) => toggleDomain(e.detail)}
        on:setProvider={(e) => provider = e.detail}
        on:submit={startSolve}
      />
    {:else}
      <ProcessTimeline {currentPhase} />

      <div class="agents-grid">
        {#each agentResponses as response, i}
          <AgentPanel {response} index={i} />
        {/each}
      </div>

      {#if currentPhase === 'completed'}
        <button class="reset-btn" on:click={reset}>
          <span class="icon">↻</span> New Problem
        </button>
      {/if}
    {/if}
  </div>
</main>

<style>
  main {
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
  }

  .grid-bg {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
      linear-gradient(rgba(0, 255, 170, 0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0, 255, 170, 0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    position: relative;
    z-index: 1;
  }

  .agents-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }

  .reset-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 2rem auto 0;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #00ffaa20, #00aa7720);
    border: 1px solid #00ffaa40;
    color: #00ffaa;
    font-family: 'Sora', sans-serif;
    font-size: 1rem;
    font-weight: 500;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .reset-btn:hover {
    background: linear-gradient(135deg, #00ffaa30, #00aa7730);
    border-color: #00ffaa60;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 255, 170, 0.2);
  }

  .reset-btn .icon {
    font-size: 1.2rem;
  }
</style>
