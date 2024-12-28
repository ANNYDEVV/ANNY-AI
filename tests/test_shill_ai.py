```python
import unittest
from app.shill_ai import ShillAI

class TestShillAI(unittest.TestCase):
    def test_evaluate_thesis(self):
        ai = ShillAI("test_handle", "test_wallet", "test_endpoint")
        result = ai.evaluate_thesis("This is a strong investment thesis.")
        self.assertIn("compelling", result.lower())

    def test_execute_trade(self):
        ai = ShillAI("test_handle", "test_wallet", "test_endpoint")
        response = ai.execute_trade("test_token_address")
        self.assertEqual(response, "Trade executed")

if __name__ == '__main__':
    unittest.main()
```
