# USF-2 Invocation Prompts

Ready-to-use prompts for invoking USF-2 with Claude Code.

---

## Quick Invocations

### General Analysis
```
use USF to analyze [topic/code/system]
```

### Security Focus
```
use USF to audit the security of [component]
```

### Maximum Rigor
```
use USF max on [target]
```

### Quick Check
```
use USF quick to check [item]
```

---

## Domain-Specific Prompts

### Security Audit
```
use USF to perform a comprehensive security audit of the authentication system.
Focus on:
- Input validation vulnerabilities
- Authentication bypass risks
- Session management weaknesses
- Authorization flaws
```

### Code Review
```
use USF to review this code for:
- Potential bugs and edge cases
- Performance issues
- Security vulnerabilities
- Code quality improvements
```

### Architecture Analysis
```
use USF to analyze the system architecture and identify:
- Single points of failure
- Scalability bottlenecks
- Security boundaries
- Integration risks
```

### Protocol Analysis
```
use USF to analyze this protocol design for:
- Correctness and completeness
- Security properties
- Performance characteristics
- Edge cases and failure modes
```

---

## Compute-Specific Prompts

### Hivemind (Consensus)
```
use USF with hivemind to reach consensus on [decision/analysis]
```

### Swarm (Maximum Coverage)
```
use USF swarm to exhaustively analyze [target]
```

### Tournament (Best Answer)
```
use USF tournament to find the best approach for [problem]
```

### Map-Reduce (Large Tasks)
```
use USF map-reduce to analyze [large codebase/dataset]
```

---

## Precision-Specific Prompts

### PL1 - Quick Check
```
use USF PL1 to quickly verify [claim/code]
```

### PL3 - Standard (Default)
```
use USF to analyze [target]
```

### PL5 - Maximum Rigor
```
use USF PL5 to thoroughly verify [critical component]
```

---

## Combined Prompts

### Security + Maximum
```
use USF hivemind PL5 to audit the payment processing system for security vulnerabilities
```

### Research + Comprehensive
```
use USF swarm to research all approaches for implementing [feature]
```

### Comparison
```
use USF tournament to compare these implementation options:
1. [Option A]
2. [Option B]
3. [Option C]
```

---

## Integration Prompts

### With Specific Instructions
```
use USF to analyze this code. Focus specifically on:
- Memory management issues
- Thread safety concerns
- Error handling completeness

After analysis, provide remediation recommendations.
```

### Multi-Stage
```
First, use USF to identify all potential security issues.
Then, prioritize them by severity.
Finally, suggest fixes for the top 3 issues.
```

### With Context
```
Context: This is a financial application handling PCI data.

use USF PL5 to audit the data handling code for:
- PCI compliance issues
- Data exposure risks
- Encryption weaknesses
```

---

## Output Format Requests

### Summary Only
```
use USF to analyze [target], then summarize findings in bullet points
```

### Detailed Report
```
use USF to generate a detailed security report for [component]
```

### Actionable Items
```
use USF to identify issues and provide actionable remediation steps
```

---

## Tips for Effective Prompts

1. **Be Specific**: Include the target and focus areas
2. **Set Context**: Mention domain-specific requirements
3. **Request Format**: Specify how you want results presented
4. **Chain Tasks**: Use multi-stage prompts for complex analysis

---

## Examples with Expected Behavior

### Example 1: Security Audit
```
Prompt: use USF to audit the login endpoint security

Expected:
- Auto-detects: hivemind, PL5
- Spawns: 9 chains + 7 experts = 16 agents
- Focuses on: authentication, input validation, session management
```

### Example 2: Quick Review
```
Prompt: use USF quick to check this function for bugs

Expected:
- Auto-detects: sequential, PL1
- Spawns: 1 chain + 3 experts = 4 agents
- Fast turnaround, basic analysis
```

### Example 3: Comparison
```
Prompt: use USF tournament to compare React vs Vue for this project

Expected:
- Uses: tournament compute type
- Spawns competing analysis agents
- Returns winner with reasoning
```

---

**Remember**: USF-2 will auto-detect the best parameters from your prompt, but you can always override with explicit instructions.
