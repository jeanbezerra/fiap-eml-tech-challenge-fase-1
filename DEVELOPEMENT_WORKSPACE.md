# Development Workspace

Este documento tem como objetivo orientar os desenvolvedores na configuração de um **ambiente de desenvolvimento padronizado**, garantindo que todos utilizem as mesmas dependências, ferramentas e banco de dados.  
Dessa forma, evitamos divergências entre ambientes que possam comprometer a qualidade do software e a sinergia do time.

## 1. Gerenciador de Pacotes: UV

O projeto utiliza o **[uv](https://docs.astral.sh/uv/)** como gerenciador de pacotes Python moderno e de alta performance.

### Instalação no Windows (PowerShell)

Execute o comando em seu terminal PowerShell como Administrador.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Após a instalação, verifique a versão:

```powershell
uv --version
```

## 2. IDEs Recomendadas

Escolha a IDE ou editor de texto de sua preferência entre as opções abaixo:

PyCharm (JetBrains)
 – recomendado para projetos complexos em Python.

Visual Studio Code (Microsoft)
 – leve, extensível e multiplataforma.

- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Microsoft Visual Code](https://code.visualstudio.com/)
- [Banco de Dados PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- [DBeaver Community](https://dbeaver.io/download/)

## 3. Banco de Dados
