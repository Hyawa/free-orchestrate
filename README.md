# free-orchestrate

An [OpenCode](https://opencode.ai) skill that orchestrates coding work across
**free models only**, with **DeepSeek V4.1 Flash Free** as the lead
planner/integrator.

[![skills.sh](https://skills.sh/b/Hyawa/free-orchestrate)](https://skills.sh/Hyawa/free-orchestrate)

## What it does

- Keeps a free model as the orchestrator: it plans, decomposes, delegates, and
  integrates.
- Delegates bounded units to other free models for reading, writing, and review.
- Integrates only evidence-backed results (diffs, tests, verification).
- Ships with playbooks, a briefing template, a model catalog, and a config
  checker.

## Install

### With the skills CLI

```bash
npx skills add Hyawa/free-orchestrate --skill free-orchestrate -a opencode
```

Replace `Hyawa` with your own owner only if you install from a fork. The CLI
installs the skill to `.agents/skills/free-orchestrate/` in the current project.
Add `-g` to install it globally for your OpenCode user.

### With OpenCode manually

Copy `skills/free-orchestrate` into your project's `.opencode/skills/` (or
`.agents/skills/`) directory, or point the `skills` config at it:

```jsonc
{
  "skills": ["./skills/free-orchestrate"]
}
```

### Requirements

- An OpenCode account (the free models are served by the OpenCode Console).
  Run `/connect` and sign in.
- Do not set `OPENCODE_DISABLE_FREE_MODELS=1`; it hides the free models.

## Usage

1. Copy `opencode.jsonc.example` to `opencode.jsonc` in your project.
2. Check the models available in your account with `/models`.
3. Ask the agent to orchestrate a task, for example:

   ```text
   Orchestrate the migration of the billing endpoints to v2
   ```

4. The orchestrator decomposes the work, launches free workers, and reports.

## Files

```text
skills/free-orchestrate/
├── SKILL.md                       # orchestration instructions
├── references/
│   ├── models.md                  # free model catalog and selection guide
│   ├── playbooks.md               # reusable orchestration patterns
│   ├── briefing-template.md       # worker briefing template
│   ├── opencode.jsonc.example     # same config as the repository root
│   └── pt-BR.md                   # Portuguese quick reference
└── scripts/
    └── check-free-models.py       # verify a config uses only free models
opencode.jsonc.example             # companion OpenCode config
```

The config example exists twice on purpose: the root copy is for people who
clone the repository, and the `references/` copy ships with the skill when it is
installed through the skills CLI. Keep both in sync.

## Verify the config stays free

```bash
python skills/free-orchestrate/scripts/check-free-models.py opencode.jsonc
python skills/free-orchestrate/scripts/check-free-models.py --catalog
```

The first command parses JSONC, collects the root `model` and every
`agents.*.model`, and exits with status `1` if any of them is not a free
`opencode/*` model. The second prints the live free catalog from models.dev, so
you can pick a replacement when an offer disappears.

## Privacy

Free tiers trade price for data. Retention and training terms differ per model
and change without notice. For client code, check the current terms and prefer
the models your policy allows. When in doubt, assume the prompt may be retained
and do not send secrets. See `references/models.md`.

## Contributing

Open an issue or pull request. Keep the skill free-only: do not add paid models
to the default roster.

## License

MIT. See [LICENSE](LICENSE).

---

# free-orchestrate (Português)

Uma skill do [OpenCode](https://opencode.ai) que orquestra trabalho de
programação usando **apenas modelos gratuitos**, com o **DeepSeek V4.1 Flash
Free** como orquestrador principal.

## O que faz

- Mantém um modelo free como orquestrador: ele planeja, decompõe, delega e
  integra.
- Delega unidades delimitadas para outros modelos free de leitura, escrita e
  revisão.
- Integra apenas resultados com evidência (diffs, testes, verificação).
- Vem com playbooks, template de briefing, catálogo de modelos e verificador
  de config.

## Instalação

### Com o skills CLI

```bash
npx skills add Hyawa/free-orchestrate --skill free-orchestrate -a opencode
```

Substitua `Hyawa` pelo seu próprio owner apenas se instalar a partir de um fork.
O CLI instala a skill em `.agents/skills/free-orchestrate/` no projeto atual. Use
`-g` para instalar globalmente para o seu usuário do OpenCode.

### Com o OpenCode manualmente

Copie `skills/free-orchestrate` para `.opencode/skills/` (ou
`.agents/skills/`) no seu projeto, ou aponte o config `skills` para ele:

```jsonc
{
  "skills": ["./skills/free-orchestrate"]
}
```

### Requisitos

- Conta no OpenCode (os modelos free são servidos pela Console do OpenCode).
  Rode `/connect` e entre.
- Não defina `OPENCODE_DISABLE_FREE_MODELS=1`; isso esconde os modelos free.

## Uso

1. Copie `opencode.jsonc.example` para `opencode.jsonc` no seu projeto.
2. Confira os modelos disponíveis na sua conta com `/models`.
3. Peça para o agente orquestrar uma tarefa, por exemplo:

   ```text
   Orquestre a migração dos endpoints de billing para v2
   ```

## Verificação

```bash
python skills/free-orchestrate/scripts/check-free-models.py opencode.jsonc
python skills/free-orchestrate/scripts/check-free-models.py --catalog
```

O primeiro comando lê o `model` raiz e todos os `agents.*.model` e retorna `1` se
algum não for um modelo free do provider `opencode`. O segundo imprime o catálogo
free ao vivo, útil quando uma oferta some.

## Privacidade

Os modelos free trocam preço por dados. Regras de retenção e treino variam por
modelo e mudam sem aviso. Para código de clientes, confira os termos atuais e
prefira os modelos que a sua política permite. Na dúvida, assuma que o prompt
pode ser retido e não envie segredos. Veja `references/models.md`.

## Contribuição

Abra uma issue ou pull request. Mantenha a skill free-only: não adicione
modelos pagos ao time padrão.

## Licença

MIT. Veja [LICENSE](LICENSE).
