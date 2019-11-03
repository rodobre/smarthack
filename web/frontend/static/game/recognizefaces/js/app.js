if (!localStorage['token']) {
	document.location = '//' + document.location.host;
}
var DATA;

getData();

function getData() {
	var req = new XMLHttpRequest();
	req.open('GET', '/api/view_members', true);
	req.setRequestHeader('Token', localStorage['token']);
	req.onload = function() {};
	req.onreadystatechange = function() {
		// Call a function when the state changes.
		if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
			try {
				DATA = JSON.parse(this.responseText);
			} catch (e) {
				DATA = [
					{
						name: 'Maria Jones',
						img: 'https://cdn.discordapp.com/attachments/633037289743712286/640246227778273344/woman1.jpg'
					},
					{
						name: 'James Morgan',
						img: 'https://cdn.discordapp.com/attachments/633037289743712286/640246255288844341/man1.jpg'
					},
					{
						name: 'Piers Johnson',
						img: 'https://cdn.discordapp.com/attachments/633037289743712286/640246279112359986/man2.jpg'
					},
					{
						name: 'Michael Morrison',
						img:
							'https://cdn.discordapp.com/attachments/633037289743712286/640245068313395201/testimonial-4.jpg'
					},
					{
						name: 'Luigi Martinelli',
						img:
							'https://cdn.discordapp.com/attachments/633037289743712286/640245081051234325/testimonial-5.jpg'
					}
				];
			}
		}
		GameObj.data = DATA;
		GameObj.create_new_game();
	};
	req.send(null);
}

var answers = [
	document.getElementById('answer1'),
	document.getElementById('answer2'),
	document.getElementById('answer3')
];

var challenge_img = document.getElementById('challenge-img');

var idx = -1;

// declare modal
let modal = document.getElementById('popup1');

function closeModal() {
	closeicon.addEventListener('click', function(e) {
		modal.classList.remove('show');
		startGame();
	});
}
// close icon in modal
let closeicon = document.querySelector('.close');

answers[0].onclick = handle_click;
answers[1].onclick = handle_click;
answers[2].onclick = handle_click;

var global_freeze = false;

function Game(data) {
	this.data = data;

	this.create_new_game = function() {
		this.rounds = this.data ? this.data.length : 0;
		this.current_round = 0;
		this.correct_answer = -1;
		this.correct_answers = 0;
		this.wrong_answers = 0;
		this.time = 0;
		this.starRating = 3;
		this.used_idx = [];
		this.started = true;

		if (this.rounds > 0) this.new_round();
	};

	this.end_game = function() {
		this.started = false;
		modal.style = '';
		modal.classList.add('show');

		//showing move, rating, time on modal
		document.getElementById('finalMove').innerHTML = this.correct_answers;
		document.getElementById('starRating').innerHTML = this.starRating;
		document.getElementById('totalTime').innerHTML = timer.innerHTML;

		//closeicon on modal
		closeModal();
	};

	this.new_round = function() {
		if (this.started == false) return;
		if (this.current_round == this.rounds) {
			this.end_game();
			send_stats(this.time, this.correct_answers, this.wrong_answers);
		} else {
			var i = -1;
			while (true) {
				i = Math.floor(Math.random() * this.data.length);
				if (this.used_idx.indexOf(i) < 0) break;
			}
			this.used_idx.push(i);
			var i2 = -1;
			var i3 = -1;
			while (true) {
				i2 = Math.floor(Math.random() * this.data.length);
				i3 = Math.floor(Math.random() * this.data.length);
				if (i2 != i3 && i != i2 && i != i3) break;
			}

			var c = Math.floor(Math.random() * 3);
			answers[c].innerText = this.data[i].name;
			answers[(c + 1) % 3].innerText = this.data[i2].name;
			answers[(c + 2) % 3].innerText = this.data[i3].name;
			challenge_img.src = this.data[i].img;
			this.correct_answer = c;
			this.current_round++;
		}
	};

	this.answer = async function(ans) {
		var sl = 0;
		if (ans == this.correct_answer) {
			this.correct_answers++;
			sl = 2500;
		} else {
			this.wrong_answers++;
			if (this.starRating > 1) this.starRating--;
			sl = 5000;
		}
		global_freeze = true;
		answers[this.correct_answer].classList.add('good');
		answers[(this.correct_answer + 1) % 3].classList.add('wrong');
		answers[(this.correct_answer + 2) % 3].classList.add('wrong');

		document.getElementById('goodans').innerHTML = this.correct_answers.toString() + ' Answers right';
		document.getElementById('badans').innerHTML = this.wrong_answers.toString() + ' Answers wrong';
		await sleep(sl);
		answers[this.correct_answer].classList.remove('good');
		answers[(this.correct_answer + 1) % 3].classList.remove('wrong');
		answers[(this.correct_answer + 2) % 3].classList.remove('wrong');
		this.new_round();
		global_freeze = false;
	};
}

function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

var _x_ = [ 'a' ];
var GameObj = new Game(_x_);

function handle_click() {
	if (global_freeze == true) return;
	idx = answers.indexOf(this);
	GameObj.answer(idx);
}

const SERVER_URL = document.location.host;
//const STATS_URL = 'http://' +  SERVER_URL + '/api/send_stats';
const STATS_URL = 'http://' + SERVER_URL + '/api/send_stats';
async function send_stats(t, ar, aw) {
	try {
		postData(STATS_URL, { time: t, answers_right: ar, answers_wrong: aw });
	} catch (e) {
		console.log('a');
	}
}

async function postData(url = '', data = {}) {
	var xmlhttp = new XMLHttpRequest(); // new HttpRequest instance
	xmlhttp.open('POST', url);
	xmlhttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
	xmlhttp.setRequestHeader('Token', localStorage['token']);
	xmlhttp.send(JSON.stringify(data));
}

var timer = document.querySelector('.timer');
function startTimer() {
	interval = setInterval(function() {
		if (GameObj.started == true) {
			GameObj.time++;
			timer.innerHTML = Math.floor(GameObj.time / 60) + ' mins ' + GameObj.time % 60 + ' seconds';
		} else {
			timer.innerHTML = '0 mins 0 seconds';
		}
	}, 1000);
}

startTimer();

function playAgain() {
	document.getElementById('goodans').innerHTML = GameObj.correct_answers.toString() + ' Answers right';
	document.getElementById('badans').innerHTML = GameObj.wrong_answers.toString() + ' Answers wrong';
	modal.classList.remove('show');
	GameObj.create_new_game();
}
