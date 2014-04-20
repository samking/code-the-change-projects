var xhr = new XMLHttpRequest();
xhr.open("POST", "http://rishibedi.apiary.io/project");
xhr.setRequestHeader("Content-Type", "application/json");
      //xhr.onreadystatechange = function () {
        //if (this.readyState == 4) {
        //  alert('Status: '+this.status+'\nHeaders: '+JSON.stringify(this.getAllResponseHeaders())+'\nBody: '+this.responseText);
       // }
      //};
      xhr.send("{ \"title\": \"Interesting Project\",\n  \"github\": \"https://github.com/rbedi/ctc-internal-backend/\",\n  \"organization\": \"Code the Change\",\n  \"description\": \"What a cool project!\"\n  \"tags\": [ \"fun\", \"coding\", \"life\" ]\n}");
      var xhr = new XMLHttpRequest();
      xhr.open("GET", "http://rishibedi.apiary.io/project/42");
      var obj;
      xhr.onreadystatechange = function () {
        if (this.readyState == 4) {
          obj = jQuery.parseJSON(this.responseText);
          console.log(obj);
          document.getElementById("projectTitle").innerHTML = obj.title;
          document.getElementById("technicalObjectives").innerHTML = obj.description;
          document.getElementById("gitHub").innerHTML = "<a href="+obj.github+">Github</a>";
          alert('Status: '+this.status+'\nHeaders: '+JSON.stringify(this.getAllResponseHeaders())+'\nBody: '+this.responseText);
        }
      };
      xhr.send(null);
      //alert(obj.title);