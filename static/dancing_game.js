

let truckCount = 0;
let spkrcount = 0;

function requisitionTruck() {
    // 1 - Show the hidden "speakers" section
    document.getElementById('speakers').style.display = 'block';

    // 2 - Increment the truck counter
    truckCount += 1;
    document.getElementById('truckCount').innerText = `Trucks: ${truckCount}`;

    // 3 - Change button label
    const button = document.getElementById('requisition-btn');
    button.innerText = 'Add another truck';
}


function requisitionspker() {
    if (spkrcount === 0) {
    // 1 - Show the hidden "target" section
    document.getElementById('target').style.display = 'block';
    document.getElementById('spkrcount').style.display = 'block';

    // 2 - Increment the speaker counter
    spkrcount += 1;
    document.getElementById('spkrcount').innerText = `Speakers: ${spkrcount}`;

    // 3 - Hide the boss button
    document.getElementById('quest-text').style.display = 'none';
    document.getElementById('spkr-1').style.display = 'none';

    const button = document.getElementById('spkr-2');
    button.innerText = 'Add another speaker';
    } else {

    spkrcount += 1;
    document.getElementById('spkrcount').innerText = `Speakers: ${spkrcount}`;


    }    
}


function searchLocation() {
    const input = document.getElementById('locationInput').value.trim().toLowerCase();
    const resultDiv = document.getElementById('locationResult');

    // Dummy data for now, you can replace these with real data later
    const locations = {
        "test": {
            name: "Testland",
            population: 100,
            places: ["Test1", "Test2", "Test3"]
        },
        // Add other mock locations here if you want
        "sample": {
            name: "Sample City",
            population: 250000,
            places: ["Sample Park", "Sample Mall", "Sample Beach"]
        }
    };

    // Check if the location exists in the dummy data
    if (locations[input]) {
        const locationData = locations[input];
        resultDiv.innerHTML = `
            <p><strong>Location:</strong> ${locationData.name}</p>
            <p><strong>Population:</strong> ${locationData.population}</p>
            <p><strong>Places within 5 miles:</strong> ${locationData.places.join(", ")}</p>
        `;
    } else {
        resultDiv.innerHTML = `<p>No data found for "${input}".</p>`;
    }
}

function sendToFlask(population) {
    fetch('/your-flask-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ population: population })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

//--------------------------------------------------------------------------------------//
//Sequencer MiniGame
//--------------------------------------------------------------------------------------//
document.addEventListener("DOMContentLoaded", function() {

let sequence = new Array(16).fill(false); // 16 steps initialized to false (off)
let audioContext = new (window.AudioContext || window.AudioContext)();
let intervalId = null;
let kick = new Audio("static/Sounds/Kick808.wav");
// kick.preload = "auto"; // Preload the audio
let time = 100


document.querySelectorAll('.step').forEach(button => {
  button.addEventListener('click', () => {
    const stepIndex = button.getAttribute('data-step') - 1;
    sequence[stepIndex] = !sequence[stepIndex]; // Toggle the step
    button.classList.toggle('active', sequence[stepIndex]);
  });
});

// Sequencer logic
document.getElementById('playBtn').addEventListener('click', () => {
  if (intervalId) return; // Prevent multiple intervals

  let currentStep = 1;
  const totalSteps = 16;

  intervalId = setInterval(() => {
    // Remove 'playing' class from all steps
    document.querySelectorAll('.step').forEach(btn => {
      btn.classList.remove('playing');
    });

    const currentBtn = document.querySelector(`.step[data-step="${currentStep}"]`);
    if (currentBtn) {
      currentBtn.classList.add('playing');
      if (currentBtn.classList.contains('active')) {
        playkick();
      }
    }

    currentStep++;
    if (currentStep > totalSteps) {
      currentStep = 1;
    }
  }, time);
});

// STOP
document.getElementById('stopBtn').addEventListener('click', () => {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;

    // Remove all borders when stopped
    document.querySelectorAll('.step').forEach(btn => {
      btn.classList.remove('playing');
    });
  }
});


document.getElementById('clearBtn').addEventListener('click', () => {
  sequence.fill(false);
  document.querySelectorAll('.step').forEach(button => button.classList.remove('active'));
});

function playSound() {
  const oscillator = audioContext.createOscillator();
  oscillator.type = 'sine'; // sine wave
  oscillator.frequency.setValueAtTime(440, audioContext.currentTime); // A4 note
  oscillator.connect(audioContext.destination);
  oscillator.start();
  oscillator.stop(audioContext.currentTime + 0.1); // Short burst sound
}

function playkick() {
  kick.pause(); // Stop the previous kick (if playing)
  kick.currentTime = 0; // Reset the playback to the beginning
  kick.play();
  console.log(kick.duration);
}




})