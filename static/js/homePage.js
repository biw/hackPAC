var loggedInStatus = true;
var currentUserId = "sampleUserLogIn";
var selectedArticle = {iden:"a", upvotes:500, longDescription:"wowowowow number 1 this should be longer example example :) ", header:"Sample Top"};
var article1 = {iden:"b", upvotes:20, longDescription:"heyy this should be longer example example :) ", header:"Sample 1"};
var article2 = {iden:"c", upvotes:300, longDescription:"hahahahha omg how do you write long descriptions wau this is an amazing barrier to entry love it ", header:"Sample 2"};
var articleList = [article1, article2];

$(document).ready(function(){
	updateHeaderBar(loggedInStatus);

	// show extended descriptions
	$(document.body).on("click", "sub-post.sub-post-min>p",function() {

	    // get the iframe and the hidden_src
	    var iframe = $(this).prev()
	    var hidden_src = iframe.attr("hidden-src")

	    //add the iframe items, and show it
	    iframe.addClass("article-frame")
	    iframe.removeClass("hidden-frame")
	    iframe.attr("src", hidden_src)

	    //replace the paragraph text to close it
	    var p_text = $(this).html()
	    p_text = p_text.replace("+ Open", "- Close")
	    $(this).html(p_text)

	    //switch the view class
	    $(this).parent().removeClass("sub-post-min")
	    $(this).parent().addClass("sub-post-max")
	})

	// hide extended desriptions
	$(document.body).on("click", "upvote",function() {

	    // get the iframe and the hidden_src
	    var articleholder = $(this).prev();

	    // //add the iframe items, and show it
	    // iframe.addClass("hidden-frame")
	    // iframe.removeClass("article-frame")
	    // iframe.attr("src", "")

	    // //replace the paragraph text to close it
	    // var p_text = $(this).html()
	    // p_text = p_text.replace("- Close", "+ Open")
	    // $(this).html(p_text)

	    // //switch the view class
	    // $(this).parent().removeClass("sub-post-max")
	    // $(this).parent().addClass("sub-post-min")
	})

	// upvote
	$(document.body).on("click", "sub-post.sub-post-max>p",function() {

	    // get the iframe and the hidden_src
	    var iframe = $(this).prev()

	    //add the iframe items, and show it
	    iframe.addClass("hidden-frame")
	    iframe.removeClass("article-frame")
	    iframe.attr("src", "")

	    //replace the paragraph text to close it
	    var p_text = $(this).html()
	    p_text = p_text.replace("- Close", "+ Open")
	    $(this).html(p_text)

	    //switch the view class
	    $(this).parent().removeClass("sub-post-max")
	    $(this).parent().addClass("sub-post-min")
	})


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
		$("#username").replaceWith("<li><a href='/dashboard'>".concat(currentUserId, "</a></li>"));
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

