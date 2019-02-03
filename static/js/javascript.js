/* javascript code here */
// the back to top buttons
let topBtn = document.getElementById("top-btn");
let qAddBtn = document.getElementById("quick-add-btn");
window.onscroll = ()=>{
    if($("#top-btn").length) // my bad, jquery seemed to be the quickest around this one
        scrollFunc()
}
function scrollFunc(){
    if(document.body.scrollTop > 20 || document.documentElement.scrollTop > 20){
        topBtn.style.display = "block";
        qAddBtn.style.bottom = "64px";
    }else{
        topBtn.style.display = "none";
        qAddBtn.style.bottom = "10px";
    }
}
function topFunc(){
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
}

/*
    *the functons for showing and hiding the side navigation bar
    * for the profile and manage products pages
*/
function openNav() {
    document.getElementById("side-nav").style.display = "block";
    document.getElementById("side-nav").style.width = "300px";
    document.getElementById("main").style.left = "300px";
}

/* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
function closeNav() {
    document.getElementById("side-nav").style.display = "none";
    document.getElementById("side-nav").style.width = "0";
    document.getElementById("main").style.left = "0";
}

function charCount(input) {
	var len = input.length;
	if (len <= 50) {
        document.getElementById("count").innerHTML = len + ' out of 50 characters';
        $('#count').css('color', 'black')
    }
	else {
        document.getElementById("count").innerHTML = len + ' out of 50 characters. Limit Exceeded, please keep it brief.';
        $('#count').css('color', 'red')
    }

}
function checkInput() {

}