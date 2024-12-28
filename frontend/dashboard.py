```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html', trades=get_trade_history())

def get_trade_history():
    # Fetch trade history from the blockchain
    return []

if __name__ == '__main__':
    app.run(debug=True)
```
