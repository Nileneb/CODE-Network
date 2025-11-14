
// trying to validate the form before it submits
function checkForm(){
    var fname = document.querySelector('input[name="first_name"]').value;
    var lname = document.querySelector('input[name="last_name"]').value;
    var mail = document.querySelector('input[name="email"]').value;
    
    if(fname=="" || lname=="" || mail==""){
        alert("Please fill out all required fields!");
        return false;
    }
    return true;
}


// search functionality 
// Note ToDo: figure out how to actually filter the contacts
function searchContacts(){
    var input=document.querySelector('.search-box');
    if(input){
        var searchTerm=input.value.toLowerCase();
        console.log("searching for: "+searchTerm);
    }
}


// burger menu for mobile - finally figured this out!
function setupBurgerMenu(){
    var burger=document.querySelector('.burger-menu');
    var navLinks=document.querySelector('.nav-links');
    
    if(burger && navLinks){
        burger.addEventListener('click',function(){
            navLinks.classList.toggle('active');
            burger.classList.toggle('active');
            console.log('menu toggled');
        });
    }
}


// everything runs when page finishes loading
window.onload=function(){
    console.log("page loaded!");
    
    var searchBox=document.querySelector('.search-box');
    if(searchBox){
        searchBox.addEventListener('keyup',searchContacts);
    }
    
    setupBurgerMenu();
};