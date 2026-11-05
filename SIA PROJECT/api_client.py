import requests


class APIClient:
  """Handles raw HTTP GET requests and network error handling."""

  def __init__(self, base_url, timeout=8):
    self.base_url = base_url
    self.timeout = timeout

  def get_json(self, params=None):
    try:
      response = requests.get(
          self.base_url, params=params, timeout=self.timeout
      )
      response.raise_for_status()
      return True, response.json()
    except requests.RequestException as e:
      return False, f"Network/API Error: {e}"