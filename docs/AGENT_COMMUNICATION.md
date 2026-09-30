# DIMRI AI — Agent Communication

## Goal

Agents should not operate as isolated chatbots. They should exchange structured work packets through the Company Brain.

## Standard work packet

- workflow_id
- sender_agent
- recipient_agent
- objective
- inputs
- evidence/source references
- requested output
- status
- priority
- permissions required
- verification state
- timestamps

## Handoff example

Founder:
"Find 10 businesses that need product photography and prepare opportunities."

DIMRI CEO:
1. Lead Research Agent finds candidates.
2. Research Agent verifies public business information.
3. Marketing Agent identifies relevant service angle.
4. Sales Agent prepares personalized outreach/proposal.
5. Operations creates follow-up tasks.
6. Founder approval gate is required before consequential external commitments.

## Memory

Company memory stores:
- company principles
- decisions
- workflow history
- source/evidence references
- project context
- approved SOPs

Production memory should move to persistent storage; this prototype uses in-process memory only.
