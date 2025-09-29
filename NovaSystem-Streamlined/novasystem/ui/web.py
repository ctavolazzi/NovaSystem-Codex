"""
Web Interface for NovaSystem.

This module provides a Flask-based web interface for the Nova Process.
"""

from flask import Flask, render_template, request, jsonify, Response
import asyncio
import json
import logging
import threading
from typing import Dict, Any
import uuid
from datetime import datetime

from ..core.process import NovaProcess
from ..core.memory import MemoryManager
from ..core.workflow import WorkflowProcess
from ..config.models import get_default_model
from ..database import init_database, get_performance_tracker
from ..database.performance_tracker import SessionMetrics, AgentMetrics

logger = logging.getLogger(__name__)

class WebInterface:
    """Web interface for NovaSystem."""

    def __init__(self):
        self.app = Flask(__name__, template_folder='../../templates', static_folder='../../templates/shared')
        self.active_sessions = {}

        # Initialize database and performance tracking
        try:
            init_database()
            self.performance_tracker = get_performance_tracker()
            logger.info("Performance tracking initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize performance tracking: {e}")
            self.performance_tracker = None

        self.setup_routes()
        self.setup_database_routes()

    def setup_routes(self):
        """Setup Flask routes."""

        @self.app.route('/')
        def index():
            """Main page."""
            return render_template('index_new.html')

        @self.app.route('/static/shared/<path:filename>')
        def shared_static(filename):
            """Serve shared navigation files."""
            return self.app.send_static_file(filename)

        @self.app.template_global()
        def config():
            """Make config available in templates."""
            return self.app.config

        @self.app.route('/workflow')
        def workflow():
            """Workflow UI page."""
            return render_template('workflow_new.html')

        @self.app.route('/api/workflow/execute', methods=['POST'])
        def execute_workflow():
            """Start a new workflow execution session."""
            try:
                data = request.get_json()
                if not data or 'nodes' not in data or 'connections' not in data:
                    return jsonify({'error': 'Invalid workflow data provided'}), 400

                nodes = data.get('nodes')
                connections = data.get('connections')

                # Create session for the workflow
                session_id = str(uuid.uuid4())

                workflow_process = WorkflowProcess(data)

                self.active_sessions[session_id] = {
                    'type': 'workflow',
                    'workflow_process': workflow_process,
                    'started_at': datetime.now(),
                    'status': 'running',
                }

                logger.info(f"Starting workflow session {session_id} with {len(nodes)} nodes and {len(connections)} connections.")

                # Start the workflow execution in a background thread
                thread = threading.Thread(target=self.run_async_in_thread, args=(workflow_process.execute(),))
                thread.start()

                return jsonify({
                    'session_id': session_id,
                    'status': 'started',
                    'message': 'Workflow session initiated successfully'
                })

            except Exception as e:
                logger.error(f"Error starting workflow session: {str(e)}")
                return jsonify({'error': f'Internal server error: {str(e)}'}), 500

        @self.app.route('/api/solve', methods=['POST'])
        def solve_problem():
            """Start a new problem-solving session."""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400

                problem = data.get('problem', '').strip()
                domains = data.get('domains', ['General'])
                max_iterations = data.get('max_iterations', 3)
                model = data.get('model', get_default_model())

                # Enhanced validation
                if not problem:
                    return jsonify({'error': 'Problem statement is required'}), 400

                if len(problem) < 10:
                    return jsonify({'error': 'Problem statement should be at least 10 characters long'}), 400

                if max_iterations < 1 or max_iterations > 20:
                    return jsonify({'error': 'Max iterations must be between 1 and 20'}), 400

                if not domains or not all(d.strip() for d in domains):
                    return jsonify({'error': 'At least one expertise domain is required'}), 400

                # Create session
                session_id = str(uuid.uuid4())

                # Create Nova Process with enhanced error handling
                try:
                    memory_manager = MemoryManager()
                    nova_process = NovaProcess(
                        domains=domains,
                        model=model,
                        memory_manager=memory_manager
                    )
                except Exception as e:
                    logger.error(f"Error creating Nova Process: {str(e)}")
                    return jsonify({'error': f'Failed to initialize AI system: {str(e)}'}), 500

                # Store session with enhanced metadata
                self.active_sessions[session_id] = {
                    'nova_process': nova_process,
                    'problem': problem,
                    'domains': domains,
                    'max_iterations': max_iterations,
                    'model': model,
                    'started_at': datetime.now(),
                    'status': 'running',
                    'progress': 0,
                    'current_iteration': 0
                }

                # Start background task in a new thread
                thread = threading.Thread(target=self.run_async_in_thread, args=(self._run_problem_solving(session_id, problem, max_iterations),))
                thread.start()

                return jsonify({
                    'session_id': session_id,
                    'status': 'started',
                    'message': 'Problem-solving session started successfully',
                    'model_used': model,
                    'estimated_time': f'{max_iterations * 30}-{max_iterations * 60} seconds',
                    'domains': domains
                })

            except Exception as e:
                logger.error(f"Error starting problem-solving session: {str(e)}")
                return jsonify({'error': f'Internal server error: {str(e)}'}), 500

        @self.app.route('/api/sessions/<session_id>/status')
        def get_session_status(session_id):
            """Get enhanced session status."""
            if session_id not in self.active_sessions:
                return jsonify({'error': 'Session not found'}), 404

            session = self.active_sessions[session_id]

            # Handle workflow session type
            if session.get('type') == 'workflow':
                workflow_process = session['workflow_process']
                return jsonify({
                    'session_id': session_id,
                    'status': session['status'],
                    'type': 'workflow',
                    'node_states': workflow_process.node_states,
                    'node_outputs': workflow_process.node_outputs,
                    'execution_order': workflow_process.get_execution_order(), # Assuming this is safe to call again
                    'started_at': session['started_at'].isoformat()
                })

            nova_process = session['nova_process']

            try:
                status = nova_process.get_status()
            except Exception as e:
                logger.error(f"Error getting session status: {str(e)}")
                status = {
                    'current_iteration': session.get('current_iteration', 0),
                    'total_iterations': session.get('max_iterations', 3),
                    'is_active': session['status'] == 'running',
                    'problem_statement': session['problem'][:100] + '...'
                }

            # Calculate progress percentage
            progress = 0
            if status['total_iterations'] > 0:
                progress = min(100, (status['current_iteration'] / status['total_iterations']) * 100)

            return jsonify({
                'session_id': session_id,
                'status': session['status'],
                'current_iteration': status['current_iteration'],
                'total_iterations': status['total_iterations'],
                'progress_percentage': round(progress, 1),
                'is_active': status['is_active'],
                'problem_statement': status['problem_statement'],
                'domains': session['domains'],
                'model': session['model'],
                'started_at': session['started_at'].isoformat(),
                'estimated_completion': self._estimate_completion(session)
            })

        @self.app.route('/api/sessions/<session_id>/result')
        def get_session_result(session_id):
            """Get enhanced session result."""
            if session_id not in self.active_sessions:
                return jsonify({'error': 'Session not found'}), 404

            session = self.active_sessions[session_id]
            nova_process = session['nova_process']

            try:
                result = nova_process.get_solution_history()
            except Exception as e:
                logger.error(f"Error getting session result: {str(e)}")
                result = {'error': 'Failed to retrieve solution'}

            return jsonify({
                'session_id': session_id,
                'result': result,
                'status': session['status'],
                'problem': session['problem'],
                'domains': session['domains'],
                'model': session['model'],
                'completed_at': session.get('completed_at', datetime.now()).isoformat(),
                'duration': self._calculate_duration(session),
                'metadata': {
                    'total_iterations': session['max_iterations'],
                    'expertise_areas': len(session['domains']),
                    'problem_complexity': self._assess_complexity(session['problem'])
                }
            })

        @self.app.route('/api/sessions')
        def list_sessions():
            """List all sessions."""
            sessions = []
            for session_id, session_data in self.active_sessions.items():
                sessions.append({
                    'session_id': session_id,
                    'status': session_data['status'],
                    'started_at': session_data['started_at'].isoformat(),
                    'problem': session_data.get('problem', 'Workflow')[:100] + '...'
                })
            return jsonify(sessions)

        @self.app.route('/api/sessions/kill-all', methods=['POST'])
        def kill_all_sessions():
            """Kill all active sessions."""
            try:
                killed_count = 0
                for session_id, session_data in list(self.active_sessions.items()):
                    # Mark session as killed
                    session_data['status'] = 'killed'
                    session_data['killed_at'] = datetime.now()
                    killed_count += 1

                # Clear all sessions
                self.active_sessions.clear()

                logger.info(f"Killed {killed_count} active sessions")

                return jsonify({
                    'message': f'Successfully killed {killed_count} active sessions',
                    'killed_count': killed_count,
                    'status': 'success'
                })

            except Exception as e:
                logger.error(f"Error killing sessions: {str(e)}")
                return jsonify({'error': f'Failed to kill sessions: {str(e)}'}), 500

        @self.app.route('/api/sessions/<session_id>/kill', methods=['POST'])
        def kill_session(session_id):
            """Kill a specific session."""
            try:
                if session_id not in self.active_sessions:
                    return jsonify({'error': 'Session not found'}), 404

                session_data = self.active_sessions[session_id]
                session_data['status'] = 'killed'
                session_data['killed_at'] = datetime.now()

                # Remove from active sessions
                del self.active_sessions[session_id]

                logger.info(f"Killed session {session_id}")

                return jsonify({
                    'message': f'Successfully killed session {session_id}',
                    'session_id': session_id,
                    'status': 'success'
                })

            except Exception as e:
                logger.error(f"Error killing session {session_id}: {str(e)}")
                return jsonify({'error': f'Failed to kill session: {str(e)}'}), 500

    def setup_database_routes(self):
        """Setup database API routes."""
        if not self.performance_tracker:
            logger.warning("Performance tracking not available, skipping database routes")
            return

        # Import and register database API blueprint
        from ..database.api import db_api
        self.app.register_blueprint(db_api)

        # Add analytics dashboard route
        @self.app.route('/analytics')
        def analytics_dashboard():
            """Analytics dashboard page."""
            return render_template('analytics_new.html')

        # Add real-time monitor route
        @self.app.route('/monitor')
        def realtime_monitor():
            """Real-time monitoring dashboard page."""
            return render_template('monitor_new.html')

        @self.app.route('/settings')
        def settings():
            """Settings page."""
            return render_template('settings.html')

        @self.app.route('/help')
        def help():
            """Help and documentation page."""
            return render_template('help.html')

        @self.app.route('/about')
        def about():
            """About page."""
            return render_template('about.html')

        @self.app.route('/sessions')
        def sessions():
            """Session manager page."""
            return render_template('sessions.html')

        @self.app.route('/history')
        def history():
            """Session history page."""
            return render_template('history.html')

    def run_async_in_thread(self, coro):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coro)
        loop.close()

    async def _run_problem_solving(self, session_id: str, problem: str, max_iterations: int):
        """Run the problem-solving process in the background with progress tracking."""
        try:
            session = self.active_sessions[session_id]
            nova_process = session['nova_process']

            # Update progress tracking
            session['current_iteration'] = 0
            session['progress'] = 0

            # Run the process
            result = await nova_process.solve_problem(
                problem,
                max_iterations=max_iterations,
                stream=False
            )

            # Update session status
            session['status'] = 'completed'
            session['result'] = result
            session['completed_at'] = datetime.now()
            session['progress'] = 100

        except Exception as e:
            logger.error(f"Error in problem-solving session {session_id}: {str(e)}")
            session['status'] = 'error'
            session['error'] = str(e)
            session['completed_at'] = datetime.now()

    def _estimate_completion(self, session: dict) -> str:
        """Estimate completion time based on session data."""
        if session['status'] == 'completed':
            return "Completed"

        elapsed = datetime.now() - session['started_at']
        remaining_iterations = session['max_iterations'] - session.get('current_iteration', 0)
        avg_time_per_iteration = elapsed.total_seconds() / max(1, session.get('current_iteration', 1))
        estimated_remaining = remaining_iterations * avg_time_per_iteration

        if estimated_remaining < 60:
            return f"~{int(estimated_remaining)} seconds"
        else:
            return f"~{int(estimated_remaining / 60)} minutes"

    def _calculate_duration(self, session: dict) -> str:
        """Calculate session duration."""
        if session['status'] == 'completed':
            duration = session['completed_at'] - session['started_at']
        else:
            duration = datetime.now() - session['started_at']

        total_seconds = duration.total_seconds()
        if total_seconds < 60:
            return f"{int(total_seconds)} seconds"
        else:
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            return f"{minutes}m {seconds}s"

    def _assess_complexity(self, problem: str) -> str:
        """Assess problem complexity based on length and content."""
        word_count = len(problem.split())
        char_count = len(problem)

        if word_count < 20 or char_count < 100:
            return "Simple"
        elif word_count < 50 or char_count < 300:
            return "Moderate"
        elif word_count < 100 or char_count < 600:
            return "Complex"
        else:
            return "Very Complex"

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = True):
        """Run the web interface."""
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Main function to run the web interface."""
    interface = WebInterface()
    interface.run()

if __name__ == "__main__":
    main()
