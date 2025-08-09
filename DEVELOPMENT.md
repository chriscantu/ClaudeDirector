# ClaudeDirector Development Guide

## 🛠️ Development Workflow

### Performance Monitoring
Built-in strategic performance validation:
```bash
./claudedirector demo validate       # Quick strategic workflow validation
./claudedirector demo scenario       # Comprehensive director scenario testing
```

**Performance Targets:**
- Memory usage: <500MB (strategic data and AI caching)
- Query response: <200ms (database optimization with WAL mode)
- Full system validation: <30s (comprehensive workflow testing)

### Architecture Validation
```bash
# Check code quality
./claudedirector validate architecture

# Run comprehensive tests
./claudedirector test all

# Check performance benchmarks
./claudedirector benchmark
```

### Git Workflow Optimizations
Intelligent pre-commit hooks optimize development velocity:
```bash
./claudedirector git setup          # Intelligent git hooks
./claudedirector git commit -m "msg" # Optimized commits
```

**Smart Hook Features:**
- ⚡ **Markdown Skip**: No tests run for `.md` changes (docs)
- 🧠 **Intelligent Analysis**: Code complexity analysis for Python changes
- 📊 **Performance Impact**: Automated performance regression detection
- 🔍 **Strategic Validation**: Ensures director workflow compatibility

## 🏗️ Development Architecture

### Code Organization
```
lib/claudedirector/
├── core/                    # Core platform functionality
├── p0_features/            # P0 Strategic Metrics Framework
│   ├── domains/            # Business domain logic
│   └── shared/             # Shared infrastructure
├── memory/                 # Strategic intelligence storage
└── tools/                  # Development utilities
```

### Database Development
The platform uses a hybrid database architecture:
- **SQLite**: Primary storage with AI optimizations
- **DuckDB**: Analytics workloads (future)
- **Faiss**: Semantic search (future)

### Testing Strategy
```bash
# Unit tests
pytest lib/tests/

# Integration tests
pytest lib/tests/integration/

# Strategic workflow validation
./claudedirector demo scenario
```

## 🔧 Contributing

### Adding New Features
1. Create feature branch: `git checkout -b feature/your-feature`
2. Implement with tests: `pytest lib/tests/`
3. Validate architecture: `./claudedirector validate`
4. Test strategic workflows: `./claudedirector demo validate`

### Performance Optimization
- Target <200ms query response time
- Memory usage <500MB total
- Strategic validation <30s

### Code Quality
- Follow SOLID principles (enforced by pre-commit hooks)
- Maintain >90% test coverage
- Strategic persona compatibility required

---

**Note**: This guide is for ClaudeDirector platform developers. For end-user documentation, see the main [README.md](README.md).
