# KoboQuotes to LLM Synthesis

A small personal tool to generate dense book summaries from your Kobo highlights using LLMs.

## Overview

This tool takes your exported Kobo highlights, processes them through an LLM (Large Language Model), and generates a structured markdown summary including:
- Context
- Main thesis and arguments
- Key points

## How to Use

*This script relies on OpenRouter for LLM calls, make sure to have your API key in env.*

1. **Export your Kobo highlights**
   - Connect your Kobo device.
   - Extract highlights using [this method](https://gist.github.com/samuelsmal/0f0b7a87fbbfe4798cb572bbf1394de4).
   - Save the exported text file.

2. **Process highlights**
   - Place your exported highlights in the `quote_folder` directory.
   - Run the script:
     ```bash
     uv run main.py --file_name <YOUR_FILENAME_WITHOUT_ITS_EXTENSION>  --model <THE_MODEL_YOU_WANNA_USE> # or --all
     ```


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
