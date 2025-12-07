"""
Workflow Orchestration for NovaSystem.

This module defines the WorkflowProcess class, which is responsible for
interpreting a workflow graph, executing agents in the correct order,
and managing the flow of data between them.
"""

from typing import Any, Dict, List
import logging
from collections import deque
import asyncio

from .process import NovaProcess
from .memory import MemoryManager
from ..config.models import get_model_for_agent

logger = logging.getLogger(__name__)

class WorkflowProcess:
    """Orchestrates the execution of a multi-agent workflow."""

    def __init__(self, workflow_data: Dict[str, Any]):
        """
        Initialize the workflow process.

        Args:
            workflow_data: A dictionary containing 'nodes' and 'connections'.
        """
        self.nodes = workflow_data.get('nodes', [])
        self.connections = workflow_data.get('connections', [])
        self.node_map = {node['id']: node for node in self.nodes}
        self.adjacency_list = {node['id']: [] for node in self.nodes}
        self.in_degree = {node['id']: 0 for node in self.nodes}
        self.node_states = {node['id']: 'pending' for node in self.nodes}
        self.node_outputs = {}

        self._build_graph()

    def _build_graph(self):
        """Builds the graph structure for topological sorting."""
        for conn in self.connections:
            source_id = conn.get('from')
            target_id = conn.get('to')
            if source_id in self.adjacency_list and target_id in self.in_degree:
                self.adjacency_list[source_id].append(target_id)
                self.in_degree[target_id] += 1
            else:
                logger.warning(f"Invalid connection found: {conn}")

    def get_execution_order(self) -> List[str]:
        """
        Performs a topological sort of the graph to determine execution order.

        Returns:
            A list of node IDs in the order they should be executed.
            Returns an empty list if a cycle is detected.
        """
        queue = deque([node_id for node_id, degree in self.in_degree.items() if degree == 0])
        sorted_order = []

        while queue:
            node_id = queue.popleft()
            sorted_order.append(node_id)

            for neighbor_id in self.adjacency_list.get(node_id, []):
                self.in_degree[neighbor_id] -= 1
                if self.in_degree[neighbor_id] == 0:
                    queue.append(neighbor_id)

        if len(sorted_order) == len(self.nodes):
            return sorted_order
        else:
            logger.error("Cycle detected in the workflow graph. Execution aborted.")
            return []  # Cycle detected

    async def execute(self):
        """Executes the workflow by calling real NovaProcess agents."""
        execution_order = self.get_execution_order()

        if not execution_order:
            self.node_states = {node_id: 'error' for node_id in self.node_map}
            return

        logger.info(f"Workflow execution order: {execution_order}")

        for node_id in execution_order:
            self.node_states[node_id] = 'processing'
            logger.info(f"Executing node: {node_id}")

            try:
                # 1. Gather inputs from parent nodes
                parent_outputs = []
                for conn in self.connections:
                    if conn.get('to') == node_id:
                        parent_id = conn.get('from')
                        if parent_id in self.node_outputs:
                            parent_outputs.append(self.node_outputs[parent_id])

                current_input = "\n".join(parent_outputs)
                if not current_input:
                    # For root nodes, use their title as the initial problem
                    current_input = self.node_map[node_id].get('title', 'Start workflow')

                # 2. Map node type to agent domain
                node_type = self.node_map[node_id].get('type')
                domain_map = {
                    'research-bot': ['Research', 'Data Collection'],
                    'data-analyst': ['Data Analysis', 'Statistics'],
                    'code-helper': ['Software Development', 'Python'],
                    'marketing-bot': ['Marketing', 'Copywriting'],
                    'problem-solver': ['General', 'Synthesis', 'Problem Solving']
                }
                domains = domain_map.get(node_type, ['General'])

                # 3. Instantiate and run the NovaProcess for the agent
                memory_manager = MemoryManager()
                # Use centralized model configuration based on agent type
                agent_model = get_model_for_agent(node_type.replace('-', '_'))
                nova_process = NovaProcess(
                    domains=domains,
                    model=agent_model,
                    memory_manager=memory_manager
                )

                # Add timeout to prevent hanging
                try:
                    result = await asyncio.wait_for(
                        nova_process.solve_problem(current_input, max_iterations=2),
                        timeout=300  # 5 minute timeout
                    )
                except asyncio.TimeoutError:
                    logger.error(f"Node {node_id} timed out after 5 minutes")
                    self.node_states[node_id] = 'error'
                    self.node_outputs[node_id] = "Error: Process timed out after 5 minutes"
                    continue

                # 4. Store the output
                output = result.get('final_synthesis', 'No result found.')
                self.node_outputs[node_id] = output

                self.node_states[node_id] = 'completed'
                logger.info(f"Node {node_id} completed.")

            except Exception as e:
                logger.error(f"Error executing node {node_id}: {e}")
                self.node_states[node_id] = 'error'
                self.node_outputs[node_id] = f"Error: {e}"


        logger.info("Workflow execution finished.")
        return self.node_outputs
