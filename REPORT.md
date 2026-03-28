# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question:** "What is the agentic loop?"

**Answer:** The agent explained that the agentic loop is the core pattern where an LLM receives a task, reasons about it, decides whether to use tools, executes those tools, observes the results, and iterates until the task is complete. This differs from a simple chatbot which just responds once.

**Question:** "What labs are available in our LMS?" (before MCP tools)

**Answer:** Before MCP tools were configured, the agent had no access to live LMS data and would respond that it doesn't have access to that information or would try to use general knowledge.

## Task 1B — Agent with LMS tools

**Question:** "What labs are available?"

**Answer:**
```
Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

Is there a specific lab you'd like to know more about? I can show you pass rates, scores, group performance, or submission timelines for any of these labs.
```

The agent successfully called the `mcp_lms_lms_labs` MCP tool and returned real lab names from the backend.

**MCP Tools Registered:**
- `mcp_lms_lms_health` - Check backend health
- `mcp_lms_lms_labs` - Get list of labs
- `mcp_lms_lms_learners` - Get learners for a lab
- `mcp_lms_lms_pass_rates` - Get pass rates
- `mcp_lms_lms_timeline` - Get submission timeline
- `mcp_lms_lms_groups` - Get group statistics
- `mcp_lms_lms_top_learners` - Get top learners
- `mcp_lms_lms_completion_rate` - Get completion rate
- `mcp_lms_lms_sync_pipeline` - Trigger ETL sync

## Task 1C — Skill prompt

**Question:** "Show me the scores" (without specifying a lab)

**Answer:** The agent, guided by the LMS skill prompt, first called `lms_labs` to get available labs, then asked the user to specify which lab they want to see scores for, following the strategy defined in `workspace/skills/lms/SKILL.md`.

The skill prompt teaches the agent:
- Which LMS tools are available and when to use each
- To ask for lab selection when not specified
- To format numeric results nicely
- To keep responses concise
