// Grab references to the key elements once, on page load,
// so we don't have to re-query the DOM every time something happens.
const setRow = document.querySelector(".set-row");           // the one visible entry row (acts as a staging area now)
const addSetButton = document.getElementById("add-set-button");
const pendingList = document.getElementById("pending-sets-list");     // <ul> where summary <li>s get added
const hiddenContainer = document.getElementById("hidden-sets-container"); // invisible div holding the real submitted data

// Runs every time the user clicks "Add"
addSetButton.addEventListener("click", () => {

    // Find this specific row's inputs by their "name" attribute.
    // (Scoped to setRow, not the whole document, in case this ever needs
    // to support more than one row again later.)
    const exerciseSelect = setRow.querySelector("select[name='exercise']");
    const setsInput = setRow.querySelector("input[name='sets']");
    const repsInput = setRow.querySelector("input[name='reps']");
    const weightInput = setRow.querySelector("input[name='weight']");

    // Pull out the actual values the user typed/selected right now
    const exerciseId = exerciseSelect.value;   // the <option>'s value (an exercise's DB id)
    const exerciseLabel = exerciseSelect.value === "__new__"
    ? newExerciseInput.value
    : exerciseSelect.options[exerciseSelect.selectedIndex].text;// the human-readable name, for display only
    const setsVal = setsInput.value;
    const repsVal = repsInput.value;
    const weightVal = weightInput.value;

    // Guard clause: if any field is still empty, stop here and do nothing.
    // Prevents adding a blank/incomplete entry to the list.
    if (!exerciseId || !setsVal || !repsVal || !weightVal) return;

    // --- Build the visible summary line item ---
    const li = document.createElement("li");
    li.textContent = `${exerciseLabel} — ${setsVal} x ${repsVal} @ ${weightVal} lbs `;

    // Give this specific entry its own Remove button
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";                       // prevents it from accidentally submitting the form
    removeBtn.className = "remove-pending-button";    // for styling / future JS targeting
    removeBtn.textContent = "Remove";
    li.appendChild(removeBtn);          // put the button INSIDE this <li>

    pendingList.appendChild(li);        // add the finished <li> to the visible list on the page

    // Wire up this specific Remove button, for this specific <li>.
    // Because this listener is created fresh each time Add runs, it's
    // automatically "attached" to the correct entry — no need to search
    // for which row it belongs to.
    removeBtn.addEventListener("click", () => {
        li.remove();   // removes just this one <li> from the DOM
    });

    // --- Create the actual data that gets submitted with the form ---
    // The visible row's inputs no longer have "name" attributes, so they
    // don't submit anything themselves. These hidden inputs are what
    // Flask will actually see in request.form when Save Workout is clicked.
    ["exercise", "sets", "reps", "weight"].forEach((field, i) => {
        const val = [exerciseId, setsVal, repsVal, weightVal][i]; // match field name to its value by position
        const hidden = document.createElement("input");
        hidden.type = "hidden";                 // invisible, but still submits with the form
        hidden.name = field + "[]";             // the "[]" is what lets Flask's getlist() collect multiple entries
        hidden.value = val;
        hiddenContainer.appendChild(hidden);
    });

    // --- Reset the visible row so it's ready for the next entry ---
    exerciseSelect.value = "";
    setsInput.value = "";
    repsInput.value = "";
    weightInput.value = "";
});

//New-exercise toggle

const exerciseSelect = setRow.querySelector("select[name='exercise']");
const newExerciseInput = setRow.querySelector("input[name='new_exercise_name']");

exerciseSelect.addEventListener("change", () => {
   if (exerciseSelect.value === "__new__"){
       newExerciseInput.style.display = "";
       newExerciseInput.focus();
   } else {
       newExerciseInput.style.display = "none";
       newExerciseInput.value = "";
   }
});