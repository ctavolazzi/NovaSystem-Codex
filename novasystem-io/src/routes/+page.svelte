<script lang="ts">
  import { onMount } from 'svelte';

  const API_BASE = 'http://localhost:8000';

  type DocumentResponse = {
    id: number;
    log_id: number;
    doc_type: string;
    title: string;
    notes: string | null;
    created_at: string;
    download_url: string;
  };

  type DocumentJobStatus = {
    job_id: string;
    status: 'queued' | 'processing' | 'completed' | 'failed';
    document?: DocumentResponse | null;
    error?: string | null;
  };

  type LogEntry = {
    id: number;
    created_at: string;
    activity: string;
    details: string | null;
    tags: string[];
    metadata: Record<string, unknown>;
    documents: DocumentResponse[];
  };

  let activity = '';
  let details = '';
  let tags = '';
  let metadataInput = '';
  let logs: LogEntry[] = [];
  let loading = false;
  let isFetching = false;
  let errorMessage = '';
  let successMessage = '';

  let filterSearch = '';
  let filterTag = '';
  let filterStart = '';
  let filterEnd = '';
  let filterLimit = 50;

  const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
  const DOCUMENT_POLL_INTERVAL = 2000;

  let documentNotes: Record<number, string> = {};
  let documentStatus: Record<number, string> = {};
  let pendingDocumentJobs: Record<number, string[]> = {};

  onMount(() => {
    fetchLogs();
  });

  const buildQueryString = () => {
    const params = new URLSearchParams();
    if (filterSearch.trim()) params.set('search', filterSearch.trim());
    if (filterTag.trim()) params.set('tag', filterTag.trim());
    if (filterStart) params.set('start', new Date(filterStart).toISOString());
    if (filterEnd) params.set('end', new Date(filterEnd).toISOString());
    if (filterLimit) params.set('limit', String(filterLimit));
    return params.toString();
  };

  const fetchLogs = async () => {
    isFetching = true;
    errorMessage = '';
    try {
      const query = buildQueryString();
      const response = await fetch(`${API_BASE}/api/logs${query ? `?${query}` : ''}`);
      if (!response.ok) {
        throw new Error('Failed to load log entries.');
      }
      const payload = await response.json();
      logs = payload.items ?? [];
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Unexpected error while fetching logs.';
    } finally {
      isFetching = false;
    }
  };

  const parseTags = (value: string) =>
    value
      .split(',')
      .map((tag) => tag.trim())
      .filter(Boolean);

  const parseMetadata = () => {
    const trimmed = metadataInput.trim();
    if (!trimmed) return {};
    try {
      return JSON.parse(trimmed);
    } catch (error) {
      throw new Error('Metadata must be valid JSON.');
    }
  };

  const resetForm = () => {
    activity = '';
    details = '';
    tags = '';
    metadataInput = '';
  };

  const submitLog = async () => {
    errorMessage = '';
    successMessage = '';
    loading = true;
    try {
      const metadata = parseMetadata();
      const response = await fetch(`${API_BASE}/api/logs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          activity: activity.trim(),
          details: details.trim() || null,
          tags: parseTags(tags),
          metadata
        })
      });
      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || 'Unable to record log entry.');
      }
      const newLog: LogEntry = await response.json();
      successMessage = 'Activity recorded successfully.';
      logs = [newLog, ...logs];
      resetForm();
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Unexpected error while saving the log entry.';
    } finally {
      loading = false;
    }
  };

  const handleSubmit = async (event: SubmitEvent) => {
    event.preventDefault();
    if (!activity.trim()) {
      errorMessage = 'Activity description is required.';
      return;
    }
    await submitLog();
  };

  const updateDocumentNotes = (logId: number, value: string) => {
    documentNotes = { ...documentNotes, [logId]: value };
  };

  const addPendingJobId = (logId: number, jobId: string) => {
    pendingDocumentJobs = {
      ...pendingDocumentJobs,
      [logId]: [...(pendingDocumentJobs[logId] ?? []), jobId]
    };
  };

  const removePendingJobId = (logId: number, jobId: string) => {
    const remaining = (pendingDocumentJobs[logId] ?? []).filter((id) => id !== jobId);
    const updatedJobs = { ...pendingDocumentJobs };
    if (remaining.length) {
      updatedJobs[logId] = remaining;
    } else {
      delete updatedJobs[logId];
    }
    pendingDocumentJobs = updatedJobs;
  };

  const appendDocumentToLog = (logId: number, document: DocumentResponse) => {
    logs = logs.map((entry) => {
      if (entry.id !== logId) return entry;
      const alreadyExists = entry.documents.some((item) => item.id === document.id);
      if (alreadyExists) return entry;
      return { ...entry, documents: [...entry.documents, document] };
    });
    documentNotes = { ...documentNotes, [logId]: '' };
    documentStatus = { ...documentStatus, [logId]: 'Document ready.' };
    successMessage = `Document generated: ${document.title}`;
  };

  const updateDocumentStatusMessage = (logId: number, status: DocumentJobStatus['status']) => {
    let message = '';
    if (status === 'queued') {
      message = 'Document queued…';
    } else if (status === 'processing') {
      message = 'Document processing…';
    }
    if (message) {
      documentStatus = { ...documentStatus, [logId]: message };
    }
  };

  const monitorDocumentJob = async (logId: number, initialStatus: DocumentJobStatus) => {
    if (!initialStatus?.job_id) {
      throw new Error('Document job response was missing an identifier.');
    }

    const jobId = initialStatus.job_id;
    addPendingJobId(logId, jobId);

    try {
      let currentStatus: DocumentJobStatus = initialStatus;

      while (true) {
        if (currentStatus.status === 'completed') {
          if (currentStatus.document) {
            appendDocumentToLog(logId, currentStatus.document);
            return;
          }
          throw new Error('Document metadata was not provided for the completed job.');
        }

        if (currentStatus.status === 'failed') {
          const message = currentStatus.error || 'Document generation failed.';
          throw new Error(message);
        }

        updateDocumentStatusMessage(logId, currentStatus.status);

        await wait(DOCUMENT_POLL_INTERVAL);

        const response = await fetch(`${API_BASE}/api/documents/jobs/${jobId}`);
        if (!response.ok) {
          const message = await response.text();
          throw new Error(message || 'Unable to check document job status.');
        }
        const nextStatus: DocumentJobStatus = await response.json();
        currentStatus = nextStatus;
      }
    } finally {
      removePendingJobId(logId, jobId);
    }
  };

  const generateDocument = async (log: LogEntry, docType: string) => {
    errorMessage = '';
    successMessage = '';
    documentStatus = { ...documentStatus, [log.id]: 'Submitting document request…' };
    try {
      const response = await fetch(`${API_BASE}/api/logs/${log.id}/documents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          doc_type: docType,
          notes: documentNotes[log.id]?.trim() || null
        })
      });
      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || 'Failed to generate document.');
      }
      const jobStatus: DocumentJobStatus = await response.json();
      await monitorDocumentJob(log.id, jobStatus);
    } catch (error) {
      documentStatus = { ...documentStatus, [log.id]: '' };
      errorMessage = error instanceof Error ? error.message : 'Unexpected error while generating document.';
    }
  };

  const formatDate = (value: string) => new Date(value).toLocaleString();
