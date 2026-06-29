const queryInput = document.getElementById("queryInput");
const searchButton = document.getElementById("searchButton");
const answerText = document.getElementById("answerText");
const statusText = document.getElementById("statusText");

async function searchQuery() {
  const question = queryInput.value.trim();

  if (!question) {
    statusText.textContent = "Please enter a question.";
    answerText.textContent = "";
    queryInput.focus();
    return;
  }

  searchButton.disabled = true;
  queryInput.disabled = true;
  statusText.textContent = "Searching...";
  answerText.textContent = "Thinking...";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    answerText.textContent = data.answer || "No answer returned.";
    statusText.textContent = "Done";
  } catch (error) {
    answerText.textContent = "Sorry, something went wrong while getting the answer.";
    statusText.textContent = error.message;
  } finally {
    searchButton.disabled = false;
    queryInput.disabled = false;
    queryInput.focus();
  }
}

searchButton.addEventListener("click", searchQuery);

queryInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    searchQuery();
  }
});