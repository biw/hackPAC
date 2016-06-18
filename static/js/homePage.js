var loggedInStatus = true;
var currentUserId = "meia";
var selectedArticle = {iden:"a", upvotes:500, longDescription:"wowowowow number 1 this should be longer example example :) ", header:"Sample Top"};
var article1 = {iden:"b", upvotes:20, longDescription:"heyy this should be longer example example :) ", header:"Sample 1"};
var article2 = {iden:"c", upvotes:300, longDescription:"hahahahha omg how do you write long descriptions wau this is an amazing barrier to entry love it ", header:"Sample 2"};
var articleList = [article1, article2];

$(document).ready(function(){
	updateHeaderBar(loggedInStatus);
	if (selectedArticle) {
		displayArticle(selectedArticle);
	}

	for (index in articleList) {
		if (articleList[index] != selectedArticle) {
			displayArticle(articleList[index]);
		}
	}
});

// true: logged in
// false: not logged in
function updateHeaderBar(loggedInStatus) {
	if (loggedInStatus) {
		$("#username").replaceWith("<li><a href='/'>".concat(currentUserId, "</a></li>"));
		$("#loggedin").show();
		$("#notloggedin").hide();
	}
	else {
		$("#loggedin").hide();
		$("#notloggedin").show();
	}
};

function displayArticle(article) {
	var iden = article.iden;
	var upvotes = article.upvotes;
	var longDescription = article.longDescription;
	var header = article.header;
	$('#articles').append("<table><tr><td><img class='vote' onClick='upvote(".concat(iden, ")' id='",iden,"'src='static/img/upvote.png' alt='Upvote'/></td><td>", upvotes, "</td><td>", header,"</td></tr></table>")); 
	$('#articles').append("<div class='descriptions' id='".concat(iden,"'style='display: none;''>",longDescription, "</div></br>"));
}

function upvote(id) {
	article = getArticleById(id);
	if (article != selectedArticle) {
		articleList[article].upvotes += 1; // article = index of article in list
		articleList.splice(article, 1);
		articleList.push(selectedArticle);
		selectedArticle = article;
		location.reload();
	}

}

function getArticleById(articleid) {
	if (articleid === selectedArticle.id) {
		return selectedArticle
	} else {
		for (index in articleList) {
			if (articleList[index].id == articleid) {
				return index;
			}
		}
	}
	return "Not Found Error"	
}

function onRowClick(articleid) {
	$(".descriptions").hide();
	$("#articleid").show();
}

