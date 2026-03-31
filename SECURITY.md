# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public issue
2. Email the maintainer or use GitHub's private vulnerability reporting

## Security Measures

- **SSRF Protection**: All URL-fetching scripts validate against private IP ranges
- **No Credentials**: No API keys or secrets stored in repository
- **Input Validation**: URLs validated before fetching
- **Minimal Dependencies**: Only 3 Python packages (beautifulsoup4, requests, lxml)
- **No Remote Execution**: Scripts only fetch and parse content, never execute remote code
