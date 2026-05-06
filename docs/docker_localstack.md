# Docker local + LocalStack (S3)

Objetivo: subir o **CardioIA** (Flask + frontend estático) junto com **LocalStack** simulando **S3**, para testar a cópia opcional dos logs de predição (`agents/pipeline/persistence.py`).

## Pré-requisitos

- Docker Desktop (ou Docker Engine + Compose v2)
- O `Dockerfile` copia o repositório (inclui `ml/modelo_risco_cardiaco.joblib` versionado); se alterar o modelo localmente, volte a `docker compose build`.

## Subir

Na raiz do repositório:

```powershell
docker compose up --build
```

- **API:** http://localhost:5000  
- **LocalStack (edge):** http://localhost:4566  

O serviço `web` executa `scripts/init_localstack_s3.py` antes do Flask para criar o bucket `cardioia-logs` (nome configurável por `CARDIOIA_S3_LOG_BUCKET`).

## Variáveis relevantes

| Variável | Descrição |
|----------|-----------|
| `AWS_ENDPOINT_URL` | No Compose: `http://localstack:4566` (dentro da rede Docker). No host (boto3 manual): `http://localhost:4566` |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | LocalStack aceita valores de teste (`test` / `test`) |
| `CARDIOIA_S3_LOG_BUCKET` | Bucket para upload dos JSON de `agents/logs/` após cada predição |

## OpenAI / Watson no container

Copie `.env.example` para `.env` e preencha `OPENAI_API_KEY` (e Watson, se quiser). Monte ou copie o `.env` para o contexto de build **não** é feito por defeito no `docker-compose` (evita vazar segredos na imagem). Para injetar variáveis:

```powershell
docker compose run --rm -e OPENAI_API_KEY=sk-... web python -m agents.main
```

Ou use `docker compose --env-file .env up` (Compose lê variáveis para interpolação; para o processo `web` passe `env_file` no YAML se desejar — não está ativo por defeito).

## Verificar objeto no S3

Com o stack a correr:

```powershell
aws --endpoint-url=http://localhost:4566 s3 ls s3://cardioia-logs/cardioia-logs/
```

(ajuste o prefixo conforme as chaves gravadas: `cardioia-logs/<ficheiro>.json`)

## Parar

```powershell
docker compose down
```

## CI: imagem no GHCR + testes na imagem

O workflow [`.github/workflows/docker-publish-and-test.yml`](../.github/workflows/docker-publish-and-test.yml) faz **build**, corre **`pytest backend/tests agents/tests`** dentro do container e publica em **`ghcr.io/<dono-minúsculo>/<repo-minúsculo>:latest`** (e tag com o SHA do commit).

**Primeira vez:** no GitHub, *Settings → Actions → General → Workflow permissions*, garanta leitura/escrita em pacotes se o push ao GHCR falhar.

**Local (Docker Hub ou outro registo):** na raiz do repo, com login já feito (`docker login`):

```powershell
.\scripts\docker-build-test-push.ps1 -Image "docker.io/SEU_USUARIO/cardioia-fase6" -Tag "latest" -EnvFile ".env"
```

Use `-SkipPush` para apenas validar build + testes.

## Imagem já no registo + LocalStack (`docker-compose.pull.yml`)

Depois do workflow (ou de um `docker push` manual), defina o nome completo da imagem e suba sem rebuild do código:

```powershell
$env:CARDIOIA_IMAGE = "ghcr.io/SEU_DONO_MINUSCULO/SEU_REPO_MINUSCULO:latest"
docker compose -f docker-compose.pull.yml up
```

Requer `.env` na raiz (o ficheiro é montado como `env_file` do serviço `web`).

## Publicar no GHCR a partir desta máquina

1. Crie um *Personal Access Token* (classic) com `write:packages` (e `read:packages`).
2. Login:

```powershell
echo SEU_TOKEN | docker login ghcr.io -u SEU_USUARIO_GITHUB --password-stdin
```

3. Tag + push (ajuste dono/repo em minúsculas):

```powershell
docker tag cardioia:ci ghcr.io/SEU_DONO/seu-repo:latest
docker push ghcr.io/SEU_DONO/seu-repo:latest
```

4. No GitHub: *Package* → *Package settings* → visibilidade **public** (se quiser `docker pull` sem autenticação).

## Testar só a imagem publicada (sem compose)

```powershell
docker pull ghcr.io/SEU_DONO/seu-repo:latest
docker run --rm --env-file .env ghcr.io/SEU_DONO/seu-repo:latest python -m pytest backend/tests agents/tests -q --tb=short
```
