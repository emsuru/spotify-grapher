# GrooveGrapher Planning

## Vision
Create a delightful, privacy-first platform where music lovers can explore their Spotify listening patterns through beautiful visualizations and share insights with friends, turning personal data into playful discoveries about musical identity.

## Goals
- [ ] Build a secure web app for uploading and analyzing Spotify data exports
- [ ] Create shareable, beautiful visualizations that spark conversation
- [ ] Add social features for comparing musical tastes with friends
- [ ] Implement discovery features to find patterns and recommendations
- [ ] Support both quick (1-year) and full lifetime Spotify exports

## Tech Stack

### Core Stack (from template)
- **Backend**: Python (FastAPI)
- **Frontend**: JavaScript/TypeScript (Node.js)
- **Database**: SQLite for local dev, PostgreSQL for production
- **Authentication**: Supabase auth with Google OAuth and JWT tokens
- **Deployment**: Docker + GitHub Actions CI/CD

### Additional Libraries
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib (backend), D3.js/Chart.js (frontend)
- **File Handling**: zipfile, json
- **Async Processing**: Celery for large file processing

## Architecture Decisions

### Data Processing Pipeline
- Upload handler validates and extracts zip files
- Background job processes JSON files into normalized format
- Results cached in database with user association
- Visualization endpoints serve pre-computed aggregations

### Privacy First
- All processing happens server-side, no data sent to third parties
- Users can delete all their data with one click
- Optional anonymous mode for sharing visualizations
- Data retention policy: 30 days unless user opts for permanent storage

### Observability
- Structured logging with correlation IDs
- OpenTelemetry for tracing with wrapper functions
- Processing time metrics for optimization
- Error tracking for failed uploads/processing

### Testing Strategy
- Unit tests for all data processing functions
- Integration tests for upload/visualization flow
- Mock Spotify data fixtures for consistent testing
- Property-based testing for edge cases
- Minimum 80% coverage

### Error Handling
- Custom exception classes for data validation
- Graceful handling of malformed Spotify exports
- User-friendly error messages for common issues
- Centralized error handler
- Never expose internal errors or file paths to users

## Conventions

### Git
- Branch naming: `feature/description`, `fix/description`
- Commit messages: `type: description` (feat, fix, docs, chore)
- PR template with checklist
- Squash merge to main

### Code Style
- Type hints everywhere (mypy strict mode)
- Docstrings for public functions
- Max line length: 88 (Black default)
- Imports sorted with isort
- Frontend: Prettier + ESLint

### API Naming
- Resources: plural nouns (`/uploads`, `/visualizations`)
- Actions: verbs (`/uploads/{id}/process`)
- Query params: snake_case
- Response fields: snake_case

### Data Schema
- Consistent timestamp fields: `created_at`, `updated_at`
- UUID primary keys for user-generated content
- Soft deletes with `deleted_at` field
- JSON columns for flexible metadata

## Security Considerations
- [ ] File upload validation (size, type, content)
- [ ] Zip bomb protection
- [ ] SQL injection prevention via ORM
- [ ] XSS prevention in visualization sharing
- [ ] Rate limiting on uploads (5 per hour per user)
- [ ] Secrets in environment variables
- [ ] CORS properly configured
- [ ] Content Security Policy headers

## Performance Targets
- Upload processing: < 10s for 1-year export
- Visualization generation: < 500ms
- API response time: < 200ms (p95)
- Database queries: < 50ms
- Docker image size: < 500MB
- Memory usage: < 512MB per container
- Max file upload size: 100MB

## Feature Roadmap

### Phase 1: Core Features
- File upload and validation
- Basic visualizations (top artists, tracks, listening patterns)
- User accounts and data management

### Phase 2: Social Features
- Shareable visualization links
- Friend comparisons
- Musical compatibility scores

### Phase 3: Intelligence
- Listening pattern insights
- Mood detection from playlists
- Personalized discoveries based on gaps in listening

### Phase 4: Extended Platform Support
- Apple Music import
- Last.fm integration
- YouTube Music support

---
**Note to AI**: This document defines our architecture. Always follow these patterns when implementing features. Reference the examples/ folder for core data processing patterns.