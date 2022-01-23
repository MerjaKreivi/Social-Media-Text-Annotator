// Meria's Annotator for Social Media Texts
// University of Oulu
// Created by Merja Kreivi-Kauppinen (2021-2022)

// Social-Media-Text-Annotator/HateSpeechAnnotator API admin.js

//"use strict";

const DEBUG = true;
const MASONJSON = "application/vnd.mason+json";
const PLAINJSON = "application/json";

const HSCategoryList = ["violence", "swear", "troll", "bully", "ethnic", "politics", "sexual", "idiom", "immigration", "women", "group", "religion", "opinion"];

const HSCategoryLists = [["national", "immigration", "foreign", "ethnic", "religion"],
                        ["opinion", "politics", "status", "smedia", "work"],
                        ["sexual", "gender", "women", "health", "family"],
                        ["threat", "insult", "violence", "appearance", "joke"],
                        ["swear", "bully", "troll", "coded", "idiom"],
                        ["other"]]

// for pagination purposes
let current_page = 1;
const numberOfItemsOnPage = 15;

function renderError(jqxhr) {
    let msg = jqxhr.responseJSON["@error"]["@message"];
    showToast(msg);
}

function renderMsg(msg) {    
    showToast(msg);
}

function showToast(msg) {
    let toast = $("div.toast");
    let body = toast.find(".toast-body")[0];
    body.innerText = msg;
    toast.show();
    setTimeout(function () {
        toast.hide();
    }, 5000);
}

function showLoginAlert(xhr) {
    let msg = xhr.responseJSON["@error"]["@message"];
    alert(msg);    
}

function showAddUserAlert(xhr) {
    let msg = xhr.responseJSON["@error"]["@message"];
    alert(msg);    
}

function getResource(href, renderer) {
    $.ajax({
        url: href,
        success: renderer,
        error: renderError
    });
}

function sendData(href, method, item, postProcessor) {
    console.log(href);
    console.log(method);
    console.log(item);
    console.log(JSON.stringify(item));
    $.ajax({
        url: href,
        type: method,
        data: JSON.stringify(item),
        contentType: PLAINJSON,
        processData: false,
        success: postProcessor,
        error: renderError
    });
}

function sendAddUserData(href, method, item, postProcessor) {
    console.log(href);
    console.log(method);
    console.log(item);
    console.log(JSON.stringify(item));
    $.ajax({
        url: href,
        type: method,
        data: JSON.stringify(item),
        contentType: PLAINJSON,
        processData: false,
        success: postProcessor,
        error: showAddUserAlert
    });
}

function sendLoginData(href, method, item, postProcessor) {
    console.log(href);
    console.log(method);
    console.log(item);
    console.log(JSON.stringify(item));
    $.ajax({
        url: href,
        type: method,
        data: JSON.stringify(item),
        contentType: PLAINJSON,
        processData: false,
        success: postProcessor,
        error: showLoginAlert
    });
}

function sendTextData(href, method, formData, postProcessor) {
    console.log(href);
    console.log(method);  
    console.log(formData);
    $.ajax({
        url: href,
        type: method,
        data: formData,
        contentType: false,
        processData: false,
        success: postProcessor,
        error: renderError
    });
}

function followLink(event, a, renderer) {
    event.preventDefault();
    getResource($(a).attr("href"), renderer);
}

function backToTextCollection() {
    renderMsg("Delete/Update was successful");    
    $('#testform').each(function(){
        this.reset();
    });    
    $('#testform').hide(); 
    hideAnnoFormButtons();
    getResource(`http://localhost:5000/api/texts/pages/page?page=${sessionStorage.getItem("current_page")}&showOnPage=${numberOfItemsOnPage}`, renderTextsInPage);
}

function getTextCollection(event) {
    event.preventDefault();
    $('.textAnnotationForm').css({'display':'none'});
    getResource(`http://localhost:5000/api/texts/pages/page?page=${sessionStorage.getItem("current_page")}&showOnPage=${numberOfItemsOnPage}`, renderTextsInPage);
}

// define delete of resource
function deleteResource(href, callback) {    
    $.ajax({
        url:href,
        type:"DELETE",
        success: callback,
        error: renderError
    });
}

// define delete of text resource
function deleteTextResource(href) {    
    $.ajax({
        url:href,
        type:"DELETE",
        success: renderMsg("text deleted."),        
        error: renderError
    });
}

// define update-edit-put of resource
function updateResource(href, callback) {
    $.ajax({
        url:href,
        type:"PUT",
        success: callback,        
        error:renderError
    });
}

// -------------------------------------------------------------------------------------
// go to destination on front SPA

//* $("div.navigation").html(
    //    "<a href='" +
    //    "' onClick='renderUserPage(event)'> Go to Home </a>"
    //); 

function gotoHome(event) {
    event.preventDefault();
    hideAnnoFormButtons();
    hideUserFormButtons();

    let currentUser = sessionStorage.getItem("CurrentUser");        
    getResource("http://localhost:5000/api/users/" + currentUser, function(userData) {
        renderHomePage(userData);
    });
}

function gotoToolbox(event) {
    event.preventDefault();
    hideAnnoFormButtons();
    hideSaveButtons();
    $("#testform").hide();
    $("#addAnnotationBtnId").hide();
    $("#editAnnotationBtnId").hide();
    $("#deleteAnnotationBtnId").hide();

    let currentUser = sessionStorage.getItem("CurrentUser");        
    getResource("http://localhost:5000/api/users/" + currentUser, function(userData) {
        renderSelection(userData);
    });
}

// -------------------------------------------------------------------------------------
// HOME page - start up page - log out page

