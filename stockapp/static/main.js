// This is gonna be my javascript file

function nextDrink(did) {
    drink = document.getElementById(did)
    if (drink.style.display === "none") {
        drink.style.display = "block";
    }else {
        drink.style.display = "none";
    }
}

function showNewList() {
    var content = "";
    input = document.getElementsByTagName("input");
    for (i=0; i < input.length; i++) {
        content += input[i].name + " " + input[i].value + "\n";
    }
    alert(content)
}
