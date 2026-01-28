# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for Phase 2
- Date range search functionality
- Return flight constraint checking
- Multiple data source integration (Amadeus, Kiwi)
- Result persistence to JSON files
- Price comparison across sources
- Command-line argument parsing

### Planned for Phase 3
- Automated monitoring via GitHub Actions
- Email alerts for price drops
- Historical price tracking
- Web dashboard (optional)

## [1.0.0] - 2026-01-28

### Added - Phase 1 POC
- Initial release of flight search POC
- Core search functionality using SerpApi (Google Flights)
- Custom constraint filtering:
  - Departure time window (07:30-18:00)
  - Arrival time window (08:00-21:00)
  - Maximum trip duration (12 hours)
  - Smart connection time checks (Schengen-aware)
- Multi-passenger pricing (Adult + Child)
- Price sorting (cheapest first)
- Setup verification script (test_setup.py)
- Configuration file support (config.ini)
- Comprehensive documentation:
  - README.md
  - QUICKSTART.md
  - PHASE1_SUMMARY.md
  - CONTRIBUTING.md
- Git repository structure
- MIT License

### Features
- Searches WRO → TLV/HFA routes
- Filters invalid connections automatically
- Warns about tight connections
- Displays top 10 results
- EUR currency support

### Technical
- Python 3.8+ support
- SerpApi integration
- Modular code structure
- Error handling for API failures
- Comprehensive code comments

### Documentation
- 5-minute quick start guide
- Full setup instructions
- Configuration examples
- Usage examples
- Troubleshooting section

## Project Milestones

### Phase 1: POC (✅ Complete - 2026-01-28)
- Core search and filtering functionality
- Single data source (SerpApi)
- Manual execution
- Basic output

### Phase 2: Enhanced Search (🔄 In Progress)
- Multiple data sources
- Automated date range searching
- Return flight logic
- Result persistence

### Phase 3: Automation (📋 Planned)
- Scheduled monitoring
- Price tracking
- Email alerts
- Historical analysis

---

## Version History Legend

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

[Unreleased]: https://github.com/YOUR_USERNAME/flight-search/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/YOUR_USERNAME/flight-search/releases/tag/v1.0.0