function renderHomePage(body) {
    // clear and define the view before rendering
    $("div.navigation").empty();
    // do not empty - to show bootswatch sandstone
    //muutos $(".resulttable thead").empty();
    $(".resulttable tbody").empty();

    showHomeButtons();
    hideUserFormButtons();
    $("#userFormId").hide();
    $("#newUserFormId").hide();
    $("#editUserBtnId").hide();
    $("#deleteUserBtnId").hide();
    $("#textListBtnId").hide();    
    $("#userAccountBtnId").hide();
    $("#textUploadFormId").hide();
    $("#user_nick").hide();
    $("#user_nick_label").hide();
 
    let form = $("#homeFormId");
    
    // define login button event
    $("#loginAsUserButtonId").on( "click", function(event) {
        event.preventDefault();
    });

    // define create account button event
    $("#createUserButtonId").on("click", function(event) {        
        event.preventDefault();
    });
}

function hideHomeButtons() {
    $("#loginAsUserButtonId").hide();
    $("#createUserButtonId").hide();
}

function showHomeButtons() {
    $("#loginAsUserButtonId").show();
    $("#createUserButtonId").show();
}

// -------------------------------------------------------------------------------------
// LOGIN USER page
// database is populated and users are already in database
// user item - api/users/<user>

function renderLoginResponse(data, status, xhr) {
    if (xhr.status === 200) {
        console.log("User login accepted.")
        let href = xhr.getResponseHeader("Location");
        if (href) {
            console.log(href);
            $("#userFormId").hide();
            getResource(href, renderSelection);            
        }
    }
    else {
        console.log(xhr.status)
        console.log("User login failed. New user? Create new account or try again.")
        alert("User login failed - invalid user name or password");
    }
}

function renderAddUserResponse(data, status, xhr) {
    if (xhr.status === 201) {
        console.log("New user was created successfully.")
        let href = xhr.getResponseHeader("Location");
        if (href) {
            console.log(href);
            $("#user_nick").hide();
            $("#user_nick_label").hide();
            $("#userFormId").hide();            
            getResource(href, renderSelection);            
        }
    }
    else {
        console.log(xhr.status)
        console.log("Add of new user failed")
        alert("Add of new user failed - invalid user name or password");
    }
}

function renderUserPage(body) {
    // clear and define the view before rendering
    $("div.navigation").empty();
    // do not empty - to show bootswatch sandstone
    //muutos $(".resulttable thead").empty();
    $(".resulttable tbody").empty();

    $("#userFormId").show();
    showUserFormButtons();
    hideHomeButtons();
    $("#newUserFormId").hide();
    $("#loginAsUserButtonId").hide();
    $("#createUserButtonId").hide();
    $("#editUserBtnId").hide();
    $("#deleteUserBtnId").hide();
    $("#textListBtnId").hide();    
    $("#userAccountBtnId").hide();
    $("#textUploadFormId").hide();
    $("#user_nick").hide();
    $("#user_nick_label").hide();

    $("#user_name").attr('disabled', false);    

    // get resource 'users' here after Home page changes - see below
    // getResource("http://localhost:5000/api/users/")

    let data = {};
    let form = $("#userFormId");
    
    // define login POST for user that already exists
    $("#loginUserBtnId").on( "click", function(event) {
        event.preventDefault();
        event.stopPropagation();
        $("#loginUserBtnId").show();
        //console.log("User login not implemented yet");
        if ($("#user_name").val() !== '') {
            data.user_name = $("#user_name").val();
        }
        else {
            alert("Please enter user name")
        }
        if ($("#user_password").val() !== '') {
            data.user_password = $("#user_password").val();
        }
        else {
            alert("Please enter password")
        }
        if ($("#user_name").val() !== '' && $("#user_password").val() !== '') {
            console.log($("#user_name").val() + " " + $("#user_password").val())
            // send login data after asynchronous resource has finished
            getResource("http://localhost:5000/api/users/", function(body) {
                loginCtrl = body["@controls"]["annometa:login"];
                sendLoginData(loginCtrl.href, loginCtrl.method, data, renderLoginResponse);
            });                            
        }       
    });
}

// --------------------------------------------------------------------------
// hide and show functions for user account buttons

function hideUserFormButtons() {
    $("#addUserBtnId").hide();
    $("#editUserBtnId").hide();
    $("#deleteUserBtnId").hide();
    $("#loginUserBtnId").hide();
    $("#textListBtnId").hide();
    $("#userAccountBtnId").hide();
}

function showUserFormButtons() {
    $("#addUserBtnId").show();
    $("#editUserBtnId").show();
    $("#deleteUserBtnId").show();
    $("#loginUserBtnId").show();
    $("#textListBtnId").show();    
    $("#userAccountBtnId").show();
}

// -------------------------------------------------------------------------------------
// CREATE NEW USER page
// database is populated and users are already in database
// user item - api/users/<user>
// can be used to create new user account

