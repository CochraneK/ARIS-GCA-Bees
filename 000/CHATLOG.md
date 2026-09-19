# ARIS4C 000 · Controller Conversation Log

Public-safe summaries of material portfolio-control decisions. This is not hidden chain-of-thought.

## 2026-09-19 · 000 operating model consolidated

- 000 is the permanent portfolio command center and normal execution entry point.
- Git is the canonical long-term state.
- Paper-specific chats are optional deep-dive rooms rather than sources of truth.
- Primary states are Finish / Active / Wait / Block.
- Default Active WIP is 1; normal maximum is 3.
- Before switching papers, substantive work must be checkpointed to Git and the paper handoff synchronized.
- In the absence of explicit user override, scheduling is completion-first: continue genuine Active work, then choose the highest-progress Wait paper.
- A dedicated Git-resident `000/` handoff was created so another agent/account/computer can take over portfolio control without access to the original chat.
