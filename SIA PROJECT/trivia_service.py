import html
import random
from api_client import APIClient


class TriviaService:
  """Manages OpenTDB categories and parses raw JSON into playable questions."""

  CATEGORIES = {
      "VIDEO GAMES": 15,
      "ANIME & MANGA": 31,
      "COMPUTERS & TECH": 18,
      "GENERAL KNOWLEDGE": 9,
  }

  def __init__(self):
    self.client = APIClient("https://opentdb.com/api.php")

  def get_questions(self, category_name="VIDEO GAMES", amount=10):
    category_id = self.CATEGORIES.get(category_name, 15)
    params = {
        "amount": amount,
        "category": category_id,
        "type": "multiple",
    }

    success, data = self.client.get_json(params=params)
    if not success:
      return False, data

    if data.get("response_code") != 0:
      return False, "API returned no questions for this category."

    questions = []
    for item in data.get("results", []):
      correct = html.unescape(item["correct_answer"])
      incorrect = [html.unescape(ans) for ans in item["incorrect_answers"]]
      options = incorrect + [correct]
      random.shuffle(options)

      questions.append({
          "question": html.unescape(item["question"]),
          "correct": correct,
          "options": options,
          "difficulty": item["difficulty"].upper(),
      })

    return True, questions