function renderNeWUserPage(body) {
    // clear and define the view before rendering
    $("div.navigation").empty();
    // do not empty - to show bootswatch sandstone
    //muutos $(".resulttable thead").empty();
    $(".resulttable tbody").empty();

    $("#newUserFormId").show();
    showUserFormButtons();
    hideHomeButtons();
    $("#loginUserBtnId").hide();
    $("#userFormId").hide();
    $("#loginUserBtnId").hide();
    $("#loginAsUserButtonId").hide();
    $("#createUserButtonId").hide();
    $("#editUserBtnId").hide();
    $("#deleteUserBtnId").hide();
    $("#textListBtnId").hide();    
    $("#userAccountBtnId").hide();
    $("#textUploadFormId").hide();
    $("#user_nick").show();    
    $("#user_nick_label").show();

    $("#new_user_name").attr('disabled', false);    

    // get resource 'users' here after Home page changes - see below
    // getResource("http://localhost:5000/api/users/")

    let data = {};
    let form = $("#newUserFormId");
    
    // define add POST for new user
    $("#addUserBtnId").on("click", function(event) {        
        event.preventDefault();
        $("#user_nick_label").show();
        $("#user_nick").show();
        //console.log("Add user with post not implemented yet");
        if ($("#new_user_name").val() !== '') {
            data.user_name = $("#new_user_name").val();
        }
        else {
            alert("Please enter user name")
        }
        if ($("#new_user_nick").val() !== '') {
            data.user_nick = $("#new_user_nick").val();
        }
        else {
            alert("Please enter a nick name")
        }
        if ($("#new_user_password").val() !== '') {
            data.user_password = $("#new_user_password").val();
        }
        else {
            alert("Please enter password")
        }
        if ($("#new_user_name").val() !== '' && $("#new_user_password").val() !== '') {
            console.log($("#new_user_name").val() + " " + $("#new_user_password").val())
            // send login data after asynchronous resource has finished
            getResource("http://localhost:5000/api/users/", function(body) {
                addUserCtrl = body["@controls"]["annometa:add-user"];
                sendAddUserData(addUserCtrl.href, addUserCtrl.method, data, renderAddUserResponse);
            });
        }            
    }); 
}

// USER ACCOUNT page -------------------------------------------------------------
// can be used to delete user or change password

function renderUserData(body) {
    // show html form
    $("#newUserFormId").show();
    // show/hide buttons
    $("#deleteUserBtnId").show();
    $("#editUserBtnId").show();
    $("#addUserBtnId").hide();
    $("#loginUserBtnId").hide();
    $("#textListBtnId").hide();    
    $("#userAccountBtnId").hide();

    $("#new_user_name").attr("value", body.user_name);
    $("#new_user_name").attr('disabled', true);
    $("#new_user_nick").attr("value", body.user_nick);
    $("#new_user_nick").attr('disabled', true);
    //$("#new_user_password").attr("value", body.user_password);

    let data = {};

    // define delete for user that already exists
    $("#deleteUserBtnId").on( "click", function(event) {
        event.preventDefault();
        //console.log("User delete not implemented yet");
        if ($("#new_user_password").val() !== '') {
            data.user_password = $("#new_user_password").val();
            data.user_name = $("#new_user_name").val();
            let deleteUserCtrl = body["@controls"]["annometa:delete"];
            console.log()
            deleteResource(deleteUserCtrl.href, renderHomePage);
        }
        else {
            alert("Password cannot be empty")
        }
    });

    // define put-edit for user that already exists
    $("#editUserBtnId").on( "click", function(event) {
        event.preventDefault();
        //console.log("User edit not implemented yet");
        if ($("#new_user_password").val() !== '') {
            data.user_password = $("#new_user_password").val();
            data.user_name = $("#new_user_name").val();             
            let editCtrl = body["@controls"]["edit"];            
            console.log()
            sendData(editCtrl.href, editCtrl.method, data, function() {
                $("#newUserFormId").hide();
                getResource(body["@controls"]["self"]["href"], renderSelection);
            });
        }
        else {
            alert("Password cannot be empty")
        }
    });
}

// Toolbox page -------------------------------------------------------------

// render device / user account selection
function renderSelection(body) {    
    console.log(body);
    // define logged in current user
    sessionStorage.setItem("CurrentUser", body.user_name);
    // define html form for device selection buttons
    let form = $("#selectionFormId");
    // show UI blocks
    document.getElementById("leftSidebar").style.display = "block";
    document.getElementById("rightSidebar").style.display = "block";
    // clear the view before rendering
    $("div.navigation").empty();
    // show buttons
    showUserFormButtons();
    
    $("#textListBtnId").show();
    $("#userAccountBtnId").show();
    // hide buttons and tables
    $("#newUserFormId").hide();
    $("#addUserBtnId").hide();
    $("#editUserBtnId").hide();
    $("#deleteUserBtnId").hide();
    $("#loginUserBtnId").hide();
    // do not empty - to show bootswatch sandstone
    // muutos $(".resulttable thead").empty();
    $(".resulttable tbody").empty(); 
    $("#userFormId").hide();

    // use .off to prevent textListBtnId event firing more than once
    $("#textListBtnId").off('click').on('click', function(event) {
        event.preventDefault();                
        sessionStorage.setItem("current_page", current_page);            
        getResource(`http://localhost:5000/api/texts/pages/page?page=${sessionStorage.getItem("current_page")}&showOnPage=${numberOfItemsOnPage}`, renderTextsInPage);
    });

    $("#userAccountBtnId").on( "click", function(event) {
        event.preventDefault();
        getResource(body["@controls"]["self"]["href"], renderUserData);
    });    
}


// Text table page -------------------------------------------------------------

// define table items for text
function createItemTable(item, links) {    
    let textlink = truncate(item.HSOriginalComment);
    // @controls.textannotation.href
    // to have annotation reference here in some day
    //let annotationPolarity = "No annotation";
    let link = "<a tabindex='0'" + 
    "data-bs-toggle='popover'" + 
    "data-bs-trigger='focus'" + 
    "title='Complete text'" + 
    "data-bs-content='" + 
    item.HSOriginalComment + "'>" + 
    textlink + "</a>";

    /* Future implementation, For retrieving annotation reference
    if (item["@controls"].hasOwnProperty("textannotation")) {
        getResource(item["@controls"]["textannotation"]["href"], function(annotation) {
            annotationPolarity = `Polarity ${annotation.SentencePolarity}`;
        });
    }*/        
    return "<tr><td>" + item.id +
            "</td><td>" + link +                        
            "</td><td>" + links + "</td></tr>";   
}

