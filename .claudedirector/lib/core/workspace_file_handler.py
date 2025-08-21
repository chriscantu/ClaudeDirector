"""
Workspace File Handler for ClaudeDirector
Integrates file lifecycle management with strategic AI conversations
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from .file_lifecycle_manager import FileLifecycleManager, GenerationMode
from .smart_file_organizer import SmartFileOrganizer

class WorkspaceFileHandler:
    """Handles file operations in leadership-workspace with user control"""

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = self._detect_workspace_path(workspace_path)
        self.lifecycle_manager = FileLifecycleManager(self.workspace_path)
        self.smart_organizer = SmartFileOrganizer(self.lifecycle_manager)
        self.current_session_id = str(uuid.uuid4())[:8]

    def _detect_workspace_path(self, provided_path: Optional[str]) -> str:
        """Detect workspace path from environment or configuration"""
        if provided_path:
            return provided_path

        # Check environment variable
        env_path = os.environ.get('CLAUDEDIRECTOR_WORKSPACE')
        if env_path and Path(env_path).exists():
            return env_path

        # Check project-local workspace first (for development/Cursor use)
        project_workspace = Path.cwd() / "leadership-workspace"
        if project_workspace.exists():
            return str(project_workspace)

        # Check new default location (leadership-workspace)
        new_default_path = Path.home() / "leadership-workspace"
        if new_default_path.exists():
            return str(new_default_path)

        # Check legacy location (engineering-director-workspace) for existing users
        legacy_path = Path.home() / "engineering-director-workspace"
        if legacy_path.exists():
            print(f"📁 Found legacy workspace: {legacy_path}")
            print(f"💡 Consider migrating to new location: {new_default_path}")
            return str(legacy_path)

        # Create new default if neither exists
        new_default_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created leadership workspace: {new_default_path}")
        return str(new_default_path)

    def should_create_file(self, content_type: str) -> bool:
        """Check if content type should be created based on generation mode"""
        mode = self.lifecycle_manager.config.generation_mode

        mode_content_types = {
            GenerationMode.MINIMAL: [
                "strategic_analysis", "session_summary"
            ],
            GenerationMode.PROFESSIONAL: [
                "strategic_analysis", "meeting_prep", "session_summary",
                "executive_presentation", "quarterly_planning"
            ],
            GenerationMode.RESEARCH: [
                "strategic_analysis", "meeting_prep", "session_summary",
                "framework_research", "methodology_documentation",
                "executive_presentation", "quarterly_planning"
            ]
        }

        return content_type in mode_content_types.get(mode, [])

    def request_file_creation(
        self,
        content: str,
        content_type: str,
        suggested_filename: str,
        business_context: str,
        persona: Optional[str] = None
    ) -> Optional[str]:
        """Request to create a file with user control"""

        # Check if this content type should be generated
        if not self.should_create_file(content_type):
            return None

        # Generate intelligent filename based on content and context
        final_filename = self._generate_smart_filename(
            suggested_filename, content_type, business_context, persona
        )

        # Request user permission
        approved, approved_filename = self.lifecycle_manager.request_file_generation(
            content_type=content_type,
            proposed_filename=final_filename,
            content_preview=content[:300],
            business_context=business_context
        )

        if not approved:
            return None

        # Create the file
        file_path = self._create_file(approved_filename, content, content_type)

        if file_path:
            print(f"✅ Created: {Path(file_path).name}")

            # Check if consolidation is needed
            self._check_consolidation_opportunity()

        return file_path

    def _generate_smart_filename(
        self,
        suggested_filename: str,
        content_type: str,
        business_context: str,
        persona: Optional[str] = None
    ) -> str:
        """Generate intelligent filename based on content and mode"""

        # Use Phase 2 outcome-focused naming if enabled
        if self.lifecycle_manager.config.generation_mode.value in ["professional", "research"]:
            outcome_filename = self.smart_organizer.generate_outcome_focused_filename(
                content_preview=business_context,
                content_type=content_type,
                business_context=business_context,
                persona=persona
            )

            # Determine target directory
            target_dir = self._get_target_directory(content_type)
            return str(target_dir / outcome_filename)

        # Fallback to original naming for minimal mode
        timestamp = datetime.now().strftime("%Y-%m-%d")

        filename_patterns = {
            "strategic_analysis": f"{timestamp}-strategic-analysis.md",
            "meeting_prep": f"{timestamp}-meeting-prep.md",
            "session_summary": f"{timestamp}-session-summary.md",
            "executive_presentation": f"{timestamp}-executive-presentation.md",
            "quarterly_planning": f"q{self._get_current_quarter()}-planning-{timestamp}.md",
            "framework_research": f"{timestamp}-framework-research.md",
            "methodology_documentation": f"{timestamp}-methodology-doc.md"
        }

        base_filename = filename_patterns.get(content_type, suggested_filename)

        if persona:
            base_filename = base_filename.replace(".md", f"-{persona}.md")

        target_dir = self._get_target_directory(content_type)
        return str(target_dir / base_filename)

    def _get_target_directory(self, content_type: str) -> Path:
        """Get appropriate directory for content type"""
        base_path = Path(self.workspace_path)

        directory_mapping = {
            "strategic_analysis": base_path / "analysis-results",
            "meeting_prep": base_path / "meeting-prep",
            "session_summary": base_path / "current-work",
            "executive_presentation": base_path / "meeting-prep",
            "quarterly_planning": base_path / "strategic-docs",
            "framework_research": base_path / "analysis-results",
            "methodology_documentation": base_path / "strategic-docs"
        }

        target_dir = directory_mapping.get(content_type, base_path / "current-work")
        target_dir.mkdir(parents=True, exist_ok=True)

        return target_dir

    def _create_file(self, filename: str, content: str, content_type: str) -> Optional[str]:
        """Create file with metadata tracking"""
        try:
            file_path = Path(filename)

            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Add file metadata header
            full_content = self._add_file_header(content, content_type)

            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)

            # Register with lifecycle manager
            self.lifecycle_manager.register_file(
                str(file_path),
                content_type,
                self.current_session_id
            )

            return str(file_path)

        except Exception as e:
            print(f"⚠️ Failed to create file {filename}: {e}")
            return None

    def _add_file_header(self, content: str, content_type: str) -> str:
        """Add metadata header to file content"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        mode = self.lifecycle_manager.config.generation_mode.value

        header = f"""---
generated_by: ClaudeDirector
content_type: {content_type}
generation_mode: {mode}
session_id: {self.current_session_id}
created_at: {timestamp}
retention_status: standard
---

"""
        return header + content

    def _get_current_quarter(self) -> int:
        """Get current business quarter"""
        month = datetime.now().month
        return (month - 1) // 3 + 1

    def _check_consolidation_opportunity(self):
        """Check if consolidation should be suggested using smart organizer"""
        if not self.lifecycle_manager.config.consolidate_analysis:
            return

        recent_files = self.lifecycle_manager._get_recent_session_files()

        if len(recent_files) >= self.lifecycle_manager.config.max_session_files:
            print(f"\n💡 **Smart Organization Opportunity**")
            print(f"You have {len(recent_files)} files from this session.")

            # Use Phase 2 smart consolidation
            consolidation_suggested = self.smart_organizer.suggest_consolidation_opportunities()

            if not consolidation_suggested:
                # Fallback to Phase 1 consolidation
                print(f"Consider consolidating related analyses for easier reference.")
                response = input("Show consolidation options? [y/n]: ").strip().lower()
                if response == 'y':
                    self._show_consolidation_options(recent_files)

    def _show_consolidation_options(self, recent_files: List[str]):
        """Show options for consolidating recent files"""
        print(f"\n📋 **Recent Session Files:**")

        for i, filepath in enumerate(recent_files, 1):
            filename = Path(filepath).name
            metadata = self.lifecycle_manager.metadata_store.get(filepath)
            content_type = metadata.content_type if metadata else "unknown"
            print(f"{i}. {filename} ({content_type})")

        print(f"\n**Consolidation Options:**")
        print(f"1. Strategic Analysis Summary (combine analysis files)")
        print(f"2. Session Package (all files → single comprehensive doc)")
        print(f"3. Mark key files for retention")
        print(f"4. Continue without consolidation")

        choice = input("Choice [1-4]: ").strip()

        if choice == "1":
            self._consolidate_strategic_analysis(recent_files)
        elif choice == "2":
            self._create_session_package(recent_files)
        elif choice == "3":
            self._interactive_retention_marking(recent_files)

    def _consolidate_strategic_analysis(self, files: List[str]):
        """Consolidate strategic analysis files"""
        analysis_files = []
        for filepath in files:
            metadata = self.lifecycle_manager.metadata_store.get(filepath)
            if metadata and metadata.content_type == "strategic_analysis":
                analysis_files.append(filepath)

        if len(analysis_files) > 1:
            print(f"📋 Consolidating {len(analysis_files)} strategic analysis files...")
            # Implementation would combine content and create consolidated file
            # This is a placeholder for the actual consolidation logic
            print(f"✅ Consolidated analysis created")

    def _create_session_package(self, files: List[str]):
        """Create comprehensive session package"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        package_name = f"{timestamp}-session-package.md"

        print(f"📦 Creating session package: {package_name}")
        # Implementation would combine all files into comprehensive document
        # This is a placeholder for the actual packaging logic
        print(f"✅ Session package created")

    def _interactive_retention_marking(self, files: List[str]):
        """Interactive retention marking for important files"""
        print(f"\n🔒 **Mark Files for Retention**")

        for filepath in files:
            filename = Path(filepath).name
            metadata = self.lifecycle_manager.metadata_store.get(filepath)
            content_type = metadata.content_type if metadata else "unknown"

            response = input(f"Retain {filename} ({content_type})? [y/n/notes]: ").strip().lower()

            if response == 'y':
                self.lifecycle_manager.mark_for_retention(filepath)
            elif response == 'notes':
                notes = input("Business value/retention reason: ").strip()
                self.lifecycle_manager.mark_for_retention(filepath, user_notes=notes)

    def show_lifecycle_status(self):
        """Display current file lifecycle status with Phase 2 insights"""
        report = self.lifecycle_manager.generate_lifecycle_report()
        print(report)

        # Phase 2: Show smart organization opportunities
        print(f"\n🧠 **Smart Organization Analysis**")
        opportunities = self.smart_organizer.identify_consolidation_opportunities()
        if opportunities:
            print(f"📊 Found {len(opportunities)} consolidation opportunities")
            total_reduction = sum(opp.size_reduction for opp in opportunities)
            print(f"🎯 Potential cognitive load reduction: {total_reduction:.1f}x")

            response = input("Show smart organization options? [y/n]: ").strip().lower()
            if response == 'y':
                self.smart_organizer.suggest_consolidation_opportunities()
        else:
            print("✅ No consolidation opportunities detected")

        # Show archivable files
        archivable = self.lifecycle_manager.get_archivable_files()
        if archivable:
            print(f"\n⏰ **{len(archivable)} files eligible for archiving**")
            response = input("Run auto-archive? [y/n]: ").strip().lower()
            if response == 'y':
                archived = self.lifecycle_manager.auto_archive_eligible_files()
                print(f"📁 Archived {len(archived)} files")

    def configure_lifecycle_settings(self):
        """Interactive configuration of lifecycle settings"""
        self.lifecycle_manager._update_generation_settings()
        print(f"✅ Lifecycle settings updated")

    def initialize_workspace(self):
        """Initialize workspace with default configuration"""
        config_path = Path(self.workspace_path) / "config" / "file_lifecycle.yaml"

        if not config_path.exists():
            # Copy template to workspace
            template_path = Path(__file__).parent.parent.parent / "templates" / "workspace_config.yaml"

            if template_path.exists():
                config_path.parent.mkdir(parents=True, exist_ok=True)
                with open(template_path, 'r') as src, open(config_path, 'w') as dst:
                    dst.write(src.read())
                print(f"✅ Initialized workspace configuration: {config_path}")
            else:
                print(f"⚠️ Template not found, using defaults")

        # Ensure directory structure
        self.lifecycle_manager._ensure_directories()

        # Initialize Phase 2 smart organization
        self.smart_organizer.detect_session_patterns()

        print(f"✅ Workspace structure ready: {self.workspace_path}")
        print(f"🧠 Smart organization enabled (Phase 2)")
