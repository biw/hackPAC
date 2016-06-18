$(document).ready(function(){
	var loggedInUser = 'SampleUser1';
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
	    var p_text = $(this).html();
	    p_text = p_text.replace("+ Look closely ", "- I'm done!");
	    //document.getElementById('emoticon').innerHTML = "<i class='em em---1'></i>";
	    $(this).html(p_text);

	    //switch the view class
	    $(this).parent().removeClass("sub-post-min")
	    $(this).parent().addClass("sub-post-max")
	})

	// hide extended desriptions
	$(document.body).on("click", "upvote",function() {

	    // get the post and id
	    var post = $(this).parent();
	    var id = post[0]["id"];

	    //makes call back to database and then refreshes the page
	    upvote(id, loggedInUser);

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
});




function upvote(postid, userid) {
	$.get('/api/upvote?postid='+postid+'&voterId'+voterId,function() {
        location.reload();
	},'html');

}