function renderTextPage(parent, page) {        
    page.forEach(function (textItemOnPage) {
        if (!("pagenumber" in textItemOnPage)) {
            parent.append(TextContentRow(textItemOnPage));
        }
    });
}

// define item print outs for Text Content metadata 
function TextContentRow(item) {
    let links = "<a href='" +
        item["@controls"].self.href +     
        "' class='btn btn-danger' tabindex='-1' role='button' onclick='followLink(event, this, deleteTextContent)'>Delete</a>&nbsp;" +		
		"<a href='" +
        item["@controls"].self.href +     
        "' class='btn btn-primary' tabindex='-1' role='button' onclick='followLink(event, this, renderTextsCarousel)'>Modify</a>";
        return createItemTable(item, links);
}

// define delete for text on list/table
function deleteTextContent(textItem) {
    let deleteCtrl = textItem["@controls"]["annometa:delete"];
    deleteTextResource(deleteCtrl.href);
    // Define delay with set timeout
    setTimeout(() => {getResource(`http://localhost:5000/api/texts/pages/page?page=${sessionStorage.getItem("current_page")}&showOnPage=${numberOfItemsOnPage}`, renderTextsInPage)}, 1000);
}

// REQUIRED for text list update, when a new is added
function getSubmittedTextContent(data, status, jqxhr) {
    renderMsg("Text update was successful");    
    getResource(`http://localhost:5000/api/texts/pages/page?page=${sessionStorage.getItem("current_page")}&showOnPage=${numberOfItemsOnPage}`, renderTextsInPage);
}

// for adding a new text - define render for TextContent
function renderTextForm(ctrl) {
    $("#textUploadFormId").show();
    $("#textUploadFormId").attr("action", ctrl.href);
    $("#textUploadFormId").attr("method", ctrl.method);

    $("#cancelUploadBtn").show();
    $("#uploadBtn").show();

    $("#cancelUploadBtn").off('click').on("click", function(event) {        
        event.preventDefault();
        $("#HateSpeechTextarea").val('');
    });

    $("#uploadBtn").off('click').on("click", function(event) {        
        event.preventDefault();                
        $("#cancelUploadBtn").hide();
        $("#uploadBtn").hide();
        
        let form = $(".textUploadForm");
                 
        let data = {};
        data.user_name = sessionStorage.getItem("CurrentUser");
        data.HSOriginalComment =  $("#HateSpeechTextarea").val();
        sendData(form.attr("action"), form.attr("method"), data, getSubmittedTextContent);        
    }); 
}

var updateButtonStatus = function() {
    if ($.trim($('#HateSpeechTextarea').val()).length < 1) {
        $("#uploadBtn").attr('disabled', true);
    } else {
        $("#uploadBtn").attr('disabled', false);        
    }    
  },
  init = function() {
    $('#textarea').change(function() {
        updateButtonStatus();      
    });        
    $('#textarea').keyup(function() {
        updateButtonStatus();      
    });    
    $('#textarea').click(function() {
        updateButtonStatus();      
    });
    setInterval(function() {
        updateButtonStatus();      
    }, 500);
  };

function renderTextsCarousel(item) {
    // clear the view before rendering
    $("div.navigation").empty();
    // do not empty - to show bootswatch sandstone
    // muutos  $(".resulttable thead").empty();
    $(".resulttable tbody").empty();    
    $(".textListForm").hide();    

    $("div.navigation").html(
        "<a href='" +
        "' onClick='getTextCollection(event)'> Back to text list </a>"
    );

    //$("div.navigation").html(
    //    "<a href='" +
    //    "' onClick='backToData(event)'> Back to Data </a>");
    
    $('.textAnnotationForm').css({'display':'block'});
    getResource("http://localhost:5000/api/texts/", function(texts) {        
        renderCarousel(texts, item);
    });

    populateAnnotationForm(item);
}

function populateAnnotationForm(item) {
    // provides annotation as response if there is one
    if (item["@controls"].hasOwnProperty("textannotation"))
    {
        // api/textannotations/<id>/
        getResource(item["@controls"].textannotation.href, function(annotationItem) {
            populateTextAnnotationForm(annotationItem, true);
        });
    }
    else {
        // create and define POST-add for new annotation
        populateEmptyTextAnnotationForm(item);
    }
}

function renderCarousel(body, selectedItem) {
    let ci = $(".carousel-inner");
    let position = 0;
    body.items.forEach(function (item) {
        if (item.id === selectedItem.id) {            
            ci.append(createCarouselItem(item, true));
        }
        else {            
            ci.append(createCarouselItem(item, false));
        }        
        position++;
    });   
}

function createCarouselItem(item, setAsActive) {
    let cItem = $("<div>", {"class":"carousel-item"});
    if (setAsActive) {
        cItem.addClass("active");
    }
    cItem.addClass("text-center p-4");    
    cItem.append(createCarouselTextElement(item));    
    cItem.append(createTextId(item["@controls"].self.href));
    return cItem;
}

function createCarouselTextElement(item) {
    let textItem = "<p>" + 
    item.HSOriginalComment + 
    "</p>";
    return textItem;
}

function createTextId(id) {
    let textId = document.createElement('div');
    textId.style.display = "none";
    textId.classList.add("text-item-id");
    let textHref = document.createElement('p');
    textHref.classList.add("text-href");
    textHref.innerText = id;
    textId.append(textHref);    
    return textId;
}

// ---------------------------------------------------------------------
// define page/window for text data table
// function to render uploaded text data and metadata

