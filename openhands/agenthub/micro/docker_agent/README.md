# Docker Agent

The Docker Agent is a specialized micro-agent in OpenHands that handles Docker-related operations, including:
- Dockerfile creation and optimization
- Docker Compose configuration
- Container management
- Docker best practices implementation

## Capabilities

1. **Dockerfile Management**
   - Create new Dockerfiles
   - Optimize existing Dockerfiles
   - Implement multi-stage builds
   - Follow security best practices

2. **Docker Compose**
   - Create and modify compose files
   - Configure service dependencies
   - Set up networking and volumes
   - Handle environment variables

3. **Container Operations**
   - Resource optimization
   - Health check implementation
   - Logging configuration
   - Lifecycle management

## Trigger Words

The agent activates when it detects these keywords:
- `docker`
- `container`
- `dockerfile`
- `compose`

## Usage Examples

1. Create a new Dockerfile:
```bash
Create a Dockerfile for a Node.js application that runs on port 3000
```

2. Set up multi-container environment:
```bash
Create a Docker Compose configuration for a web app with MongoDB database
```

3. Optimize existing setup:
```bash
Optimize the Dockerfile to reduce build time and image size
```

## Best Practices Enforced

1. **Security**
   - Non-root user usage
   - Specific version tags
   - Minimal base images
   - Security scanning recommendations

2. **Performance**
   - Layer optimization
   - Build caching
   - Multi-stage builds
   - Resource management

3. **Maintainability**
   - Clear documentation
   - Environment variables
   - Health checks
   - Logging configuration

## Input/Output

### Inputs
- `task`: The main instruction or request
- `context`: Additional context or requirements

### Outputs
- `result`: Description of the actions taken
- `files_modified`: List of files created or modified

## Container Requirements

The agent runs in a container with:
- Docker CLI (24.0.7)
- Basic shell utilities
- File manipulation tools