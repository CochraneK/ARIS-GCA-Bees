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


## 2026-09-19 · Public dashboard simplification and split view

- The user removed all public card actions except **English** and **中文**; Figures, Tables, Pipeline, Source, and EN/ZH/FIG/TAB completion badges remain backend metadata only.
- The top-level `All projects` view was redesigned as a continuously rolling research showcase.
- The user then clarified that only `All projects` should use the rolling showcase; status subviews should keep the prior detailed project-card panel.
- Current implementation on `main`: All = marquee; Finish/Active/Wait/Block = detailed cards; search = detailed cards; Hero summary = All only.
- Before deleting the chat, the live repository and representative project handoffs were re-read; the canonical portfolio contains 17 papers and current state is recoverable from Git.
- Recovery checkpoint: `000/PRE_DELETE_CHECKPOINT_2026-09-19.md`.
