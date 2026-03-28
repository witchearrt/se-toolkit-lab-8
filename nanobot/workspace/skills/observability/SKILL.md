---
name: observability
description: Use observability MCP tools for logs and traces
always: true
---

# Observability Skill

You have access to observability tools via MCP for VictoriaLogs and VictoriaTraces.

## Available Tools

- `logs_search` — Search logs by query and time range
- `logs_error_count` — Count errors per service over a time window
- `traces_list` — List recent traces for a service
- `traces_get` — Get a specific trace by ID

## Guidelines

1. **When asked about errors or failures:**
   - First call `logs_error_count` with a recent time window (e.g., 10 minutes)
   - If errors exist, call `logs_search` to get details
   - Look for `trace_id` in error logs
   - Call `traces_get` with the trace ID to see the full request flow

2. **When asked about system health:**
   - Check for recent errors with `logs_error_count` (last 10-60 minutes)
   - If no errors, report system is healthy
   - If errors exist, investigate with `logs_search` and `traces_get`

3. **Time ranges:**
   - Use `minutes` parameter to scope queries
   - For "recent" or "last hour", use 60 minutes
   - For "last 10 minutes", use 10 minutes
   - Be specific about time windows in your responses

4. **Response formatting:**
   - Summarize findings concisely
   - Don't dump raw JSON
   - Mention specific services, error types, and trace IDs when relevant
   - If you find an error trace, explain what failed and where

## Example Interactions

**User:** "Any errors in the last hour?"
**You:** Call `logs_error_count` with `minutes=60`, then report results.

**User:** "What went wrong?"
**You:** 
1. Call `logs_error_count` with `minutes=10`
2. If errors exist, call `logs_search` with `severity:ERROR`
3. Extract `trace_id` from logs
4. Call `traces_get` with the trace ID
5. Summarize the failure chain

**User:** "Check system health"
**You:** Call `logs_error_count` for the LMS backend service and report if healthy or not.
