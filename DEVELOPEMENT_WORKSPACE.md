# Development Workspace

Este documento tem como objetivo orientar os desenvolvedores na configuração de um **ambiente de desenvolvimento padronizado**, garantindo que todos utilizem as mesmas dependências, ferramentas e banco de dados.

Dessa forma, evitamos divergências entre ambientes que possam comprometer a qualidade do software e a sinergia do time.

## 1 - Pastas

A base de um ambiente de desenvolvimento eficiente começa pela padronização da estrutura de pastas. Definir um caminho único, previamente acordado, onde todos os projetos de código irão residir ao longo de seu ciclo de vida é tão importante quanto possuir requisitos bem definidos e um backlog claro de atividades.

Sem essa uniformidade, o trabalho colaborativo torna-se caótico, não é viável desenvolver um software em equipe sem um padrão mínimo de ferramentas, IDEs, sistemas operacionais e, principalmente, uma estrutura de diretórios comum que atenda aos objetivos de cada projeto. A ausência desse alinhamento gera retrabalho, perda de produtividade e dificuldade na integração de entregas.

**1.1 - Boas práticas a adotar**

- Defina um diretório raiz único para todos os projetos relacionados;
- Mantenha nomenclaturas consistentes (sem espaços ou caracteres especiais desnecessários);
- Separe claramente os tipos de artefatos, como código-fonte, documentação, testes, pacotes gerados e dependências;
- Evite alterações não acordadas, garantindo que qualquer mudança de estrutura seja discutida previamente com a equipe.

**1.2 - Reflexão importante:**

Antes de propor ou adotar novas mudanças, consulte todos os membros do projeto. Dessa forma, garantimos um ambiente unificado, totalmente integrado, previsível e nivelado para todos os envolvidos. A padronização é um dos pilares para a colaboração efetiva e para a qualidade contínua do produto de software.

**1.3 - Estrutura recomendada:**

Para este projeto, recomenda-se a criação de uma estrutura de diretórios centralizada, garantindo que todos os desenvolvedores utilizem caminhos padronizados. Dessa forma, evitamos divergências entre ambientes locais e asseguramos maior previsibilidade durante o desenvolvimento.

A proposta é manter workspaces separados por IDE, organizados da seguinte forma:

```
C:\FIAP\EML\WORKSPACES\workspace-techchallenger   # Projetos da trilha Tech Challenger
C:\FIAP\EML\WORKSPACES\workspace-visualcode       # Projetos desenvolvidos no Visual Studio Code
C:\FIAP\EML\WORKSPACES\workspace-pycharm          # Projetos desenvolvidos no PyCharm
```

Comandos para criação desta estrutura de pastas:

**1.3.1 - Windows (PowerShell ou CMD)**
```powershell
mkdir C:\FIAP\EML\WORKSPACES\workspace-techchallenger
mkdir C:\FIAP\EML\WORKSPACES\workspace-visualcode
mkdir C:\FIAP\EML\WORKSPACES\workspace-pycharm
```

**1.3.2 - Linux**

```sh
mkdir -p ~/FIAP/EML/WORKSPACES/workspace-techchallenger
mkdir -p ~/FIAP/EML/WORKSPACES/workspace-visualcode
mkdir -p ~/FIAP/EML/WORKSPACES/workspace-pycharm
```

**1.3.3 - macOS**

```sh
mkdir -p ~/FIAP/EML/WORKSPACES/workspace-techchallenger
mkdir -p ~/FIAP/EML/WORKSPACES/workspace-visualcode
mkdir -p ~/FIAP/EML/WORKSPACES/workspace-pycharm
```


Essa abordagem garante não apenas organização local, mas também clareza quando novos membros ingressarem no time, tornando a curva de aprendizado e integração mais rápida.


## 2 - Gerenciador de Pacotes: UV

O projeto utiliza o **[uv](https://docs.astral.sh/uv/)** como gerenciador de pacotes Python moderno e de alta performance.

**2.1 Instalação no Windows (PowerShell)

Execute o comando em seu terminal PowerShell como Administrador.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Após a instalação, verifique a versão:

```powershell
uv --version
```

## 3 - IDE - Integrated Development Environment

Escolha a IDE ou editor de texto de sua preferência entre as opções abaixo:

PyCharm (JetBrains)
 – recomendado para projetos complexos em Python.

Visual Studio Code (Microsoft)
 – leve, extensível e multiplataforma.

- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Microsoft Visual Code](https://code.visualstudio.com/)
- [Banco de Dados PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
- [DBeaver Community](https://dbeaver.io/download/)

## 4 - Banco de Dados
