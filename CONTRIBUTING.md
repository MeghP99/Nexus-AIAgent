# Contributing to Agentic Research Assistant

Thank you for your interest in contributing to the Agentic Research Assistant! This document provides guidelines for contributing to this project.

## 🎯 Project Vision

This project aims to showcase advanced AI agent architecture with production-ready code quality. All contributions should align with these principles:

- **Clean Architecture**: Maintain separation of concerns and modular design
- **Type Safety**: Use comprehensive type annotations
- **Documentation**: Provide clear docstrings and comments
- **Testing**: Include appropriate test coverage
- **Performance**: Optimize for efficiency and scalability

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (venv, conda, etc.)

### Local Development
```bash
# Fork and clone the repository
git clone https://github.com/your-username/agentic-research-assistant.git
cd agentic-research-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
streamlit run app.py
```

## 📋 Contribution Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Include comprehensive docstrings for all public methods
- Maintain consistent naming conventions

### Architecture Principles
- **Single Responsibility**: Each class should have one reason to change
- **Dependency Injection**: Use dependency injection for testability
- **Interface Segregation**: Prefer small, focused interfaces
- **Open/Closed**: Open for extension, closed for modification

### Adding New Tools
To add a new tool to the agent:

1. **Create Tool Class**: Inherit from `BaseTool`
```python
from src.tools.base_tool import BaseTool

class NewTool(BaseTool):
    def _get_name(self) -> str:
        return "new_tool"
    
    def _get_description(self) -> str:
        return "Description of what this tool does"
    
    def _check_availability(self) -> bool:
        # Check if tool is properly configured
        return True
    
    def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        # Implement tool logic
        pass
```

2. **Register Tool**: Add to `ToolManager` in `src/agent/tool_manager.py`
3. **Update Prompts**: Add tool description in `PromptManager`
4. **Add Tests**: Create comprehensive test cases
5. **Update Documentation**: Add tool documentation

### Testing
- Write unit tests for all new functionality
- Include integration tests for tool interactions
- Ensure all tests pass before submitting PR
- Aim for high test coverage (>80%)

### Documentation
- Update README.md for significant features
- Add docstrings for all public methods
- Include type hints and parameter descriptions
- Update ARCHITECTURE.md for structural changes

## 🔄 Pull Request Process

### Before Submitting
1. **Fork** the repository
2. **Create branch** from main: `git checkout -b feature/your-feature-name`
3. **Make changes** following the guidelines above
4. **Test thoroughly** - ensure all tests pass
5. **Update documentation** as needed
6. **Commit** with clear, descriptive messages

### PR Requirements
- **Clear Title**: Descriptive title explaining the change
- **Detailed Description**: Explain what changes were made and why
- **Testing**: Describe how the changes were tested
- **Documentation**: Confirm documentation is updated
- **No Breaking Changes**: Unless absolutely necessary and well-documented

### Review Process
1. Automated checks must pass (linting, tests)
2. Code review by maintainers
3. Address any feedback or requested changes
4. Final approval and merge

## 🐛 Bug Reports

### Before Reporting
- Check existing issues for duplicates
- Ensure you're using the latest version
- Test with minimal configuration

### Bug Report Template
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- Python version:
- OS:
- Browser (if applicable):
- API keys configured:

**Additional Context**
Screenshots, logs, or other helpful information
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other solutions you considered

**Additional Context**
Any other relevant information
```

## 🎨 Design Principles

### UI/UX Guidelines
- **Responsive Design**: Support all screen sizes
- **Accessibility**: Follow WCAG guidelines
- **Performance**: Optimize for fast loading
- **Intuitive**: Self-explanatory interface

### Code Organization
```
src/
├── tools/          # Tool implementations
├── agent/          # Agent logic and coordination
├── ui/             # User interface components
├── retrievers/     # Legacy retriever classes
└── __init__.py
```

## 📊 Performance Considerations

- **Async Operations**: Use async/await for I/O operations
- **Caching**: Implement appropriate caching strategies
- **Error Handling**: Graceful error handling and recovery
- **Monitoring**: Include logging for debugging and monitoring

## 🔒 Security Guidelines

- **API Keys**: Never commit API keys or secrets
- **Input Validation**: Validate all user inputs
- **Error Messages**: Don't expose sensitive information in errors
- **Dependencies**: Keep dependencies updated and secure

## 📈 Metrics and Quality

### Code Quality Metrics
- **Type Coverage**: >95% type annotations
- **Test Coverage**: >80% line coverage
- **Complexity**: Keep cyclomatic complexity low
- **Documentation**: Comprehensive docstrings

### Performance Metrics
- **Response Time**: <3 seconds for typical queries
- **Memory Usage**: Efficient memory management
- **Error Rate**: <1% error rate in production
- **Availability**: >99% uptime

## 🤝 Community

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions and reviews

### Recognition
Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special mention for outstanding contributions

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make the Agentic Research Assistant better! 🚀