function renderTexts(body) {
    // clear the view before rendering    
    document.getElementById("leftSidebar").style.display = "none";
    document.getElementById("rightSidebar").style.display = "none";
    
    $("#HateSpeechTextarea").val('');
    $("div.navigation").empty();
    // do not empty - to show bootswatch sandstone
    // muutos $(".resulttable thead").empty();
    $(".resulttable tbody").empty();    
       // carousel class ref
    $(".carousel-indicators").empty();
    $(".carousel-inner").empty();
    
    hideAnnoFormButtons();
    $("#textListFormId").show();
    
    //$("div.navigation").html(
    //    "<a href='" +        
    //    "' onClick='gotoToolbox(event)'> Go to Toolbox </a>"         
    //);        

    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(TextContentRow(item));
    });    
    
    renderTextForm(body["@controls"]["annometa:add-text"]);
}

// ---------------------------------------------------------------------
// NOT USED currently, renders all pages 
// define page/window for paginated text data table
// function to render uploaded text data and metadata in pages

function renderTextsInPages(body) {
    // clear the view before rendering    
    document.getElementById("leftSidebar").style.display = "none";
    document.getElementById("rightSidebar").style.display = "none";
    
    $("#HateSpeechTextarea").val('');
    $("div.navigation").empty();
    // do not empty - to show bootswatch sandstone
    // muutos $(".resulttable thead").empty();
    $(".resulttable tbody").empty();    
       // carousel class ref
    $(".carousel-indicators").empty();
    $(".carousel-inner").empty();
    
    hideAnnoFormButtons();
    $("#textListFormId").show();       

    $(".resulttable").empty();    
    
    renderPaginationLinks( document.getElementById("hatespeechPagesId"), body["@pagecount"], sessionStorage.getItem("current_page"));

    for (let i = 0; i < body.pages.length; i++) {
        $element = $(('<tbody></tbody>'));
        $element.attr("page", i+1);
        $(".resulttable").append($element);
        renderTextPage($element, body.pages[i]);        
    }
    
    renderTextForm(body["@controls"]["annometa:add-text"]);
}

// ---------------------------------------------------------------------
// define page/window for paginated text data table
// function to render uploaded text data and metadata in pages

function renderTextsInPage(body) {
    // clear the view before rendering    
    document.getElementById("leftSidebar").style.display = "none";
    document.getElementById("rightSidebar").style.display = "none";
    
    $("#HateSpeechTextarea").val('');
    $("div.navigation").empty();
    // do not empty - to show bootswatch sandstone
    // muutos $(".resulttable thead").empty();
    $(".resulttable tbody").empty();    
       // carousel class ref
    $(".carousel-indicators").empty();
    $(".carousel-inner").empty();
    
    hideAnnoFormButtons();
    $("#textListFormId").show();         
    
    renderPaginationLinks( document.getElementById("hatespeechPagesId"), body["@pagecount"], sessionStorage.getItem("current_page"));

    let tbody = $(".resulttable tbody");
    tbody.empty();
    body.items.forEach(function (item) {
        tbody.append(TextContentRow(item));
    });  
    
    renderTextForm(body["@controls"]["annometa:add-text"]);
}

// make the pagination links at the bottom of the page
function renderPaginationLinks(parent, pageCount, currentPage) {
    $("#hatespeechPagesId").empty();        
    for (let i = 1; i <= pageCount; i++) {                        
        let button = addPageItem(i, currentPage);
        parent.appendChild(button);
    }    
}

// make the individual page link to the bottom of the page
function addPageItem(pagenumber, currentPage) {
    let paginationBtn = document.createElement("li");
    paginationBtn.classList.add("page-item");
    let pageLink = document.createElement("a");
    pageLink.classList.add("page-link");
    pageLink.setAttribute("href", "#");
    pageLink.innerText = pagenumber;
    if (parseInt(currentPage) === pagenumber) {
        paginationBtn.classList.add("active");
    }
    paginationBtn.addEventListener('click', function(e) {
        e.preventDefault();
        console.log(e.target.innerText);
        sessionStorage.setItem("current_page", e.target.innerText);
        getResource(`http://localhost:5000/api/texts/pages/page?page=${e.target.innerText}&showOnPage=${numberOfItemsOnPage}`, renderTextsInPage);

    });
    paginationBtn.append(pageLink);
    
    return paginationBtn;
}
// helper functions for text annotation -----------------------------------

function createheaderForFormRow(valueString) {
    return "<div class='col-md-2 col-form-label'><label>'" +
                valueString + "</label></div>"
}

function createSpanForFormRow(valueString) {
    return "<div class='col-md-5'><span>'" +
                valueString + "</span></div>"
}

function appendToForm(form, rowHeader, rowValue) {
    let rowElement = "<div class='row'>" + rowHeader + rowValue + "</div>";
    form.append(rowElement);
}

function getSubmittedAnnotation(data, status, xhr) {
    renderMsg("Submit of new annotation was successful");
    let href = xhr.getResponseHeader("Location");
    console.log(href);
    if (href) {
        getResource(href, populateTextAnnotationForm);
    }
}

function getEditedAnnotation(data, status, xhr) {
    renderMsg("EDIT of annotation was successful");
    let href = xhr.getResponseHeader("Location");
    console.log(href);
    if (href) {
        getResource(href, populateTextAnnotationForm);
    }
}

// define checkbox values to json format

function isHateSpeech() {
    const rb = document.getElementById("isHateSpeechRadio");
    if (rb.checked) {
        return true;
    }
    return false;
}

function getCheckedValue(radioButtonGroupName) {
    const rbs = document.querySelectorAll(`input[name="${radioButtonGroupName}"]`);
    for (const rb of rbs) {
        if (rb.checked) {
            return parseInt(rb.value);                    
        }
    }        
}

// ----------------------------------------------------------------------------------

