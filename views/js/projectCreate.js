var xhr = new XMLHttpRequest();
xhr.open("POST", "http://ctcprojects.apiary.io/project");
xhr.setRequestHeader("Content-Type", "application/json");
xhr.onreadystatechange = function () {
  if (this.readyState == 4) {
    //alert('Status: '+this.status+'\nHeaders: '+JSON.stringify(this.getAllResponseHeaders())+'\nBody: '+this.responseText);
  }
};
function projectInformation() {
	var projectTitle = title.value;
	var categories = category.value;
	var projObj = objective.value;
	var git = gitHub.value;
	var org = organization.value;
	var people = peopleInvolved.value;
	var desc = description.value;
	var techObj = technicalObjectives.value;
	var allTags = tags.value;
	console.log(projectTitle);
	console.log(categories);
	console.log(projObj);
	console.log(git);
	console.log(org);
	console.log(people);
	console.log(desc);
	console.log(techObj);
	console.log(allTags);
}

//document.getElementById("button").onclick = projectInformation();
//console.log(title);
xhr.send("{ \"title\": \"Interesting Project\",\n  \"github\": \"https://github.com/rbedi/ctc-internal-backend/\",\n  \"organization\": \"Code the Change\",\n  \"description\": \"What a cool project!\"\n  \"tags\": [ \"fun\", \"coding\", \"life\" ]\n}");