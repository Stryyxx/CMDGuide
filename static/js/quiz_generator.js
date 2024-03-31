document.addEventListener("DOMContentLoaded", function () {
	const addQuestionBtn = document.getElementById("addQuestion");
	const generateQuizBtn = document.getElementById("generateQuiz");
	const questionsContainer = document.getElementById("questionsContainer");

	let questionIdCounter = 0;
	let choiceIdCounter = 0;

	addQuestionBtn.addEventListener("click", function () {
		questionIdCounter++;
		const questionTemplate = document.getElementById("questionTemplate");
		const questionClone = document.importNode(questionTemplate.content, true);

		// Set up the question ID for correctAnswer naming
		const correctAnswerName = "correctAnswer" + questionIdCounter;
		questionClone.querySelector(".choicesContainer").setAttribute("data-question-id", questionIdCounter);

		const addChoiceBtn = questionClone.querySelector(".addChoiceBtn");
		addChoiceBtn.addEventListener("click", function (e) {
			e.preventDefault();
			const choiceTemplate = document.getElementById("choiceTemplate");
			const choiceClone = document.importNode(choiceTemplate.content, true);

			choiceIdCounter++;
			const choiceInput = choiceClone.querySelector("input[type='text']");
			choiceInput.dataset.choiceId = choiceIdCounter;

			const correctChoiceCheckbox = choiceClone.querySelector(".correctChoiceCheckbox");
			correctChoiceCheckbox.name = correctAnswerName;
			correctChoiceCheckbox.value = choiceIdCounter;

			const deleteChoiceBtn = choiceClone.querySelector(".deleteChoiceBtn");
			deleteChoiceBtn.addEventListener("click", function (e) {
				e.preventDefault();
				deleteChoiceBtn.parentNode.remove();
			});

			addChoiceBtn.before(choiceClone);
		});

		const deleteQuestionBtn = questionClone.querySelector(".deleteQuestionBtn");
		deleteQuestionBtn.addEventListener("click", function (e) {
			e.preventDefault();
			deleteQuestionBtn.parentNode.remove();
		});

		questionsContainer.appendChild(questionClone);
	});

	generateQuizBtn.addEventListener("click", function () {
		const quizName = document.getElementById("quizName").value;
		const questions = Array.from(questionsContainer.children).map((questionDiv) => {
			const questionInput = questionDiv.querySelector('input[type="text"]');
			const choices = Array.from(questionDiv.querySelectorAll(".choice")).map((choiceDiv) => {
				const input = choiceDiv.querySelector('input[type="text"]');
				const checkbox = choiceDiv.querySelector(".correctChoiceCheckbox");
				return {
					id: parseInt(input.dataset.choiceId, 10),
					choice: input.value,
					isCorrect: checkbox.checked,
				};
			});
			return {
				question: questionInput.value,
				choices: choices,
			};
		});

		const quizData = {
			quizName: quizName,
			questions: questions,
		};

		fetch("", {
			method: "POST",
			headers: {
				"X-CSRFToken": getCookie("csrftoken"),
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				quizData: quizData,
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				if (data.success) {
					const quizId = data.quizId;
					console.log("Quiz submitted successfully with ID:", quizId);
					alert("Quiz Submitted. Quiz ID: " + quizId);
				} else alert("Server Error, try again later");
			});

		function getCookie(cname) {
			// CHATGPT generated this to isolate the csrf out of the django cookie.
			let name = cname + "=";
			let decodedCookie = decodeURIComponent(document.cookie);
			let ca = decodedCookie.split(";");
			for (let i = 0; i < ca.length; i++) {
				let c = ca[i];
				while (c.charAt(0) == " ") {
					c = c.substring(1);
				}
				if (c.indexOf(name) == 0) {
					return c.substring(name.length, c.length);
				}
			}
			return "";
		}

		console.log(JSON.stringify(quizData));
	});
});
