"""
Persona Manager Integration for Transparency System
Seamless integration with existing ClaudeDirector persona pipeline
"""

import asyncio
from typing import Dict, Any, Optional, Callable
import logging
from dataclasses import dataclass

from .integrated_transparency import IntegratedTransparencySystem, TransparencyContext


logger = logging.getLogger(__name__)


@dataclass
class PersonaResponse:
    """Enhanced persona response with transparency information"""

    content: str
    persona: str
    transparency_summary: Optional[Dict[str, Any]] = None
    processing_time: float = 0.0
    enhancements_applied: bool = False


class TransparentPersonaManager:
    """
    Enhanced Persona Manager that integrates transparency into existing ClaudeDirector personas
    Designed to be a drop-in replacement for existing persona managers
    """

    def __init__(
        self,
        transparency_system: IntegratedTransparencySystem,
        original_persona_manager=None,
    ):
        self.transparency_system = transparency_system
        self.original_persona_manager = original_persona_manager
        self.persona_handlers = {}

        # Performance and debugging
        self.debug_mode = transparency_system.config.get("debug_mode", False)
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging for transparency operations"""
        if self.debug_mode:
            logging.basicConfig(level=logging.DEBUG)
            logger.debug("Transparent Persona Manager initialized with debug mode")

    def register_persona(self, persona_name: str, handler: Callable):
        """Register a persona handler with the manager"""
        self.persona_handlers[persona_name] = handler
        logger.debug(f"Registered persona: {persona_name}")

    async def generate_persona_response(
        self,
        persona: str,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> PersonaResponse:
        """
        Generate a persona response with full transparency integration

        Args:
            persona: Name of the persona to use
            query: User query to process
            context: Additional context for the persona
            **kwargs: Additional arguments for persona handlers

        Returns:
            PersonaResponse with transparency information
        """
        # Create transparency context
        transparency_context = self.transparency_system.create_transparency_context(
            persona
        )

        try:
            # Add transparency context to persona handler kwargs
            handler_kwargs = kwargs.copy()
            handler_kwargs["transparency_context"] = transparency_context
            handler_kwargs["context"] = context or {}

            # Generate base response using appropriate method
            if self.original_persona_manager:
                # Delegate to existing persona manager
                base_response = await self._delegate_to_original_manager(
                    persona, query, handler_kwargs
                )
            elif persona in self.persona_handlers:
                # Use registered handler
                base_response = await self.persona_handlers[persona](
                    query, **handler_kwargs
                )
            else:
                # Fallback to default handler
                base_response = await self._default_persona_handler(
                    persona, query, handler_kwargs
                )

            # Apply transparency enhancements
            enhanced_response = self.transparency_system.apply_transparency(
                transparency_context, base_response
            )

            # Create response object
            persona_response = PersonaResponse(
                content=enhanced_response,
                persona=persona,
                transparency_summary=self.transparency_system.create_transparency_summary(
                    transparency_context
                ),
                processing_time=transparency_context.total_processing_time,
                enhancements_applied=transparency_context.has_enhancements,
            )

            if self.debug_mode:
                logger.debug(
                    f"Generated transparent response for {persona}: {persona_response.transparency_summary}"
                )

            return persona_response

        except Exception as e:
            logger.error(f"Error generating persona response for {persona}: {str(e)}")
            # Return error response with transparency context
            error_response = f"I apologize, but I encountered an error while processing your request. Please try again."

            return PersonaResponse(
                content=error_response,
                persona=persona,
                transparency_summary=self.transparency_system.create_transparency_summary(
                    transparency_context
                ),
                processing_time=transparency_context.total_processing_time,
                enhancements_applied=False,
            )

    async def _delegate_to_original_manager(
        self, persona: str, query: str, kwargs: Dict[str, Any]
    ) -> str:
        """Delegate to original persona manager if available"""
        if hasattr(self.original_persona_manager, "generate_response"):
            return await self.original_persona_manager.generate_response(
                persona, query, **kwargs
            )
        elif hasattr(self.original_persona_manager, "get_persona_response"):
            return await self.original_persona_manager.get_persona_response(
                persona, query, **kwargs
            )
        else:
            # Fallback method call
            return await self.original_persona_manager(persona, query, **kwargs)

    async def _default_persona_handler(
        self, persona: str, query: str, kwargs: Dict[str, Any]
    ) -> str:
        """Default persona handler for unregistered personas"""
        kwargs.get("transparency_context")

        # Basic persona-style response
        response = f"As {persona}, I understand your query: {query}. "

        # Add persona-specific flavor based on known personas
        if persona.lower() == "diego":
            response += (
                "From a strategic perspective, let me analyze this systematically..."
            )
        elif persona.lower() == "camille":
            response += (
                "Taking an innovative approach, I see several opportunities here..."
            )
        elif persona.lower() == "rachel":
            response += "From a change management standpoint, we need to consider..."
        elif persona.lower() == "alvaro":
            response += "Looking at this through a technical lens, I can identify..."
        elif persona.lower() == "martin":
            response += "From a business development angle, this presents..."
        else:
            response += "Let me provide you with a comprehensive analysis..."

        # Simulate some processing for demonstration
        await asyncio.sleep(0.1)

        return response

    def track_mcp_call(
        self,
        transparency_context: TransparencyContext,
        server_name: str,
        capability: str,
        processing_time: float,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """Convenience method to track MCP calls"""
        self.transparency_system.track_mcp_call(
            transparency_context,
            server_name,
            capability,
            processing_time,
            success,
            error_message,
        )

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get transparency system performance statistics"""
        return self.transparency_system.get_performance_stats()

    def get_persona_stats(self) -> Dict[str, Any]:
        """Get persona-specific statistics"""
        return {
            "registered_personas": list(self.persona_handlers.keys()),
            "has_original_manager": self.original_persona_manager is not None,
            "debug_mode": self.debug_mode,
            "transparency_config": self.transparency_system.config,
        }


