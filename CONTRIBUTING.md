# Contributing to Books Dashboard

Thank you for your interest in contributing! Here's how you can help:

## 🐛 Reporting Issues

Found a bug? Please create an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

## 💡 Suggesting Improvements

Have an idea? Open an issue with the `enhancement` label and describe:

- The feature or improvement
- Why it would be useful
- Possible implementation approach

## 🔧 Making Changes

### Setup Development Environment

```bash
git clone https://github.com/yourusername/books-dashboard.git
cd books-dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Development Workflow

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**: Keep commits focused and descriptive

3. **Test your changes**
```bash
streamlit run main.py
```

4. **Push and create a Pull Request**
```bash
git push origin feature/your-feature-name
```

## ✅ Pull Request Guidelines

- Use clear, descriptive titles
- Reference related issues
- Describe the changes and why they're needed
- Keep changes focused on a single feature/fix
- Test thoroughly before submitting

## 📋 Code Style

- Follow PEP 8 conventions
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and modular

## 📚 Documentation

If your changes affect functionality:

- Update the README if needed
- Add docstrings to new functions
- Include usage examples

## ❓ Questions?

Open an issue with the `question` label or reach out to the maintainers.

---

**Thank you for contributing!** 🎉
