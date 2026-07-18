# Contributing to AI Market Trend Analyzer

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/forex_stats.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Push to your fork: `git push origin feature/your-feature`
6. Submit a Pull Request

## Development Setup

```bash
# Clone and setup
git clone https://github.com/chellamani777/forex_stats.git
cd forex_stats
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Configure pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## Code Style

### Formatting
```bash
black .
```

### Linting
```bash
flake8 . --max-line-length=100
```

### Type Checking
```bash
mypy .
```

## Commit Messages

Follow conventional commits:

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
refactor: Refactor code
test: Add tests
chore: Maintenance
```

## Pull Request Process

1. Update documentation if needed
2. Add/update tests
3. Ensure all tests pass: `pytest`
4. Update CHANGELOG.md
5. Fill out PR template

## Testing

### Run all tests
```bash
pytest
```

### Run specific tests
```bash
pytest tests/unit/test_indicators.py
```

### Coverage report
```bash
pytest --cov=core --cov-report=html
```

## Documentation

- Add docstrings to all functions
- Use type hints
- Update README if user-facing changes
- Add examples for new features

## Issues

### Reporting Bugs
1. Check if issue already exists
2. Provide reproducible example
3. Include Python version and OS
4. Attach error logs

### Feature Requests
1. Check existing issues/discussions
2. Describe use case clearly
3. Explain expected behavior
4. Provide examples

## Code Review

- Review is collaborative
- Be respectful and constructive
- Ask questions if unclear
- Approve once satisfied

## Questions?

- GitHub Discussions
- GitHub Issues
- Email: support@example.com

## License

By contributing, you agree that your contributions will be licensed under MIT License.

Thanks for contributing! 🎉
