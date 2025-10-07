# Contributing to PiRhoAI MSME Analytics MVP

Thank you for your interest in contributing to PiRhoAI! This document provides guidelines and information for contributors.

## 🚀 Ways to Contribute

- **Report Bugs**: Found an issue? Open an issue with clear details
- **Suggest Features**: Have an idea? Start a discussion or create a feature request
- **Write Code**: Fix bugs, implement features, or improve documentation
- **Improve Documentation**: Help make our docs better and clearer
- **Test**: Help test new features and report your findings

## 📝 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please be respectful and constructive in all interactions.

## 🐛 Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Provide clear reproduction steps
4. Include relevant system information
5. Describe expected vs. actual behavior

## ✨ Suggesting Features

1. Check existing features and discussions
2. Open a feature request issue
3. Clearly describe the proposed feature
4. Explain how it benefits users
5. Consider implementation feasibility

## 🛠️ Development Setup

```bash
# Clone the repository
git clone https://github.com/dataaispark-spec/PiRhoAI.git
cd PiRhoAI

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

## 💻 Code Guidelines

### Python Standards
- Follow PEP 8 style guide
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Write clear commit messages

### Code Structure
- Place new modules in appropriate directories (`src/core/`, `src/data/`, etc.)
- Update requirements.txt if adding dependencies
- Add unit tests for new functionality when possible

### Pull Requests
1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Add/change tests as needed
5. Ensure all tests pass
6. Update documentation if needed
7. Submit a pull request with clear description

## 📋 Testing

Run tests using pytest:
```bash
python -m pytest tests/
```

For Streamlit app testing, launch locally and verify functionality.

## 🎨 Documentation

- Update README.md for major changes
- Add inline comments for complex logic
- Update this contributing guide if processes change

## 🔒 Security

- Report security vulnerabilities via issues@pirhoai.ai
- Never commit sensitive information (API keys, passwords, etc.)
- Use environment variables for configuration

## 📞 Contact

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- General Questions: Create an issue with "question" label

Thank you for contributing to PiRhoAI! 🎉
