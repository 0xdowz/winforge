# Contributing to WinForge

Thank you for considering contributing to **WinForge**! Community involvement helps keep this tool reliable, safe, and up to date.

---

## Code of Conduct

- Be respectful and constructive in all discussions, issues, and pull requests.
- Prioritize **user safety** above all else. Tweaks that can compromise Windows system stability or disable core security features will not be accepted.

---

## How to Contribute

### 1. Reporting Bugs
- Check existing GitHub Issues to avoid duplicate reports.
- Provide your OS version (Windows 10 / 11), exact CLI command used, and output log from `%LOCALAPPDATA%\WinForge\logs\winforge.log`.

### 2. Suggesting Tweaks
- Proposed tweaks must include:
  - Tweak ID and category.
  - Precise Win32 Registry key or Service name.
  - Risk rating (0–100) and justification.
  - Inverse rollback logic.

### 3. Submitting Pull Requests
1. Fork the repository and create a feature branch (`git checkout -b feature/new-tweak`).
2. Implement your changes following PEP 8 coding standards.
3. Add unit tests in `tests/` covering your changes.
4. Run full test suite:
   ```cmd
   python -m pytest tests/
   ```
5. Ensure 100% of unit tests pass before submitting your PR.
