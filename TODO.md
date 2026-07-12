# TODOs

## 1. Human clarification

Give the agent a task with missing information that it cannot safely infer.

- [ ] Add an `ask_user(question)` tool.
- [ ] Suspend the agent run when the tool is called.
- [ ] Resume with the answer as the tool result without repeating completed work.
- [ ] Keep clarification separate from approval for mutating actions.

**Done:** The agent asks for missing information and continues the same run after the user responds.

## 2. Irreversible actions

Add `delete_file(path)` and request a project cleanup.

- [ ] Classify tools as read-only or mutating.
- [ ] Show a dry-run plan before deletion.
- [ ] Require approval and log mutations.

**Done:** Nothing is deleted without explicit approval.

## 3. State and resumability

Terminate an agent mid-task, then restart it.

- [ ] Persist messages, results, status, and budget.
- [ ] Resume without repeating completed work.
- [ ] Make operations idempotent where possible.

**Done:** A resumed run produces the same result as an uninterrupted run.

## 4. MCP integration

Connect the agent to a filesystem or Playwright MCP server and complete a task using its tools.

- [ ] Configure and connect to an MCP server.
- [ ] Discover its available tools and expose their schemas to the model.
- [ ] Execute MCP tool calls and return their results to the agent loop.
- [ ] Handle connection failures, tool errors, and timeouts.
- [ ] Apply the same approval policy to mutating MCP tools.

**Done:** The agent discovers and safely uses tools provided by a filesystem or Playwright MCP server.
