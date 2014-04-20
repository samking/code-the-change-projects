document.write('<nav class="navbar navbar-default" role="navigation">');
document.write('<!-- Brand and toggle get grouped for better mobile display -->');
document.write('<div class="navbar-header">');
document.write('<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">');
document.write('<span class="sr-only">Toggle navigation</span>');
document.write('<span class="icon-bar"></span>');
document.write('<span class="icon-bar"></span>');
document.write('<span class="icon-bar"></span></button>');
document.write('<a class="navbar-brand">Code The Change</a>');
document.write('</div>');

document.write('<!-- Collect the nav links, forms, and other content for toggling -->');
document.write('<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">');
document.write('<ul class="nav navbar-nav">');

var url = document.URL;
var split = url.split("/");
var page = split[split.length - 1];
var pages = ["dashboard.html", "non_profit_partner_profiles.html", "allProjects.html", "projectCreate.html"];
var titles = ["Home", "Partners", "Projects", "Create New Project"];

for(var i = 0; i < 4; i++) {
	document.write('<li');
	if(page === pages[i]) {
		document.write(' class="active"');
	}
	document.write('><a href="' + pages[i] + '">' + titles[i] + '</a></li>');
}

//not really being of any use, commenting it out

//document.write('<li class="dropdown">');
//document.write('<a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown <b class="caret"></b></a>');
//document.write('<ul class="dropdown-menu">');
//document.write('<li><a href="#">Action</a></li>');
//document.write('<li><a href="#">Another action</a></li>');
//document.write('<li><a href="#">Something else here</a></li>');
//document.write('<li class="divider"></li>');
//document.write('<li><a href="#">Separated link</a></li>');
//document.write('<li class="divider"></li>');
//document.write('<li><a href="#">One more separated link</a></li>');
//document.write('</ul>')


document.write('</li></ul>');
document.write('<form class="navbar-form navbar-right" role="search">');
document.write('<div class="form-group">');
document.write('<input type="text" class="form-control" placeholder="Search"></div>');
document.write('<button type="submit" class="btn btn-default">Submit</button></form>');
document.write('<ul class="nav navbar-nav navbar-right"></ul></div>');
document.write('<!-- /.navbar-collapse --></nav>');
