# Coleta de Fundos de Investimento - CVM

Este projeto coleta dados diários de fundos de investimento diretamente da CVM.

## Funcionalidades

- Download de arquivos mensais de fundos (.zip)
- Extração de informações como: data, valor da cota, patrimônio, aportes e resgates
- Junção com cadastro oficial da CVM contendo tipo e nome do fundo

## Como usar

```bash
pip install -r requirements.txt
python src/coleta_fundos_cvm.py
```

## Updating the Repository

To ensure you have the latest changes from the repository, use the following command:

```bash
git pull
```

This will fetch and merge changes from the remote repository into your local copy.

## Synchronizing the Repository

To synchronize your local repository with the remote repository, you can use the following commands:

```bash
git fetch
git merge
```

The `git fetch` command retrieves the latest changes from the remote repository without modifying your working directory. The `git merge` command applies those changes to your current branch.

## Fonte dos dados

[CVM - Dados Abertos](https://dados.cvm.gov.br/dados/FI/)


## Analises

[Maiores resgates e aportes](src/analise/analise_v01.html)