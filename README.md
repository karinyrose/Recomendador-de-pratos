# Recomendador de Pratos

Programa em Python que recomenda pratos de um cardápio de delivery com base em orçamento, preferência vegetariana e palavras-chave. Tem dois modos: um **offline baseado em regras** e um **modo IA** opcional que conversa em linguagem natural.

## Como funciona

- `cardapio.json`: base de dados com os pratos (nome, categoria, preço, tags, se é vegetariano).
- `recomendador.py`: carrega o cardápio, filtra por orçamento e restrição alimentar, pontua os pratos pelas palavras-chave e mostra os melhores.
- **Modo IA:** se a variável `ANTHROPIC_API_KEY` estiver definida, o programa envia o cardápio como contexto para um modelo de linguagem, que responde de forma conversacional recomendando apenas itens que existem no cardápio.

## Como rodar

Requer Python 3.9+.

```bash
# modo regras (não precisa de chave nem de instalar nada)
python recomendador.py

# modo IA (opcional)
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave"
python recomendador.py

# forçar o modo regras mesmo com a chave definida
python recomendador.py --regras
```

## Exemplo (modo regras)

```
Orcamento maximo em R$ (Enter para ignorar): 35
Vegetariano? (s/n): s
Palavras-chave separadas por espaco (ex: leve queijo): leve

Sugestoes pra voce:
  1. Hamburguer de Grao-de-Bico (vegetariano) - R$ 27.50
     Hamburguer vegetal com alface, tomate e molho especial.
  2. Bowl Vegano de Quinoa (vegetariano) - R$ 34.50
     Quinoa, legumes assados, homus e tahine.
```

Pratos que não combinam com nenhuma palavra-chave digitada são descartados. Em caso de empate na pontuação, o mais barato aparece primeiro.

## Conceitos praticados

- Leitura de arquivos JSON
- Funções, listas, dicionários e ordenação com `sort` e `key`
- Filtros e sistema simples de pontuação
- Uso de variáveis de ambiente
- Integração com uma API de IA (prompt de sistema + histórico de conversa)

## Próximos passos

- [ ] Testes automatizados com `pytest`
- [ ] Interface web com Streamlit ou Flask
- [ ] Mais filtros (tempo de entrega, avaliação, restrições como sem lactose)
- [ ] Busca semântica com embeddings (RAG)

## Autor

Feito por **[kariny rose vaz]**, estudante de Sistemas de Informação.
