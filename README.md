# b2bflow-supabase-zapi

**Autor:** Matheus Abrahão
**Tipo:** Teste Técnico
**Data:** Dezembro 2024

Sistema que envia mensagens personalizadas para contatos do Supabase via Z-API.

## 🎯 Objetivo

Enviar a mensagem **"Olá {{nome_contato}}, tudo bem com você?"** para contatos cadastrados no Supabase via Z-API.

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
- **ID da instância** (ex: `3E59322D375AE025F1F3CA4350A8658A`)
- **Token da instância** (ex: `DBC4373D35407896C7321867`)

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
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Z-API
ZAPI_BASE_URL=https://api.z-api.io
ZAPI_INSTANCE_ID=3E59322D375AE025F1F3CA4350A8658A
ZAPI_TOKEN=DBC4373D35407896C7321867
ZAPI_CLIENT_TOKEN=F8e627502f92f48abbcb7cf1c96ec83b9S

# App
DRY_RUN=true   # true = só testa, false = envia de verdade
LOG_LEVEL=INFO
MAX_MESSAGES=3
```

## 🧪 Como Usar

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