function showAnnoFormButtons() {
    $("#addAnnotationBtnId").show();
    $("#editAnnotationBtnId").show();
    $("#editAnnotationBtnId").prop("disabled", false);
    $("#deleteAnnotationBtnId").show();
    $("#deleteAnnotationBtnId").prop("disabled", false);
}

function hideAnnoFormButtons() {
    $("#addAnnotationBtnId").hide();
    $("#editAnnotationBtnId").hide();
    $("#deleteAnnotationBtnId").hide();
    $(".textListForm").hide();
}

function showSaveButtons() {
    $("#submitChangesBtnId").show();
    $("#cancelChangesBtnId").show();
}

function hideSaveButtons() {
    $("#submitChangesBtnId").hide();
    $("#cancelChangesBtnId").hide();
}

// EDIT - PUT for text annotation --------------------------------------------------------------

function putTextAnnotationContent(event) {
    event.stopPropagation();
    let data = {};
    let form = $(".annotationMetaForm");

    data.id = parseInt(($('input[id="annotationId"]', '#testform').val()));
    data.text_id = parseInt(($('input[id="textId"]', '#testform').val()));
    data.user_id = parseInt(($('input[id="userId"]', '#testform').val()));
    data.HS_binary = isHateSpeech();    
    data.SentencePolarity = getCheckedValue("polarityRadioOptions");    
    data.HS_class =  getCheckedValue("intensityRadioOptions");
    data.HS_category = getSelectedValues();    
    data.SentenceEmotionCategory = $("#SentenceEmotionCategory").val();
    data.HSinUrbanFinnish = $("#HSinUrbanFinnish").val();
    data.HSinFinnish = $("#HSinFinnish").val();    

    sendData(form.attr("action"), form.attr("method"), data, getEditedAnnotation);
}

function getSelectedValues() {
    selectedList = [];
    $('.HSCategoryButton').each(function() {
        if (this.checked)
            selectedList.push( this.labels[0].innerText);       
    });
    return selectedList.join(",  ");        
}

function editTextAnnotationContent(event) {
    event.stopPropagation();
    $("#testform").find('*').attr('disabled', false);
    hideAnnoFormButtons();    

    // prevent submit changes event firing more than once
    $("#submitChangesBtnId").off('click').on('click', function(event) {
        putTextAnnotationContent(event);
    });    
    
    $("#cancelChangesBtnId").on( "click", function(e) {                
        const annoForm = $("#annotationMetaFormId");
        getResource(annoForm.attr("action"), populateTextAnnotationForm);
    });
}

// ADD - POST for text annotation --------------------------------------------------------------

function submitTextAnnotationContent(event) {
    //event.stopPropagation();
    let data = {};
    let form = $(".annotationMetaForm");
        
    data.id = parseInt(($('input[id="annotationId"]', '#testform').val()));
    data.text_id = parseInt(($('input[id="textId"]', '#testform').val()));
    data.user_id = parseInt(($('input[id="userId"]', '#testform').val()));
    data.HS_binary = isHateSpeech();
    data.SentencePolarity = getCheckedValue("polarityRadioOptions");    
    data.HS_class =  getCheckedValue("intensityRadioOptions");
    data.HS_category = getSelectedValues();   
    data.SentenceEmotionCategory = $("#SentenceEmotionCategory").val();
    data.HSinUrbanFinnish = $("#HSinUrbanFinnish").val();
    data.HSinFinnish = $("#HSinFinnish").val();    
    
    sendData(form.attr("action"), form.attr("method"), data, getEditedAnnotation);
}

function populateEmptyTextAnnotationForm(textItem) {
    $("div.notification").empty();
    $('.textAnnotationForm').css({'display':'block'});
    
    $("#testform").show();
    // set current user and text id's
    $("#annotatorName").attr("value", sessionStorage.getItem("CurrentUser"));
    $("#textId").attr("value", textItem.id);
    $("#userId").attr("value", textItem.user_id);
    $("#annotationId").attr("value", $("#annotationId").attr("placeholder"));

    // clear text fields if not already empty
    $("#HSinFinnish").val('');
    $("#HSinUrbanFinnish").val('');
    $("#SentenceEmotionCategory").val('');   

    // uncheck all radio button groups
    uncheckRadioButton("binaryRadioOptions");
    uncheckRadioButton("polarityRadioOptions");
    uncheckRadioButton("intensityRadioOptions");
        
    clearHSCategoryPlaceHolder();
    populateHSCategoryButtonGroups(HSCategoryLists);

    // enable fields
    $("#testform").find('*').attr('disabled', false);        

    // get textannotation collection to get the control, method and encoding
    getResource(textItem["@controls"].textannotations.href, function(annotationCollection) {
        console.log(annotationCollection);
        ctrl = annotationCollection["@controls"]["annometa:add-textannotation"];                
        $("#annotationMetaFormId").attr("action", ctrl.href);
        $("#annotationMetaFormId").attr("method", ctrl.method);
        console.log($("#annotationMetaFormId").attr("method"));
        console.log($("#annotationMetaFormId").attr("action"));
    });
    $("#testform").show();
    $("#addAnnotationBtnId").show();
    $("#editAnnotationBtnId").hide();
    $("#deleteAnnotationBtnId").hide();
    $("#addAnnotationBtnId").off('click').on( "click", function(event) {      
        event.preventDefault();  
        submitTextAnnotationContent(event);
      });      
}

function enableTextFields() {    
  let checkBox = document.getElementById("text_class");  
  if (checkBox.checked == true){    
    $("#text_language").prop( "disabled", false );
    $("#text_text").prop( "disabled", false );
  } else {
    $("#text_language").prop( "disabled", true );    
    $("#text_text").prop( "disabled", true );
  } 
}

