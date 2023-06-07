## Clonagem do repositório e configuração inicial:
- Certifique-se de ter um servidor MySQL em execução em seu próprio computador na porta 3306. É recomendado ter um usuário "root" com uma senha vazia, conforme o exemplo abaixo:

```python
import mysql.connector

conn = mysql.connector.connect(
  user='root',
  host='localhost',
  password=''
)
```

- Caso alguma dessas configurações esteja diferente em seu ambiente, por favor, altere conforme necessário.

## Instalação de pacotes necessários:
1. **tkinter**
2. **mysql.connector**

Para instalar esses pacotes, execute o seguinte comando:

```python
pip install tk mysql-connector-python
```

## Funcionalidades do aplicativo:
- Digite um nome e um código para o cliente.
- Ao clicar no botão "Validar", o aplicativo realizará uma consulta para tentar localizar o usuário no banco de dados. Se a consulta falhar, um pop-up de erro será exibido.
- Ao clicar no botão "Registrar", será realizado um INSERT no banco de dados para cadastrar o cliente com seu respectivo código.
- Os clientes cadastrados serão listados abaixo, permitindo que sejam editados ou excluídos conforme necessário.