class PersonaIntegrationFactory:
    """Factory for creating integrated persona managers"""

    @staticmethod
    def create_transparent_manager(
        transparency_config: str = "default", original_manager=None
    ) -> TransparentPersonaManager:
        """
        Create a transparent persona manager

        Args:
            transparency_config: Configuration type ("default", "minimal", "debug")
            original_manager: Existing persona manager to integrate with

        Returns:
            TransparentPersonaManager instance
        """
        from .integrated_transparency import create_transparency_system

        transparency_system = create_transparency_system(transparency_config)
        return TransparentPersonaManager(transparency_system, original_manager)

    @staticmethod
    def wrap_existing_manager(existing_manager, transparency_config: str = "default"):
        """
        Wrap an existing persona manager with transparency

        Args:
            existing_manager: Existing persona manager to wrap
            transparency_config: Configuration type for transparency

        Returns:
            TransparentPersonaManager wrapping the existing manager
        """
        return PersonaIntegrationFactory.create_transparent_manager(
            transparency_config, existing_manager
        )


class MCPIntegrationHelper:
    """Helper class for integrating MCP calls with transparency"""

    def __init__(
        self,
        transparency_context: TransparencyContext,
        persona_manager: TransparentPersonaManager,
    ):
        self.transparency_context = transparency_context
        self.persona_manager = persona_manager

    async def call_mcp_server(
        self, server_name: str, capability: str, **call_kwargs
    ) -> Any:
        """
        Make an MCP server call with automatic transparency tracking

        Args:
            server_name: Name of the MCP server
            capability: Capability being called
            **call_kwargs: Arguments for the MCP call

        Returns:
            Result from MCP server call
        """
        import time

        start_time = time.time()

        try:
            # TODO: Replace with actual MCP server call logic
            # Simulate MCP integration - replace with actual MCP client
            result = await self._simulate_mcp_call(server_name, capability, call_kwargs)

            processing_time = time.time() - start_time

            # Track successful call
            self.persona_manager.track_mcp_call(
                self.transparency_context,
                server_name,
                capability,
                processing_time,
                success=True,
            )

            return result

        except Exception as e:
            processing_time = time.time() - start_time

            # Track failed call
            self.persona_manager.track_mcp_call(
                self.transparency_context,
                server_name,
                capability,
                processing_time,
                success=False,
                error_message=str(e),
            )

            raise e

    async def _simulate_mcp_call(
        self, server_name: str, capability: str, call_kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate MCP server call for demonstration"""
        await asyncio.sleep(0.05)  # Simulate network call

        return {
            "server": server_name,
            "capability": capability,
            "result": "simulated_result",
            "kwargs": call_kwargs,
        }
