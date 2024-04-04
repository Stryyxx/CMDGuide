document.addEventListener("DOMContentLoaded", function () {
	// Get references to DOM elements
	const addQuestionBtn = document.getElementById("addQuestion");
	const generateQuizBtn = document.getElementById("generateQuiz");
	const questionsContainer = document.getElementById("questionsContainer");

	// Initialize counters for question and choice IDs
	let questionIdCounter = 0;
	let choiceIdCounter = 0;

	// Event listener for adding a new question
	addQuestionBtn.addEventListener("click", function () {
		// Increment question ID counter
		questionIdCounter++;
		// Clone the question template
		const questionTemplate = document.getElementById("questionTemplate");
		const questionClone = document.importNode(questionTemplate.content, true);

		// Set up the question ID for correctAnswer naming
		const correctAnswerName = "correctAnswer" + questionIdCounter;
		questionClone.querySelector(".choicesContainer").setAttribute("data-question-id", questionIdCounter);

		// Event listener for adding a new choice
		const addChoiceBtn = questionClone.querySelector(".addChoiceBtn");
		addChoiceBtn.addEventListener("click", function (e) {
			e.preventDefault();
			// Clone the choice template
			const choiceTemplate = document.getElementById("choiceTemplate");
			const choiceClone = document.importNode(choiceTemplate.content, true);

			// Increment choice ID counter
			choiceIdCounter++;
			// Set the choice ID for data attribute
			const choiceInput = choiceClone.querySelector("input[type='text']");
			choiceInput.dataset.choiceId = choiceIdCounter;

			// Set up correct choice checkbox
			const correctChoiceCheckbox = choiceClone.querySelector(".correctChoiceCheckbox");
			correctChoiceCheckbox.name = correctAnswerName;
			correctChoiceCheckbox.value = choiceIdCounter;

			// Event listener for deleting a choice
			const deleteChoiceBtn = choiceClone.querySelector(".deleteChoiceBtn");
			deleteChoiceBtn.addEventListener("click", function (e) {
				e.preventDefault();
				deleteChoiceBtn.parentNode.remove();
			});

			// Append the choice to the choices container
			addChoiceBtn.before(choiceClone);
		});

		// Event listener for deleting a question
		const deleteQuestionBtn = questionClone.querySelector(".deleteQuestionBtn");
		deleteQuestionBtn.addEventListener("click", function (e) {
			e.preventDefault();
			deleteQuestionBtn.parentNode.remove();
		});

		// Append the question to the questions container
		questionsContainer.appendChild(questionClone);
	});

	// Event listener for generating the quiz
	generateQuizBtn.addEventListener("click", function () {
		// Get quiz name and questions data
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

		// Prepare quiz data for submission
		const quizData = {
			quizName: quizName,
			questions: questions,
		};

		// Fetch request to submit quiz data
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

		// Function to retrieve CSRF token from cookie
		function getCookie(cname) {
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

		// Log the quiz data for debugging purposes
		console.log(JSON.stringify(quizData));
	});
});
