# Free model catalog

Free models are served by the OpenCode Console through the `opencode` provider.
They are limited-time offers and require an OpenCode account (`/connect`). Check
`/models` for what is enabled in your account and region.

## Orchestrator

| Model | ID | Context | Output | Notes |
|---|---|---|---|---|
| DeepSeek V4.1 Flash Free | `opencode/deepseek-v4.1-flash-free` | 200K | 32K | Default lead. Reasoning and tool use. |

The free tier is smaller than the paid variant (1M context, 384K output). Write
plans to disk and read short summaries instead of holding everything in one
context.

## Workers

| Model | ID | Context | Output | Role |
|---|---|---|---|---|
| GLM-5.3-Flash Free | `opencode/glm-5.3-flash-free` | 200K | 32K | Review, structured output |
| MiniMax M3.1 Flash Free | `opencode/minimax-m3.1-flash-free` | 1M | 512K | Large-context reading |
| Step 5 Preview Free | `opencode/step-5-preview-free` | 1M | 65K | Implementation |
| LongCat 2.5 Free | `opencode/longcat-2.5-free` | 1M | 262K | Large files (100 req/day) |
| MiMo-V2.6-Flash Free | `opencode/mimo-v2.6-flash-free` | 200K | 32K | Implementation |
| DeepSeek V4 Flash Free | `opencode/deepseek-v4-flash-free` | 200K | 128K | Second opinion, long output |
| Nemotron 3.5 Super VL Free | `opencode/nemotron-3.5-super-vl-free` | 1M | 131K | Vision |

## Notable extras

| Model | ID | Context | Output | Why it is interesting |
|---|---|---|---|---|
| Space Bunny Free | `opencode/space-bunny-free` | 1M | 512K | Largest free output window |
| Crouton Alpha Free | `opencode/crouton-alpha-free` | 1M | 270K | Long output at 1M context |
| Ox Alpha Free (Unlimited) | `opencode/x-preview-f-free` | 1M | 131K | Advertised as unlimited |
| Nemotron 3.5 Lightning Free | `opencode/nemotron-3.5-lightning-free` | 262K | 262K | Output equals context |
| Kimi K2.5 Free | `opencode/kimi-k2.5-free` | 262K | 262K | Symmetric window |
| Qwen3.6 Plus Free | `opencode/qwen3.6-plus-free` | 262K | 65K | General |
| Nemotron 3 Ultra Free | `opencode/nemotron-3-ultra-free` | 1M | 128K | General |
| Beam Free | `opencode/beam-free` | 1M | 131K | General |
| Flint 40B Free | `opencode/flint-40b-free` | 262K | 65K | Small and fast |
| Iceman Free | `opencode/iceman-free` | 262K | 131K | Stealth, no public model page |
| Big Pickle | `opencode/big-pickle` | 200K | 32K | Stealth, no `-free` suffix |
| Grok Code Fast 1 | `opencode/grok-code` | 256K | 256K | Stealth, no `-free` suffix |
| Inkling 2 Small Free | `opencode/inkling-2-small-free` | 1M | 131K | Region limits may apply |
| MiniMax M3 Free | `opencode/minimax-m3-free` | 200K | 32K | Smaller MiniMax |
| Laguna S 2.1 Free | `opencode/laguna-s-2.1-free` | 256K | 32K | Coding |
| MiMo V2 Pro Free | `opencode/mimo-v2-pro-free` | 1M | 64K | Coding at 1M context |

## Selection guide

- **Reading / mapping:** MiniMax M3.1 Flash Free, Space Bunny Free, or LongCat 2.5
  Free (1M context).
- **Implementation:** Step 5 Preview Free or MiMo-V2.6-Flash Free.
- **Review / tests:** GLM-5.3-Flash Free.
- **Huge single output:** Space Bunny Free (512K) or Crouton Alpha Free (270K).
- **Large files with a request budget:** LongCat 2.5 Free, but watch the 100
  requests/day limit.
- **Vision:** Nemotron 3.5 Super VL Free.

## Privacy

Free tiers trade price for data. Retention and training terms differ per model
and change without notice, so treat this list as a starting point, not a
guarantee. For client code, check the provider's current terms and prefer the
models your own policy allows. When in doubt, assume the prompt may be retained
and do not send secrets.

## Keeping this list current

The catalog is generated from <https://models.dev/api.json> (provider
`opencode`, zero-cost models). Use the script to print the live list:

```bash
python skills/free-orchestrate/scripts/check-free-models.py --catalog
```

Free offers disappear and new ones appear without notice, so run this before
choosing a roster. Also check `/models` in OpenCode, which reflects what your
account can actually use right now. Always have a fallback model in mind.

## Notes

- Do not set `OPENCODE_DISABLE_FREE_MODELS=1`; it hides the free tier.
- Some free models have no `-free` suffix (`big-pickle`, `grok-code`). The
  validator accepts them explicitly.
- Free models are the *only* models this skill may use. If none of the roster is
  available, stop and tell the user instead of falling back to a paid model.
