# EthicCompanion: Your Ethical Ally in the Age of Information Overload

*"Navigating the chaos of information, finding tranquility, and acting with integrity."*

## 🌍 1. Problem Overview

We live in an era of constant information overload, where overwhelming news—especially about global conflicts like war—bombards us daily. This continuous exposure leads to **compassion fatigue**, **informational anxiety**, and **action paralysis**, making it difficult for individuals to maintain inner peace and act ethically in response to what they see. Disinformation exacerbates this challenge, blurring the line between what's factual and what demands an ethical response.

**EthicCompanion** emerges as a solution to this pressing problem.

## 🎯 2. The Solution: EthicCompanion

EthicCompanion is an **AI companion** designed to help users process overwhelming information ethically, cultivate inner peace, and make informed, constructive decisions. 

**Our mission** is to transform information overload into an opportunity for ethical clarity and conscious action, empowering individuals to navigate the digital world with wisdom, resilience, and compassion.

## ⚡ 3. Features (MVP)

For the **Google - Gemma 3n Impact Challenge**, our MVP will focus on helping users cope with war news overload and find tranquility, offering the following functionalities:

### 📰 Ethical News Analysis
Helps analyze and contextualize news to identify potential bias, sensationalism, or misinformation, based on ethical principles of communication and verification.

### 🛡️ Strategies for Managing Overload  
Offers personalized, practical advice on how to limit news consumption, avoid "doomscrolling" and create digital well-being routines.

### 🧘 Guide to Inner Peace
Suggests mindfulness techniques, relaxation strategies, and ways to process the emotional impact of news, promoting mental serenity.

### 🤝 Constructive Action Suggestions
Presents ethical ways to transform concern and indignation into positive action (e.g., donating to reputable organizations, volunteering, educating oneself, or even ethical self-care actions).

