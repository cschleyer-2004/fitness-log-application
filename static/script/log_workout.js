const setRow = document.querySelector(".set-row");
const addSetButton = document.getElementById("add-set-button");
const pendingList = document.getElementById("pending-sets-list");
const hiddenContainer = document.getElementById("hidden-sets-container");

addSetButton.addEventListener("click", () => {
    const exerciseSelect = setRow.querySelector("select[name='exercise']");
    const setsInput = setRow.querySelector("input[name='sets']");
    const repsInput = setRow.querySelector("input[name='reps']");
    const weightInput = setRow.querySelector("input[name='weight']");

    const exerciseId = exerciseSelect.value;
    const exerciseLabel = exerciseSelect.options[exerciseSelect.selectedIndex].text;
    const setsVal = setsInput.value;
    const repsVal = repsInput.value;
    const weightVal = weightInput.value;

    if (!exerciseId || !setsVal || !repsVal || !weightVal) return;

    const li = document.createElement("li");
    li.textContent = `${exerciseLabel} — ${setsVal} x ${repsVal} @ ${weightVal} lbs `;

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "remove-pending-button";
    removeBtn.textContent = "Remove";
    li.appendChild(removeBtn);

    pendingList.appendChild(li);

    removeBtn.addEventListener("click", () => {
        li.remove();
    });

    // Hidden inputs so this entry actually submits with the form
    ["exercise", "sets", "reps", "weight"].forEach((field, i) => {
        const val = [exerciseId, setsVal, repsVal, weightVal][i];
        const hidden = document.createElement("input");
        hidden.type = "hidden";
        hidden.name = field + "[]";
        hidden.value = val;
        hiddenContainer.appendChild(hidden);
    });

    // Reset the visible row for the next entry
    exerciseSelect.value = "";
    setsInput.value = "";
    repsInput.value = "";
    weightInput.value = "";
});