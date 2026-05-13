# READ ME

## How to use

- Source folder is legalDocumentDraft
- Copy documents in legalDocumentDraft/legalDocs folder
- File name should exactly match.
- Create a .env file
- Add GOOGLE_GEMINI_API_KEY=YOUR KEY
- Run command python legal_document_draft.py

## Current Architecture

### Memory

- This AI agent use simple procedural memory.
- After every edit by user, agent compare and summarize the change suggested by user.
- Agent add this summery at the end of the system prompt to be used from next turn.

### Model

- This agent use gemini-2.5-flash, as this one of the free models

### Assumptions

- This agent parse one file at a time.

### Evaluation Mode

- Agent depends on end users edit for evaluation.

## Architecture improvement suggestions

### Memory

- Semantic memory : Keep every document and their final drafts in a vector database. Agent functionality then can be extended to query about documents.

- Episodic memory : Add document noise level detection either deterministically or using LLM. If document exceeds certain threshold, fetch similar  documents and draft from vector db and add as examples(few shot prompting).

- Procedural memory (upgrade) : Instead of edit summery, add specific rule suggested by user as procedural memory. E.g: date format, legal definition, law etc.

- User profile memory : Basic user information to improve user experience

- Organization memory : To keep organization wide rules.

### Model

- Use langchain or similar to abstract specific model.
- Use memory tools to save various memories.
- Add router to route between various models. Use low cost model to determine file noise and route to appropriate higher models.

### Functionality

- Allow multiple similar file parse.
- Check if file already parsed using a traditional database.

### Context management

- When using multiple files: Upload one by one and create shorter document.Extract structured data, discard formatting, preserve substantive content. Combine them to create draft. If documents has natural hierarchy use that.

- When in user edit mode: Use compression method.

### Evaluation

- Force agent to ground every line in draft to a portion of original document.


## Sample Document Source

- https://www.reddit.com/r/MachineLearning/comments/j5yt90/n_highquality_legal_nlp_dataset/