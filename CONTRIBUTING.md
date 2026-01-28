# Contributing to Flight Search System

Thank you for your interest in contributing to this project!

## Project Goal

This is primarily a **personal project** for finding the best flight deals from Wrocław (WRO) to Israel (TLV/HFA) with specific constraints. However, suggestions and improvements are welcome.

## How to Contribute

### 1. Issues

If you find a bug or have a feature suggestion:

1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, OS)

### 2. Pull Requests

For code contributions:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   ```bash
   python test_setup.py
   python flight_search_poc.py
   ```
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: brief description of change"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create Pull Request**
   - Describe what you changed and why
   - Reference any related issues

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

### Example:

```python
def check_connection_time(layover: Dict, is_schengen_exit: bool) -> bool:
    """
    Check if connection time is sufficient
    
    Args:
        layover: Dictionary with connection details
        is_schengen_exit: Whether this connection exits Schengen
    
    Returns:
        True if connection time is sufficient, False otherwise
    """
    duration = layover.get('duration', 0)
    min_required = 120 if is_schengen_exit else 60
    return duration >= min_required
```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/flight-search-wro-israel.git
cd flight-search-wro-israel

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
export SERPAPI_KEY='your_test_key'

# Run tests
python test_setup.py
python flight_search_poc.py
```

## Areas for Contribution

### High Priority
- [ ] Support for additional data sources (Amadeus, Kiwi)
- [ ] Date range search optimization
- [ ] Return flight constraint logic
- [ ] Unit tests

### Medium Priority
- [ ] Better error handling
- [ ] Result caching
- [ ] Price history tracking
- [ ] Command-line argument parsing

### Low Priority
- [ ] Web interface
- [ ] Mobile app
- [ ] Additional airline integrations
- [ ] Graphical price trends

## Testing Guidelines

Before submitting a PR:

1. **Verify setup works**
   ```bash
   python test_setup.py
   ```

2. **Test with real searches**
   ```bash
   python flight_search_poc.py
   ```

3. **Compare with Google Flights**
   - Verify prices are accurate
   - Check constraints are applied correctly
   - Ensure no false positives/negatives

4. **Test edge cases**
   - No flights available
   - API errors
   - Invalid dates
   - Unusual time zones

## Documentation

If your contribution changes functionality:

- Update README.md
- Update code comments
- Update config.ini if needed
- Add examples in QUICKSTART.md

## Questions?

Open an issue for discussion before starting major work.

## License

By contributing, you agree your contributions will be licensed under the MIT License.

---

Thank you for helping improve this project! ✈️
