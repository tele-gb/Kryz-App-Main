

let truckCount = 0;
let spkrcount = 0;
let potdancers = 0;
let dncrcount = 0;

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
        document.getElementById('dropbeat').style.display = 'block';
        potdancers += locationData.population;
        console.log(locationData.population,potdancers)
        document.getElementById('pot_dancers').innerText = `Potential Dancers: ${potdancers}`;
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

function revealsequencer() {
  // 1 - Show the hidden "speakers" section
  document.getElementById('sequencer').style.display = 'block';

  // // 2 - Increment the truck counter
  // truckCount += 1;
  // document.getElementById('truckCount').innerText = `Trucks: ${truckCount}`;

  // // 3 - Change button label
  // const button = document.getElementById('requisition-btn');
  // button.innerText = 'Add another truck';
}

//--------------------------------------------------------------------------------------//
//Sequencer MiniGame
//--------------------------------------------------------------------------------------//
document.addEventListener("DOMContentLoaded", function() {

// =======================
// Initialization
// =======================
let sequence = new Array(16).fill(false); // 16 steps initialized to false
let audioContext = new (window.AudioContext || window.webkitAudioContext)();
let kick = new Audio("static/Sounds/Kick808.wav");
let snare = new Audio("static/Sounds/ClapDMX.wav");
let hat = new Audio("static/Sounds/Hihat.wav");

let bpmSlider = document.getElementById("BPM");
let bpmDisplay = document.getElementById("bpmDisplay");
let bpm = parseInt(bpmSlider.value);
bpmDisplay.textContent = bpm;

let isPlaying = false;
let currentStep = 1;
const totalSteps = 16;

// =======================
// Utility Functions
// =======================
function bpmcalc(bpm) {
  const time = (1 / (bpm / 60)) * 250;
  console.log(`Beat duration: ${time} ms`);
  return time;
}

function playkick() {
  kick.pause();         // Stop any current playback
  kick.currentTime = 0; // Rewind to start
  kick.play();
  console.log("KIK: " + Date.now());
}

function playsnare() {
  snare.pause();         // Stop any current playback
  snare.currentTime = 0; // Rewind to start
  snare.volume = 0.30
  snare.play();
  console.log("SNARE: " + Date.now());
}

function playhat() {
  hat.pause();         // Stop any current playback
  hat.currentTime = 0; // Rewind to start
  hat.play();
  console.log("HAT: " + Date.now());
}

function playSound() {
  const oscillator = audioContext.createOscillator();
  oscillator.type = 'sine';
  oscillator.frequency.setValueAtTime(440, audioContext.currentTime);
  oscillator.connect(audioContext.destination);
  oscillator.start();
  oscillator.stop(audioContext.currentTime + 0.1);
}

// =======================
// Sequencer Logic (Smooth Tempo)
// =======================
function playStep() {
  // Clear previous highlights from all grids
  document.querySelectorAll('.step').forEach(btn => {
    btn.classList.remove('playing');
  });

  // Play sounds for each grid container
  ['#gridkik', '#gridsnr', '#gridhh'].forEach(gridId => {
    const currentBtn = document.querySelector(`${gridId} .step[data-step="${currentStep}"]`);
    if (currentBtn) {
      currentBtn.classList.add('playing');
      if (currentBtn.classList.contains('active')) {
        if (gridId === '#gridkik') {
          playkick();
        } else if (gridId === '#gridsnr') {
          playsnare();
        } else if (gridId === '#gridhh') {
          playhat();
        }
      }
    }
  });

  currentStep++;
  if (currentStep > totalSteps) currentStep = 1;

  if (isPlaying) {
    setTimeout(playStep, bpmcalc(bpm)); // Use updated bpm for next beat
  }
}

// =======================
// UI Event Listeners
// =======================

// Step Buttons Toggle
document.querySelectorAll('.step').forEach(button => {
  button.addEventListener('click', () => {
    const stepIndex = parseInt(button.getAttribute('data-step')) - 1;
    sequence[stepIndex] = !sequence[stepIndex];
    button.classList.toggle('active', sequence[stepIndex]);
  });
});

// Play Button
document.getElementById('playBtn').addEventListener('click', () => {
  if (!isPlaying) {
    isPlaying = true;
    currentStep = 1;
    playStep();
  }
});

// Stop Button
document.getElementById('stopBtn').addEventListener('click', () => {
  isPlaying = false;
  document.querySelectorAll('.step').forEach(btn => btn.classList.remove('playing'));
});

// Clear Button
document.getElementById('clearBtn').addEventListener('click', () => {
  sequence.fill(false);
  document.querySelectorAll('.step').forEach(button => button.classList.remove('active'));
});

// BPM Slider
bpmSlider.addEventListener("input", function () {
  bpm = parseInt(this.value);
  bpmDisplay.textContent = bpm;
  // No need to restart anything – beat timing updates smoothly on next step
});

})