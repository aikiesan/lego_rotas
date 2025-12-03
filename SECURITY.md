# Security Policy

## Environment Variables and Secrets

This project uses environment variables to manage sensitive configuration like database passwords. **Never commit `.env` files to version control.**

### Setup for Development

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Generate a secure password:
   ```bash
   # Generate a random secure password
   openssl rand -base64 32
   ```

3. Update `.env` with your secure password:
   ```
   POSTGRES_PASSWORD=<your-generated-password>
   ```

### GitGuardian Alert Resolution

If you received a GitGuardian alert about hardcoded secrets:

- **The alert is expected** - Earlier commits included example passwords for demonstration
- **This has been fixed** - The project now uses environment variables
- **No action required** - Just ensure you follow the setup instructions above

### Files That Should NEVER Be Committed

These files are already in `.gitignore`:
- `.env` (root directory)
- `backend/.env`
- `frontend/.env.local`
- Any file containing real credentials or API keys

### Production Security Checklist

When deploying to production:

- [ ] Use strong, randomly generated passwords (min 32 characters)
- [ ] Store secrets in proper secret management (AWS Secrets Manager, Azure Key Vault, etc.)
- [ ] Enable SSL/TLS for database connections
- [ ] Use different passwords for each environment (dev, staging, production)
- [ ] Rotate credentials regularly
- [ ] Never use default or example passwords
- [ ] Enable database authentication and firewall rules
- [ ] Use environment-specific `.env` files (never committed)
- [ ] Review and update `CORS` settings in FastAPI (currently allows all origins)
- [ ] Set `DEBUG=False` in production backend

### Reporting Security Issues

If you discover a security vulnerability, please email the maintainers directly rather than opening a public issue.

## Development vs Production

### Development (Local)
- Example passwords in `.env.example` are for **reference only**
- Docker Compose uses environment variables from `.env`
- Suitable for local testing only

### Production
- Use proper secret management systems
- Never use example or default passwords
- Enable all security features (SSL, authentication, firewalls)
- Follow your organization's security policies

## Dependencies

Keep dependencies updated to patch security vulnerabilities:

```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm audit fix
npm update
```

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
