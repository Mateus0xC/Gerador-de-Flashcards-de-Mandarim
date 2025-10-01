# Gerador de Flashcards de Mandarim

Este projeto gera flashcards prontos para importar no **Anki**, usando a API do Gemini para obter definições, pinyin e dados de caracteres.

---

## 📦 Requisitos

Antes de rodar o programa, é necessário ter o **Python 3.10+** instalado.  
Também é preciso instalar as dependências:

```bash
pip install google-genai lxml requests
```

---

## 🃏 Configuração no Anki

### ✅ Recomendado (automático)

1. Abra o Anki.  
2. Arraste o arquivo `exemplo.apkg` para a seção **Baralhos**.  
3. Isso vai criar automaticamente:  
   - Um baralho chamado **Mandarim**  
   - Uma nota de exemplo **“你好”** com três cartões relacionados

> Você pode excluir essa nota de exemplo depois — o **tipo de nota** e os **modelos de cartão** continuarão salvos.  
> Depois disso, você pode **renomear o tipo de nota** e também **editar os modelos de cartão** conforme desejar.  
> Lembre-se: o nome do tipo de nota deve sempre bater com o valor de `NOTE_TYPE_NAME` no `config.json`.  

<details>
<summary>📝 <b>Configuração manual</b> (clique para abrir)</summary>

1. No Anki, vá em:  
   **Adicionar → Escolher tipo → Gerenciar → Adicionar → Duplicar: Básico**  
2. Renomeie para o mesmo valor definido em `NOTE_TYPE_NAME` (do `config.json`).  
3. Selecione o tipo de nota que acabou de criar → **Campos** → adicione os seguintes campos na ordem exata:  
   `word`, `definition`, `pinyin`, `sound`, `strokes`, `chars`  
4. Clique em **Salvar**.  
5. Depois de gerar um flashcard qualquer, importe-o no Anki.  
6. Vá até o **Painel**.  
7. Localize a nota recém-importada e clique em **Editar**.
8. Ver abaixo como **editar modelos de cartão**.

</details>

<details>
<summary>✏️ <b>Editar modelos de cartão</b> (clique para abrir)</summary>

Dentro do editor de nota, clique em **Cartões...** para abrir as opções de modelos.  
Nos modelos, você pode usar os seguintes placeholders:  

- `{{word}}` → a palavra em mandarim  
- `{{definition}}` → o significado da palavra  
- `{{pinyin}}` → o pinyin da palavra  
- `{{sound}}` → o áudio de pronúncia da palavra  
- `{{strokes}}` → imagens da ordem dos traços de cada caractere (pode ficar vazio se não encontrado)  
- `{{chars}}` → lista com cada caractere da palavra e seu significado individual <b>(fica vazio se a palavra tiver apenas um caractere)</b>

Você pode organizar os modelos de cartão do jeito que quiser.  
Use `<br>` para inserir quebras de linha no layout.
</details>

---

## ⚙️ Configuração do projeto

Edite o arquivo **`config.json`** incluído no projeto:

```json
{
  "GEMINI_API_KEY": "Sua chave de API aqui",
  "LANGUAGE": "Português (Brasil)",
  "NOTE_TYPE_NAME": "Mandarin"
}
```

- **`GEMINI_API_KEY`** → cole aqui sua chave da API Gemini  
- **`LANGUAGE`** → o idioma de tradução desejado (ex.: `Português (Brasil)`)  
- **`NOTE_TYPE_NAME`** → o nome do tipo de nota que será usado no Anki (Padrão: `Mandarin`)

<details>
<summary>🔑 <b>Como obter sua chave da API Gemini</b> (clique para abrir)</summary>

1. Acesse o [console de API da Gemini](https://aistudio.google.com/) ou abra diretamente a seção de **API Keys**.  
2. Faça login com sua conta Google.  
3. Clique em **Criar chave de API** / **Create API Key**.  
4. Copie o valor gerado e cole em `GEMINI_API_KEY` dentro do `config.json`.  

> Observação: o caminho exato pode variar, mas procure por “API Keys” ou “Credentials” no console da Gemini.
</details>

---

## 🚀 Uso

1. Execute o arquivo `generate_flashcards.py`

2. Digite os caracteres da palavra chinesa a ser estudada **(pinyin não é permitido)**.  
   - Para gerar múltiplos cards, separe as palavras com espaço.

3. O programa vai gerar um arquivo chamado **`flashcards.txt`**.

4. Arraste o `flashcards.txt` para dentro do Anki (na seção **Baralhos**).
