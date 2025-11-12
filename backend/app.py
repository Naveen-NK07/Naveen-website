from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

# ---------- EMAIL FUNCTION ----------
def send_email(name, rating, message):
    sender = "naveenparthipan07@gmail.com"     # your Gmail
    receiver = "naveenparthipan07@gmail.com"   # where you receive reviews
    password = "vxvzwzhugiynxbqe"              # Gmail App Password (not normal password)

    subject = f"New Review from {name}"
    body = f"""
    Name: {name}
    Rating: {rating} stars
    Message: {message}
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("📧 Email sent successfully!")
    except Exception as e:
        print("❌ Email send failed:", e)


# ---------- API ENDPOINTS ----------

@app.route("/api/reviews", methods=["POST"])
def add_review():
    try:
        data = request.json
        name = data.get("name")
        rating = int(data.get("rating", 0))
        message = data.get("message")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("📥 Received review:", name, rating, message)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reviews (name, rating, message, date)
            VALUES (%s, %s, %s, %s)
        """, (name, rating, message, date))
        conn.commit()
        cursor.close()
        conn.close()

        send_email(name, rating, message)

        return jsonify({"message": "Review added successfully!"}), 201

    except Exception as e:
        print("❌ Error adding review:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reviews ORDER BY id DESC")
        reviews = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(reviews)
    except Exception as e:
        print("❌ Error fetching reviews:", e)
        return jsonify({"error": str(e)}), 500


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)

