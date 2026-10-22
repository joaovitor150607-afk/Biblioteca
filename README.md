# Sistema de Biblioteca — Projeto 2

Projeto da disciplina Construção de Backend (IESB). Gerencia autores, livros, membros e empréstimos com regras de negócio em Django.

## Funcionalidades
- Cadastro de Autores, Livros e Membros pelo Django Admin
- Empréstimo com prazo de 14 dias e controle de estoque
- Devolução com reposição de cópia
- Indicação de empréstimos atrasados
- Relatório de livros mais emprestados com `annotate()` e `Count()`
- Testes automatizados das regras de negócio

## Como rodar no Windows (VS Code)
1. Abra esta pasta no VS Code.
2. No terminal, crie o ambiente virtual: `python -m venv venv`
3. Ative-o: `venv\Scripts\activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Crie as tabelas: `python manage.py makemigrations biblioteca` e `python manage.py migrate`
6. Crie o administrador: `python manage.py createsuperuser`
7. Inicie o servidor: `python manage.py runserver`
8. Acesse `http://127.0.0.1:8000/` e `http://127.0.0.1:8000/admin/`

## Banco de dados
Por padrão, o projeto usa SQLite para facilitar a execução local. O guia da disciplina também permite SQLite para testes. Não envie credenciais ou arquivos `.env` ao GitHub.

## Testes
Execute `python manage.py test`.

## Prints
Inclua capturas do Admin, da listagem de livros e dos empréstimos antes de publicar no GitHub.

## Autor
Preencha com seu nome — IESB 2026.
