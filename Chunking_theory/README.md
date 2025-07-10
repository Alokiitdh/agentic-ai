
# 📚 Chunking Theory in LangChain

Chunking refers to splitting large documents into smaller pieces (chunks) to process them efficiently in downstream applications such as Retrieval-Augmented Generation (RAG), document search, QA systems, etc.

LangChain provides multiple strategies to handle chunking intelligently.

---

## 🔸 Types of Chunking Strategies

We will use **LangChain** for the following chunking types:

1. **Character Text Splitter:**
   Splits documents based on chunk size and overlap. A basic method with no semantic understanding.

2. **Recursive Character Text Splitter:**
   Similar to the character splitter but adds intelligent splitting using newlines (`\n`) and other separators to avoid splitting in the middle of sentences/words unless necessary.

3. **Document-Specific Splitter:**
   Custom splitting based on the document type. For example:
   - Markdown files → split by `#`, `##`, `###` headings.
   - Python files → split based on function/class boundaries.
   - Other formats can have their own custom logic.

4. **Semantic Chunking:**
   Uses **embeddings** to create semantically meaningful chunks rather than fixed-size spans. Ensures each chunk carries a complete idea or topic.

---

## 1️⃣ Character Text Splitter

### ✳️ Overview

This is the simplest type of chunking and comes in two variations:

- **Token-based**
- **Character-based**

Both require a separator like `\n` for proper chunking. If not provided, the entire document may be treated as a single chunk.

---

### 🔹 Token-Based Chunking

- **How it splits:** Uses a tokenizer like `tiktoken` to count tokens.
- **Chunk size is measured by:** Number of tokens.
- **Useful when:** Working with LLMs (e.g., OpenAI models) which have token limits.
- **Separator:** Usually `\n`.

```python
# Example: Using tiktoken for token counting
import tiktoken
encoding = tiktoken.get_encoding("cl100k_base")
tokens = encoding.encode("Your text here")

```

* * * * *

### 🔹 Character-Based Chunking

-   **How it splits:** Based on a character sequence. Defaults to `\n\n`.

-   **Chunk size is measured by:** Number of characters.

-   **Separator:** By default `\n\n`.

**How to use:**

-   To get raw string chunks → use `.split_text()`

-   To get LangChain `Document` objects → use `.create_documents()`

```
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(your_document)

```

* * * * *

2️⃣ Recursive Character Text Splitter
-------------------------------------

### ✳️ Overview

Recommended for general-purpose text. It recursively tries to split based on a **list of separators** until chunks are of acceptable size.

-   **Default split priority:** `["\n\n", "\n", " ", ""]`

-   **Goal:** Preserve paragraphs → sentences → words as long as possible.

-   **Chunk size is measured by:** Number of characters.

**How it works:**

1.  Attempts to split by double newlines `\n\n` (paragraphs)

2.  Then single newlines `\n` (lines)

3.  Then spaces `" "` (words)

4.  Finally as last resort, character-level splitting

```
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

chunks = splitter.split_text(your_document)

```

* * * * *

3️⃣ Document-Specific Splitter
------------------------------

### ✳️ Overview

These splitters are **customized** to the type of document. They ensure logical boundaries are respected.

-   **Markdown Files:**\
    Split by headings like `#`, `##`, `###`.

-   **Python Files:**\
    Respects code structure --- splits by **function** and **class** blocks.

-   **Other Formats:**\
    Tailor splitting rules according to the document's structure.

**Benefits:**

-   Maintains logical grouping

-   Context-aware chunking

-   Avoids breaking syntactic units

```
# Example: MarkdownSplitter (coming soon / custom logic)

```

* * * * *

4️⃣ Semantic Chunking
---------------------

### ✳️ Overview

Instead of splitting by size, semantic chunking splits by **meaning** using **embeddings**. Ideal when chunks must capture entire concepts or topics.

### 🧠 How It Works:

1.  **Split text into sentences**

2.  **Group sentences** into small batches (e.g., 3 sentences each)

3.  **Compute embeddings** for each group

4.  **Compare embeddings** and merge semantically similar groups

5.  **Result:** Meaningful, topic-coherent chunks

```
# Pseudocode only --- actual implementations use embedding models
sentences = split_into_sentences(text)
groups = group_sentences(sentences, n=3)
embeddings = compute_embeddings(groups)
semantic_chunks = merge_similar_groups(embeddings)

```

### ✅ Key Benefits

-   Semantic coherence

-   Ideal for vector search & LLM applications

-   Avoids splitting meaningful ideas across chunks

* * * * *

📝 Summary
----------

| Splitter Type | Based On | Best Use Case | Preserves Meaning? |
| --- | --- | --- | --- |
| Character Text Splitter | Fixed character count | Simple, predictable chunking | ❌ |
| Token-Based Splitter | Fixed token count | Token-sensitive models (OpenAI, etc.) | ❌ |
| Recursive Text Splitter | Paragraph → word level | General text, balanced context and size | ⚠️ Partial |
| Document Specific Splitter | Doc structure (e.g., markdown) | Code, structured files, technical docs | ✅ |
| Semantic Chunking | Embedding similarity | High-quality semantic retrieval, RAG | ✅✅ |

* * * * *

> 🧠 **Tip:** For best results, combine **recursive** or **document-aware** chunking with **semantic retrieval** in production LLM pipelines.


```