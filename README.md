# Nexus Repository Manager Documentation

## Table of Contents

1. [Current Infrastructure Challenges](#current-infrastructure-challenges)
   - [External Dependency Risks](#external-dependency-risks)
   - [Security Vulnerabilities](#security-vulnerabilities)
   - [Performance Issues](#performance-issues)
2. [Why Nexus Repository Manager?](#why-nexus-repository-manager)
   - [Key Benefits](#key-benefits)
   - [Performance Improvements](#performance-improvements)
   - [Security Enhancements](#security-enhancements)
3. [Nexus Architecture](#nexus-architecture)
   - [Repository Types](#repository-types)
   - [Technology Support](#technology-support)
4. [High Availability Setup](#high-availability-setup)
   - [OSS vs PRO Comparison](#oss-vs-pro-comparison)
   - [HA Components](#ha-components)
   - [Deployment Configuration](#deployment-configuration)
5. [Post-Installation Setup](#post-installation-setup)
   - [Initial Configuration](#initial-configuration)
   - [Repository Creation](#repository-creation)

---

## Current Infrastructure Challenges

### Current Setup Overview

Our Jenkins deployment is configured as follows:

- **Location**: Private subnet without direct internet access
- **Network Path**: Outbound traffic → NAT Gateway → Internet Gateway
- **Security**: Jenkins is not publicly exposed (good practice)
- **Artifact Management**: No Nexus/Artifactory - direct internet downloads

### External Dependency Risks

#### The Problem

Every Jenkins build is **100% dependent on external services**. During each build:

1. Jenkins reaches out to multiple third-party registries over the internet
2. Dependencies are downloaded repeatedly
3. Any slow, rate-limited, or unavailable service causes build failures

#### Why This Matters

Even when everything internal is perfect:

- ✅ Application code has no issues
- ✅ Jenkins service is healthy
- ✅ EC2/Kubernetes infrastructure is up
- ✅ Resources (CPU, memory, disk) are normal
- ✅ NAT Gateway and routing are functional

**Builds can still fail** because dependency resolution happens outside our control.

#### NAT Gateway Limitations

Common misconception: *"We have NAT, so internet access is reliable"*

Reality:

- NAT provides only a **network path**
- Does NOT guarantee:
  - Service availability
  - Bandwidth fairness
  - API rate acceptance
  - CDN responsiveness
- NAT IPs can be throttled by external services
- Multiple concurrent builds amplify throttling issues

### Security Vulnerabilities

#### Current Security Risks

| Risk | Description | Impact |
|------|-------------|--------|
| **Supply Chain Attacks** | Blindly trusts public registries | Compromised packages reach production |
| **No Payload Inspection** | NAT cannot inspect content | Malicious code goes undetected |
| **Version Control** | No control over dependency versions | Unstable/vulnerable versions can be pulled |
| **No Auditing** | Cannot track what was downloaded | Compliance failures |

#### Common Threats

- Compromised npm packages
- Malicious Docker images
- Upstream dependency replacements
- Hijacked library versions

### Performance Issues

#### No Central Artifact Storage

**Current Behavior:**
- Build artifacts stored temporarily on Jenkins agents
- Artifacts lost when workspace is cleaned or agent recreated
- No centralized, persistent system of record

**Consequences:**
- Cannot rollback to previous versions easily
- Must rebuild from source for rollbacks (risky)
- No artifact traceability
- Inconsistent deployments

---

## Why Nexus Repository Manager?

### Key Benefits

#### 1. Faster Builds (30-70% improvement)

**How It Works:**

Every software project relies on dependencies:
- Java → Maven/Gradle (.jar files)
- Node.js → npm modules
- Docker → base images
- Python → pip packages

**Without Nexus:**
- Dependencies downloaded from internet every build
- Large projects have hundreds/thousands of dependencies
- Each download takes time (several minutes)
- Slow and unreliable builds

**With Nexus:**
- Local copy stored on first download
- Subsequent builds pull directly from Nexus
- Much faster than internet downloads

**Example Time Savings:**

| Build Time | Without Nexus | 30% Reduction | 70% Reduction |
|------------|---------------|---------------|---------------|
| Original | 20 minutes | 14 minutes | 6 minutes |
| Daily Builds (10x) | 200 minutes | 140 minutes | 60 minutes |
| **Weekly Savings** | - | **6 hours** | **14 hours** |

#### 2. Reduced Internet Dependency

**Problem Without Nexus:**
- Every build fetches from internet via NAT
- Build failures if NAT is down
- Slower builds due to network latency
- Risk from external registry unavailability

**Solution With Nexus:**
- Acts as local cache and proxy
- First fetch from internet, then cached locally
- Subsequent builds work without internet access

**Builds continue working even if:**
- ✅ NAT Gateway fails
- ✅ Internet outage occurs
- ✅ External registry is down
- ✅ Network maintenance in progress

#### 3. Enhanced Security & Supply Chain Control

**Without Nexus:**
- No control over dependency versions
- Direct pulls from public registries
- Risk of compromised upstream libraries
- No vulnerability scanning

**With Nexus:**
- **Approved repositories only** - whitelist trusted sources
- **Version blocking** - prevent vulnerable/unapproved versions
- **Security integrations:**
  - **Sonatype IQ** - vulnerability and license scanning
  - **Snyk** - code and dependency security
  - **Trivy** - Docker image vulnerability scanning
- **Automated detection** before deployment

#### 4. Artifact Versioning & Rollback

**Without Nexus:**
- Artifacts lost after deployment
- Rollback requires rebuild from source
- Rebuild risks:
  - Changed dependencies
  - Different build environment
  - Inconsistent artifacts

**With Nexus:**
- Every artifact stored with unique version
  - `myapp-1.2.3.jar`
  - `myapp-1.2.4.jar`
- Easy rollback to any previous version
- No rebuild required
- Guaranteed exact same artifact
- Reproducible builds for compliance

### Performance Improvements

#### Build Speed Optimization

**No Repeated Downloads:**
- Central cache for all dependencies
- Any Jenkins agent or developer can reuse
- Reduces redundancy across teams
- Improves efficiency organization-wide

#### Comparison Tables

**Security Comparison:**

| Aspect | NAT Only | NAT + Nexus |
|--------|----------|-------------|
| Internet isolation | ✅ | ✅ |
| Malicious dependency blocking | ❌ | ✅ |
| Approved repo enforcement | ❌ | ✅ |
| Audit trail | ❌ | ✅ |
| Checksum verification | ❌ | ✅ |

> **Key Insight:** NAT protects network, Nexus protects software supply chain

**Performance & Stability:**

| Aspect | NAT Only | NAT + Nexus |
|--------|----------|-------------|
| Dependency caching | ❌ | ✅ |
| Build speed | Slow | Fast (30-70% improvement) |
| Offline builds | ❌ | Partial ✅ |
| External repo outage | CI down ❌ | CI safe ✅ |

**Artifact Management:**

| Feature | NAT Only | Nexus |
|---------|----------|-------|
| Store build outputs | ❌ | ✅ |
| Versioning | ❌ | ✅ |
| Environment promotion (QA → UAT → PROD) | ❌ | ✅ |
| Rollback capability | ❌ | ✅ |

---

## Nexus Architecture
<img width="605" height="401" alt="image" src="https://github.com/user-attachments/assets/30f70ca0-7c6f-4aa6-8256-6075f3ab8f9a" />

### Repository Types

Nexus provides three types of repositories to manage artifacts effectively:

#### A) Hosted Repository

**Purpose:** Store internal company artifacts

**Use Cases:**
- Internal Docker images
- Internal npm packages
- Internal Helm charts
- Private libraries and tools

**Benefits:**
- Full control over internal artifacts
- Version management
- Access control
- Audit trails

#### B) Proxy Repository

**Purpose:** Cache external dependencies locally

**How It Works:**

1. Connects to public internet registry (Docker Hub, npmjs, Ubuntu apt, etc.)
2. Downloads package **only once**
3. Caches inside Nexus
4. Subsequent requests served from cache (no internet required)

**Examples:**
- `docker-proxy` → pulls from Docker Hub
- `npm-proxy` → pulls from registry.npmjs.org
- `apt-proxy` → pulls from archive.ubuntu.com

**Key Benefits:**
- Solves security issues
- Dramatically improves speed
- Reduces internet dependency
- Provides offline capability

#### C) Group Repository

**Purpose:** Combine hosted and proxy repositories into single endpoint

**Benefits:**
- Developers configure **ONE URL** only
- Transparent routing to hosted/proxy repos
- Simplified configuration management

**Example:**
- `npm-group` = `npm-hosted` + `npm-proxy`
- `docker-group` = `docker-hosted` + `docker-proxy`

### How Proxy Repository Works

**Example:** Developer runs `npm install express`

**Request Flow:**
```
Developer → Nexus → npm-group → [npm-hosted + npm-proxy]
```

**Process:**

1. **Check Cache:** npm-proxy checks if `express` is cached locally
2. **Cache Hit:** If cached → return immediately (fast)
3. **Cache Miss:** If not cached → fetch from `https://registry.npmjs.org/`
4. **Store:** Nexus caches the package
5. **Return:** Package delivered to developer

**Subsequent Requests:** Served directly from cache (no internet)

### Technology Support

Nexus supports all major package formats and registries:

| Technology | Proxy Target | Hosted Repo | Group Repo |
|------------|--------------|-------------|------------|
| **npm/yarn/pnpm** | `registry.npmjs.org` | `npm-hosted` | `npm-group` |
| **Docker** | `registry-1.docker.io` | `docker-hosted` | `docker-group` |
| **Ubuntu apt** | `archive.ubuntu.com` | `apt-hosted` | `apt-group` |
| **Helm** | `charts.helm.sh` | `helm-hosted` | `helm-group` |
| **Python (pip)** | `pypi.org` | `pypi-hosted` | `pypi-group` |
| **Maven/Java** | `repo.maven.apache.org` | `maven-hosted` | `maven-group` |

### Jenkins Integration

**Jenkins pulls everything from Nexus:**
- npm installs
- Maven builds
- Docker image builds
- apt package installs
- Helm chart downloads

**Result:** Everything is secure, cached, and controlled

---

## High Availability Setup

### OSS vs PRO Comparison

#### Important Reality Check

> ⚠️ **Nexus OSS (free version) does NOT support true clustered HA**
> 
> Only **Nexus PRO** supports official HA (multiple active nodes + shared blob storage + shared database)

#### What You GET with OSS on Kubernetes

| Feature | Status | Description |
|---------|--------|-------------|
| **Automatic pod restart** | ✅ | Kubernetes restarts crashed pods → Basic resilience |
| **Persistent storage** | ✅ | PVC keeps data safe → No data loss on pod recreation |
| **Easy upgrades** | ✅ | Helm-based rolling upgrades → Controlled downtime |
| **Scalable storage** | ✅ | S3, PVC, NFS support → Better reliability |
| **Small/medium teams** | ✅ | Free version sufficient for most use cases |

#### What You DON'T GET with OSS on Kubernetes

| Limitation | Status | Description |
|------------|--------|-------------|
| **Multi-pod load balancing** | ❌ | `replicaCount` must be 1 |
| **Active-active clustering** | ❌ | Only Nexus PRO supports this |
| **True High Availability** | ❌ | Pod restart ≠ HA cluster |
| **Horizontal scaling** | ❌ | Cannot run multiple replicas |

### HA Components

For **Nexus PRO High Availability**, you need:

#### 1. Multiple Nexus PRO Application Pods (2-3 nodes)

- All nodes active-active
- Behind single Kubernetes Ingress or LoadBalancer
- Load distributed across pods

#### 2. External PostgreSQL Database

**Why Required:**

Nexus PRO HA requires shared metadata storage across all nodes for:
- Repository configuration
- Component and asset information
- Permissions and roles
- User accounts
- Task states
- Job management
- Internal indexes
- **Distributed lock management** (prevents corruption)

**Recommended:**
- AWS RDS PostgreSQL
- Managed service for reliability
- Automated backups
- Multi-AZ deployment

**Important:** Database stores metadata only, NOT artifacts

#### 3. Shared Blob Store

All Nexus pods must access **one shared storage** for artifacts.

**Recommended:**
- **AWS S3** (best for AWS deployments)
- MinIO (on-premises alternative)
- NFS (not recommended for production)

**Data Separation:**
- ✅ **Artifacts** → Stored in Blob Store (S3/MinIO)
- ✅ **Metadata** → Stored in Database (PostgreSQL)

#### 4. Ingress / Load Balancer

Distributes traffic between Nexus pods for high availability.

### Deployment Configuration

#### Helm Values for Nexus PRO HA
```yaml
# High Availability Configuration
replicaCount: 2  # Multiple active pods

# Nexus PRO Image
image:
  repository: sonatype/nexus3
  tag: latest
  pullPolicy: Always

# Enable PRO features
nexusPro: true  # MUST be true for HA

# Environment Configuration
env:
  nexus_base_url: "https://nexus.example.com"

# Nexus HA Properties
nexus:
  properties:
    nexus.ha.enabled: "true"
    nexus.ha.database.enabled: "true"
    nexus.ha.blobstore.enabled: "true"

# Disable local persistence (use external blobstore)
persistence:
  enabled: false

# S3 Blob Store Configuration
blobStore:
  type: s3
  s3:
    bucket: nexus-ha-artifacts
    region: ap-south-1
    prefix: nexus-data/
    accessKeyId: "<AWS_ACCESS_KEY>"
    secretAccessKey: "<AWS_SECRET_KEY>"

# External PostgreSQL Configuration
database:
  enabled: false  # We use external DB
  
externalDatabase:
  type: postgresql
  host: "nexus-db.example.com"
  port: 5432
  name: "nexus"
  username: "nexus_user"
  password: "nexus_pass"

# Service Configuration
service:
  type: LoadBalancer

# Resource Limits
resources:
  requests:
    cpu: 1
    memory: 4Gi
  limits:
    cpu: 2
    memory: 8Gi
```

#### Deployment Commands
```bash
# Add Helm repository
helm repo add oteemo https://oteemo.github.io/charts

# Update Helm repositories
helm repo update

# Install Nexus with HA configuration
helm install nexus-ha oteemo/nexus -f values.yaml

# Verify deployment
kubectl get pods -l app=nexus
kubectl get svc nexus-ha
```

---

## Post-Installation Setup

### Initial Configuration

#### 1. Access Nexus UI
```bash
# Get Nexus URL
kubectl get svc nexus-ha

# Open in browser
http://<NEXUS_URL>:8081
```

#### 2. Initial Login

- **Username:** `admin`
- **Password:** Found in `/nexus-data/admin.password`
```bash
# Get initial password (if using Kubernetes)
kubectl exec -it <nexus-pod> -- cat /nexus-data/admin.password
```

**Important:** Change default password immediately after first login

#### 3. Security Configuration

**Recommended Settings:**

1. **Anonymous Access** (for learning/development only)
   - Settings → Security → Anonymous Access → Enable

2. **Docker Authentication** (Critical)
   - Settings → Security → Realms
   - Move **Docker Bearer Token Realm** to *Active* list

3. **User Management**
   - Create role-based access
   - Follow principle of least privilege

### Repository Creation

#### A) npm Repositories (Node.js)

##### 1. npm-proxy (Proxy Repository)
```
Settings → Repositories → Create repository → npm (proxy)
```

**Configuration:**
- **Name:** `npm-proxy`
- **Remote storage:** `https://registry.npmjs.org/`
- **Blob store:** `default`

##### 2. npm-hosted (Hosted Repository)
```
Settings → Repositories → Create repository → npm (hosted)
```

**Configuration:**
- **Name:** `npm-hosted`
- **Blob store:** `default`
- **Deployment policy:** Allow redeploy (for development)

##### 3. npm-group (Group Repository)
```
Settings → Repositories → Create repository → npm (group)
```

**Configuration:**
- **Name:** `npm-group`
- **Members:** `npm-hosted`, `npm-proxy`
- **Blob store:** `default`

**Developer Configuration:**
```bash
# Set npm registry
npm config set registry http://nexus.example.com/repository/npm-group/

# Verify
npm config get registry
```

---

#### B) Docker Repositories

##### 1. docker-proxy (Proxy Repository)
```
Settings → Repositories → Create repository → docker (proxy)
```

**Configuration:**
- **Name:** `docker-proxy`
- **Remote storage:** `https://registry-1.docker.io`
- **Docker Index:** Use Docker Hub
- **HTTP connector:** Enable (choose port or path-based)

**Routing Options:**
- **Path-based:** `/repository/docker-proxy/` (recommended for Kubernetes)
- **Port-based:** Custom port (requires additional exposure)

##### 2. docker-hosted (Hosted Repository)
```
Settings → Repositories → Create repository → docker (hosted)
```

**Configuration:**
- **Name:** `docker-hosted`
- **HTTP connector:** Enable
- **Blob store:** `default`

##### 3. docker-group (Group Repository)
```
Settings → Repositories → Create repository → docker (group)
```

**Configuration:**
- **Name:** `docker-group`
- **Members:** `docker-hosted`, `docker-proxy`
- **HTTP connector:** Enable

**Docker Configuration:**
```bash
# Login to Nexus Docker registry
docker login nexus.example.com:8082

# Pull through Nexus
docker pull nexus.example.com:8082/nginx:latest

# Tag and push to hosted
docker tag myapp:latest nexus.example.com:8082/myapp:latest
docker push nexus.example.com:8082/myapp:latest
```

**Important Note:**
- If using port-based Docker connectors, expose those ports from Nexus
- If Nexus runs behind Kubernetes Ingress, use path-based routing (no extra ports needed)

---

#### C) Ubuntu APT Repositories

##### 1. ubuntu-apt-proxy (Proxy Repository)
```
Settings → Repositories → Create repository → apt (proxy)
```

**Configuration:**
- **Name:** `ubuntu-apt-proxy`
- **Remote storage:** `http://archive.ubuntu.com/ubuntu`
- **Distribution:** `jammy` (or your Ubuntu version)
- **Blob store:** `default`

##### 2. apt-hosted (Optional - Hosted Repository)
```
Settings → Repositories → Create repository → apt (hosted)
```

**Configuration:**
- **Name:** `apt-hosted`
- **Distribution:** `jammy`
- **Blob store:** `default`

**Use Case:** Host internal .deb packages

##### 3. apt-group (Optional - Group Repository)
```
Settings → Repositories → Create repository → apt (group)
```

**Configuration:**
- **Name:** `apt-group`
- **Members:** `apt-hosted`, `ubuntu-apt-proxy`

**Ubuntu Configuration:**
```bash
# Add Nexus APT source
echo "deb http://nexus.example.com/repository/ubuntu-apt-proxy/ jammy main restricted universe multiverse" | \
  sudo tee /etc/apt/sources.list.d/nexus.list

# Update package list
sudo apt update

# Install packages through Nexus
sudo apt install <package-name>
```

---

## Best Practices

### Repository Organization

1. **Use Group Repositories** for developer/CI access
2. **Separate Hosted repos** for different teams/projects
3. **Configure Proxy repos** for each external registry
4. **Regular cleanup** of old artifacts

### Security Recommendations

1. **Disable anonymous access** in production
2. **Enable LDAP/SSO** integration
3. **Use Docker Bearer Token Realm** for Docker authentication
4. **Regular security scans** with integrated tools
5. **Implement RBAC** (Role-Based Access Control)

### Performance Optimization

1. **Use blob stores** efficiently (S3 for cloud)
2. **Configure cleanup policies** to remove old artifacts
3. **Monitor disk usage** and set quotas
4. **Enable aggressive caching** for frequently used dependencies

### Monitoring & Maintenance

1. **Set up health checks** in Kubernetes
2. **Monitor blob store** size and growth
3. **Regular database backups** (for PRO with PostgreSQL)
4. **Track repository usage** metrics
5. **Review audit logs** periodically

---

## Troubleshooting

### Common Issues

#### Cannot Pull Docker Images

**Symptoms:**
- `unauthorized: access to the requested resource is not authorized`

**Solution:**
1. Verify Docker Bearer Token Realm is active
2. Check repository permissions
3. Verify `docker login` credentials
4. Ensure correct registry URL

#### Slow Artifact Downloads

**Symptoms:**
- Slow pulls from Nexus compared to internet

**Solution:**
1. Check network connectivity between Jenkins/client and Nexus
2. Verify blob store performance (S3 vs local)
3. Check Nexus resource limits (CPU/Memory)
4. Review concurrent connection limits

#### Repository Not Caching

**Symptoms:**
- Every request goes to upstream registry

**Solution:**
1. Verify proxy repository remote URL
2. Check Maximum component age in proxy settings
3. Review negative cache settings
4. Clear repository cache and retry

---

## Conclusion

Nexus Repository Manager transforms your CI/CD pipeline by:

- ✅ **Reducing build times** by 30-70%
- ✅ **Eliminating internet dependency** for builds
- ✅ **Securing supply chain** with vulnerability scanning
- ✅ **Enabling artifact versioning** and easy rollbacks
- ✅ **Providing centralized control** over all dependencies
- ✅ **Improving team productivity** with faster, reliable builds

### Next Steps

1. Deploy Nexus (OSS for small teams, PRO for enterprise HA)
2. Configure repositories for your technology stack
3. Integrate with Jenkins pipelines
4. Train team on Nexus usage
5. Implement security scanning tools
6. Monitor and optimize performance

---

## Additional Resources

- [Nexus Repository Manager Documentation](https://help.sonatype.com/repomanager3)
- [Helm Chart Repository](https://github.com/sonatype/helm3-charts)
- [Docker Configuration Guide](https://help.sonatype.com/repomanager3/nexus-repository-administration/formats/docker-registry)
- [npm Configuration Guide](https://help.sonatype.com/repomanager3/nexus-repository-administration/formats/npm-registry)

---
 
**Maintained By:** DevOps Team
