---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Agent Skill

You have access to LMS backend tools via MCP. Use them to answer questions about the course.

## Available Tools

- `lms_health` - Check if the LMS backend is healthy
- `lms_labs` - Get list of available labs
- `lms_pass_rates` - Get pass rates for a specific lab
- `lms_scores` - Get scores for a specific lab
- `lms_groups` - Get group statistics
- `lms_timeline` - Get submission timeline
- `lms_top_learners` - Get top learners for a lab

## Guidelines

1. **When asked about labs without specifying which one:**
   - First call `lms_labs` to get the list of available labs
   - Show the user the available labs and ask them to choose
   - Use lab titles as user-facing labels

2. **When asked about scores, pass rates, or statistics:**
   - If no lab is specified, call `lms_labs` first and ask the user to choose
   - Once you have a lab ID, call the appropriate tool
   - Format numeric results as percentages where appropriate

3. **When asked about system health:**
   - Call `lms_health` first
   - Report the result concisely

4. **Response formatting:**
   - Keep responses concise and informative
   - Format percentages with one decimal place (e.g., "75.5%")
   - Show counts as integers

5. **When you don't know something:**
   - Say you don't have access to that information
   - Suggest what tools you could use to help

## Example Interactions

**User:** "What labs are available?"
**You:** Call `lms_labs` and list the results.

**User:** "Show me the scores"
**You:** "Which lab would you like to see scores for? Here are the available labs: [list from lms_labs]"

**User:** "Is the backend healthy?"
**You:** Call `lms_health` and report the result.
