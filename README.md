# FIAP - Faculdade de Informática e Administração Paulista 

<p align="center">
<a href="https://www.fiap.com.br/"><img src="Assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

# Construindo uma Máquina Agrícola: Gestão de agronegócio

## 👨‍🎓 Integrantes: 
- João José Domingues Silva
- Lais Londo Claus
- Murilo Santana
- Lucas Alves Ladeira

## 👩‍🏫 Professores:
### Tutor(a) 
- [Lucas Gomes Moreira](https://www.linkedin.com/company/inova-fusca)
### Coordenador(a)
- [Nome do Coordenador](https://www.linkedin.com/company/inova-fusca)

## 📜 Descrição

*Este projeto simula um sistema de irrigação inteligente para agricultura de precisão, integrando sensores físicos (simulados) a um microcontrolador ESP32. O objetivo é coletar dados de sensores de umidade, nutrientes e pH, controlar uma bomba de irrigação (relé/LED) e armazenar os dados em um banco de dados SQL para análise posterior. O projeto também implementa operações CRUD e permite a visualização e manipulação dos dados via interface de terminal.*

---

## 📁 Estrutura de pastas

- **ProjetoMaquinaAgricola/**: Pasta principal do projeto, contendo todo o código-fonte, scripts Python, arquivos do ESP32, banco de dados e documentação.
  - **src/**: Código-fonte do ESP32 (lógica de sensores e controle).
  - **Database/**: Scripts Python para manipulação do banco de dados SQLite, arquivo de dados e banco gerado.
  - **Assets/**: Imagens e diagramas do circuito.
  - **terminal_interface.py**: Interface de menu interativo para o usuário manipular os dados.
  - **README.md**: Guia e explicação geral sobre o projeto (este arquivo).

---

## 📖 Tutorial e detalhes do projeto

O tutorial completo de uso, detalhes do circuito, lógica de funcionamento, exemplos de dados, justificativa do modelo de dados e instruções de execução estão disponíveis no arquivo [README.md](/Documents/README.md) dentro da pasta `Documents`.

---

## 🗃 Histórico de lançamentos

* 1.0.0 - 21/04/2025

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