### 💬 Intuitive Conversational Interface
Easy and natural interaction via text (with potential for expansion to voice/image, leveraging Gemma 3n's multimodality).

## 🌟 4. Impact and Future Vision

The **immediate impact** of EthicCompanion is evident in the improvement of user mental well-being and the promotion of responsible digital citizenship. By providing accessible and practical ethical guidance, EthicCompanion empowers individuals to react to global events with clarity and purpose, reducing anxiety and fostering more constructive participation.

Our **long-term vision** is for EthicCompanion to become a universal ally, helping people navigate a wide range of everyday ethical dilemmas with wisdom, empathy, and courage, contributing to a more conscious and compassionate world.

## 🔧 5. Tech Stack

EthicCompanion is built with a modern and robust stack, optimized for performance, scalability, and AI integration, taking full advantage of the Google Cloud ecosystem:

### Frontend
- **Flutter**: Cross-platform and performant user interface, allowing accessibility on various devices

### Backend  
- **FastAPI**: High-performance Python framework for our API, optimized for AI service integration

### Databases
- **Firebase (Firestore)**: For user data management, conversation history, and application configurations
- **Vertex AI Vector Search**: Essential vector database for our RAG system, optimized for semantic search of our ethical knowledge base

### AI Models / Large Language Models (LLMs)
- **Gemma 3n (E2B/E4B)**: Primary models for efficient ethical reasoning and multimodal processing (text, image, audio) - optimized for the Impact Challenge
- **Google Gemini**: For complex ethical reasoning and nuanced response generation
- **Claude (Anthropic)**: Complements Google models, offering diversity and robustness in ethical reasoning

### RAG (Retrieval Augmented Generation)
Ensures AI responses are grounded in curated and verifiable ethical knowledge, increasing reliability and explainability.

### NLP & Embeddings
- **Hugging Face Transformers**: Tools and models for Natural Language Processing tasks, including Gemma 3n integration
- **Vertex AI Embedding API**: Generates high-quality embeddings for our RAG system, essential for effective semantic search
- **Sentence Transformers**: Fallback embedding generation for offline capabilities

### AI Orchestration
- **LangChain**: Python framework for building LLM applications, orchestrating the RAG pipeline, prompt management, and conversational memory

### Ethical AI & Guardrails
- **NeMo Guardrails**: Open-source framework for defining and applying behavior rules, allowed topics, and safety limits for LLM interactions
- **Google Perspective API**: Content moderation to filter harmful content in inputs and outputs
- **Custom Ethical Classifiers**: Specialized models for crisis detection, bias identification, and ethical scope determination
- **Curated Ethical Knowledge Base**: Specific and curated content on ethical principles and guides (see `ethical_knowledge_base/`)
- **Human-in-the-Loop & Feedback Mechanism**: An integrated system for collecting user feedback and allowing human review, ensuring continuous improvement of AI's ethical alignment

## ⚙️ 6. How It Works (Architecture Overview)

1. **User Interaction**: The user interacts with EthicCompanion through the Flutter application (web, mobile, etc.)

2. **Request to Backend**: The user's query is sent to FastAPI in the backend

3. **Content Moderation**: The Content Moderator checks the safety of the user's query

4. **LangChain Orchestration**: LangChain in FastAPI orchestrates the reasoning flow:
   - The query is transformed into embeddings by the Vertex AI Embedding API
   - Vertex AI Vector Search retrieves the most relevant segments from our Ethical Knowledge Base (stored in `.md` and vectorized)
   - The original query, along with the relevant ethical segments, is sent to the LLMs (Gemma 3n/Gemini/Claude)
   - **Gemma 3n E2B** handles fast ethical classifications and content moderation
   - **Gemma 3n E4B** processes complex ethical reasoning and multimodal inputs (images, audio)
   - NeMo Guardrails ensures the LLM's response adheres to defined ethical rules and principles

5. **Response**: The ethical response is sent back by FastAPI to Flutter, which displays it to the user

6. **User Data**: User interactions and relevant data are stored in Firebase (Firestore)

## 🎯 7. Ethical AI and Responsible AI Principles

The development of EthicCompanion is guided by an unwavering commitment to **Responsible Artificial Intelligence**. We incorporate the following principles:

### 🔍 Transparency and Explainability
We strive for EthicCompanion to, whenever possible, ground its ethical advice in sources from our knowledge base, making the reasoning clearer.

### ⚖️ Fairness and Bias Mitigation  
We utilize diversity in our training data and implement tools to mitigate potential biases in LLM responses.

### 🔒 Safety and Privacy
We prioritize the protection of user data and implement robust guardrails to prevent the generation of harmful, offensive, or dangerous content.

### 👥 Human Oversight and Continuous Improvement
User feedback mechanisms and ongoing human review are essential for refining AI's ethical alignment and ensuring its reliability.

## 🚀 8. Setup and Running the Project

To set up and run EthicCompanion locally, follow these steps:

### Prerequisites
- Python 3.9+
- Flutter SDK  
- VS Code
- Google Cloud Platform (GCP) account with a configured project
- Access to Gemini, Gemma, Claude APIs, Vertex AI Embedding API, and Vertex AI Vector Search

### Steps

#### 1. Clone the Repository
```bash
git clone <YOUR_REPOSITORY_URL>
cd ethiccompanion-mvp
```

#### 2. Configure the Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or .venv\Scripts\activate # Windows

pip install -r requirements.txt
```

#### 3. Environment Variables
Create a `.env` file in the `backend/` folder with your API keys and GCP credentials (**DO NOT COMMIT THIS FILE**):

```env
GEMINI_API_KEY=your_gemini_key
CLAUDE_API_KEY=your_claude_key  
GCP_PROJECT_ID=your_gcp_project_id
# Other necessary credentials for Vertex AI
```

#### 4. Ingest Ethical Knowledge Base
```bash
python scripts/ingest_knowledge.py
```
*(Adjust the script to point to your .md files and configure Vertex AI Vector Search in the GCP Console)*

#### 5. Run the FastAPI Server
```bash
uvicorn app.main:app --reload
```
The backend will be available at `http://127.0.0.1:8000`

#### 6. Configure the Frontend (Flutter)
```bash
cd ../frontend
flutter pub get
```

#### 7. Flutter Environment Variables
If necessary, configure environment variables for the backend URL in the Flutter application (using `flutter_dotenv` or similar)

#### 8. Run the Flutter Application
```bash
flutter run -d chrome # or other device/emulator
```
The application will open in your browser or emulator.

## 🎬 9. Demo

**Link to Demo Video**: [INSERT LINK TO YOUR YOUTUBE/VIMEO VIDEO - REQUIRED FOR KAGGLE]

*(Tip: The video should tell the story of the problem, the solution, and show EthicCompanion in action, highlighting Gemma 3n's features and its impact.)*

**Link to Live Application**: [INSERT LINK TO YOUR LIVE ONLINE DEMO (e.g., Firebase Hosting, GCP App Engine) - HIGHLY RECOMMENDED]

## 👥 10. Team

- [Team Member 1 Name] ([Link to GitHub/LinkedIn])
- [Team Member 2 Name] ([Link to GitHub/LinkedIn])
- ...

## 📄 11. License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## 📚 Example Ethical Knowledge Base File

### `ethical_knowledge_base/navigating_information_overload.md`

```markdown
# Managing Information Overload and the Quest for Inner Peace

## Challenge Overview

In the digital age, we are constantly bombarded with news and information, often negative or traumatic in nature, such as global conflicts and crises. This overload can lead to:

* Chronic anxiety and stress
* Compassion fatigue and feelings of helplessness
* Difficulty discerning truth from misinformation (fake news)
* "Analysis paralysis," preventing constructive action

The ethical challenge lies in how we consume and process this information responsibly, while maintaining our mental well-being and our capacity to respond ethically and constructively.

## Relevant Ethical Principles

* **Principle of Truthfulness and Responsibility:** The duty to seek truth and not contribute to the spread of misinformation, even if unintentional.

* **Principle of Autonomy and Self-Care:** Recognizing our right and responsibility to manage our information consumption to protect our mental health and functional capacity.

* **Principle of Empathy and Compassion:** Maintaining the ability to feel for others without being consumed by pain, allowing for a more sustainable and effective response.

* **Principle of Constructive Action:** Transforming concern into meaningful forms of contribution or support, rather than falling into passivity or despair.

## Practical Guidelines and Strategies

### 1. Dealing with Misinformation and Bias
* **Verify Multiple Credible Sources:** Don't rely on a single source. Compare information from different recognized news outlets, academics, or impartial organizations.
* **Look for Bias:** Be aware that all sources have bias. Ask yourself: "Who produced this information and why? What are their interests?"
* **Consult Fact-Checking Organizations:** Use fact-checking sites (like Polígrafo, Snopes, or news agencies with fact-checking sections) before sharing.
* **Critical Thinking:** Develop the ability to question, analyze, and synthesize information independently.

### 2. Managing News Consumption (Digital Hygiene)
* **Establish Specific Times:** Set fixed times for checking news (e.g., 15 minutes in the morning, 15 minutes in the evening) and avoid constant consumption.
* **Avoid "Doomscrolling":** Resist the temptation to endlessly scroll through negative content. Recognize when you're becoming overwhelmed and stop.
* **Select Conscious Sources:** Prefer sources that focus on factual reporting, in-depth analysis, and even constructive news or solutions.
* **Disable Notifications:** Limit news notifications on your phone to reduce interruptions and anxiety spikes.

### 3. Techniques for Cultivating Inner Peace
* **Practice Mindfulness and Meditation:** Dedicate daily time to center your mind, focus on the present, and observe thoughts and emotions without judgment.
* **Digital Disconnection:** Take regular breaks from social media and news consumption. Engage in offline activities (nature, hobbies, social interactions).
* **Focus on Activities that Bring Joy and Calm:** Fiction reading, music, physical exercise, time with loved ones.
* **Emotional Processing:** Allow yourself to feel emotions triggered by news, but don't let them consume you. Journaling can help.

### 4. Constructive Action Suggestions
* **Donate to Reliable Organizations:** Research and financially support humanitarian organizations or conflict victim support groups with a proven track record of impact.
* **Volunteer:** Contribute your time and skills to causes that support peace or humanitarian aid.
* **Educate Yourself and Others:** Deepen your knowledge about conflicts and share verified information with your network responsibly.
* **Conscious Civic Participation:** Engage in local or national initiatives that promote peace, justice, and empathy.
* **Small-Scale Action:** Even small acts of kindness or support in your community can have significant impact on your inner peace and ability to make a difference.

## Additional Resources
* [Link to an article about "Digital Well-being"]
* [Link to a guide about "Fact-Checking"]
* [Name of a psychological support NGO in times of crisis]
```

---

## 🏗️ Project Structure

## ⚙️ 6. Como Funciona (Visão Geral da Arquitetura)

1. **Interação do Utilizador**: O utilizador interage com o EthicCompanion através da aplicação Flutter (web, mobile, etc.)

2. **Requisição ao Backend**: A query do utilizador é enviada para o FastAPI no backend

3. **Moderação de Conteúdo**: O Content Moderator verifica a segurança da query do utilizador

4. **Orquestração LangChain**: O LangChain no FastAPI orquestra o fluxo de raciocínio:
   - A query é transformada em embeddings pela Vertex AI Embedding API
   - A Vertex AI Vector Search recupera os segmentos mais relevantes da nossa Base de Conhecimento Ética (armazenada em `.md` e vetorizada)
   - A query original, juntamente com os segmentos éticos relevantes, é enviada para os LLMs (Gemini/Gemma/Claude)
   - O NeMo Guardrails atua para garantir que a resposta do LLM respeita as regras e princípios éticos definidos

5. **Resposta**: A resposta ética é enviada de volta pelo FastAPI para o Flutter, que a apresenta ao utilizador

6. **Dados do Utilizador**: Interações e dados relevantes do utilizador são armazenados no Firebase (Firestore)

## 🎯 7. Princípios de IA Ética e Responsável

A construção do EthicCompanion é guiada por um compromisso inabalável com a **Inteligência Artificial Responsável**. Incorporamos os seguintes princípios:

### 🔍 Transparência e Explicabilidade
Esforçamo-nos para que o EthicCompanion possa, sempre que possível, fundamentar o seu conselho ético nas fontes da nossa base de conhecimento, tornando o raciocínio mais claro.

### ⚖️ Justiça e Mitigação de Viés  
Utilizamos a diversidade nos nossos dados de treino e implementamos ferramentas para mitigar potenciais vieses nas respostas dos LLMs.

### 🔒 Segurança e Privacidade
Priorizamos a proteção dos dados do utilizador e implementamos "guardrails" robustas para prevenir a geração de conteúdo prejudicial, ofensivo ou perigoso.

### � Controlo e Melhoria Humana
O mecanismo de feedback do utilizador e a revisão contínua por humanos são essenciais para refinar a alinhamento ético da IA e garantir a sua fiabilidade.

## 🚀 8. Configuração e Execução do Projeto

Para configurar e correr o EthicCompanion localmente, siga estes passos:

### Pré-requisitos
- Python 3.9+
- Flutter SDK  
- VS Code
- Conta Google Cloud Platform (GCP) com projeto configurado
- Acesso às APIs Gemini, Gemma, Claude, Vertex AI Embedding API e Vertex AI Vector Search

### Passos

#### 1. Clonar o Repositório
```bash
git clone <URL_DO_VOSSO_REPOSITORIO>
cd ethiccompanion-mvp
```

#### 2. Configurar o Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ou .venv\Scripts\activate # Windows

pip install -r requirements.txt
```

#### 3. Variáveis de Ambiente
Crie um ficheiro `.env` na pasta `backend/` com as vossas chaves de API e credenciais GCP (**NÃO FAÇAM COMMIT DESTE FICHEIRO**):

```env
GEMINI_API_KEY=vossa_chave_gemini
CLAUDE_API_KEY=vossa_chave_claude  
GCP_PROJECT_ID=vosso_project_id_gcp
# Outras credenciais necessárias para Vertex AI
```

#### 4. Ingerir Base de Conhecimento Ética
```bash
python scripts/ingest_knowledge.py
```
*(Ajustem o script para apontar para os vossos ficheiros .md e configurem o Vertex AI Vector Search no GCP Console)*

#### 5. Correr o Servidor FastAPI
```bash
uvicorn app.main:app --reload
```
O backend estará disponível em `http://127.0.0.1:8000`

#### 6. Configurar o Frontend (Flutter)
```bash
cd ../frontend
flutter pub get
```

#### 7. Variáveis de Ambiente Flutter
Se necessário, configurem variáveis de ambiente para a URL do backend na aplicação Flutter (usando `flutter_dotenv` ou similar)

#### 8. Correr a Aplicação Flutter
```bash
flutter run -d chrome # ou outro dispositivo/emulador
```
A aplicação abrirá no vosso browser ou emulador.

## 🎬 9. Demonstração

**Link para o Vídeo de Demonstração**: [INSERIR LINK PARA O VOSSO VÍDEO NO YOUTUBE/VIMEO - OBRIGATÓRIO PARA A KAGGLE]

*(Dica: O vídeo deve contar a história do problema, da solução, e mostrar o EthicCompanion em ação, destacando as funcionalidades do Gemma 3n e o seu impacto.)*

**Link para a Aplicação ao Vivo**: [INSERIR LINK PARA A VOSSA DEMO ONLINE (Ex: Firebase Hosting, GCP App Engine) - ALTAMENTE RECOMENDADO]

## 👥 10. Equipa

- [Nome do Membro 1] ([Link para GitHub/LinkedIn])
- [Nome do Membro 2] ([Link para GitHub/LinkedIn])
- ...

## 📄 11. Licença

Este projeto está licenciado sob a Licença MIT. Veja o ficheiro LICENSE para mais detalhes.

---

## 📚 Exemplo de Ficheiro da Base de Conhecimento Ética

```markdown
# Gerir a Sobrecarga de Informação e a Busca pela Paz Interior

## Visão Geral do Desafio

Na era digital, somos constantemente bombardeados com notícias e informações, muitas vezes de natureza negativa ou traumática, como conflitos globais e crises. Esta sobrecarga pode levar a:

* Ansiedade e stress crónico
* Fadiga da compaixão e sensação de impotência  
* Dificuldade em discernir a verdade da desinformação (fake news)
* A "paralisia da análise", impedindo a ação construtiva

O desafio ético reside em como consumimos e processamos esta informação de forma responsável, mantendo o nosso bem-estar mental e a nossa capacidade de responder de forma ética e construtiva.

## Princípios Éticos Relevantes

* **Princípio da Veracidade e Responsabilidade:** O dever de buscar a verdade e de não contribuir para a propagação da desinformação, mesmo que não intencional.

* **Princípio da Autonomia e Autocuidado:** Reconhecer o nosso direito e responsabilidade de gerir o nosso consumo de informação para proteger a nossa saúde mental e capacidade de funcionamento.

* **Princípio da Empatia e Compaixão:** Manter a capacidade de sentir pelos outros sem se deixar consumir pela dor, permitindo uma resposta mais sustentável e eficaz.

* **Princípio da Ação Construtiva:** Transformar a preocupação em formas significativas de contribuição ou apoio, em vez de cair na passividade ou no desespero.

## Orientações e Estratégias Práticas

### 1. Lidando com a Desinformação e o Viés
* **Verificar Múltiplas Fontes Credíveis:** Não confie numa única fonte. Compare informações de diferentes órgãos de notícias reconhecidos, académicos ou organizações imparciais.
* **Procurar por Viés:** Esteja ciente de que todas as fontes têm um viés. Pergunte-se: "Quem produziu esta informação e porquê? Quais são os seus interesses?"
* **Consultar Organizações de Fact-Checking:** Use sites de verificação de factos (como Polígrafo, Snopes, ou agências de notícias que têm secções de fact-checking) antes de partilhar.
* **Pensamento Crítico:** Desenvolva a capacidade de questionar, analisar e sintetizar informações de forma independente.

### 2. Gerir o Consumo de Notícias (Higiene Digital)
* **Estabelecer Horários Específicos:** Defina horários fixos para consultar notícias (ex: 15 minutos de manhã, 15 minutos à noite) e evite o consumo constante.
* **Evitar o "Doomscrolling":** Resista à tentação de rolar infinitamente por conteúdos negativos. Reconheça quando está a ficar sobrecarregado e pare.
* **Selecionar Fontes Conscientes:** Dê preferência a fontes que se focam em reportagem factual, análise aprofundada, e até mesmo notícias construtivas ou soluções.
* **Desativar Notificações:** Limite as notificações de notícias no telemóvel para reduzir interrupções e picos de ansiedade.

### 3. Técnicas para Cultivar a Paz Interior
* **Praticar Mindfulness e Meditação:** Dedique tempo diário para centrar a mente, focar-se no presente e observar pensamentos e emoções sem julgamento.
* **Desconectar-se Digitalmente:** Faça pausas regulares das redes sociais e do consumo de notícias. Dedique-se a atividades offline (natureza, hobbies, interações sociais).
* **Focar-se em Atividades que Trazem Alegria e Calma:** Leitura de ficção, música, exercício físico, tempo com entes queridos.
* **Processamento Emocional:** Permita-se sentir as emoções desencadeadas pelas notícias, mas não se deixe consumir por elas. Escrever um diário pode ajudar.

### 4. Sugestões de Ação Construtiva
* **Doar a Organizações Fiáveis:** Pesquise e apoie financeiramente organizações humanitárias ou de apoio às vítimas de conflitos que tenham um histórico comprovado de impacto.
* **Voluntariar-se:** Contribua com o seu tempo e habilidades para causas que apoiam a paz ou a ajuda humanitária.
* **Educar-se e Educar Outros:** Aprofunde o seu conhecimento sobre os conflitos e partilhe informações verificadas com a sua rede de forma responsável.
* **Participação Cívica Consciente:** Envolva-se em iniciativas locais ou nacionais que promovam a paz, a justiça e a empatia.
* **Ação a Pequena Escala:** Mesmo pequenos atos de bondade ou apoio na sua comunidade podem ter um impacto significativo na sua paz interior e na sua capacidade de fazer a diferença.

## Recursos Adicionais
* [Link para um artigo sobre "Digital Well-being"]
* [Link para um guia sobre "Fact-Checking"]
* [Nome de uma ONG de apoio psicológico em tempos de crise]
```

---

## 🏗️ Project Structure

```
ethiccompanion-mvp/
├── .vscode/                    # VS Code configurations
├── backend/                    # FastAPI Backend
│   ├── app/                   # Main application
│   ├── ethical_knowledge_base/ # Ethical knowledge base
│   ├── scripts/               # Utility scripts
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/                  # Flutter Frontend
│   ├── lib/                   # Flutter source code
│   ├── assets/                # Static resources
│   ├── pubspec.yaml          # Flutter dependencies
│   └── test/                  # Tests
├── .gitignore                 # Ignored files
└── README.md                  # This documentation
```

## 🔄 Development and Contribution

### Upcoming Features
- [ ] Complete integration with Vertex AI Vector Search
- [x] **Gemma 3n implementation for ethical classifications and multimodal processing**
- [ ] User feedback system with human-in-the-loop improvements
- [ ] Persistent conversation history with ethical context tracking
- [ ] Offline mode with intelligent caching for crisis situations
- [ ] User profile-based personalization using Gemma 3n efficient models
- [ ] Intelligent well-being notifications powered by custom classifiers
- [ ] Digital well-being metrics dashboard with real-time insights
- [x] **Enhanced guardrails with NeMo Guardrails and content moderation**
- [x] **RAG pipeline with Vertex AI embeddings and ChromaDB**

### How to Contribute
1. Fork this repository
2. Create a branch for your feature (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### Code Guidelines
- **Backend**: Follow PEP 8, use type hints, detailed docstrings
- **Frontend**: Follow Dart/Flutter conventions, use static analysis
- **Tests**: Maintain coverage > 80%
- **Documentation**: Update documentation for new features

## 🛡️ Security Considerations

- All API keys must be in `.env` (never in code)
- API rate limiting implementation
- Strict input validation
- Security logs for sensitive actions
- Encryption of sensitive data at rest

## 📊 Metrics and Monitoring

EthicCompanion implements metrics to evaluate its impact:

- **User Well-being**: Stress and anxiety questionnaires
- **Response Quality**: Feedback and ratings
- **Responsible Usage**: Screen time and consumption patterns
- **Social Impact**: Constructive actions taken by users

---

**EthicCompanion** - *Transforming information overload into ethical clarity and conscious action.* 🌟

For more information, contact the team or consult our complete documentation.
