# SecureNova – AI Identity Security Assessment and Protection

## Project Overview

SecureNova is an AI Identity Security project focused on identifying, testing, and protecting AI applications from identity-related security threats.

The project explores how AI agents, APIs, authentication systems, and external services can be secured against attacks such as prompt injection, identity spoofing, credential exposure, and unauthorized tool access.

It follows a practical security approach covering threat modeling, identity management, red-team testing, blue-team defence, and security policies.

## Project Objectives

- Identify security risks in AI-powered applications.
- Design secure identity and access management using Auth0.
- Simulate real-world AI security attacks.
- Implement security controls to prevent and detect attacks.
- Map security controls to industry frameworks.
- Develop security policies and recommendations.

## Project Modules

### Project 1 – Threat Modeling an AI Identity System

Identified potential security threats affecting AI agents and their communication flows.

**Key Activities:**
- Identified human and non-human identities.
- Applied the STRIDE threat modeling methodology.
- Created a Data Flow Diagram using OWASP Threat Dragon.
- Developed attack trees for major AI security threats.
- Mapped relevant attacks to MITRE ATLAS.
- Prepared a risk assessment register.

### Project 2 – AI Identity and Access Management

Developed an Auth0-backed Flask application to demonstrate secure authentication and authorization.

**Key Activities:**
- Integrated Auth0 authentication.
- Implemented Role-Based Access Control (RBAC).
- Configured User and Admin roles.
- Implemented Multi-Factor Authentication (MFA).
- Configured Machine-to-Machine authentication.
- Implemented JWT validation and access-token handling.
- Tested token expiration and access restrictions.

### Project 3 – Red-Team Security Assessment

Performed controlled security testing to identify weaknesses in AI agent interactions and tool execution.

**Attack Scenarios:**
1. Indirect Prompt Injection
2. Agent Identity Spoofing
3. System Prompt Extraction
4. RAG Poisoning
5. MCP Tool Abuse

**Key Activities:**
- Created controlled attack scenarios using Python.
- Tested prompt manipulation and credential exposure.
- Simulated unauthorized agent identity claims.
- Tested system prompt extraction attempts.
- Simulated malicious instructions in retrieved documents.
- Evaluated unauthorized tool-execution scenarios.
- Documented findings using CVSS and MITRE ATLAS.

### Project 4 – Blue-Team Security Controls

Implemented defensive security mechanisms to detect, prevent, and reduce the impact of the attacks identified during red-team testing.

**Key Activities:**
- Implemented input guardrails against prompt injection.
- Added sensitive credential detection and output redaction.
- Generated Ed25519 cryptographic key pairs.
- Implemented digital signature verification for agent messages.
- Configured Auth0 token lifetime and refresh-token rotation.
- Tested refresh-token replay protection.
- Implemented anomaly detection scenarios.
- Prepared a before-and-after comparison of red-team and blue-team results.

### Project 5 – Security Policy and Compliance

Developed security documentation and compliance mapping to establish security governance for AI identities.

**Key Activities:**
- Created an AI Identity Security Policy.
- Documented AI identity lifecycle management.
- Defined credential rotation and secrets management standards.
- Prepared incident response procedures.
- Mapped security controls to the NIST AI Risk Management Framework.
- Mapped relevant attacks and controls to the OWASP Top 10 for LLM Applications.
- Prepared a risk priority matrix.
- Developed five key security recommendations.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Identity Management | Auth0 |
| AI Integration | Google Gemini API |
| Authentication | OAuth 2.0, OpenID Connect, JWT |
| Cryptography | Ed25519, Python Cryptography |
| Threat Modeling | OWASP Threat Dragon |
| Attack Mapping | MITRE ATLAS |
| Security Frameworks | NIST AI RMF, OWASP LLM Top 10 |
| Development Tools | Visual Studio Code, Git, GitHub |
| Data and Documentation | CSV, Excel, Markdown |

## Repository Structure

```text
SecureNova/
│
├── 01-threat-model/
│   └── Threat modeling documents and diagrams
│
├── 02-iam-design/
│   └── Auth0 and Flask application
│
├── 03-red-team/
│   └── Simulated AI security attack scripts
│
├── 04-blue-team/
│   └── Defensive security controls and testing
│
├── 05-policy/
│   └── Security policies and compliance documents
│
└── README.md
```

## Security Testing and Results

The project evaluated five major AI security attack categories and implemented corresponding defensive controls.

The testing demonstrated:

- Prompt injection detection and blocking.
- Sensitive credential redaction.
- Agent message signature verification.
- Refresh-token rotation and replay detection.
- Anomaly detection for suspicious activity.
- Improved security outcomes after applying defensive controls.

The project also includes a risk assessment using CVSS 3.1 and a comparison of red-team and blue-team testing results.

## Compliance and Security Frameworks

The project references the following security frameworks:

- **NIST AI Risk Management Framework:** Govern, Map, Measure, and Manage.
- **OWASP Top 10 for LLM Applications:** Mapping relevant AI application vulnerabilities to implemented controls.
- **MITRE ATLAS:** Mapping AI-related attack techniques to documented security findings.
- **STRIDE:** Identifying security threats across system components and identity flows.
- **CVSS 3.1:** Assessing the severity of identified security findings.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Visual Studio Code
- Auth0 account
- Google Gemini API key

## Security Considerations

- Never upload API keys, client secrets, access tokens, refresh tokens, or Flask secret keys to GitHub.
- Store sensitive configuration in environment variables.
- Use `.gitignore` to exclude `.env` files and virtual environments.
- Perform security testing only in authorized environments.
- Use synthetic credentials and demo accounts for attack simulations.

**Testing Disclaimer:** Some red-team and blue-team activities in this project use controlled Python simulations and mock services. They demonstrate security concepts and defensive behaviour and should not be interpreted as proof of vulnerabilities or protections in a production environment.

## Future Enhancements

- Integrate a production-ready secrets management solution.
- Implement centralized security monitoring and alerting.
- Extend agent authentication and authorization mechanisms.
- Integrate a vector database for realistic RAG security testing.
- Implement a dedicated MCP server with secure tool authorization.
- Expand automated security testing and compliance reporting.

## Conclusion

SecureNova demonstrates a practical approach to securing AI-powered applications through identity management, threat modeling, controlled security testing, defensive controls, and compliance documentation.

The project highlights the importance of protecting AI identities, securing credentials, validating agent communication, and continuously monitoring AI application behaviour.

