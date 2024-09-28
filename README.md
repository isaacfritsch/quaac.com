# 1 quaac.com
![fotologopato](https://github.com/user-attachments/assets/dc8b4ba1-f960-4542-a9cd-a50ca1eeefa4)  

O quaac.com é uma plataforma colaborativa de questões, criada com o objetivo de ajudar estudantes de qualquer área a cumprirem com seus objetivos educacionais. Por meio do compartilhamento de provas anteriores, resoluções, comentários e discussões, o quaac.com se torna um ambiente perfeito para colaboração mútua e aprimoramento acadêmico, tudo de forma gratuita.

As principais tecnologias utilizadas foram:
● Django para o back-end e parte do front-end com seu sistema de
templates;  
● HTMX usado para requisições Ajax;  
● Alpine.js para adicionar interatividade e funcionalidades dinâmicas;  
● Bulma escolhido para facilitar a adição do CSS, com um estilo elegante;  
● Heroku para o deploy, que já inclui PostgreSQL [9] em seu processo de
deployment para o banco de dados SQL, aproveitando o suporte nativo do
Django ao PostgreSQL e ao uso de ORM (Object-Relational-Mapping), o que
facilita consultas e manipulação de dados;  
● Digital Ocean utilizado para o armazenamento de arquivos de mídia não
gerenciados pelo Django em produção, através de um bucket S6, facilitando
o gerenciamento de arquivos na nuvem;  
● jstree escolhido para implementar o sistema de tags em forma de árvore,
permitindo a visualização e organização hierárquica das tags;  
● Vanilla JS para receber eventos e administrar processos específicos junto ao
HTMX, utilizando JavaScript puro sem dependências adicionais;  
● WhiteNoise integrado ao Django para servir arquivos estáticos em
produção, eliminando a necessidade de um servidor separado para esse
propósito;  

# 2.1 Estrutura da Plataforma
![diagramadecasos](https://github.com/user-attachments/assets/0ecfc19a-7444-48c3-aaaa-01863ee7d2c1)  
Figura 1 - Diagrama de casos de uso da plataforma

A Figura 1 apresenta um diagrama simplificado das principais interações que o usuário pode realizar no quaac.com. O site é dividido em quatro seções principais: Home, Comunidade, Questões e Perfil do Usuário, e a seguir será explicado como cada uma dessas interações acontece em cada seção.

2.1.1 Home  
Apresenta uma descrição e informações de uso, a criação da comunidade e seu painel de seleção. As comunidades são ambientes com objetivos educacionais específicos, nos quais os usuários poderão inserir questões relacionadas a esses objetivos. A figura 2 mostra o exemplo atual de uso da Home, com uma comunidade criada, a Unicamp: para questões de provas anteriores das matérias da Unicamp.
![home](https://github.com/user-attachments/assets/3f24460f-0c03-4b09-8644-9bd82486ca10)  
Figura 2 - Página da Home do quaac.com

A barra de navegação possui alguns botões (Home, Login e Register), quando o usuário clicar no botão “Register” um modal aparecerá para inserir as informações de criação de um novo usuário. O mesmo vale para o botão “login”, para inserir as informações de login. A figura 3 mostra esses modais. O botão “Home” redireciona para a página da home.
![login](https://github.com/user-attachments/assets/1245d8eb-3925-4040-95f7-b8ddb2b3fa70)
![register](https://github.com/user-attachments/assets/0066c5ca-32f6-41b6-bfb4-fcc318a90cad)  
Figura 3 - Modais de Registro e Login no quaac.com

2.1.2 Comunidade  
Para encontrar questões o usuário poderá filtrar pelas tags criadas pelo moderador e outras opções de tags padrão: não respondidas, com comentários, com solução e todas as tags incluídas, como mostra a Figura 4. 
![comunidade](https://github.com/user-attachments/assets/c56e90c6-aa71-4cd7-b860-16a19becf0c4)  
Figura 4 - Página da comunidade Unicamp

As questões são filtradas pelas tags selecionadas e apresentadas em ordem decrescente de curtidas, um tipo simples de sistema de recomendação colaborativo. O moderador pode criar/editar tags e configurá-las em um sistema de árvores. 

2.1.3 Questão  
Qualquer usuário pode inserir uma questão clicando no botão "Adicionar nova questão", sendo redirecionado para o formulário de adição de uma nova questão, como mostra a Figura 5.
![formularioquestao](https://github.com/user-attachments/assets/8c099e2f-d9db-424c-a177-b634d052ab44)    
Figura 5 - Página do formulário para adicionar uma nova questão

Após a criação, as questões podem ser acessadas pelos usuários, que podem respondê-las, curtir, acessar soluções/comentários ou contribuir com soluções/comentários pertinentes (Figura 6). Cada solução e comentário podem ter comentários resposta.
![questao](https://github.com/user-attachments/assets/acd95321-b8b3-4cc2-8eab-7f19fbf8ec33)  
Figura 6 - Uma questão inserida por um usuário na comunidade Unicamp

2.1.4 Perfil do Usuário  
É possível editar as informações pessoais, verificar comunidades e questões criadas, questões marcadas como respondidas ou curtidas, e questões com comentários ou soluções (Figura 7). Com isso, o perfil se torna uma ferramenta importante para revisão e aprimoramento dos estudos por questões.
![perfil](https://github.com/user-attachments/assets/9815e6bc-e26d-4455-9336-826a416613ca)  
Figura 7 - Página de perfil de um usuário

Essa não foi uma descrição extensa das páginas e funcionalidades da plataforma, apenas uma descrição geral dos principais pontos.

# Instalação

## Requisitos

Antes de começar, certifique-se de que você tenha os seguintes requisitos instalados:

- **Python 3.8+**  
- **pip** (gerenciador de pacotes Python)  
- **Node.js** (para a instalação de pacotes de frontend)  

## Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento do Quaac.

### 1. Clone o Repositório
```shell
git clone https://github.com/isaacfritsch/quaac.com.git
cd quaac
```

### 2. Crie um Ambiente Virtual 
Recomendamos o uso de um ambiente virtual para isolar as dependências do projeto.
```shell
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

### 3. Instale as Dependências
Use o pip para instalar as dependências do backend e npm para o frontend.

```shell
pip install -r requirements.txt
npm install
```

Faça as migrações do Django e inicie o servidor local
```shell
python manage.py migrate
python manage.py runserver
```
  



