# Changed Files ESLint Gate

## Goal

After every AI code modification, run ESLint only on the files changed by the current task.

This prevents common post-migration issues:

- unused imports
- no-unused-vars
- no-undef
- invalid Vue template syntax
- TypeScript parser lint issues
- formatting conflicts with local root config

## Project root

```text
/Users/lizhenwei/workspace/vueworkspace/bairong/asset-cube-html
```

The project root has lint-related configuration files such as:

```text
.browserslistrc
.editorconfig
.eslintignore
.eslintrc.cjs
.eslintrc.js
.lintstagedrc
.prettierignore
.prettierrc
.prettierrc.json
.stylelintignore
.stylelintrc
.stylelintrc.json
```

## Required Rule

After each meaningful code change, run:

```bash
python3 scripts/check_changed_eslint.py
```

If the skill is installed inside the project:

```bash
python3 .agents/skills/component-refactor/scripts/check_changed_eslint.py
```

If the changed files are known:

```bash
python3 scripts/check_changed_eslint.py \
  --files src/views/foo/page2/index.vue src/router/modules/foo2.js
```

## Fixing ESLint Issues

If ESLint fails:

1. read the lint output;
2. fix only the reported files;
3. do not modify business logic;
4. rerun changed-files ESLint;
5. repeat until pass.

Optional auto-fix:

```bash
python3 scripts/check_changed_eslint.py --fix
```

Use `--fix` only for safe formatting/import/order issues. If auto-fix touches logic, inspect the diff.

## Acceptance Requirement

A Page2 migration is not accepted until:

- changed-files ESLint passes;
- lint output is included in the final report;
- any remaining lint failure is explicitly documented as a blocker or exception.