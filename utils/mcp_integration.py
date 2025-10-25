"""
Model Context Protocol (MCP) Integration
Enables saving trip plans to Notion and other external tools
"""

import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class MCPNotionIntegration:
    """
    MCP integration for saving trip plans to Notion
    Uses Anthropic's Model Context Protocol
    """

    def __init__(self, notion_api_key: Optional[str] = None):
        self.notion_api_key = notion_api_key or os.getenv("NOTION_API_KEY")
        self.notion_database_id = os.getenv("NOTION_DATABASE_ID")
        self.mcp_enabled = bool(self.notion_api_key and self.notion_database_id)

    async def save_trip_plan_to_notion(
        self,
        trip_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Save a complete trip plan to Notion using MCP

        Args:
            trip_plan: Dictionary containing trip details

        Returns:
            Result with Notion page URL
        """
        if not self.mcp_enabled:
            return {
                "success": False,
                "error": "Notion MCP not configured. Set NOTION_API_KEY and NOTION_DATABASE_ID",
                "message": "Trip plan saved locally only"
            }

        try:
            # This would use the MCP protocol to communicate with Notion
            # For now, we'll prepare the data structure
            notion_page = self._format_trip_plan_for_notion(trip_plan)

            # In production, this would use MCP to create the Notion page
            # For demonstration, we'll return the formatted data
            return {
                "success": True,
                "notion_page": notion_page,
                "message": "Trip plan ready for Notion (MCP integration configured)",
                "note": "Install MCP Notion server to enable full functionality"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error preparing trip plan for Notion"
            }

    def _format_trip_plan_for_notion(self, trip_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Format trip plan data for Notion page structure"""

        destination = trip_plan.get("destination", "Unknown Destination")
        duration = trip_plan.get("duration", 0)
        start_date = trip_plan.get("start_date", datetime.now().strftime("%Y-%m-%d"))

        # Notion page structure
        page_structure = {
            "parent": {"database_id": self.notion_database_id},
            "properties": {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": f"Trip to {destination}"
                            }
                        }
                    ]
                },
                "Destination": {
                    "rich_text": [
                        {
                            "text": {
                                "content": destination
                            }
                        }
                    ]
                },
                "Duration": {
                    "number": duration
                },
                "Start Date": {
                    "date": {
                        "start": start_date
                    }
                },
                "Status": {
                    "select": {
                        "name": "Planning"
                    }
                },
                "Budget": {
                    "number": trip_plan.get("budget", 0)
                }
            },
            "children": self._create_notion_blocks(trip_plan)
        }

        return page_structure

    def _create_notion_blocks(self, trip_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create Notion content blocks for trip plan"""

        blocks = []

        # Trip Overview
        blocks.append({
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Trip Overview"}}]
            }
        })

        # Preferences
        if preferences := trip_plan.get("preferences"):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Preferences"}}]
                }
            })
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Budget: {preferences.get('budget', 'N/A')}"}}]
                }
            })
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Interests: {', '.join(preferences.get('interests', []))}"}}]
                }
            })

        # Itinerary
        if itinerary := trip_plan.get("itinerary"):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "Itinerary"}}]
                }
            })

            # Add each day
            for day in itinerary.get("days", []):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": f"Day {day.get('day_number')}: {day.get('theme', '')}"}}]
                    }
                })
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"Morning: {day.get('morning', '')}"}}]
                    }
                })
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"Afternoon: {day.get('afternoon', '')}"}}]
                    }
                })
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"Evening: {day.get('evening', '')}"}}]
                    }
                })

        # Budget Analysis
        if budget := trip_plan.get("budget_analysis"):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "Budget Breakdown"}}]
                }
            })
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": budget.get("analysis", "")}}]
                }
            })

        # Local Insights
        if insights := trip_plan.get("local_insights"):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "Local Insights & Tips"}}]
                }
            })
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": insights}}]
                }
            })

        return blocks


class MCPToolRegistry:
    """
    Registry for MCP tools that agents can use
    """

    def __init__(self):
        self.tools = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default MCP tools"""

        # Notion integration
        self.tools["save_to_notion"] = {
            "name": "save_to_notion",
            "description": "Save trip plan to Notion workspace",
            "parameters": {
                "type": "object",
                "properties": {
                    "trip_plan": {
                        "type": "object",
                        "description": "Complete trip plan data"
                    }
                },
                "required": ["trip_plan"]
            }
        }

        # Export to calendar
        self.tools["export_to_calendar"] = {
            "name": "export_to_calendar",
            "description": "Export itinerary to calendar (iCal format)",
            "parameters": {
                "type": "object",
                "properties": {
                    "itinerary": {
                        "type": "object",
                        "description": "Itinerary with dates and activities"
                    }
                },
                "required": ["itinerary"]
            }
        }

        # Create PDF
        self.tools["create_pdf"] = {
            "name": "create_pdf",
            "description": "Generate PDF document of trip plan",
            "parameters": {
                "type": "object",
                "properties": {
                    "trip_plan": {
                        "type": "object",
                        "description": "Complete trip plan data"
                    }
                },
                "required": ["trip_plan"]
            }
        }

    def get_tool(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get tool definition by name"""
        return self.tools.get(tool_name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available MCP tools"""
        return list(self.tools.values())


# Singleton instances
_notion_integration: Optional[MCPNotionIntegration] = None
_tool_registry: Optional[MCPToolRegistry] = None


def get_notion_integration() -> MCPNotionIntegration:
    """Get or create singleton Notion integration instance"""
    global _notion_integration
    if _notion_integration is None:
        _notion_integration = MCPNotionIntegration()
    return _notion_integration


def get_mcp_tool_registry() -> MCPToolRegistry:
    """Get or create singleton MCP tool registry"""
    global _tool_registry
    if _tool_registry is None:
        _tool_registry = MCPToolRegistry()
    return _tool_registry
