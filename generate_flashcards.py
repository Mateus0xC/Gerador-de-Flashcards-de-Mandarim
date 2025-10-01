# type: ignore

from google import genai
from google.genai.types import Schema
from lxml import html
import json, requests, os

with open("config.json", "r", encoding="utf-8") as f:
  CONFIG = json.load(f)

LANGUAGE = CONFIG.get("LANGUAGE", "English")

prompt = '''\
Explain the Mandarin Chinese word "{word}".  
Return the answer in JSON format according to the provided schema.  

Mandatory rules:
- The field "word.meaning" must contain the main meanings of the word translated into "{language}".  
- The field "word.pinyin" must contain the full pinyin of the word.  
- The field "characters" must contain a list with **each character of the input word exactly as it appears**, in order.  
- Each character listed in "characters" must have:
  - "character": the character itself from the input word  
  - "meaning": the meaning of that character translated into "{language}" (without components or radicals).  
- Never include radicals, inner parts, or graphical decompositions.  
- All texts must be lowercase.  

IMPORTANT NOTE:  
The following examples are written in English only as a demonstration.  
All generated meanings must be in "{language}".  

Correct example (input word: "你好"):
{{
  "word": {{
    "meaning": "hello, hi",
    "pinyin": "nǐhǎo"
  }},
  "characters": [
    {{
      "character": "你",
      "meaning": "you"
    }},
    {{
      "character": "好",
      "meaning": "good, well"
    }}
  ]
}}

Correct example (input word: "她"):
{{
  "word": {{
    "meaning": "she, her",
    "pinyin": "tā"
  }},
  "characters": [
    {{
      "character": "她",
      "meaning": "she, her"
    }}
  ]
}}

Incorrect example (DO NOT do this — input word: "她"):
{{
  "word": {{
    "meaning": "she, her",
    "pinyin": "tā"
  }},
  "characters": [
    {{
      "character": "女",
      "meaning": "woman"
    }},
    {{
      "character": "也",
      "meaning": "also"
    }}
  ]
}}
'''

client = genai.Client(api_key=CONFIG.get("GEMINI_API_KEY"))

response_schema = Schema(
  type="OBJECT",
  properties={
    "word": Schema(
      type="OBJECT",
      properties={
        "meaning": Schema(type="STRING"),
        "pinyin": Schema(type="STRING"),
      },
      required=["meaning", "pinyin"],
    ),
    "characters": Schema(
      type="ARRAY",
      items=Schema(
        type="OBJECT",
        properties={
          "character": Schema(type="STRING"),
          "meaning": Schema(type="STRING"),
        },
        required=["character", "meaning"],
      )
    ),
  },
  required=["word", "characters"]
)

def get_word_info(word):
  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[{"role":"user", "parts":[{"text":prompt.format(word=word,language=LANGUAGE)}]}],
    config={
      "response_mime_type": "application/json",
      "response_schema": response_schema
    }
  )
  return response.parsed

def get_audio(word):
  return f"[sound:https://translate.google.com/translate_tts?ie=UTF-8&amp;q={word}&amp;tl=zh-CN&amp;client=tw-ob]"

def get_stroke_images(characters):
  result = ''
      
  if CONFIG.get("REMOVE_DUPLICATE_CHARACTERS", False):
    seen = set()
    characters = [char for char in characters if not (char["character"] in seen or seen.add(char["character"]))]

  for char in characters:
    url = f'https://www.strokeorder.com/chinese/{char["character"]}'
    response = requests.get(url)
    response.raise_for_status()
    tree = html.fromstring(response.content)
    img_url = tree.xpath("/html/body/div[2]/div/div[1]/div/div/div[4]/img/@src")
    
    if img_url:
      full_url = requests.compat.urljoin(url, img_url[0])
      result += f'<img src="{full_url}"> '
      
  return result

def get_character_meanings(characters):
  if CONFIG.get("REMOVE_DUPLICATE_CHARACTERS", False):
    seen = set()
    characters = [char for char in characters if not (char["character"] in seen or seen.add(char["character"]))]

  if len(characters) == 1:
    return ""
  else:
    return "<br>".join(f'{char["character"]}: {char["meaning"]}' for char in characters)


def generate_flashcard(word, info):
  fields = [
    CONFIG.get("NOTE_TYPE_NAME", "Mandarin"),  # Tipo de nota
    word,                                      # {{word}}
    info['word']['meaning'],                   # {{definition}}
    info['word']['pinyin'],                    # {{pinyin}}
    get_audio(word),                           # {{sound}}
    get_stroke_images(info['characters']),     # {{strokes}}
    get_character_meanings(info['characters']) # {{chars}}
  ]
  return "\t".join(fields) + "\n"

def write_flashcards_file(flashcards):
  content = "#separator:tab\n#html:true\n#notetype column:1\n"
  
  if not flashcards:
    return
  
  for flashcard in flashcards:
    content += ''.join(flashcard)
  
  output_folder = CONFIG.get("OUTPUT_FOLDER", ".")
  if output_folder != ".":
    os.makedirs(output_folder, exist_ok=True)
  output_file = os.path.join(output_folder, "flashcards.txt")
  
  with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)
    
  print("✅ Flashcards salvos com sucesso!")

if __name__ == "__main__":
  user_input = input("Insira as palavras (separadas por espaços): ")
      
  if user_input:
    words = user_input.split(" ")
    flashcards = []
    
    for i, word in enumerate(words):
      try:
        info = get_word_info(word)
        flashcards.append(generate_flashcard(word, info))
        print(f"🎴 Flashcard '{word}' gerado. ({i+1}/{len(words)})")
        
      except Exception as e:
        print(f"⚠️ Erro ao processar '{word}': {e}")

    write_flashcards_file(flashcards)
