const alertMessage = document.getElementById("alert");
const previousButton = document.getElementById("previous");
const nextButton = document.getElementById("next");
const tryAgainButton = document.getElementById("try-again");
const welcomeButton = document.querySelector("#welcome-button");
let loading = false;

let questions = [];
let answers = [];

let url = '/api';

function getData() {
  return new Promise((resolve, reject) => {
    loading = true;
    fetch(url, {
      method: 'GET',
    })
      .then((res) => res.json())
      .then(({data}) => {
        questions = data.map((question, index) => ({
          id: index + 1,
          title: question.question,
          choices: [
            {
              title: question.option_a,
              value: "A",
              correct: question.answer === "A"
            },
            {
              title: question.option_b,
              value: "B",
              correct: question.answer === "B"
            },
            {
              title: question.option_c,
              value: "C",
              correct: question.answer === "C"
            },
          ]
        }))
        answers = questions.map((question) => ({
          question: question.id,
          answer: "",
        }));
        resolve();
      })
      .catch((error) => {
        console.log("ERROR :>> ", error);
        alertMessage.innerHTML = error.message;
        alertMessage.classList.add("error");
        reject();
      })
      .finally(() => {
        loading = false;
      });
  });
}

let currentQuestionId = 1;

tryAgainButton.addEventListener("click", async function () {
  answers = [];
  questions = [];
  await getData();
  showQuestion(1);
  const resultScreen = document.getElementById("result");
  const quizScreen = document.getElementById("quiz");
  resultScreen.classList.remove("show");
  nextButton.innerText = "next";
  quizScreen.classList.add("show");
});

previousButton.addEventListener("click", () => {
  if (currentQuestionId <= 1) return;
  currentQuestionId = --currentQuestionId;
  showQuestion(currentQuestionId);
});

nextButton.addEventListener("click", () => {
  if (currentQuestionId === questions.length) {
    showResult();
  } else {
    currentQuestionId = ++currentQuestionId;
    showQuestion(currentQuestionId);
  }
});

welcomeButton.addEventListener("click", async function () {
  // Check if the alert box is open and close it
  if (
    alertMessage.innerHTML !== "" ||
    alertMessage.classList.contains("success") ||
    alertMessage.classList.contains("error")
  ) {
    alertMessage.classList.remove("success", "error");
    alertMessage.innerHTML = "";
  }
  const welcomeName = document.querySelector("#welcome-name");
  // Check if the user did not input a name
  if (!welcomeName.value) {
    alertMessage.innerHTML = "Please provide a name before proceeding!";
    alertMessage.classList.add("error");
  } else {
    // Close the welcome screen
    // and open the question screen
    const welcome = document.querySelector("#welcome");
    const quiz = document.querySelector("#quiz");
    welcome.classList.add("hide");
    quiz.classList.add("show");
    // Store the username
    let usernameElement = document.getElementById("username");
    usernameElement.innerText = welcomeName.value;
    await getData();
    showQuestion(1);
  }
});

function storeAnswer(questionId, answer) {
  const choice = answers.find((answer) => answer.question === questionId);
  const index = answers.indexOf(choice);
  answers[index] = {
    ...choice,
    // answer: answer
    answer,
  };
}

function showQuestion(id) {
  const question = questions.find((item) => item.id === id);
  currentQuestionId = id;
  if (question) {
    const questionElement = document.getElementById("question");
    questionElement.innerHTML = `${id}/${questions.length}. ${question.title}`;
    const choicesElement = document.getElementById("choices");

    // Get the user answer for this question
    const answer = answers.find((item) => item.question === question.id);

    const choices = question.choices.map(
      (choice) =>
        `
        <div class="choice">
          <input ${
            answer.answer === choice.value ? "checked" : ""
          } onclick="storeAnswer(${question.id}, '${
          choice.value
        }')" type="radio" id="${choice.value}" name="choice" value="${
          choice.value
        }" />
          <label onclick="storeAnswer(${question.id}, '${
          choice.value
        }')" for="${choice.value}">${choice.title}</label>
        </div>
      `
    );
    choicesElement.innerHTML = choices.join("");
    // if first question remove the previous button else show the next button
    if (id === 1) {
      previousButton.classList.add("hide");
    } else {
      // show the previous and next buttonp
      previousButton.classList.remove("hide");
      nextButton.classList.remove("hide");
      nextButton.innerText = "next";
    }

    if (id === questions.length) {
      nextButton.innerText = "Submit";
    } else {
    }
    // if last question change the next button to submit button
  }
}

function showResult() {
  const quizScreen = document.getElementById("quiz");
  const welcomeScreen = document.getElementById("welcome");
  const resultScreen = document.getElementById("result");

  const resultText = document.getElementById("result-text");

  let total = 0;

  answers.forEach((answer) => {
    const question = questions.find((item) => item.id === answer.question);
    const correctAnswer = question.choices.find(
      (item) => item.correct === true
    );

    if (correctAnswer?.value === answer?.answer) total++;
  });

  resultText.innerText = parseInt((total / questions.length) * 100);

  quizScreen.classList.remove("show");
  welcomeScreen.classList.add("hide");
  resultScreen.classList.add("show");
}
