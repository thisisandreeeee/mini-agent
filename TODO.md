# TODOs

## 0. Chat-based agent workflow

Refactor the agent workflow from a single task run into an ongoing chat.

- [ ] Accept multiple user messages in the same conversation.
- [ ] Persist conversation history and tool results between turns.
- [ ] Let each assistant turn invoke tools before returning a response.
- [ ] Preserve context without repeating completed work.
- [ ] Support ending and resuming a conversation.

**Done:** A user can have a multi-turn conversation with the agent, including tool use, without starting a new task run for every message.

## 1. Human in the loop

Give the agent access to a tool whose use requires explicit human approval.

- [ ] Add a `requires_approval` property to tool definitions or tool calls.
- [ ] Suspend the agent workflow before executing a tool that requires approval.
- [ ] Show the proposed tool name, arguments, and expected impact to the user.
- [ ] Execute the tool only after approval and return its result to the conversation.
- [ ] Return a rejection result to the agent when approval is denied.
- [ ] Resume without repeating completed work and record the approval decision.

**Done:** Tools marked as requiring approval never execute without an explicit human decision, and the conversation continues correctly after approval or rejection.

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

## 5. Retrieval-augmented generation

Give the agent a question whose answer is contained in a collection of project documents.

- [ ] Split documents into chunks and create embeddings.
- [ ] Store and retrieve chunks by semantic similarity.
- [ ] Add the most relevant chunks to the model context.
- [ ] Cite the source document for each supported claim.
- [ ] Evaluate retrieval quality and handle questions without relevant evidence.

**Done:** The agent answers from retrieved evidence, cites its sources, and does not invent an answer when the documents are insufficient.
