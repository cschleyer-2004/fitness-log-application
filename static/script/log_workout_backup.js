// 1. On page load, grab a reference to:
//    - the container that holds all .set-row elements
//    - the "Save Workout" button's parent, or wherever you'll put an "Add Set" button

const setsContainer =  document.querySelector(".sets-container")

// 2. Add an "Add Set" button to the template (not in JS - put it in the HTML,
//    right after the existing .set-row div)

const addSetButton = document.getElementById("add-set-button")

// 3. When "Add Set" is clicked:
//    - clone the existing .set-row (or its inner HTML) as a template
//    - reset the cloned inputs' values to empty ("" for select, "" for number inputs)
//    - append the clone to the container
//    - add a small "Remove" button to the new row if you want removable rows

addSetButton.addEventListener("click", () => {
    const rows = setsContainer.querySelectorAll(".set-row");
    const template = rows[0];
    const clone = template.cloneNode(true);

    // reset cloned inputs
    clone.querySelectorAll("select, input").forEach((field) => {
        field.value = "";
    });

    setsContainer.appendChild(clone);
});

// 4. When a "Remove" button is clicked:
//    - find its parent .set-row
//    - remove it from the DOM
//    - (optional) prevent removing the very last row, so the form always has ≥1 set

setsContainer.addEventListener("click", (event) => {
   if (!event.target.classList.contains("remove-set-button")) return;

   const rows = setsContainer.querySelectorAll(".set-row");
   if (rows.length <= 1) return; // keep at least one row

   let row = event.target.closest(".set-row")
   row.remove()
});

//# for each exercise <select> in the form (there could be more than one once rows clone):
// #   listen for "change"
// #   if select.value === "__new__":
// #       find the sibling new_exercise_name input for THIS row
// #       show it, maybe focus it
// #   else:
// #       hide it, clear its value

setsContainer.addEventListener("change", (event) => {
    if (event.target.tagName !== "SELECT") return;

    let row = event.target.closest(".set-row");
    let newExerciseInput = row.querySelector("input[name=new_exercise_name]");

    if (event.target.value === "__new__") {
        // show newExerciseInput, maybe .focus() it
        newExerciseInput.style.display = ""
        newExerciseInput.focus()
    } else {
        // hide newExerciseInput, clear its value
    }
});

// 5. Naming: this is the important part for the backend -
//    every cloned row's <select> and <input> need name="exercise[]",
//    name="reps[]", name="weight[]" (note the [] - more on this below)