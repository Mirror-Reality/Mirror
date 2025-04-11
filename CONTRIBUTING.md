# Contributing Guide

## 1. Ways to Contribute

We welcome all forms of contributions, including but not limited to:

- Bug reports
- Feature suggestions
- Documentation improvements
- Code fixes
- New features
- Test improvements
- Discussion participation

## 2. Before You Start

Before contributing, please ensure:

1. Read the project's README.md
2. Check existing Issues and Pull Requests
3. Ensure your contribution aligns with project goals
4. Understand the project's code standards

## 3. Development Environment Setup

Please refer to the "Quick Start" section in README.md.

## 4. Code Standards

### 4.1 Backend (Python)
- Use Black for code formatting
- Use isort for import sorting
- Use flake8 for code checking
- Use mypy for type checking
- Follow PEP 8 standards

Example:
```python
from typing import List, Optional

def process_data(data: List[str], limit: Optional[int] = None) -> List[str]:
    """
    Process the given data with optional limit.
    
    Args:
        data: List of strings to process
        limit: Optional limit on number of items
        
    Returns:
        Processed list of strings
    """
    if limit is not None:
        data = data[:limit]
    return [item.upper() for item in data]
```

### 4.2 Frontend (TypeScript/React)
- Use Prettier for code formatting
- Use ESLint for code checking
- Use TypeScript for type checking
- Follow React best practices

Example:
```typescript
import React, { useState, useEffect } from 'react';

interface Props {
  initialCount: number;
  onCountChange: (count: number) => void;
}

export const Counter: React.FC<Props> = ({ initialCount, onCountChange }) => {
  const [count, setCount] = useState(initialCount);

  useEffect(() => {
    onCountChange(count);
  }, [count, onCountChange]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
};
```

### 4.3 Smart Contracts (Rust)
- Use rustfmt for code formatting
- Use clippy for code checking
- Follow Rust best practices
- Write comprehensive tests

Example:
```rust
use anchor_lang::prelude::*;

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + 32)]
    pub mirror: Account<'info, Mirror>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct Mirror {
    pub owner: Pubkey,
    pub is_active: bool,
}
```

## 5. Commit Standards

Follow Conventional Commits specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types include:
- feat: New feature
- fix: Bug fix
- docs: Documentation update
- style: Code formatting
- refactor: Code restructuring
- test: Testing related
- chore: Build process or auxiliary tool changes

## 6. Workflow

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

## 7. Pull Request Process

1. Ensure PR description is clear
2. Ensure all tests pass
3. Ensure code meets standards
4. Wait for code review
5. Make changes based on feedback

## 8. Testing Requirements

### 8.1 Backend Tests
- Unit test coverage > 80%
- Integration tests for main features
- Performance tests for critical paths

### 8.2 Frontend Tests
- Component tests
- Functional tests
- Performance tests

### 8.3 Smart Contract Tests
- Unit tests
- Integration tests
- Security tests

## 9. Documentation Requirements

- Update relevant documentation
- Add necessary comments
- Update API documentation
- Update example code

## 10. Code of Conduct

- Maintain professionalism and respect
- Provide constructive feedback
- Follow project standards
- Respond to communication promptly

## 11. Issue Reporting

When reporting issues, please provide:
- Issue description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment information
- Relevant logs

## 12. Feature Suggestions

When suggesting new features, please provide:
- Feature description
- Use cases
- Implementation suggestions
- Related references

## 13. License

All contributions will be under the project's MIT License.

## 14. Contact

For questions, contact:
- Project maintainers
- Community forum
- GitHub Issues 