// -------------------------------------------------------------------------------------
function uncheckRadioButton(group) {
    const rbs = document.querySelectorAll(`input[name="${group}"]`);            
    for (const rb of rbs) {
        rb.checked = false;                    
    }       
}

function updateRadioValue(group, value) {
    const rbs = document.querySelectorAll(`input[name="${group}"]`);            
    for (const rb of rbs) {
        if (parseInt(rb.value) === value) {
            rb.checked = true;
            break;
        }
    }            
}

function populateHSCategorySelection(list) {
    let selection = $("#HSCategorySelect");
    let i = 1;
    for (const item in list) {
        let option = `<option value="${i}">${item}</option>`;
        selection.appendChild(option);
        i++;
    }
}

function populateHSCategoryButtonGroups(grouplist) {
    let buttonGroup = document.getElementById("HSCategoryPlaceHolder");
    let i = 1;
    grouplist.forEach(group => {
        let rowDiv = document.createElement("div");
        rowDiv.classList.add("row");
        // Make an div element like this : <div class="col-md-2 col-form-label"><label class="HS_category_header">HS categories</label></div>
        let colDiv = document.createElement("div");
        colDiv.classList.add("col-md-2");
        colDiv.classList.add("col-form-label");
        let label = document.createElement("label");
        label.classList.add("HS_category_header");
        label.innerText = `HS categories ${i}`;
        colDiv.appendChild(label);
        rowDiv.appendChild(colDiv);
        
        let colSMDiv = document.createElement("div");
        colSMDiv.classList.add("col-sm");
        // Make an div element like this : <div class="btn-group" id="HSCategoryButtons" role="group" aria-label="Hatespeech category selectors"></div>
        let btnGroup = document.createElement("div");
        btnGroup.classList.add("btn-group");
        btnGroup.id = `HSCategoryButtons_${i}`;
        btnGroup.setAttribute("role", "group");
        btnGroup.setAttribute("aria-label", "Hatespeech category selectors");
        // add buttons to btnGroup parent element
        populateHSCategoryButtons(btnGroup, group, i);
        colSMDiv.appendChild(btnGroup);
        rowDiv.appendChild(colSMDiv);
        buttonGroup.appendChild(rowDiv);
        i++;   
    });
}

function populateHSCategoryButtons(parent, list, groupId) {
    let i = 1;
    list.forEach(item => {
        let input = `<input type="checkbox" class="btn-check HSCategoryButton" id="ctrBtnCheck${groupId}_${i}" autocomplete="off">`;
        let label = `<label class="btn btn-outline-primary" for="ctrBtnCheck${groupId}_${i}">${item}</label>`        
        parent.insertAdjacentHTML( 'beforeend', input );        
        parent.insertAdjacentHTML( 'beforeend', label );
        i++;
    });
}

function populateSelectedHSCategoryButtonGroups (grouplist) {
    let buttonGroup = document.getElementById("HSCategoryPlaceHolder");
    let i = 1;
    grouplist.forEach(group => {    
        let rowDiv = document.createElement("div");
        rowDiv.classList.add("row");
        // Make an div element like this : <div class="col-md-2 col-form-label"><label class="HS_category_header">HS categories</label></div>
        let colDiv = document.createElement("div");
        colDiv.classList.add("col-md-2");
        colDiv.classList.add("col-form-label");
        let label = document.createElement("label");
        label.classList.add("HS_category_header");
        label.innerText = `HS categories ${i}`;
        colDiv.appendChild(label);
        rowDiv.appendChild(colDiv);
        
        let colSMDiv = document.createElement("div");
        colSMDiv.classList.add("col-sm");
        //Make an div element like this : <div class="btn-group" id="HSCategoryButtons" role="group" aria-label="Hatespeech category selectors"></div>
        let btnGroup = document.createElement("div");
        btnGroup.classList.add("btn-group");
        btnGroup.id = `HSCategoryButtons_${i}`;
        btnGroup.setAttribute("role", "group");
        btnGroup.setAttribute("aria-label", "Hatespeech category selectors");
        // add buttons to btnGroup parent element
        populateSelectedHSCategoryButtons(btnGroup, group);
        colSMDiv.appendChild(btnGroup);
        rowDiv.appendChild(colSMDiv);
        buttonGroup.appendChild(rowDiv);
        i++;
    });
}

function populateSelectedHSCategoryButtons (parent, dict) {    
    dict.forEach(item => {       
        parent.insertAdjacentHTML( 'beforeend', item );               
    });
}

function checkSelectedCategories(valueString) {	
    let valuelist = valueString.split(",");
    let selectedDict = {};
    let categoryDictList = [];
    let i = 1;
    valuelist.forEach(element => 
    {    	
        let inLowerCase = element.toLowerCase().trim();        
        let input = `<input type="checkbox" class="btn-check HSCategoryButton" id="ctrBtnCheck${i}" autocomplete="off" checked><label class="btn btn-outline-primary" for="ctrBtnCheck${i}">${inLowerCase}</label>`;
        selectedDict[inLowerCase] = input;
        i++;
    });    
    
    HSCategoryLists.forEach(group => {
     		category = {};
        group.forEach(item => {
            let id = Math.random().toString();
            const guid = id.split('.').pop();
        	category[item] = `<input type="checkbox" class="btn-check HSCategoryButton" id="ctrBtnCheck${guid}" autocomplete="off"><label class="btn btn-outline-primary" for="ctrBtnCheck${guid}">${item}</label>`;
        })
        categoryDictList.push(category);
    });
      
    for(var key in selectedDict) {  	
        categoryDictList.forEach(catDict => 
        {
        	for (var catKey in catDict) {
          	    if (catKey === key) {
            	    catDict[catKey] = selectedDict[key];
                    delete selectedDict[key];
                    break;
                }
            }
        })
    }
    // if there are any values left that we received from db, add them to others -category
    if (Object.keys(selectedDict).length > 0) {
        for (const [extraKey, extraValue] of Object.entries(selectedDict))
        {
            categoryDictList.forEach(dict => {
                for (const key of Object.keys(dict)) {
                    if(key === 'other') {
                        dict[extraKey] = extraValue;
                    }
                }    
            });
        }
    }
    let selectionLists = [];
    categoryDictList.forEach(dict => {
        selectionList = [];
        for (const value of Object.values(dict)) {
      	    selectionList.push(value);
		}
        selectionLists.push(selectionList);
    });
    return selectionLists;
}


