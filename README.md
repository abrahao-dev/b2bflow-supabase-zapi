# b2bflow-supabase-zapi

**Autor:** Matheus Abrahão
**Tipo:** Teste Técnico
**Data:** 8 Agosto 2025
**Repositório:** https://github.com/abrahao-dev/b2bflow-supabase-zapi

Sistema que envia mensagens personalizadas para contatos do Supabase via Z-API.

## ⚡ Execução Rápida

1. **Configure as variáveis de ambiente** (veja seção Setup)
2. **Execute:** `python main.py`

## 🔑 Variáveis de Ambiente Necessárias

```bash
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anonima

# Z-API
ZAPI_INSTANCE_ID=seu-instance-id
ZAPI_TOKEN=seu-token
```

## 🎯 Objetivo

Enviar a mensagem **"Olá {{nome_contato}}, tudo bem com você?"** para contatos cadastrados no Supabase via Z-API.

## 🔄 Fluxo do Sistema

```mermaid
graph TD
    subgraph "Usuário/Desenvolvedor"
        A[▶️ Início: Executa 'python main.py']
    end

    subgraph "Script Python (Aplicação)"
        B(⚙️ Carrega configurações do .env)
        C{Contatos foram encontrados?}
        D[🔁 Loop: Para cada contato]
        E{Modo DRY_RUN ativado?}
        F1[📄 Formata a mensagem]
        G1(✅ DRY_RUN Loga a mensagem no console)
        H1(📨 Envia mensagem via Z-API)
        I1(📝 Loga o resultado do envio)
        J[🏁 Fim]
    end

    subgraph "Supabase (Banco de Dados)"
        S1(☁️ Conecta ao Supabase)
        S2(🔍 Busca contatos ativos na tabela 'contacts')
    end

    subgraph "Z-API (Serviço Externo)"
        Z1(📲 Recebe a requisição do script)
        Z2(💬 Dispara a mensagem para o WhatsApp do contato)
    end

    A --> B
    B --> S1
    S1 --> S2
    S2 --> C

    C -- Sim --> D
    C -- Não --> J

    D -- Processar --> F1
    F1 --> E

    E -- Sim --> G1
    G1 -- Próximo --> D

    E -- Não --> H1
    H1 --> Z1
    Z1 --> Z2
    Z2 -- Retorno --> I1
    I1 -- Próximo --> D

    D -- Fim do loop --> J
```

## 🚀 Setup Completo

### 1) Clone e Instale
```bash
git clone https://github.com/seu-usuario/b2bflow-supabase-zapi.git
cd b2bflow-supabase-zapi
pip install -r requirements.txt
```

### 2) Configure o Supabase

