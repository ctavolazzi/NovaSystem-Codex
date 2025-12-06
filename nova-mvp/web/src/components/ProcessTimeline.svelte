<script>
  export let currentPhase = 'pending';

  const phases = [
    { id: 'unpacking', label: 'Unpack', description: 'DCE breaks down the problem' },
    { id: 'analyzing', label: 'Analyze', description: 'Experts analyze in parallel' },
    { id: 'synthesizing', label: 'Synthesize', description: 'DCE combines insights' },
    { id: 'completed', label: 'Complete', description: 'Solution ready' }
  ];

  function getPhaseStatus(phaseId) {
    const order = ['pending', 'unpacking', 'analyzing', 'synthesizing', 'completed'];
    const currentIndex = order.indexOf(currentPhase);
    const phaseIndex = order.indexOf(phaseId);

    if (phaseIndex < currentIndex) return 'completed';
    if (phaseIndex === currentIndex) return 'active';
    return 'pending';
  }
</script>

<div class="timeline">
  {#each phases as phase, i}
    {@const status = getPhaseStatus(phase.id)}
    <div class="phase" class:completed={status === 'completed'} class:active={status === 'active'}>
      <div class="phase-dot">
        {#if status === 'completed'}
          <span class="check">✓</span>
        {:else if status === 'active'}
          <span class="pulse"></span>
        {:else}
          <span class="number">{i + 1}</span>
        {/if}
      </div>
      <div class="phase-content">
        <span class="label">{phase.label}</span>
        <span class="description">{phase.description}</span>
      </div>
    </div>
    {#if i < phases.length - 1}
      <div class="connector" class:active={getPhaseStatus(phases[i + 1].id) !== 'pending'}></div>
    {/if}
  {/each}
</div>

<style>
  .timeline {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    overflow-x: auto;
  }

  .phase {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    min-width: 120px;
  }

  .phase-dot {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  .phase.active .phase-dot {
    background: rgba(0, 255, 170, 0.1);
    border-color: #00ffaa;
    box-shadow: 0 0 20px rgba(0, 255, 170, 0.3);
  }

  .phase.completed .phase-dot {
    background: #00ffaa;
    border-color: #00ffaa;
  }

  .phase-dot .number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    font-weight: 600;
    color: #6b7280;
  }

  .phase-dot .check {
    color: #0a0a0f;
    font-size: 1.2rem;
    font-weight: bold;
  }

  .phase-dot .pulse {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #00ffaa;
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.7; }
  }

  .phase-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    text-align: center;
  }

  .phase-content .label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #9ca3af;
    transition: color 0.3s ease;
  }

  .phase.active .phase-content .label,
  .phase.completed .phase-content .label {
    color: #e0e0e0;
  }

  .phase-content .description {
    font-size: 0.7rem;
    color: #4b5563;
    max-width: 100px;
  }

  .connector {
    width: 60px;
    height: 2px;
    background: rgba(255, 255, 255, 0.1);
    margin: 0 0.5rem;
    margin-bottom: 3rem;
    transition: background 0.3s ease;
  }

  .connector.active {
    background: linear-gradient(90deg, #00ffaa, rgba(0, 255, 170, 0.3));
  }

  @media (max-width: 700px) {
    .timeline {
      flex-wrap: wrap;
      gap: 1rem;
    }

    .connector {
      display: none;
    }

    .phase {
      min-width: 100px;
    }
  }
</style>
