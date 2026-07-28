# IADT - Análise Inteligente de Ameaças em Diagramas de Arquitetura

Sistema para automação da modelagem de ameaças em diagramas de arquitetura utilizando Visão Computacional e a metodologia STRIDE.

O projeto identifica automaticamente componentes arquiteturais em diagramas de sistemas por meio de um modelo YOLO treinado especificamente para esse domínio. Após a detecção, é realizada uma análise preliminar baseada na metodologia STRIDE, gerando automaticamente um relatório em PDF contendo as ameaças identificadas e recomendações de mitigação.

> **Projeto Acadêmico**  
> Trabalho de Conclusão de Curso (TCC)

---

## Funcionalidades

- Upload de diagramas de arquitetura através de uma interface web
- Detecção automática de componentes utilizando YOLO (Ultralytics)
- Análise de ameaças baseada na metodologia STRIDE
- Geração automática de relatório em PDF
- Interface intuitiva desenvolvida com Streamlit

---

## Fluxo da Aplicação

O funcionamento da aplicação segue o fluxo abaixo:

```text
Diagrama de Arquitetura
          │
          ▼
Detecção de Objetos (YOLO)
          │
          ▼
Componentes Detectados
          │
          ▼
Motor de Regras STRIDE
          │
          ▼
Análise de Ameaças
          │
          ▼
Relatório em PDF
```

---

## Estrutura do Projeto

```text
IADT/
│
├── app.py                  # Aplicação Streamlit
├── requirements.txt
├── README.md
│
├── models/
│   └── best.pt             # Modelo YOLO treinado
│
├── src/
│   ├── analyzer.py
│   ├── architecture.py
│   ├── models.py
│   ├── report.py
│   └── stride.py
│
├── data/
│
└── tests/
```

---

## Instalação

Clone o repositório

```bash
git clone https://github.com/seu-usuario/IADT.git
cd IADT
```

Crie um ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Executando a Aplicação

Inicie a aplicação com o Streamlit:

```bash
streamlit run app.py
```

A interface será aberta automaticamente no navegador.

---

## Dataset

O modelo de detecção foi treinado utilizando o seguinte conjunto de dados:

https://huggingface.co/datasets/guillherms/stride-architecture-components-v1

---

## Componentes Suportados

Atualmente o modelo é capaz de identificar os seguintes componentes arquiteturais:

- Usuário
- Servidor
- Processo
- Banco de Dados
- Armazenamento
- Firewall
- Balanceador de Carga
- Sistema Externo

---

## Modelagem de Ameaças

A identificação das ameaças é baseada na metodologia **STRIDE**, proposta pela Microsoft.

As categorias analisadas são:

- Spoofing
- Tampering
- Repudiation
- Information Disclosure
- Denial of Service
- Elevation of Privilege

A análise é realizada por meio de uma base de regras previamente definida, que relaciona cada componente arquitetural às possíveis ameaças e respectivas recomendações de mitigação.

---

## Limitações

Este projeto realiza uma **análise baseada exclusivamente nos componentes detectados**.

Atualmente, a aplicação **não é capaz de**:

- Identificar fluxos de dados (*Data Flows*)
- Detectar *Trust Boundaries*
- Inferir relacionamentos entre componentes
- Interpretar protocolos de comunicação
- Substituir uma modelagem de ameaças completa realizada por especialistas

Portanto, os resultados devem ser interpretados como uma **análise preliminar de apoio**, auxiliando arquitetos de software e profissionais de segurança durante as fases iniciais do processo de modelagem de ameaças.

---

## Tecnologias Utilizadas

- Python
- Streamlit
- Ultralytics YOLO
- OpenCV
- Pillow
- ReportLab

---

## Trabalhos Futuros

Como possibilidades de evolução do projeto destacam-se:

- Detecção automática de fluxos de dados
- Identificação de Trust Boundaries
- Suporte a OCR para leitura de textos dos diagramas
- Compreensão estrutural do diagrama através de grafos
- Integração com Modelos de Linguagem (LLMs)
- Suporte a novos componentes arquiteturais
- Ampliação da base de regras STRIDE

---

## Autor

**Filipe Mendes**

Trabalho de Conclusão de Curso

Tecnólogo em Análise e Desenvolvimento de Sistemas

---

## Licença

Este projeto foi desenvolvido para fins acadêmicos e educacionais.