function addToSelection(valueString) {
    let valuelist = valueString.split(",");
    let cleanList = [];
    let optionlist = [];
    let i = 1;
    valuelist.forEach(element => 
    {
        let inLowerCase = element.toLowerCase().trim();
        let input = `<input type="checkbox" class="btn-check HSCategoryButton" id="ctrBtnCheck${i}" autocomplete="off" checked><label class="btn btn-outline-primary" for="ctrBtnCheck${i}">${inLowerCase}</label>`;
        optionlist.push(input);
        cleanList.push(inLowerCase);
        i++;
    });    
    i = optionlist.length + 1;
    HSCategoryList.forEach(hsitem => 
    {
        if (!cleanList.includes(hsitem)) {
            let input = `<input type="checkbox" class="btn-check HSCategoryButton" id="ctrBtnCheck${i}" autocomplete="off"><label class="btn btn-outline-primary" for="ctrBtnCheck${i}">${hsitem}</label>`
            optionlist.push(input);
        }
        i++;
    });
    let selection = $("#HSCategoryButtons")[0];
    optionlist.forEach(optionItem => {
        selection.innerHTML += optionItem;
    });    
}

function clearHSCategoryPlaceHolder() {
    let selection = $("#HSCategoryPlaceHolder")[0];
    selection.innerHTML = "";
}

function clearButtonGroup() {    
    let selection = $("#HSCategoryButtons")[0];
    selection.innerHTML = "";
}

function populateTextAnnotationForm(annotationItem, annotationExists) {
    // api/textannotations/<id>/
    getResource(annotationItem["@controls"].annotator.href, function(annotatorItem) {
        $("#annotatorName").attr("value", annotatorItem.user_name);
        $("#textId").attr("value", annotationItem.text_id);
        $("#userId").attr("value", annotationItem.user_id);
        $("#annotationId").attr("value", annotationItem.id);    
    });
    // list of items to define annotation table
    let requiredItems = annotationItem["@controls"]["edit"]["schema"]["required"];    
    console.log(requiredItems);

    // ----------------------------------------------
    
    $('.textAnnotationForm').css({'display':'block'});    
    $("#testform").show();

    $.each(requiredItems, function(index, item) {
        if (annotationItem.hasOwnProperty(item)) 
        {
            let value = annotationItem[item];
            switch (item) {
                case "HS_binary":
                    if (value === true) {
                        $("#isHateSpeechRadio").prop("checked", true);
                    }
                    else {
                        $("#notHateSpeechRadio").prop("checked", true);
                    }
                    break;
                case "HS_class":
                    updateRadioValue("intensityRadioOptions", value);
                    break;
                case "HS_category":                                                        
                    clearHSCategoryPlaceHolder();                    
                    let buttonElements = checkSelectedCategories(value);
                    populateSelectedHSCategoryButtonGroups(buttonElements);
                    break;                                
                case "SentencePolarity":
                    updateRadioValue("polarityRadioOptions", value);
                    break;                
                case "SentenceEmotionCategory":                    
                    $("#SentenceEmotionCategory").val(value);
                    break;
                case "HSinUrbanFinnish":                    
                    $("#HSinUrbanFinnish").val(value);
                    break;
                case "HSinFinnish":                    
                    $("#HSinFinnish").val(value);
                    break;                
                default:
                    break;
            }            
            // define add-post button for new annotation
            
            $("#testform").find('*').attr('disabled', true);
            showAnnoFormButtons();
            hideSaveButtons();
            $("#addAnnotationBtnId").prop("disabled", true);            
        }      
    });

    // define put-edit for annotation that already exists
    $("#editAnnotationBtnId").on( "click", function(event) {
        event.preventDefault();        
        let editCtrl = annotationItem["@controls"]["edit"];
        $("#annotationMetaFormId").attr("action", editCtrl.href);
        $("#annotationMetaFormId").attr("method", editCtrl.method);        
        showSaveButtons();
        editTextAnnotationContent(event);
      }
    );

    // define delete for annotation that already exists
    $("#deleteAnnotationBtnId").off("click").on("click",
        function(event) {
            event.preventDefault();
            let deleteCtrl = annotationItem["@controls"]["annometa:delete"];
            $("#annotationMetaFormId").attr("action", deleteCtrl.href);
            $("#annotationMetaFormId").attr("method", deleteCtrl.method);
            console.log("Delete of text annotation was succesful " + deleteCtrl.href);
            deleteResource(deleteCtrl.href, backToTextCollection);
        }
    );
}

function truncate(input) {
    if (input.length > 25) {
       return input.substring(0, 25) + '...';
    }
    return input;
};

document.addEventListener("slide.bs.carousel", function(e){    
    let div = e.relatedTarget;
    let hrefs = div.querySelector('.text-href').innerText;
    getResource(hrefs, function(textItem) {
        populateAnnotationForm(textItem);
    });
});


// ---------------------------------------------------------------------------
// render local host upload as user page / login page

$(document).ready(function () {
    sessionStorage.clear();
    $("#testform").toggle();
    init();
    getResource("http://localhost:5000/api/users/", renderHomePage);
});
