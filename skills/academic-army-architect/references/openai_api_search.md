# OpenAI API Search Implementation

Use `scripts/openai_web_search.py` for every mandatory search pass in the Academic Army Architect workflow. The script calls the OpenAI Responses API with the `web_search` tool, uses `tool_choice="required"` by default, and emits normalized JSON for `paper_blueprint_analysis.md` and `source_ledger.json`.

## Requirements

- Python 3.10+
- `pip install openai`
- `OPENAI_API_KEY` set in the environment

## Basic usage

```powershell
python scripts/openai_web_search.py `
  --search-id S1 `
  --purpose related_paper_search `
  --query "LLM assisted literature review systems evaluation benchmark" `
  --context-file .\intake.md `
  --output .\search_S1.json
```

## Venue search

```powershell
python scripts/openai_web_search.py `
  --search-id S3 `
  --purpose venue_search `
  --query "CHI 2026 author guide review criteria papers" `
  --allowed-domain chi2026.acm.org `
  --allowed-domain dl.acm.org `
  --output .\search_S3.json
```

## Domain guidance

Choose domains by discipline instead of hard-coding one global list.

- CS / AI: `arxiv.org`, `openreview.net`, `aclanthology.org`, `dl.acm.org`, `ieeexplore.ieee.org`, `github.com`, `paperswithcode.com`, `semanticscholar.org`
- Medicine / life sciences: `pubmed.ncbi.nlm.nih.gov`, `clinicaltrials.gov`, `nature.com`, `science.org`, `cell.com`, `nejm.org`, `thelancet.com`
- Social sciences / humanities: official venue pages, DOI pages, publisher pages, SSRN, and field-specific archives

## Output contract

The script returns normalized JSON with:

- `search_id`, `purpose`, `query`, `date`, `model`
- `result.search_summary`
- `result.sources_consulted[]`
- `result.positioning_notes[]`
- `result.missing_information[]`
- `result.suggested_followup_queries[]`
- `api_sources[]` from the Responses API response where available

Copy `sources_consulted` into the analysis file and summarize the search in `source_ledger.json`. Do not use a source in the blueprint unless it appears in one of those two places.