// Referenced: http://www.freecodeexamples.com/2018/09/javascript-easy-battleship-game.html
// Referenced: w3schools.com (splice method)
// Referenced: https://stackoverflow.com/questions/40711300/javascript-do-something-every-n-seconds (space out "computer" turn)

var letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
var compShips = createShips(); // create array of computer ships
var yourShips = createShips(); // create array of your ships
var currentLocs = getAllLocations(compShips) // get all locations of currently placed ships
var sunkenShips = []; // array of sunken ships to account for winning the game
var compHits = 0; // keep track of computer hits
var totalHits = 0; // keep track of all hits to measure hit percentage
var hitPercentage = 0; // a way to store the hitting percentage (hits/ total guesses)
var wasFound = false; // a way to check if a coordinate has been found in ship locations array
var totalGuesses = []; // array to store total number of guesses
var shipNames = []; // array to display ship names in game display
var allPossibleLocations = []; // array to hold all possible locations to loop through

// Add each letter and number as a location to array
for (var r = 1; r < 11; r++) {
  for (var c = 0; c < letters.length; c++) {
    allPossibleLocations.push(letters[c] + r);
  }
}

console.log(compShips);

// Create and Display Game Elements
function startGame() {
  document.getElementById("myTable").style.display = "block";
  document.getElementById("startBTN").style.display = "none";
  document.getElementById("restartBTN").style.display = "block";
  document.getElementById("info").style.display = "none";
  document.getElementById("ships").style.display = "block";
  createGame();
  //console.log(compShips); // debugging purposes or to quickly win game
}

// Reset display and all game values
function restartGame() {
  document.getElementById("myTable").style.display = "none";
  document.getElementById("startBTN").style.display = "inline";
  document.getElementById("info").style.display = "block";
  document.getElementById("restartBTN").style.display = "none";
  document.getElementById("ships").innerHTML = "";
  document.getElementById("ships").style.display = "none";
  document.getElementById("status").style.display = "none";
  sunkenShips = [];
  guesses = [];
  shipNames = [];
  totalHits = 0;
  hitPercentage = [];
  // reset letters because letters were removed in the create ship location function to remove any duplicates
  letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
  compShips = createShips(); // create new array of computer ships
  yourShips = createShips(); // create new array of your ships
  currentLocs = getAllLocations(compShips) // get all new locations of currently placed ships
}

// Create Grid for Game
function createGame() {
  var html = "";
  var letters = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']; // make up row headers
  for (var r = 0; r < 11; r++) {
    html += "<TR id=\"row" + r + "\">"; // creates row ids with row and a number
    for (var c = 0; c < 11; c++) {
      if (r == 0) {
        html += "<TH>" + letters[c] + "</TH>"; // prints letters as column headers
      }
      else if (c == 0) {
        html += "<TH>" + r + "</TH>"; // prints numbers as row headers
      }
      else {
        // create data cells and pass cell ids to function
        html += "<TD class=\"cell\" id=\"" + letters[c] + r + "\" onclick=\"checkCoordinate(this);\">" + "</TD>";
      }
    } // for column loop
    html += "</TR>";
  } // for row loop

  document.getElementById("myTable").innerHTML = html; // print table text on page
  cells = document.getElementsByClassName("cell"); // gets all grid cells and makes array

  // add ship names to game screen
  for (var i = 0; i < compShips.length; i++) {
    shipNames.push(compShips[i][0]);
  }

  document.getElementById("ships").innerHTML = "All Ships: " + shipNames.join(", ");
}

// Set Random Locations for Ships Based on Count
function setLocation(ship, count, shipHits) {
  var shipLocations = []; // nested array of ship names and their locations
  var shipLoc = []; // array of ship locations ie ["E4", "E5", "E6"]
  var randomNum = Math.floor(Math.random() * 10 + 1); // random number to represent grid row
  var randomLoc = letters[Math.floor(Math.random() * (letters.length - 1))]; // random letter to represent grid column
  for (var i = 0; i < count; i++) {
    // if random number chosen is between 0 and 5,
    if (randomNum < 5 && randomNum > 0) {
      // add location that is one more than the random number (if random num = 5, add E6, E7, etc)
      shipLoc.push(randomLoc + (randomNum + i)); // push random locations to ship Location array
    }
    else if (letters.indexOf(randomLoc) > 2 && (randomNum == 5 || randomNum == 6)) {
      shipLoc.push(letters[letters.indexOf(randomLoc) - i] + (randomNum)); // push a horizontal location to the ship location array
    }
    else {
      // if random number chosen is between 7 and 10, add location that is one less (8 -> E7, E6)
      // this way you can account for big ships with size 5
      shipLoc.push(randomLoc + (randomNum - i));
    }
    // if you've reached the ship count, then exit
    if (count == shipLoc.length) {
      break;
    }
  }
  // remove letter from array so you won't have to deal with duplicate locations
  letters.splice(letters.indexOf(randomLoc), 1);
  shipLocations.push(shipLoc); // add ship location to nested ship locations array
  shipLocations.push(shipHits); // add way to keep track of whether each ship has been sunk
  shipLocations.unshift(ship); // add ship name to beginning of ship Locations array
  return shipLocations; // return array for use later on
}

// Create Ships
function createShips() {
  var allShips = [];
  allShips.push(setLocation("Destroyer", 2, 0));
  allShips.push(setLocation("Submarine", 3, 0));
  allShips.push(setLocation("Battleship", 4, 0));
  allShips.push(setLocation("Carrier", 5, 0));
  return allShips;
}

