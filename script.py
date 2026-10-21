import sqlite3

def criar_projeto_logico():
    # Conecta ao banco de dados (cria o arquivo se não existir)
    conexao = sqlite3.connect('ecommerce.db')
    cursor = conexao.cursor()

    print("--- Inicializando o Banco de Dados (Projeto Lógico) ---")

    # 1. Criação da Tabela CLIENTES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            data_cadastro DATE DEFAULT CURRENT_DATE
        )
    ''')

    # 2. Criação da Tabela PRODUTOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
    ''')

    # 3. Criação da Tabela PEDIDOS (Relacionamento 1:N com Clientes)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedidos (
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            data_pedido DATE DEFAULT CURRENT_DATE,
            status TEXT NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
        )
    ''')

    # 4. Criação da Tabela ITENS_PEDIDO (Relacionamento N:M - Tabela Pivot)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Itens_Pedido (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido),
            FOREIGN KEY (id_produto) REFERENCES Produtos(id_produto)
        )
    ''')
    
    conexao.commit()
    print("[Sucesso] Tabelas lógicas criadas com chaves estrangeiras e integridade referencial.")

    # --- Inserção de Dados para Demonstração ---
    try:
        # Limpa dados antigos para teste limpo
        cursor.execute("DELETE FROM Itens_Pedido")
        cursor.execute("DELETE FROM Pedidos")
        cursor.execute("DELETE FROM Produtos")
        cursor.execute("DELETE FROM Clientes")

        # Inserindo Clientes
        cursor.execute("INSERT INTO Clientes (nome, email) VALUES ('Ana Silva', 'ana@email.com')")
        cursor.execute("INSERT INTO Clientes (nome, email) VALUES ('Carlos Souza', 'carlos@email.com')")
        
        # Inserindo Produtos
        cursor.execute("INSERT INTO Produtos (nome_produto, preco, estoque) VALUES ('Notebook Dell', 4500.00, 10)")
        cursor.execute("INSERT INTO Produtos (nome_produto, preco, estoque) VALUES ('Mouse Sem Fio', 150.00, 50)")

        # Inserindo um Pedido (Ana Silva comprou)
        cursor.execute("INSERT INTO Pedidos (id_cliente, status) VALUES (1, 'Processando')")
        
        # Inserindo Itens do Pedido (Ana comprou 1 Notebook e 2 Mouses)
        cursor.execute("INSERT INTO Itens_Pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES (1, 1, 1, 4500.00)")
        cursor.execute("INSERT INTO Itens_Pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES (1, 2, 2, 150.00)")

        conexao.commit()
        print("[Sucesso] Dados simulados inseridos com sucesso.")
    except sqlite3.Error as e:
        print(f"[Erro] Falha ao inserir dados: {e}")

    # --- Consulta Lógica (JOIN) ---
    print("\n--- Relatório Lógico de Vendas (Consulta SQL JOIN) ---")
    query = '''
        SELECT 
            P.id_pedido,
            C.nome AS nome_cliente,
            PR.nome_produto,
            I.quantidade,
            (I.quantidade * I.preco_unitario) AS total_item,
            P.status
        FROM Pedidos P
        JOIN Clientes C ON P.id_cliente = C.id_cliente
        JOIN Itens_Pedido I ON P.id_pedido = I.id_pedido
        JOIN Produtos PR ON I.id_produto = PR.id_produto
    '''
    
    cursor.execute(query)
    vendas = cursor.fetchall()

    for venda in vendas:
        print(f"Pedido #{venda[0]} | Cliente: {venda[1]} | Produto: {venda[2]} | Qtd: {venda[3]} | Total: R${venda[4]:.2f} | Status: {venda[5]}")

    conexao.close()

if __name__ == '__main__':
    criar_projeto_logico()
