"""
ClaudeDirector File Lifecycle Management System
Provides user control over file generation, retention, and archiving in engineering-director-workspace
"""

import os
import yaml
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class GenerationMode(Enum):
    """File generation modes for different user preferences"""
    MINIMAL = "minimal"          # Strategic analysis only, consolidated files
    PROFESSIONAL = "professional"  # + Meeting prep, quarterly organization
    RESEARCH = "research"        # + Framework docs, methodology materials

class FileRetentionStatus(Enum):
    """File retention status for lifecycle management"""
    STANDARD = "standard"        # Subject to auto-archive rules
    RETAINED = "retained"        # User-marked for permanent retention
    ARCHIVED = "archived"        # Moved to archive directory
    TEMPORARY = "temporary"      # Auto-delete after session

@dataclass
class FileMetadata:
    """Metadata for tracking file lifecycle"""
    created_at: datetime
    last_accessed: datetime
    retention_status: FileRetentionStatus
    generation_mode: GenerationMode
    content_type: str  # "strategic_analysis", "meeting_prep", "framework_research", etc.
    session_id: Optional[str] = None
    user_notes: Optional[str] = None
    business_value: Optional[str] = None  # User-defined business value description

@dataclass
class WorkspaceConfig:
    """User configuration for file lifecycle management"""
    generation_mode: GenerationMode = GenerationMode.PROFESSIONAL
    auto_archive_days: int = 30
    consolidate_analysis: bool = True
    prompt_before_generation: bool = True
    archive_directory: str = "archived-sessions"
    retention_directory: str = "retained-assets"
    max_session_files: int = 5  # Trigger consolidation prompt