#### A) Crie um projeto no Supabase
1. Acesse [supabase.com](https://supabase.com)
2. Clique em "New Project"
3. Escolha um nome e senha
4. Aguarde a criação

#### B) Execute o SQL para criar a tabela
No **SQL Editor** do Supabase, execute:

```sql
-- (se ainda não tiver) extensão p/ gen_random_uuid
create extension if not exists pgcrypto;

create table if not exists public.contacts (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  phone_e164 text not null unique, -- formato E.164: +5511999999999
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

-- Contatos de teste
insert into public.contacts (nome, phone_e164) values
('Jose', '+5511988887777'),
('Bruno', '+5511977776666'),
('Carla', '+5511966665555');

-- habilitar RLS (normalmente já vem habilitado)
alter table public.contacts enable row level security;

-- policy de leitura pública (para role 'anon')
create policy "public read contacts"
on public.contacts
for select
using (true);
```

#### C) Obtenha as credenciais
1. Vá em **Settings** → **API**
2. Copie:
   - **Project URL** (ex: `https://abc123.supabase.co`)
   - **anon public** key (começa com `eyJ...`)

### 3) Configure a Z-API

#### A) Crie uma instância
1. Acesse [app.z-api.io](https://app.z-api.io)
2. Clique em **"Nova Instância"**
3. Escolha um nome (ex: "b2bflow-teste")
4. Aguarde a criação

#### B) Conecte o WhatsApp
1. Na sua instância, clique em **"Conectar"**
2. Escaneie o QR Code com seu WhatsApp
3. Aguarde a conexão

#### C) Configure o Security Token (opcional mas recomendado)
1. Vá em **Security** → **Account security token**
2. Clique em **"Configure now"**
3. Clique em **"Activate Token"**
4. Copie o token gerado

#### D) Obtenha as credenciais da Z-API
Na página da sua instância, copie:
- **ID da instância** (ex: `00000000000000000000000000000000`)
- **Token da instância** (ex: `00000000000000000000000000000000`)

### 4) Configure o arquivo .env

```bash
# Copie o template
cp env.example .env

# Edite o .env com suas credenciais
```

Exemplo de `.env` completo:
```bash
# Supabase
SUPABASE_URL=https://abc123.supabase.co
SUPABASE_ANON_KEY=00000000000000000000000000000000

# Z-API
ZAPI_BASE_URL=https://api.z-api.io
ZAPI_INSTANCE_ID=00000000000000000000000000000000
ZAPI_TOKEN=00000000000000000000000000000000
ZAPI_CLIENT_TOKEN=00000000000000000000000000000000

# App
DRY_RUN=true   # true = só testa, false = envia de verdade
LOG_LEVEL=INFO
MAX_MESSAGES=3
```

## 🚀 Como Executar

### Comando Principal
```bash
python main.py
```

### Teste primeiro (DRY_RUN)
```bash
# Garanta que DRY_RUN=true no .env
python test_run.py
```

Você deve ver:
```
2025-08-11 20:04:21,907 | INFO | zapi | [DRY_RUN] Would send to 5511988887777: Olá Jose, tudo bem com você?
2025-08-11 20:04:21,907 | INFO | zapi | [DRY_RUN] Would send to 5511977776666: Olá Bruno, tudo bem com você?
2025-08-11 20:04:21,908 | INFO | zapi | [DRY_RUN] Would send to 5511966665555: Olá Carla, tudo bem com você?
```

### Envio real
```bash
# Edite .env e mude para:
DRY_RUN=false

# Execute
python test_run.py
```

Você deve ver:
```
2025-08-11 20:07:31,773 | INFO | zapi | Sent to 5511988887777
2025-08-11 20:07:32,094 | INFO | zapi | Sent to 5511977776666
2025-08-11 20:07:32,431 | INFO | zapi | Sent to 5511966665555
```

## 📋 Checklist de Configuração

- [ ] Supabase criado e tabela `contacts` criada
- [ ] Contatos inseridos na tabela
- [ ] Credenciais do Supabase no `.env`
- [ ] Z-API criada e WhatsApp conectado
- [ ] Security Token configurado (opcional)
- [ ] Credenciais da Z-API no `.env`
- [ ] Teste DRY_RUN funcionando
- [ ] Envio real funcionando

## 🔧 Troubleshooting

### Erro 403 "Client-Token null not allowed"
- Configure o Account Security Token na Z-API
- Ou deixe `ZAPI_CLIENT_TOKEN=` vazio no `.env`

### Erro 400 "Invalid phone"
- Verifique se o telefone está no formato E.164: `+5511999999999`
- O código remove automaticamente o `+` antes de enviar

### Erro de conexão Supabase
- Verifique `SUPABASE_URL` e `SUPABASE_ANON_KEY`
- Confirme se a tabela `contacts` existe

### WhatsApp não conecta
- Verifique se o QR Code foi escaneado corretamente
- Aguarde alguns minutos após o escaneamento

## 📁 Estrutura do Projeto

```
b2bflow-supabase-zapi/
├── src/
│   ├── main.py          # Orquestrador principal
│   ├── settings.py      # Gerenciamento de configurações
│   ├── supa_client.py   # Cliente Supabase
│   ├── zapi_client.py   # Cliente Z-API
│   └── util.py          # Utilitários (logging, retry)
├── tests/
│   └── test_sanity.py   # Validações básicas
├── .env                 # Configurações de ambiente
├── env.example          # Template de configuração
├── requirements.txt     # Dependências Python
├── test_run.py          # Script de execução
└── README.md           # Este arquivo
```

## 🧪 Testes

```bash
# Executar testes básicos
python -c "from tests.test_sanity import test_message_format, test_phone_validation; test_message_format(); test_phone_validation(); print('✅ Validação concluída!')"

# Com pytest (opcional)
python -m pytest tests/
```

## ✅ Status do Projeto

### **Implementado:**
- ✅ Arquitetura modular com separação de responsabilidades
- ✅ Integração com Z-API (instância: b2bflow-teste)
- ✅ Cliente Z-API com retry exponencial e validação de telefone
- ✅ Cliente Supabase para busca de contatos
- ✅ Sistema de configuração via variáveis de ambiente
- ✅ Logging estruturado e tratamento robusto de erros
- ✅ Modo DRY_RUN para testes seguros
- ✅ Testes unitários para validação de funcionalidades
- ✅ Configuração de ambiente completa
- ✅ **FLUXO FUNCIONANDO DE PONTA A PONTA** ✅
