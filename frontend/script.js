document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
// Review page script
// Review page script
const reviewForm = document.getElementById("reviewForm");

if (reviewForm) {
  reviewForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const rating = document.querySelector('input[name="rating"]:checked').value;
    const message = document.getElementById("message").value;

    const review = { name, rating, message };

    try {
      // Send data to Python Flask backend
      const res = await fetch("http://127.0.0.1:5000/api/reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(review),
      });

      if (res.ok) {
        alert("✅ Thank you for your review, Naveen will appreciate your feedback!");
        reviewForm.reset();
      } else {
        alert("❌ Failed to submit review. Please try again.");
      }
    } catch (err) {
      alert("⚠️ Could not connect to server. Make sure Python backend is running.");
      console.error(err);
    }
  });
}

