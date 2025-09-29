"""
Web Interface for NovaSystem.

This module provides a Flask-based web interface for the Nova Process.
"""

from flask import Flask, render_template, request, jsonify, Response
import asyncio
import json
import logging
from typing import Dict, Any
import uuid
from datetime import datetime

from ..core.process import NovaProcess
from ..core.memory import MemoryManager

logger = logging.getLogger(__name__)

class WebInterface:
    """Web interface for NovaSystem."""

    def __init__(self):
        self.app = Flask(__name__, template_folder='../../templates')
        self.active_sessions = {}
        self.setup_routes()

    def setup_routes(self):
        """Setup Flask routes."""

        @self.app.route('/')
        def index():
            """Main page."""
            return render_template('index.html')

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
                model = data.get('model', 'gpt-4')

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

                # Start background task
                asyncio.create_task(self._run_problem_solving(session_id, problem, max_iterations))

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
                    'problem': session_data['problem'][:100] + '...'
                })
            return jsonify(sessions)

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