</script>

<svelte:head>
  <title>NovaSystem Activity Log</title>
</svelte:head>

<main class="layout">
  <section class="panel">
    <h1>Activity Log</h1>
    <p class="lead">Capture your ongoing work, generate supporting documents, and search the history.</p>

    {#if errorMessage}
      <div class="alert alert-error">{errorMessage}</div>
    {/if}
    {#if successMessage}
      <div class="alert alert-success">{successMessage}</div>
    {/if}

    <form class="log-form" on:submit|preventDefault={handleSubmit}>
      <div class="field">
        <label for="activity">Activity*</label>
        <input id="activity" bind:value={activity} placeholder="Summarise what happened" required />
      </div>
      <div class="field">
        <label for="details">Details</label>
        <textarea
          id="details"
          bind:value={details}
          rows={4}
          placeholder="Add context, blockers, or outcomes"
        ></textarea>
      </div>
      <div class="field-group">
        <div class="field">
          <label for="tags">Tags</label>
          <input id="tags" bind:value={tags} placeholder="Comma separated (e.g. research, client)" />
        </div>
        <div class="field">
          <label for="metadata">Metadata (JSON)</label>
          <input id="metadata" bind:value={metadataInput} placeholder='{"project": "Nova"}' />
        </div>
      </div>
      <button type="submit" class="primary" disabled={loading}>
        {#if loading}
          Saving…
        {:else}
          Save activity
        {/if}
      </button>
    </form>
  </section>

  <section class="panel">
    <header class="list-header">
      <h2>History</h2>
      <button class="secondary" on:click={fetchLogs} disabled={isFetching}>
        {#if isFetching}
          Refreshing…
        {:else}
          Refresh
        {/if}
      </button>
    </header>

    <div class="filters">
      <div class="field">
        <label for="search">Search</label>
        <input id="search" bind:value={filterSearch} placeholder="Keyword" />
      </div>
      <div class="field">
        <label for="filter-tag">Tag</label>
        <input id="filter-tag" bind:value={filterTag} placeholder="Tag value" />
      </div>
      <div class="field">
        <label for="start">Start</label>
        <input id="start" type="datetime-local" bind:value={filterStart} />
      </div>
      <div class="field">
        <label for="end">End</label>
        <input id="end" type="datetime-local" bind:value={filterEnd} />
      </div>
      <div class="field">
        <label for="limit">Limit</label>
        <input id="limit" type="number" min="1" max="500" bind:value={filterLimit} />
      </div>
      <button class="secondary" on:click={fetchLogs} disabled={isFetching}>Apply filters</button>
    </div>

    {#if logs.length === 0}
      <p class="empty">No activity logged yet. Add your first entry above.</p>
    {:else}
      <ul class="log-list">
        {#each logs as log (log.id)}
          <li class="log-card">
            <div class="log-summary">
              <h3>{log.activity}</h3>
              <p class="timestamp">{formatDate(log.created_at)}</p>
              {#if log.details}
                <p class="details">{log.details}</p>
              {/if}
              {#if log.tags?.length}
                <div class="tags">
                  {#each log.tags as tag}
                    <span class="tag">{tag}</span>
                  {/each}
                </div>
              {/if}
              {#if Object.keys(log.metadata ?? {}).length}
                <div class="metadata">
                  <h4>Metadata</h4>
                  <dl>
                    {#each Object.entries(log.metadata) as [key, value]}
                      <div>
                        <dt>{key}</dt>
                        <dd>{String(value)}</dd>
                      </div>
                    {/each}
                  </dl>
                </div>
              {/if}
            </div>
            <div class="log-actions">
              <label for={`notes-${log.id}`}>Document notes</label>
              <textarea
                id={`notes-${log.id}`}
                rows={3}
                value={documentNotes[log.id] ?? ''}
                on:input={(event) => updateDocumentNotes(log.id, (event.target as HTMLTextAreaElement).value)}
                placeholder="Add instructions for the generated document"
              ></textarea>
              <button class="secondary" on:click={() => generateDocument(log, 'work_summary')}>
                Generate work summary
              </button>
              {#if documentStatus[log.id]}
                <p class="status">{documentStatus[log.id]}</p>
              {/if}
              {#if log.documents.length}
                <div class="documents">
                  <h4>Documents</h4>
                  <ul>
                    {#each log.documents as document}
                      <li>
                        <a href={`${API_BASE}${document.download_url}`} target="_blank" rel="noopener noreferrer">
                          {document.title}
                        </a>
                        <span class="timestamp">{formatDate(document.created_at)}</span>
                      </li>
                    {/each}
                  </ul>
                </div>
              {/if}
            </div>
          </li>
        {/each}
      </ul>
    {/if}
  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: 'Inter', system-ui, sans-serif;
    background: #f3f4f6;
    color: #1f2937;
  }

  .layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 1.5rem;
    padding: 2rem;
    max-width: 1100px;
    margin: 0 auto;
  }

  .panel {
    background: white;
    border-radius: 1rem;
    padding: 1.75rem;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1);
  }

  h1 {
    margin: 0 0 0.5rem;
    font-size: 2rem;
  }

  h2 {
    margin: 0;
  }

  h3 {
    margin: 0;
    font-size: 1.125rem;
  }

  .lead {
    margin-top: 0;
    color: #4b5563;
  }

  .alert {
    padding: 0.75rem 1rem;
    border-radius: 0.75rem;
    margin-bottom: 1rem;
    font-weight: 500;
  }

  .alert-error {
    background: #fee2e2;
    color: #b91c1c;
  }

  .alert-success {
    background: #dcfce7;
    color: #15803d;
  }

  .log-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .field-group {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
  }

  label {
    font-weight: 600;
    color: #374151;
  }

  input,
  textarea,
  button {
    font-family: inherit;
  }

  input,
  textarea {
    padding: 0.75rem;
    border-radius: 0.75rem;
    border: 1px solid #d1d5db;
    background: #f9fafb;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    background: white;
  }

  button {
    border: none;
    border-radius: 9999px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .primary {
    background: linear-gradient(120deg, #4f46e5, #7c3aed);
    color: white;
    box-shadow: 0 10px 20px rgba(99, 102, 241, 0.25);
  }

  .secondary {
    background: #e0e7ff;
    color: #312e81;
  }

  .primary:hover:not(:disabled),
  .secondary:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 12px 24px rgba(79, 70, 229, 0.15);
  }

  .list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .filters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .empty {
    margin: 2rem 0;
    text-align: center;
    color: #6b7280;
  }

  .log-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 0;
    padding: 0;
  }

  .log-card {
    border: 1px solid #e5e7eb;
    border-radius: 1rem;
    padding: 1.25rem;
    display: grid;
    gap: 1.25rem;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  }

  .log-summary {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .timestamp {
    color: #6b7280;
    font-size: 0.9rem;
  }

  .details {
    margin: 0;
  }

  .tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .tag {
    background: #eef2ff;
    color: #4338ca;
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.8rem;
  }

  .metadata h4 {
    margin: 0;
    font-size: 0.95rem;
  }

  .metadata dl {
    margin: 0.25rem 0 0;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.2rem 1rem;
    font-size: 0.9rem;
  }

  .metadata dt {
    font-weight: 600;
    color: #374151;
  }

  .metadata dd {
    margin: 0;
    color: #4b5563;
  }

  .log-actions {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .log-actions textarea {
    resize: vertical;
  }

  .status {
    margin: 0;
    font-size: 0.85rem;
    color: #2563eb;
  }

  .documents ul {
    list-style: none;
    margin: 0.5rem 0 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
  }

  .documents a {
    color: #4f46e5;
    text-decoration: none;
    font-weight: 600;
  }

  .documents a:hover {
    text-decoration: underline;
  }

  @media (min-width: 900px) {
    .layout {
      grid-template-columns: minmax(0, 420px) minmax(0, 1fr);
    }
  }
</style>
