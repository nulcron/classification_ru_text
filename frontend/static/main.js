window.addEventListener("load", async () => {
  const btn = document.getElementById("btn-send");
  btn.addEventListener("click", classificationText);
})

async function classificationText() {
  const input = document.getElementById("input-text");
  const error = document.getElementById("error");
  const result = document.getElementById("result");
  const resultSpan = document.getElementById("result-text");
  let text = input.value;

  if ('' == text || 150 > text.length) {
    error.textContent = "Напишите текст для классификации, объёмом не менее 150 символов.";
    error.style = "display: block";
  }
  else {
    error.style = "display: none";

    try {
      const response = await postData(text);
      
      if(response.error)
      {
        error.textContent = response.result;
        error.style = "display: block";
      }
      else
      {
        error.style = "display: none";
        result.style = "display: block";
        resultSpan.textContent = response.result;
        resultSpan.style = "display: block";
      }

    } catch (error) {
      error.textContent = "Непредвиденная ошибка.";
      error.style = "display: block";
    }
  }


}

async function postData(text) {
  data = { 
    text: text
  }

  const response = await fetch("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return await response.json();
}