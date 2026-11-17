"""
Recomendador de Pratos
----------------------
Projeto simples em Python que recomenda pratos de um cardapio (cardapio.json)
com base no que a pessoa digita: orcamento, preferencia vegetariana e
palavras-chave (ex: "leve", "queijo", "peixe").

Tem dois modos:
  1) Modo regras (padrao): funciona offline, sem nenhuma chave de API.
  2) Modo IA (opcional): se existir a variavel de ambiente ANTHROPIC_API_KEY,
     um modelo de IA conversa com a pessoa usando o cardapio como contexto.
"""

import json
import os
import sys

ARQUIVO_CARDAPIO = os.path.join(os.path.dirname(__file__), "cardapio.json")


def carregar_cardapio(caminho=ARQUIVO_CARDAPIO):
    """Le o cardapio do arquivo JSON e devolve uma lista de dicionarios."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def pontuar_prato(prato, palavras):
    """
    Da uma nota ao prato: +2 para cada palavra encontrada nas tags e
    +1 para cada palavra encontrada no nome, categoria ou descricao.
    """
    pontos = 0
    texto = f"{prato['nome']} {prato['categoria']} {prato['descricao']}".lower()
    for palavra in palavras:
        if palavra in [tag.lower() for tag in prato["tags"]]:
            pontos += 2
        if palavra in texto:
            pontos += 1
    return pontos


def recomendar(cardapio, orcamento=None, vegetariano=False, palavras=None, limite=3):
    """
    Filtra o cardapio pelas restricoes (orcamento e vegetariano) e ordena os
    pratos restantes pela pontuacao das palavras-chave.
    """
    palavras = [p.strip().lower() for p in (palavras or []) if p.strip()]
    candidatos = []

    for prato in cardapio:
        if orcamento is not None and prato["preco"] > orcamento:
            continue  # estoura o orcamento
        if vegetariano and not prato["vegetariano"]:
            continue  # nao e vegetariano
        pontos = pontuar_prato(prato, palavras)
        if palavras and pontos == 0:
            continue  # o usuario pediu palavras-chave e o prato nao combina com nenhuma
        candidatos.append((pontos, prato))

    # Ordena: maior pontuacao primeiro; em empate, o mais barato primeiro
    candidatos.sort(key=lambda item: (-item[0], item[1]["preco"]))
    return [prato for _, prato in candidatos[:limite]]


def mostrar(pratos):
    """Imprime os pratos de forma amigavel."""
    if not pratos:
        print("\nNenhum prato encontrado com esses filtros. Tente outro orcamento.\n")
        return
    print("\nSugestoes pra voce:")
    for i, prato in enumerate(pratos, start=1):
        selo = " (vegetariano)" if prato["vegetariano"] else ""
        print(f"  {i}. {prato['nome']}{selo} - R$ {prato['preco']:.2f}")
        print(f"     {prato['descricao']}")
    print()


def modo_regras(cardapio):
    """Conversa simples no terminal, sem IA."""
    print("=== Recomendador de Pratos (modo regras) ===")
    print("Responda as perguntas. Ctrl+C para sair.\n")

    while True:
        entrada = input("Orcamento maximo em R$ (Enter para ignorar): ").strip()
        try:
            orcamento = float(entrada.replace(",", ".")) if entrada else None
        except ValueError:
            print("Valor invalido, ignorando orcamento.")
            orcamento = None

        vegetariano = input("Vegetariano? (s/n): ").strip().lower() == "s"
        palavras = input("Palavras-chave separadas por espaco (ex: leve queijo): ").split()

        mostrar(recomendar(cardapio, orcamento, vegetariano, palavras))

        if input("Buscar de novo? (s/n): ").strip().lower() != "s":
            print("Bom apetite!")
            break


def modo_ia(cardapio):
    """Conversa em linguagem natural usando a API da Anthropic (opcional)."""
    try:
        import anthropic
    except ImportError:
        print("Instale a biblioteca com: pip install anthropic")
        return

    cliente = anthropic.Anthropic()  # le ANTHROPIC_API_KEY do ambiente
    sistema = (
        "Voce e um assistente de um app de delivery. Recomende pratos APENAS do "
        "cardapio abaixo, citando nome e preco. Seja curto e simpatico.\n\n"
        f"CARDAPIO:\n{json.dumps(cardapio, ensure_ascii=False)}"
    )
    historico = []

    print("=== Recomendador de Pratos (modo IA) ===")
    print("Converse naturalmente. Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Voce: ").strip()
        if pergunta.lower() in ("sair", "exit", "q"):
            print("Bom apetite!")
            break
        historico.append({"role": "user", "content": pergunta})
        resposta = cliente.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=500,
            system=sistema,
            messages=historico,
        )
        texto = resposta.content[0].text
        historico.append({"role": "assistant", "content": texto})
        print(f"\nAssistente: {texto}\n")


def main():
    cardapio = carregar_cardapio()
    if os.environ.get("ANTHROPIC_API_KEY") and "--regras" not in sys.argv:
        modo_ia(cardapio)
    else:
        modo_regras(cardapio)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAte mais!")
