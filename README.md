# Harland / Longfellow1

AI product architect building local-first personal AI tools and production-grade Agent Runtime systems.

## Featured Project

### [Penpal](https://github.com/Longfellow1/penpal)

The local memory all your AIs share. Penpal remembers what you've seen, written and asked on your Mac, and serves it over MCP to Claude Code, Codex and Cursor. Every result links back to its source, and you decide what each AI is allowed to see.

- Local-first: data stays in `~/.penpal`, no cloud, no telemetry
- Per-AI grants by category: Work / Personal / Private / Financial
- Built for what "AI + bash" can't reach: things that never hit disk, history past its retention, scoped access

## What I Am Thinking About

I work on AI systems that need to be useful outside demos:

- Agent Runtime design
- Context engineering
- Memory systems
- Skill and tool orchestration
- Permission, sandbox, trace, replay, and eval
- Local-first personal AI
- Real-time voice AI products

My current architecture thesis:

> Prompt makes the model know what to do.  
> Harness makes the system ensure it is done correctly.

## Recent Direction

I am exploring how production AI systems evolve from:

```text
chatbot / workflow / routed services
```

into:

```text
Orchestrator
+ Context Engine
+ Memory System
+ Skill Runtime
+ Tool Harness
+ Trace / Replay / Eval
```

The goal is not to build more things named "agents".  
The goal is to build systems where AI behavior is controllable, observable, reusable, and safe enough for real users.

## Agent Skills

### [Principled Simplicity · deep-fix](https://github.com/Longfellow1/Principled-Simplicity-skill)

Fix the layer, not the case. An architecture-repair method for AI agent systems: find the layer that owns a recurring problem and fix the mechanism there.

### [Product Judgment](https://github.com/Longfellow1/Product-Judgment-skill)

Judge the demand before writing the PRD. An agent implementation of Yu Jun's product methodology.

## Writing Themes

I write and build around:

- local-first AI memory
- context and permissions shared across AIs
- AI products that improve thinking instead of replacing it
- production-grade Agent Runtime architecture
- turning messy real systems into clear product abstractions
