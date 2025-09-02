"""
Content Processor - Phase 3A.3.4 SOLID Extraction
Single Responsibility: Content analysis and workspace processing for stakeholders

Extracted from StakeholderIntelligenceUnified for SOLID compliance
Author: Martin | Platform Architecture with Sequential7 methodology
"""

import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class ContentProcessor:
    """
    Content and workspace processing for stakeholder detection
    
    Single Responsibility: Process content, files, and workspaces to identify
    stakeholders with optimization and parallel processing capabilities.
    """

    def __init__(
        self, 
        detection_engine=None,
        repository=None,
        enable_performance: bool = True,
    ):
        """Initialize content processor"""
        self.logger = logging.getLogger(__name__)
        self.detection_engine = detection_engine
        self.repository = repository
        self.enable_performance = enable_performance
        
        # Processing configuration
        self.supported_extensions = {'.md', '.txt', '.py', '.js', '.ts', '.json', '.yaml', '.yml'}
        self.max_file_size = 1024 * 1024  # 1MB
        self.max_workers = 4  # For parallel processing

    def process_content_for_stakeholders(
        self, content: str, context: Dict[str, Any], auto_create: bool = True
    ) -> Dict[str, Any]:
        """
        Process content and automatically handle stakeholder detection and creation
        
        Args:
            content: Text content to analyze
            context: Context information
            auto_create: Whether to automatically create stakeholder profiles
            
        Returns:
            Processing results with counts and actions taken
        """
        try:
            if not self.detection_engine or not self.repository:
                self.logger.error("Detection engine and repository required for content processing")
                return {"error": "Missing dependencies"}
                
            # Detect stakeholder candidates
            candidates = self.detection_engine.detect_stakeholders_in_content(content, context)

            candidates_detected = len(candidates)
            auto_created = 0
            profiling_needed = 0

            if auto_create:
                for candidate in candidates:
                    # Check if stakeholder already exists
                    stakeholder_id = candidate["name"].lower().replace(" ", "_")

                    if not self.repository.get_stakeholder(stakeholder_id):
                        # Create new stakeholder profile
                        stakeholder_data = {
                            "name": candidate["name"],
                            "role": candidate["role"],
                            "influence_level": candidate.get("influence_level", "medium"),
                            "detection_confidence": candidate["confidence"],
                            "source_files": [context.get("file_path", "")],
                        }

                        if self.repository.add_stakeholder(
                            stakeholder_data,
                            source="ai_detection",
                            confidence=candidate["confidence"],
                        ):
                            auto_created += 1

                            # High-confidence detections need profiling
                            if candidate["confidence"] > 0.7:
                                profiling_needed += 1

            return {
                "candidates_detected": candidates_detected,
                "auto_created": auto_created,
                "profiling_needed": profiling_needed,
                "candidates": candidates,
                "processing_timestamp": time.time(),
            }

        except Exception as e:
            self.logger.error(f"Failed to process content for stakeholders: {e}")
            return {
                "error": str(e),
                "candidates_detected": 0,
                "auto_created": 0,
                "profiling_needed": 0,
                "processing_timestamp": time.time(),
            }

    def process_workspace_for_stakeholders(
        self, workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process entire workspace for stakeholder detection
        
        Args:
            workspace_path: Path to workspace directory
            
        Returns:
            Processing results with file counts and stakeholder statistics
        """
        try:
            if not workspace_path:
                # Try to get from config or use default
                try:
                    from ..stakeholder_intelligence_unified import get_config
                    config = get_config()
                    workspace_path = str(config.workspace_path_obj)
                except:
                    self.logger.warning("No workspace path provided and unable to get from config")
                    return {"error": "No workspace path available"}

            workspace_dir = Path(workspace_path)
            if not workspace_dir.exists():
                return {"error": f"Workspace directory does not exist: {workspace_path}"}

            self.logger.info(f"Processing workspace for stakeholders: {workspace_path}")

            # Get all processable files
            files_to_process = self._get_processable_files(workspace_dir)
            
            if not files_to_process:
                return {
                    "files_processed": 0,
                    "stakeholders_found": 0,
                    "processing_time": 0,
                    "status": "no_files",
                }

            start_time = time.time()

            # Process files with optimization
            if self.enable_performance and len(files_to_process) > 5:
                results = self._process_files_with_optimization(files_to_process)
            else:
                results = self._process_files_sequential(files_to_process)

            processing_time = time.time() - start_time

            # Aggregate results
            total_stakeholders = 0
            files_processed = len([r for r in results if r is not None])
            
            for result in results:
                if result:
                    total_stakeholders += result.get("candidates_detected", 0)

            return {
                "files_processed": files_processed,
                "total_files_scanned": len(files_to_process),
                "stakeholders_found": total_stakeholders,
                "processing_time": processing_time,
                "average_time_per_file": processing_time / max(files_processed, 1),
                "results": results,
                "timestamp": time.time(),
            }

        except Exception as e:
            self.logger.error(f"Failed to process workspace for stakeholders: {e}")
            return {
                "error": str(e),
                "files_processed": 0,
                "stakeholders_found": 0,
                "processing_time": 0,
            }

    def _get_processable_files(self, workspace_dir: Path) -> List[Path]:
        """Get list of files that can be processed for stakeholder detection"""
        processable_files = []
        
        try:
            for file_path in workspace_dir.rglob("*"):
                if (
                    file_path.is_file()
                    and file_path.suffix.lower() in self.supported_extensions
                    and file_path.stat().st_size <= self.max_file_size
                    and not self._should_skip_file(file_path)
                ):
                    processable_files.append(file_path)
                    
        except Exception as e:
            self.logger.error(f"Failed to scan workspace directory: {e}")
            
        return processable_files

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during processing"""
        skip_patterns = [
            '.git', '.claudedirector', 'node_modules', '__pycache__',
            '.pytest_cache', '.vscode', '.idea', 'venv', 'env',
        ]
        
        # Check if any part of the path matches skip patterns
        path_parts = file_path.parts
        for pattern in skip_patterns:
            if pattern in path_parts:
                return True
                
        return False

    def _process_files_with_optimization(self, files: List[Path]) -> List[Optional[Dict[str, Any]]]:
        """Process files with parallel optimization"""
        results = []
        
        def process_single_file(file_path: Path) -> Optional[Dict[str, Any]]:
            """Process a single file for stakeholders"""
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                if len(content.strip()) < 10:  # Skip very short files
                    return None

                context = {
                    "file_path": str(file_path),
                    "category": self._categorize_file(file_path),
                    "size": len(content),
                }

                return self.process_content_for_stakeholders(
                    content, context, auto_create=True
                )
                
            except Exception as e:
                self.logger.warning(f"Failed to process file {file_path}: {e}")
                return None

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(process_single_file, file_path): file_path 
                for file_path in files
            }
            
            # Collect results
            for future in as_completed(future_to_file):
                result = future.result()
                results.append(result)

        return results

    def _process_files_sequential(self, files: List[Path]) -> List[Optional[Dict[str, Any]]]:
        """Process files sequentially (fallback method)"""
        results = []
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                if len(content.strip()) < 10:  # Skip very short files
                    results.append(None)
                    continue

                context = {
                    "file_path": str(file_path),
                    "category": self._categorize_file(file_path),
                    "size": len(content),
                }

                result = self.process_content_for_stakeholders(
                    content, context, auto_create=True
                )
                results.append(result)
                
            except Exception as e:
                self.logger.warning(f"Failed to process file {file_path}: {e}")
                results.append(None)

        return results

    def _categorize_file(self, file_path: Path) -> str:
        """Categorize file type for context"""
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()
        
        # Strategy/planning documents
        if any(keyword in name for keyword in ['strategy', 'plan', 'roadmap', 'vision']):
            return 'strategy'
        
        # Meeting notes
        if any(keyword in name for keyword in ['meeting', 'notes', 'minutes']):
            return 'meeting'
        
        # Documentation
        if suffix in ['.md', '.txt'] or 'readme' in name:
            return 'documentation'
        
        # Code files
        if suffix in ['.py', '.js', '.ts']:
            return 'code'
        
        # Configuration files
        if suffix in ['.json', '.yaml', '.yml'] or 'config' in name:
            return 'configuration'
        
        return 'general'

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get content processing statistics"""
        return {
            "supported_extensions": list(self.supported_extensions),
            "max_file_size": self.max_file_size,
            "max_workers": self.max_workers,
            "performance_enabled": self.enable_performance,
        }

    def add_supported_extension(self, extension: str) -> bool:
        """Add a new supported file extension"""
        try:
            if not extension.startswith('.'):
                extension = '.' + extension
            self.supported_extensions.add(extension.lower())
            return True
        except Exception as e:
            self.logger.error(f"Failed to add supported extension: {e}")
            return False

    def remove_supported_extension(self, extension: str) -> bool:
        """Remove a supported file extension"""
        try:
            if not extension.startswith('.'):
                extension = '.' + extension
            self.supported_extensions.discard(extension.lower())
            return True
        except Exception as e:
            self.logger.error(f"Failed to remove supported extension: {e}")
            return False
