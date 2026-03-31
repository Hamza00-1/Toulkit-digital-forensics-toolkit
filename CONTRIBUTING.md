# 🤝 Contributing to Aegis Forensics Suite

Thank you for your interest in contributing to **Aegis Forensics Suite**! This document outlines guidelines to help you contribute effectively.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

This project adheres to a simple principle: **be professional and respectful**. Contributors are expected to:

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the project

---

## How to Contribute

### Types of Contributions Welcome

| Type | Description |
|---|---|
| 🐛 **Bug Fixes** | Fix broken functionality or incorrect behavior |
| ✨ **New Forensic Engines** | Add new analysis modules following the existing pattern |
| 📖 **Documentation** | Improve README, docstrings, or in-code comments |
| 🧪 **Tests** | Expand the `test_toolkit.py` test suite |
| 🎨 **UI Improvements** | Enhance the desktop GUI or Flask web interface |
| ⚡ **Performance** | Optimize parsing, hashing, or carving speed |

---

## Development Setup

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/digital-forensics-toolkit.git
   cd digital-forensics-toolkit
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a new **feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## Coding Standards

- **Language:** Python 3.8+
- **Style:** Follow [PEP 8](https://pep8.org/) conventions
- **Docstrings:** All public functions must have descriptive docstrings (Google style preferred)
- **Module Pattern:** New forensic engines should expose a single primary function:
  ```python
  def your_engine(file_path: str) -> dict:
      """
      Brief description of what this engine does.
      
      Args:
          file_path (str): Path to the target file.
          
      Returns:
          dict: Results dictionary with standardized keys.
      """
  ```
- **Error Handling:** Always return `{"Error": "descriptive message"}` on failure — never raise unhandled exceptions to the GUI
- **Activity Logging:** Call `activity_tracker.log_activity(module_name, file, status)` after each forensic operation

---

## Pull Request Process

1. Ensure all existing tests pass: `python test_toolkit.py`
2. Add tests for any new functionality you introduce
3. Update `CHANGELOG.md` under `[Unreleased]` with a brief description of your changes
4. Submit your Pull Request with:
   - A clear title describing the change
   - A description of what was changed and why
   - Screenshots if the change affects the UI
5. A maintainer will review within 48 hours

---

## Reporting Issues

When reporting bugs, please include:

- **OS & Python version**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior / error message / stack trace**
- **Sample file** (if applicable and not sensitive)

Use the GitHub **Issues** tab to file a report.

---

*Thank you for helping make Aegis better!*
