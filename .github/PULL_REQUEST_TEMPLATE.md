## Description
Summary of the changes introduced by this PR.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature or tweak addition
- [ ] Documentation update
- [ ] Code cleanup / refactoring

## Verification & Testing
- [ ] All unit tests pass locally (`python -m pytest tests/`).
- [ ] Tested non-destructive execution with `--dry-run`.
- [ ] Verified non-admin behavior handles privileges gracefully.

## Safety Check
- [ ] Changes do NOT modify protected system services (`RpcSs`, `EventLog`, `WinDefend`, etc.).
- [ ] All new registry or service modifications include full rollback definitions.
