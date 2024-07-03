```markdown
# GenLayer Simulator Helm Chart
This Helm chart installs the GenLayer Simulator.
## Prerequisites
- Kubernetes cluster up and running.
- Helm 3 installed.
## Installation
1. **Package the chart:**
   ```bash
   helm package .
   ```
   This will create a chart archive file named `genlayer-simulator-0.0.1.tgz`.
2. **Install the chart:**
   ```bash
   helm install my-release -f values-docker-hub.yaml genlayer-simulator-0.0.1.tgz
   ```
   This will install the GenLayer Simulator in your Kubernetes cluster with the release name `my-release` and pull the images from the official Docker Hub registry. You can customize the release name or values.yaml as needed.
## Uninstallation
To uninstall the GenLayer Simulator, run:
```bash
helm uninstall my-release
```
This will remove all the resources associated with the release `my-release`.
## Configuration
You can customize the GenLayer Simulator installation by providing values in a YAML file. 

**Example `values.yaml`:**

```yaml
postgres:
  image: yeagerai/simulator-postgres
  name: genlayer_state
  user: postgres
  password: postgres
  port: 5432
  disk_size: 5Gi

ollama:
  image: ollama/ollama:latest
  protocol: http
  port: 11434
  disk_size: 5Gi

genvm:
  image: yeagerai/simulator-genvm:latest
  protocol: http
  port: 6000
  debugPort: 6678
  debug: 1

rpc:
  image: yeagerai/simulator-jsonrpc:latest
  protocol: http
  port: 4000
  debugPort: 4678

webrequest:
  image: yeagerai/simulator-webrequest:latest
  protocol: http
  port: 5000

frontend:
  port: 8080
  image: yeagerai/simulator-frontend:latest

vscodeDebug: false
openaiKey: "YOUR_OPENAI_KEY"
heuristAI:
  url: https://llm-gateway.heurist.xyz
  modelsUrl: https://raw.githubusercontent.com/heurist-network/heurist-models/main/models.json
  apiKey: "YOUR_HEURISTAI_KEY"
```
**Install with custom values:**

```bash
helm install my-release -f your-values.yaml genlayer-simulator-0.0.1.tgz
```