class FileLifecycleManager:
    """Manages file creation, retention, and archiving in engineering-director-workspace"""
    
    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = Path(workspace_path)
        self.config_file = self.workspace_path / "config" / "file_lifecycle.yaml"
        self.metadata_file = self.workspace_path / ".claudedirector" / "file_metadata.json"
        self.config = self._load_config()
        self.metadata_store = self._load_metadata()
        
        # Ensure required directories exist
        self._ensure_directories()
    
    def _load_config(self) -> WorkspaceConfig:
        """Load user configuration or create defaults"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = yaml.safe_load(f)
                
                return WorkspaceConfig(
                    generation_mode=GenerationMode(config_data.get('generation_mode', 'professional')),
                    auto_archive_days=config_data.get('auto_archive_days', 30),
                    consolidate_analysis=config_data.get('consolidate_analysis', True),
                    prompt_before_generation=config_data.get('prompt_before_generation', True),
                    archive_directory=config_data.get('archive_directory', 'archived-sessions'),
                    retention_directory=config_data.get('retention_directory', 'retained-assets'),
                    max_session_files=config_data.get('max_session_files', 5)
                )
            except Exception as e:
                print(f"Warning: Could not load config, using defaults: {e}")
                return WorkspaceConfig()
        else:
            # Create default config file
            default_config = WorkspaceConfig()
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config: WorkspaceConfig) -> None:
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        config_data = {
            'generation_mode': config.generation_mode.value,
            'auto_archive_days': config.auto_archive_days,
            'consolidate_analysis': config.consolidate_analysis,
            'prompt_before_generation': config.prompt_before_generation,
            'archive_directory': config.archive_directory,
            'retention_directory': config.retention_directory,
            'max_session_files': config.max_session_files
        }
        
        with open(self.config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)
    
    def _load_metadata(self) -> Dict[str, FileMetadata]:
        """Load file metadata store"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                
                metadata_store = {}
                for filepath, metadata_dict in data.items():
                    metadata_store[filepath] = FileMetadata(
                        created_at=datetime.fromisoformat(metadata_dict['created_at']),
                        last_accessed=datetime.fromisoformat(metadata_dict['last_accessed']),
                        retention_status=FileRetentionStatus(metadata_dict['retention_status']),
                        generation_mode=GenerationMode(metadata_dict['generation_mode']),
                        content_type=metadata_dict['content_type'],
                        session_id=metadata_dict.get('session_id'),
                        user_notes=metadata_dict.get('user_notes'),
                        business_value=metadata_dict.get('business_value')
                    )
                return metadata_store
            except Exception as e:
                print(f"Warning: Could not load metadata, starting fresh: {e}")
                return {}
        else:
            return {}
    
    def _save_metadata(self) -> None:
        """Save metadata store to file"""
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        serializable_data = {}
        for filepath, metadata in self.metadata_store.items():
            serializable_data[filepath] = {
                'created_at': metadata.created_at.isoformat(),
                'last_accessed': metadata.last_accessed.isoformat(),
                'retention_status': metadata.retention_status.value,
                'generation_mode': metadata.generation_mode.value,
                'content_type': metadata.content_type,
                'session_id': metadata.session_id,
                'user_notes': metadata.user_notes,
                'business_value': metadata.business_value
            }
        
        with open(self.metadata_file, 'w') as f:
            json.dump(serializable_data, f, indent=2)
    
    def _ensure_directories(self) -> None:
        """Ensure required directories exist"""
        directories = [
            self.workspace_path / "config",
            self.workspace_path / self.config.archive_directory,
            self.workspace_path / self.config.retention_directory,
            self.workspace_path / "analysis-results",
            self.workspace_path / "current-work"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def request_file_generation(
        self, 
        content_type: str, 
        proposed_filename: str, 
        content_preview: str,
        business_context: str
    ) -> Tuple[bool, str]:
        """
        Request permission to generate a file
        Returns (approved, final_filename)
        """
        if not self.config.prompt_before_generation:
            return True, proposed_filename
        
        print(f"\n🎯 **ClaudeDirector File Generation Request**")
        print(f"📄 **Proposed File**: {proposed_filename}")
        print(f"📋 **Content Type**: {content_type}")
        print(f"🎯 **Business Context**: {business_context}")
        print(f"📝 **Content Preview**:")
        print(f"   {content_preview[:200]}...")
        
        # Check if this would exceed session file limits
        recent_files = self._get_recent_session_files()
        if len(recent_files) >= self.config.max_session_files:
            print(f"\n⚠️ **Session has {len(recent_files)} files (max: {self.config.max_session_files})**")
            print(f"Consider consolidating or archiving previous files.")
        
        print(f"\n**Options:**")
        print(f"✅ [y] Create file")
        print(f"📝 [c] Create with custom filename")
        print(f"🚫 [n] Skip file creation")
        print(f"⚙️ [s] Update generation settings")
        
        response = input("Choice [y/c/n/s]: ").strip().lower()
        
        if response == 'y':
            return True, proposed_filename
        elif response == 'c':
            custom_name = input("Enter filename: ").strip()
            return True, custom_name if custom_name else proposed_filename
        elif response == 's':
            self._update_generation_settings()
            return self.request_file_generation(content_type, proposed_filename, content_preview, business_context)
        else:
            return False, ""
    
    def register_file(
        self, 
        filepath: str, 
        content_type: str, 
        session_id: Optional[str] = None
    ) -> None:
        """Register a newly created file"""
        abs_filepath = str(Path(filepath).resolve())
        
        metadata = FileMetadata(
            created_at=datetime.now(),
            last_accessed=datetime.now(),
            retention_status=FileRetentionStatus.STANDARD,
            generation_mode=self.config.generation_mode,
            content_type=content_type,
            session_id=session_id
        )
        
        self.metadata_store[abs_filepath] = metadata
        self._save_metadata()
    
    def mark_for_retention(self, filepath: str, user_notes: str = "", business_value: str = "") -> None:
        """Mark a file for permanent retention beyond auto-archive"""
        abs_filepath = str(Path(filepath).resolve())
        
        if abs_filepath in self.metadata_store:
            self.metadata_store[abs_filepath].retention_status = FileRetentionStatus.RETAINED
            self.metadata_store[abs_filepath].user_notes = user_notes
            self.metadata_store[abs_filepath].business_value = business_value
            self._save_metadata()
            print(f"✅ Marked for retention: {Path(filepath).name}")
        else:
            print(f"⚠️ File not found in metadata store: {filepath}")
    
    def get_archivable_files(self) -> List[Tuple[str, FileMetadata]]:
        """Get files eligible for archiving"""
        cutoff_date = datetime.now() - timedelta(days=self.config.auto_archive_days)
        archivable = []
        
        for filepath, metadata in self.metadata_store.items():
            if (metadata.retention_status == FileRetentionStatus.STANDARD and 
                metadata.last_accessed < cutoff_date and
                Path(filepath).exists()):
                archivable.append((filepath, metadata))
        
        return archivable
    
    def auto_archive_eligible_files(self) -> List[str]:
        """Automatically archive eligible files"""
        archivable_files = self.get_archivable_files()
        archived_files: List[str] = []
        
        if not archivable_files:
            return []
        
        print(f"\n📁 **Auto-Archive Review**: {len(archivable_files)} files eligible")
        
        for filepath, metadata in archivable_files:
            filename = Path(filepath).name
            age_days = (datetime.now() - metadata.last_accessed).days
            
            print(f"📄 {filename} (age: {age_days} days, type: {metadata.content_type})")
        
        response = input(f"\nArchive these {len(archivable_files)} files? [y/n/r]: ").strip().lower()
        
        if response == 'y':
            for filepath, metadata in archivable_files:
                if self._archive_file(filepath):
                    archived_files.append(filepath)
        elif response == 'r':
            # Review individually
            for filepath, metadata in archivable_files:
                filename = Path(filepath).name
                individual_response = input(f"Archive {filename}? [y/n/r]: ").strip().lower()
                
                if individual_response == 'y':
                    if self._archive_file(filepath):
                        archived_files.append(filepath)
                elif individual_response == 'r':
                    # Mark for retention
                    notes = input("Retention reason: ").strip()
                    self.mark_for_retention(filepath, user_notes=notes)
        
        return archived_files
    
    def _archive_file(self, filepath: str) -> bool:
        """Move file to archive directory"""
        try:
            source_path = Path(filepath)
            if not source_path.exists():
                return False
            
            # Create date-based archive structure
            archive_base = self.workspace_path / self.config.archive_directory
            archive_date = datetime.now().strftime("%Y-%m")
            archive_dir = archive_base / archive_date
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            # Move file
            destination = archive_dir / source_path.name
            source_path.rename(destination)
            
            # Update metadata
            if filepath in self.metadata_store:
                self.metadata_store[filepath].retention_status = FileRetentionStatus.ARCHIVED
                self._save_metadata()
            
            print(f"📁 Archived: {source_path.name} → {archive_date}/")
            return True
            
        except Exception as e:
            print(f"⚠️ Failed to archive {filepath}: {e}")
            return False
    
    def _get_recent_session_files(self) -> List[str]:
        """Get files from current session (within last 24 hours)"""
        cutoff = datetime.now() - timedelta(hours=24)
        recent_files = []
        
        for filepath, metadata in self.metadata_store.items():
            if (metadata.created_at > cutoff and 
                metadata.retention_status == FileRetentionStatus.STANDARD and
                Path(filepath).exists()):
                recent_files.append(filepath)
        
        return recent_files
    
    def _update_generation_settings(self) -> None:
        """Interactive settings update"""
        print(f"\n⚙️ **Current Settings:**")
        print(f"Mode: {self.config.generation_mode.value}")
        print(f"Auto-archive: {self.config.auto_archive_days} days")
        print(f"Prompt before generation: {self.config.prompt_before_generation}")
        print(f"Consolidate analysis: {self.config.consolidate_analysis}")
        
        # Update generation mode
        print(f"\n**Generation Modes:**")
        print(f"1. minimal - Strategic analysis only, consolidated files")
        print(f"2. professional - + Meeting prep, quarterly organization") 
        print(f"3. research - + Framework docs, methodology materials")
        
        mode_choice = input(f"Current mode ({self.config.generation_mode.value}): ").strip()
        if mode_choice == "1":
            self.config.generation_mode = GenerationMode.MINIMAL
        elif mode_choice == "2":
            self.config.generation_mode = GenerationMode.PROFESSIONAL
        elif mode_choice == "3":
            self.config.generation_mode = GenerationMode.RESEARCH
        
        # Update other settings
        try:
            days = input(f"Auto-archive days ({self.config.auto_archive_days}): ").strip()
            if days:
                self.config.auto_archive_days = int(days)
        except ValueError:
            pass
        
        prompt_choice = input(f"Prompt before generation? ({self.config.prompt_before_generation}) [y/n]: ").strip().lower()
        if prompt_choice in ['y', 'n']:
            self.config.prompt_before_generation = prompt_choice == 'y'
        
        self._save_config(self.config)
        print(f"✅ Settings updated!")
    
    def generate_lifecycle_report(self) -> str:
        """Generate a summary of file lifecycle status"""
        total_files = len(self.metadata_store)
        retained_files = len([m for m in self.metadata_store.values() if m.retention_status == FileRetentionStatus.RETAINED])
        archived_files = len([m for m in self.metadata_store.values() if m.retention_status == FileRetentionStatus.ARCHIVED])
        archivable_files = len(self.get_archivable_files())
        
        recent_files = self._get_recent_session_files()
        
        report = f"""
📊 **File Lifecycle Status**

📁 **Current Session**: {len(recent_files)} files
📄 **Total Tracked**: {total_files} files
🔒 **Retained**: {retained_files} files
📁 **Archived**: {archived_files} files
⏰ **Archivable**: {archivable_files} files

⚙️ **Settings**: {self.config.generation_mode.value} mode, {self.config.auto_archive_days}-day retention
"""
        
        return report