// Create list of current locations so you can check whether each coordinate clicked is being used
function getAllLocations(compShips) {
  var tempLocs = []; // list of current locations 
  for (var i = 0; i < compShips.length; i++) {
    for (var j = 0; j < compShips[i][1].length; j++) {
      // add all current locations to list
      tempLocs.push(compShips[i][1][j]);
    }
  }
  return tempLocs; // return list
}


// Check and See If Coordinate Clicked Is a Hit/Miss
function checkCoordinate(coordinate) {
  wasFound = false; // set whether ship has been sunk to false by default

  // Add all guesses to list
  if (totalGuesses.indexOf(coordinate.id) == -1) {
    totalGuesses.push(coordinate.id);
    console.log(totalGuesses.length);
  }

  // Make loop that checks whether each coordinate clicked is in the computer's ship location array
  for (var i = 0; i < compShips.length; i++) {
    for (var j = 0; j < compShips[i][1].length; j++) {
      var shipHits = compShips[1][2]; // update and save the number of hits a ship has 
      // if the coordinate = a location in the ship location array
      if (coordinate.id == compShips[i][1][j] && currentLocs.indexOf(coordinate.id) != -1) {
        document.getElementById(coordinate.id).style.background = "#FF0000"; // change hit grid cell to red 
        compShips[i][2] += 1; // increase individual ship counter by one
        shipHits += compShips[i][2]; // save number of hits to a variable 
        wasFound = true; // mark that you have found the coordinate
        // alert user when you hit a ship and let them know how many hits are left for that ship in order to sink it
        alert(compShips[i][0] + " HIT: " + shipHits + "/" + compShips[i][1].length);
        break; // exit once you've hit a ship
      }
    }

    // If coordinate is not found in ship location array
    if (wasFound === false && currentLocs.indexOf(coordinate.id) === -1) {
      // && hitShips.indexOf(coordinate.id) !== -1
      document.getElementById(coordinate.id).style.background = "#0000FF"; // change cell background to blue
      alert("MISS"); // alert user know they've missed
      break;
    }

    // If the number of ship hits is equal to the length of the ship location in the array
    // and the ship hasn't already been been sunken
    if (compShips[i][2] == compShips[i][1].length && sunkenShips.indexOf(compShips[i]) == -1) {
      alert("You've sunk my " + (compShips[i][0])); //display which ship you've sunk
      document.getElementById("status").style.display = "inline";
      sunkenShips.push(compShips[i]); // add ship name to hit ships list
      var sunkenShipNames = []; // ship names that have been sunken
      for (var i = 0; i < sunkenShips.length; i++) {
        sunkenShipNames.push(sunkenShips[i][0]); // add to list
      }
      // print the name of each ship you've sunk 
      document.getElementById("status").innerHTML = "Your Sunken Ships: " + sunkenShipNames.join(", ");
      totalHits += shipHits; // add hits to total hits
      wasFound = false; // make boolean false until you sink another ship
      break;
    }
  }

  // If you've sunken all the ships,display alert and hit percentage
  if (sunkenShips.length === compShips.length) {
    console.log(totalHits);
    console.log(totalGuesses.length);
    console.log(totalHits/totalGuesses.length);
    
    hitPercentage = 100 * (totalHits / totalGuesses.length).toFixed(2);
    alert("You Won!");
    document.getElementById("status").innerHTML = ("You guessed the location of " + sunkenShips.length + " of their ships in " + totalGuesses.length + " guesses, which means your total hit percentage was " + hitPercentage + "%.");
    window.clearInterval(computerTurn); // stop computer from playing once you've won
  }
}

// Computer makes a turn at random intervals that range between half a second to 10 seconds
var computerTurn = setInterval(computerTurn, Math.floor(Math.random() * (9500) + 500));
// Start computer turn once start button is clicked
document.getElementById("startBTN").onclick = computerTurn;

// Computer turn function
function computerTurn() {
  // array of all the locations of your ships
  var yourCurrentLocs = getAllLocations(yourShips);
  var compHitPercentage = 0; // store computer hit percentage
  var compGuesses = []; // store array of all computer guesses
  // randomly selected location from all possible locations
  var randomLocation = allPossibleLocations[Math.floor(Math.random() * (allPossibleLocations.length - 1))];
  if (yourCurrentLocs.indexOf(randomLocation) != -1) {
    compHits++; // increase hits
    compGuesses.push(randomLocation); // add guess to array
    console.log("Computer Hit: " + randomLocation + "\n" + (yourCurrentLocs.length - compHits) + "/" + yourCurrentLocs.length + " left."); // let user know if the computer hit one of your ships
  }
  // if the random location isn't in the list of your current locations, then let the user know the computer missed
  else if (yourCurrentLocs.indexOf(randomLocation) == -1) {
    compGuesses.push(randomLocation); // add guess to array
  }
  // if the computer hits all the locations in your current list, then alert the user that the computer won 
  if (compHits == yourCurrentLocs.length) {
    if (confirm("Computer Won")) {
      window.clearInterval(computerTurn); // stop computer from playing once they've won
    }
    // display computer hit percentage on game screen
    document.getElementById("status").style.display = "inline";
    document.getElementById("status").innerHTML = "The Computer guessed the location of " + yourShips.length + " of your ships in " + compGuesses.length + " guesses, which means your total hit percentage was " + (100 * (compHits / compGuesses.length).toFixed(2) + "%.");
  }
}

