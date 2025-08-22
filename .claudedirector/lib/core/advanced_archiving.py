"""
Advanced Archiving System for ClaudeDirector Phase 2
Smart archiving with search capabilities, pattern recognition, and cross-session insights
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import sqlite3


@dataclass
class ArchivedFileIndex:
    """Index entry for archived files to enable search"""

    file_path: str
    original_name: str
    archived_date: datetime
    content_type: str
    business_context: str
    content_summary: str
    keywords: List[str]
    session_id: Optional[str]
    retention_score: float  # Business value score for retrieval priority


@dataclass
class SearchResult:
    """Result from archive search"""

    file_path: str
    relevance_score: float
    content_summary: str
    business_context: str
    archived_date: datetime
    preview: str


class AdvancedArchivingSystem:
    """Advanced archiving with search and pattern recognition"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.archive_base = self.workspace_path / "archived-sessions"
        self.index_db_path = (
            self.workspace_path / ".claudedirector" / "archive_index.db"
        )

        # Initialize archive search database
        self._init_archive_database()

        # Business context extractors
        self.context_extractors = {
            "platform": self._extract_platform_context,
            "team": self._extract_team_context,
            "strategy": self._extract_strategy_context,
            "stakeholder": self._extract_stakeholder_context,
            "budget": self._extract_budget_context,
            "technical": self._extract_technical_context,
        }

    def _init_archive_database(self):
        """Initialize SQLite database for archive search"""
        self.index_db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(str(self.index_db_path)) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS archived_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE NOT NULL,
                    original_name TEXT NOT NULL,
                    archived_date TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    business_context TEXT,
                    content_summary TEXT,
                    keywords TEXT,  -- JSON array
                    session_id TEXT,
                    retention_score REAL,
                    full_content TEXT  -- For full-text search
                )
            """
            )

            # Create full-text search virtual table
            conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS archived_files_fts USING fts5(
                    original_name,
                    business_context,
                    content_summary,
                    keywords,
                    full_content,
                    content='archived_files',
                    content_rowid='id'
                )
            """
            )

            conn.commit()

    def archive_file_with_indexing(
        self, file_path: str, content_type: str, session_id: Optional[str] = None
    ) -> Optional[str]:
        """Archive file with enhanced indexing for search"""

        try:
            source_path = Path(file_path)
            if not source_path.exists():
                return None

            # Read file content for analysis
            with open(source_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract business intelligence from content
            business_context = self._extract_business_context(content)
            content_summary = self._generate_content_summary(content)
            keywords = self._extract_keywords(content)
            retention_score = self._calculate_retention_score(content, content_type)

            # Create date-based archive structure
            archive_date = datetime.now()
            archive_month = archive_date.strftime("%Y-%m")
            archive_dir = self.archive_base / archive_month
            archive_dir.mkdir(parents=True, exist_ok=True)

            # Generate archived filename with context
            archived_filename = self._generate_archived_filename(
                source_path.name, business_context, archive_date
            )
            archived_path = archive_dir / archived_filename

            # Move file to archive
            source_path.rename(archived_path)

            # Index in search database
            self._index_archived_file(
                archived_path,
                source_path.name,
                archive_date,
                content_type,
                business_context,
                content_summary,
                keywords,
                session_id,
                retention_score,
                content,
            )

            print(
                f"📁 Archived with indexing: {source_path.name} → {archive_month}/{archived_filename}"
            )
            return str(archived_path)

        except Exception as e:
            print(f"⚠️ Enhanced archiving failed for {file_path}: {e}")
            return None

    def _extract_business_context(self, content: str) -> str:
        """Extract business context from file content"""
        contexts = []

        for context_type, extractor in self.context_extractors.items():
            extracted = extractor(content)
            if extracted:
                contexts.extend(extracted)

        return ", ".join(set(contexts)) if contexts else "general"

    def _extract_platform_context(self, content: str) -> List[str]:
        """Extract platform-specific context"""
        content_lower = content.lower()
        platform_indicators = []

        if "migration" in content_lower:
            platform_indicators.append("platform-migration")
        if "scaling" in content_lower or "scale" in content_lower:
            platform_indicators.append("platform-scaling")
        if "architecture" in content_lower:
            platform_indicators.append("platform-architecture")
        if "infrastructure" in content_lower:
            platform_indicators.append("infrastructure")
        if "performance" in content_lower:
            platform_indicators.append("platform-performance")

        return platform_indicators

    def _extract_team_context(self, content: str) -> List[str]:
        """Extract team-specific context"""
        content_lower = content.lower()
        team_indicators = []

        if "hiring" in content_lower or "recruitment" in content_lower:
            team_indicators.append("team-hiring")
        if "org" in content_lower or "organization" in content_lower:
            team_indicators.append("team-structure")
        if "performance review" in content_lower:
            team_indicators.append("team-performance")
        if "growth" in content_lower:
            team_indicators.append("team-growth")

        return team_indicators

    def _extract_strategy_context(self, content: str) -> List[str]:
        """Extract strategic context"""
        content_lower = content.lower()
        strategy_indicators = []

        if "roadmap" in content_lower:
            strategy_indicators.append("strategic-roadmap")
        if "vision" in content_lower:
            strategy_indicators.append("strategic-vision")
        if "okr" in content_lower or "objectives" in content_lower:
            strategy_indicators.append("strategic-objectives")
        if "quarterly" in content_lower:
            strategy_indicators.append("quarterly-strategy")

        return strategy_indicators

    def _extract_stakeholder_context(self, content: str) -> List[str]:
        """Extract stakeholder context"""
        content_lower = content.lower()
        stakeholder_indicators = []

        if "executive" in content_lower:
            stakeholder_indicators.append("executive-communication")
        if "board" in content_lower:
            stakeholder_indicators.append("board-presentation")
        if "leadership" in content_lower:
            stakeholder_indicators.append("leadership-alignment")
        if "stakeholder" in content_lower:
            stakeholder_indicators.append("stakeholder-management")

        return stakeholder_indicators

    def _extract_budget_context(self, content: str) -> List[str]:
        """Extract budget/financial context"""
        content_lower = content.lower()
        budget_indicators = []

        if "roi" in content_lower or "return on investment" in content_lower:
            budget_indicators.append("roi-analysis")
        if "budget" in content_lower:
            budget_indicators.append("budget-planning")
        if "cost" in content_lower:
            budget_indicators.append("cost-analysis")
        if "investment" in content_lower:
            budget_indicators.append("investment-strategy")

        return budget_indicators

    def _extract_technical_context(self, content: str) -> List[str]:
        """Extract technical context"""
        content_lower = content.lower()
        technical_indicators = []

        if "technical debt" in content_lower:
            technical_indicators.append("technical-debt")
        if "migration" in content_lower:
            technical_indicators.append("technical-migration")
        if "implementation" in content_lower:
            technical_indicators.append("technical-implementation")
        if "framework" in content_lower:
            technical_indicators.append("technical-framework")

        return technical_indicators

    def _generate_content_summary(self, content: str) -> str:
        """Generate intelligent content summary"""
        lines = content.split("\n")

        # Extract headers and key content
        summary_lines = []
        for line in lines[:20]:  # First 20 lines
            line = line.strip()
            if line.startswith("#") or line.startswith("**") or line.startswith("*"):
                summary_lines.append(line.replace("#", "").replace("*", "").strip())
            elif line and len(line) > 20:
                summary_lines.append(line)

        summary = " ".join(summary_lines)

        # Truncate to reasonable length
        if len(summary) > 300:
            summary = summary[:300] + "..."

        return summary

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords for search indexing"""
        content_lower = content.lower()

        # Business keywords
        business_keywords = [
            "platform",
            "architecture",
            "scaling",
            "performance",
            "migration",
            "team",
            "hiring",
            "organization",
            "structure",
            "growth",
            "strategy",
            "roadmap",
            "vision",
            "objectives",
            "quarterly",
            "stakeholder",
            "executive",
            "board",
            "leadership",
            "communication",
            "budget",
            "roi",
            "cost",
            "investment",
            "financial",
            "technical",
            "debt",
            "implementation",
            "framework",
            "system",
        ]

        # Extract mentioned keywords
        found_keywords = []
        for keyword in business_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)

        # Extract proper nouns (potential project/system names)
        proper_nouns = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", content)
        found_keywords.extend(proper_nouns[:10])  # Limit to 10 proper nouns

        return list(set(found_keywords))

    def _calculate_retention_score(self, content: str, content_type: str) -> float:
        """Calculate business value retention score"""
        score = 0.0
        content_lower = content.lower()

        # Content type base scores
        type_scores = {
            "strategic_analysis": 8.0,
            "executive_presentation": 9.0,
            "quarterly_planning": 9.5,
            "meeting_prep": 6.0,
            "session_summary": 7.0,
            "framework_research": 5.0,
        }

        score += type_scores.get(content_type, 5.0)

        # High-value keyword bonuses
        high_value_keywords = {
            "roi": 2.0,
            "quarterly": 1.5,
            "executive": 1.5,
            "board": 2.0,
            "strategy": 1.0,
            "architecture": 1.0,
            "migration": 1.5,
            "budget": 1.5,
        }

        for keyword, bonus in high_value_keywords.items():
            if keyword in content_lower:
                score += bonus

        # Length/depth bonus
        if len(content) > 2000:
            score += 1.0

        return min(score, 10.0)  # Cap at 10.0

    def _generate_archived_filename(
        self, original_name: str, business_context: str, archive_date: datetime
    ) -> str:
        """Generate searchable archived filename"""

        # Extract primary context
        contexts = business_context.split(", ")
        primary_context = contexts[0].replace("-", "_") if contexts else "general"

        # Add date component
        date_str = archive_date.strftime("%Y%m%d")

        # Clean original name
        base_name = Path(original_name).stem
        extension = Path(original_name).suffix

        # Construct archived filename
        if primary_context != "general":
            archived_name = f"{date_str}_{primary_context}_{base_name}{extension}"
        else:
            archived_name = f"{date_str}_{base_name}{extension}"

        return archived_name

    def _index_archived_file(
        self,
        archived_path: Path,
        original_name: str,
        archived_date: datetime,
        content_type: str,
        business_context: str,
        content_summary: str,
        keywords: List[str],
        session_id: Optional[str],
        retention_score: float,
        full_content: str,
    ):
        """Index archived file in search database"""

        with sqlite3.connect(str(self.index_db_path)) as conn:
            # Insert into main table
            conn.execute(
                """
                INSERT OR REPLACE INTO archived_files
                (file_path, original_name, archived_date, content_type, business_context,
                 content_summary, keywords, session_id, retention_score, full_content)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    str(archived_path),
                    original_name,
                    archived_date.isoformat(),
                    content_type,
                    business_context,
                    content_summary,
                    json.dumps(keywords),
                    session_id,
                    retention_score,
                    full_content,
                ),
            )

            # Insert into FTS table
            conn.execute(
                """
                INSERT OR REPLACE INTO archived_files_fts
                (rowid, original_name, business_context, content_summary, keywords, full_content)
                SELECT id, original_name, business_context, content_summary, keywords, full_content
                FROM archived_files WHERE file_path = ?
            """,
                (str(archived_path),),
            )

            conn.commit()

    def search_archived_files(
        self, query: str, limit: int = 10, context_filter: Optional[str] = None
    ) -> List[SearchResult]:
        """Search archived files with relevance ranking"""

        results = []

        with sqlite3.connect(str(self.index_db_path)) as conn:
            # Build FTS query
            fts_query = self._build_fts_query(query)

            # Base search query
            sql = """
                SELECT af.file_path, af.original_name, af.archived_date,
                       af.content_type, af.business_context, af.content_summary,
                       af.retention_score, fts.rank
                FROM archived_files af
                JOIN archived_files_fts fts ON af.id = fts.rowid
                WHERE archived_files_fts MATCH ?
            """
            params = [fts_query]

            # Add context filter if specified
            if context_filter:
                sql += " AND af.business_context LIKE ?"
                params.append(f"%{context_filter}%")

            # Order by relevance and retention score
            sql += " ORDER BY fts.rank, af.retention_score DESC LIMIT ?"
            params.append(limit)

            cursor = conn.execute(sql, params)

            for row in cursor.fetchall():
                (
                    file_path,
                    original_name,
                    archived_date,
                    content_type,
                    business_context,
                    content_summary,
                    retention_score,
                    rank,
                ) = row

                # Generate preview
                preview = self._generate_search_preview(file_path, query)

                # Calculate relevance score
                relevance_score = self._calculate_relevance_score(
                    rank, retention_score, query, content_summary
                )

                result = SearchResult(
                    file_path=file_path,
                    relevance_score=relevance_score,
                    content_summary=content_summary,
                    business_context=business_context,
                    archived_date=datetime.fromisoformat(archived_date),
                    preview=preview,
                )
                results.append(result)

        return results

    def _build_fts_query(self, query: str) -> str:
        """Build FTS query from user input"""
        # Clean and tokenize query
        query_tokens = re.findall(r"\w+", query.lower())

        # Build FTS query with OR logic for flexibility
        if len(query_tokens) == 1:
            return query_tokens[0]
        else:
            return " OR ".join(query_tokens)

    def _calculate_relevance_score(
        self, fts_rank: float, retention_score: float, query: str, content_summary: str
    ) -> float:
        """Calculate combined relevance score"""

        # Normalize FTS rank (lower is better in FTS)
        fts_score = max(0, 10 - abs(fts_rank))

        # Boost for exact matches in summary
        exact_match_bonus = 2.0 if query.lower() in content_summary.lower() else 0

        # Combined relevance score
        relevance = (fts_score * 0.4) + (retention_score * 0.4) + exact_match_bonus

        return min(relevance, 10.0)

    def _generate_search_preview(self, file_path: str, query: str) -> str:
        """Generate search result preview with highlighted terms"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find relevant excerpt
            query_terms = re.findall(r"\w+", query.lower())
            content_lower = content.lower()

            # Find first occurrence of any query term
            best_pos = len(content)
            for term in query_terms:
                pos = content_lower.find(term)
                if pos != -1 and pos < best_pos:
                    best_pos = pos

            # Extract excerpt around the match
            start = max(0, best_pos - 100)
            end = min(len(content), best_pos + 200)
            excerpt = content[start:end]

            # Add ellipsis if truncated
            if start > 0:
                excerpt = "..." + excerpt
            if end < len(content):
                excerpt = excerpt + "..."

            return excerpt.strip()

        except Exception:
            return "Preview not available"

    def get_archive_statistics(self) -> Dict[str, Any]:
        """Get statistics about archived files"""
        stats = {}

        with sqlite3.connect(str(self.index_db_path)) as conn:
            # Total archived files
            cursor = conn.execute("SELECT COUNT(*) FROM archived_files")
            stats["total_files"] = cursor.fetchone()[0]

            # Files by content type
            cursor = conn.execute(
                """
                SELECT content_type, COUNT(*)
                FROM archived_files
                GROUP BY content_type
            """
            )
            stats["by_content_type"] = dict(cursor.fetchall())

            # Files by business context
            cursor = conn.execute(
                """
                SELECT business_context, COUNT(*)
                FROM archived_files
                GROUP BY business_context
                ORDER BY COUNT(*) DESC
                LIMIT 10
            """
            )
            stats["by_business_context"] = dict(cursor.fetchall())

            # Archive timeline
            cursor = conn.execute(
                """
                SELECT DATE(archived_date), COUNT(*)
                FROM archived_files
                GROUP BY DATE(archived_date)
                ORDER BY DATE(archived_date) DESC
                LIMIT 30
            """
            )
            stats["timeline"] = dict(cursor.fetchall())

            # High-value archived files
            cursor = conn.execute(
                """
                SELECT original_name, retention_score
                FROM archived_files
                ORDER BY retention_score DESC
                LIMIT 10
            """
            )
            stats["high_value_files"] = cursor.fetchall()

        return stats
