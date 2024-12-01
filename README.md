# KoboQuotes to LLM Synthesis

A small personal tool to generate comprehensive book summaries from your Kobo highlights using LLMs.

## Overview

This tool takes your exported Kobo highlights, processes them through an LLM (Large Language Model), and generates a structured markdown summary including:
- Context
- Main thesis and arguments
- Key points

Perfect for researchers, students, or avid readers who want to get more value from their reading notes.

## Dependencies

Currently uses a custom local LLM wrapper supporting OpenRouter API. Future versions will migrate to [ell](https://docs.ell.so/index.html) library.

## How to Use

1. **Export your Kobo highlights**
   - Connect your Kobo device.
   - Extract highlights using [this method](https://gist.github.com/samuelsmal/0f0b7a87fbbfe4798cb572bbf1394de4).
   - Save the exported text file.

2. **Process highlights**
   - Place your exported highlights in the `quote_folder` directory.
   - Run the script:
     ```bash
     python main.py
     ```
   - Enter the name of your quote file when prompted (without .txt).

3. **Get your synthesis**
   - Find your generated summary in the `note_folder` directory.
   - The summary will be in markdown format, ready to use in your note-taking system.

## Output Format

The generated summary follows a structured format:
```markdown
# Book Summary: [Title], by [Author], [Year]

### Context
[Historical and theoretical context]

### Thesis and Arguments
[Main ideas and supporting arguments]

### Key Points
- [Condensed insights]
