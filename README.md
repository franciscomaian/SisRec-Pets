# SisRec-Pets

O projeto SisRec-Pets foi desenvolvido por Francisco Maian e Gustavo Moraes para a matéria SCC0284 - Sistemas de Recomendação voltado para a ONG Santuário Luz dos Bichos com o objetivo de criar um modelo de recomendação de animais disponíveis para adoção de acordo com as preferências do clinete.

## Pré-Requisitos

Antes de executar o programa, certifique que os seguintes softwares estão instalados na sua máquina:

- Python
- Numpy e Pandas
- FastAPI
- Uvicorn

## Executando

### Automático

1. Modifique a variável `BASE_PATH` do arquivo `rodar.bat` e excute o mesmo arquivo

2. Abra no navegador o arquivo `index.html`

### Manualmente

1. Execute no terminal de comandos, na pasta dos arquivos, o seguinte comando:

    ```bash
    uvicorn backend:app
    ```

2. Abra no navegador o arquivo `index.html`