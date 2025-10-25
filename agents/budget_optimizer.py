"""
Budget Optimizer Agent
Specializes in budget analysis and cost optimization
"""

import os
import sys
from uagents import Agent, Context, Model
from typing import Dict, Any, List
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_integration import get_claude_assistant

load_dotenv()

# Agent configuration
budget_optimizer = Agent(
    name="BudgetOptimizer",
    seed="budget_optimizer_seed_phrase_33445",
    port=8004,
    endpoint=["http://localhost:8004/submit"]
)


class BudgetRequest(Model):
    """Request for budget analysis"""
    trip_details: Dict[str, Any]
    total_budget: float
    expenses: List[Dict[str, Any]]


class BudgetResponse(Model):
    """Response with budget optimization"""
    analysis: str
    optimized_budget: Dict[str, float]
    savings: float
    warnings: List[str]


@budget_optimizer.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent"""
    ctx.logger.info("Budget Optimizer Agent started")
    ctx.logger.info(f"Agent address: {budget_optimizer.address}")


@budget_optimizer.on_message(model=BudgetRequest)
async def handle_budget_request(
    ctx: Context,
    sender: str,
    msg: BudgetRequest
):
    """
    Analyze and optimize travel budgets using Claude's analytical capabilities
    """
    ctx.logger.info(f"Received budget optimization request")

    try:
        claude = get_claude_assistant()

        # Analyze budget using Claude
        analysis_text = await claude.optimize_budget(
            trip_details=msg.trip_details,
            current_budget=msg.total_budget,
            expenses=msg.expenses
        )

        response = BudgetResponse(
            analysis=analysis_text,
            optimized_budget={},
            savings=0.0,
            warnings=[]
        )

        await ctx.send(sender, response)
        ctx.logger.info("Budget analysis sent successfully")

    except Exception as e:
        ctx.logger.error(f"Error analyzing budget: {e}")


@budget_optimizer.on_interval(period=300.0)
async def log_status(ctx: Context):
    """Periodic status log"""
    ctx.logger.info("Budget Optimizer Agent is active and ready")


if __name__ == "__main__":
    print("Starting Budget Optimizer Agent...")
    print(f"Agent Address: {budget_optimizer.address}")
    budget_optimizer.run()
