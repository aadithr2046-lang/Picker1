from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

DEFAULT_START = 1
DEFAULT_END = 10

# Admin-controlled numbers
BASE_ALLOWED_NUMBERS = [3, 11, 22]

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Number Spinner</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{
    margin:0;
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(135deg,#667eea,#764ba2);
    font-family:Arial,sans-serif;
}
.card{
    background:#fff;
    padding:20px;
    border-radius:16px;
    width:92%;
    max-width:420px;
    text-align:center;
    box-shadow:0 20px 40px rgba(0,0,0,.3);
}
canvas{margin:20px auto;display:block}
button{
    width:100%;
    padding:14px;
    border:none;
    border-radius:30px;
    font-size:1.1rem;
    background:linear-gradient(135deg,#667eea,#764ba2);
    color:#fff;
}
.result{
    font-size:1.4rem;
    margin-top:12px;
    font-weight:bold;
}
</style>
</head>

<body>
<div class="card">
    <h2>🎡 Number Spinner</h2>

    <form method="post">
        <input type="number" name="start" value="{{ start }}" required>
        <input type="number" name="end" value="{{ end }}" required>
        <button type="submit">SPIN</button>
    </form>

    <canvas id="wheel" width="280" height="280"></canvas>

    {% if number %}
        <div class="result">🎯 Result: {{ number }}</div>
    {% endif %}
</div>

<script>
const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");

const numbers = {{ numbers }};
const colors = ["#667eea","#764ba2","#ff7675","#55efc4","#fdcb6e"];

const radius = 140;
const center = 140;

function drawWheel(){
    const angle = 2 * Math.PI / numbers.length;
    numbers.forEach((num, i)=>{
        ctx.beginPath();
        ctx.moveTo(center,center);
        ctx.arc(center,center,radius,i*angle,(i+1)*angle);
        ctx.fillStyle = colors[i % colors.length];
        ctx.fill();

        ctx.save();
        ctx.translate(center,center);
        ctx.rotate(i*angle + angle/2);
        ctx.textAlign="right";
        ctx.fillStyle="#fff";
        ctx.font="20px Arial";
        ctx.fillText(num, radius-10, 8);
        ctx.restore();
    });
}
drawWheel();
</script>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    start = DEFAULT_START
    end = DEFAULT_END
    number = None

    if request.method == "POST":
        start = int(request.form["start"])
        end = int(request.form["end"])

        allowed = [n for n in BASE_ALLOWED_NUMBERS if start <= n <= end]
        if not allowed:
            allowed = BASE_ALLOWED_NUMBERS

        number = random.choice(allowed)

    return render_template_string(
        HTML,
        start=start,
        end=end,
        number=number,
        numbers=BASE_ALLOWED_NUMBERS
    )

if __name__ == "__main__":
    app.run(debug=True)
