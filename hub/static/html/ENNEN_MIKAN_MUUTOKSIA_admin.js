<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="/static/css/admin.css">
    <title>ImageAnnotator hub admin site</title>
    <script type="text/javascript" src="/static/scripts/jquery.js"></script>
    <script type="text/javascript" src="/static/scripts/admin.js"></script>
    <!-- CSS only -->
</head>

<body style="margin-left: 50px; margin-right: 50px;">
    
    <div class="notification"></div>    
    <div class="navigation"></div>
    <div class="contents">
        <div class="imagemeta">
            <form class="imagemetaform">
            </form>
        </div>
        <div class="imagecontent"></div>        
        <!-- MUUTOS-->
        <form id = "testform" style="margin-top: 50px;">
        <!-- <div class="annotationMetaForm" id="annotationMetaFormId" style="display:none"> -->
            <div class="annotationMetaForm" id="annotationMetaFormId"></div>
                <div class="row g-3">
                    <div class='col-md-2 col-form-label'>
                        <label for="annotatorName" class="col-sm-2 col-form-label">Annotator</label>                
                    </div>
                    <div class="col-sm-3" id="annotatorNameDiv">
                        <input class="form-control" id="annotatorName" type="text" readonly>                            
                    </div>
                    <label for="imageId" class="col-sm-2 col-form-label">Image ID</label>
                    <div class="col-sm" id="imageIdDiv">
                        <input class="form-control" id="imageId" type="text" readonly>                            
                    </div>        
                </div> 
                <div class="row g-3">
                    <label for="userId" class="col-sm-2 col-form-label col-form-label-sm">User ID</label>
                    <div class="col-sm-3" id="userIddiv">                            
                        <input class="form-control" id="userId" type="text" readonly>
                    </div>
                    <label for="annotationId" class="col-sm-2 col-form-label col-form-label-sm">Annotation ID</label>
                    <div class="col-sm" id="annotatorIdDiv">                
                        <input class="form-control" id="annotationId" type="text" placeholder="Annotation not yet saved..." readonly>
                    </div>        
                </div>
                <div class="row">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="meme_class" disabled>
                        <label class="form-check-label" for="meme_class">
                            Image is a meme
                        </label>
                    </div>
                </div>
                <div class="row">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="HS_class" disabled>                
                        <label class="form-check-label" for="HS_class">Image is or contains hatespeech</label>
                    </div>                         
                </div>        
                <label class="Polarity_classA_header">Polarity_classA</label>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="inlineRadioOptions" id="Polarity_classA_Positive" value="1" checked disabled>
                    <label class="form-check-label" for="Polarity_classA_Positive">Positive</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="inlineRadioOptions" id="Polarity_classANeutral" value="0" disabled>
                    <label class="form-check-label" for="Polarity_classANeutral">Neutral</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="inlineRadioOptions" id="Polarity_classA_Negative" value="-1" disabled>
                    <label class="form-check-label" for="Polarity_classA_Negative">Negative</label>
                  </div>
            
                <div class="row">
                    <label for="Polarity_classB" class="form-label Polarity_classB_header">Polarity_classB</label>
                    <input id="Polarity_classB" type="range" value="0" name="rangeInputclassB" min="-5" max="5" onchange="updatePolarityClassB(this.value);" disabled>
                    <input type="text" id="valuePolarity_classB" value="" readonly>
                </div>
                <div class="row">
                    <label for="HS_strength" class="form-label HS_strength_header">HS_strength</label>
                    <input id="HS_strength" type="range" value="-1" name="rangeInputclassHS" min="-7" max="-1" onchange="updateHSStrength(this.value);" disabled>
                    <input type="text" id="valueHS_strength" value="" readonly>            
                </div>
            
                <div class="row">
                    <div class="col-md-2 col-form-label"><label class="HS_category_header">HS_category</label></div>
                    <div class="col-sm">
                        <input class="form-control" id="HS_category" type="text" value="" disabled>                            
                    </div> 
                </div>
                <div class="row">
                    <div class="form-check">
                        <label class="form-check-label" for="text_class">Image contains text</label>
                        <input class="form-check-input" type="checkbox" value="" id="text_class" onclick="enableTextFields()" disabled>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-2 col-form-label"><label class="Text_language_header">Text_language</label></div>
                    <div class="col-sm">
                        <input class="form-control" id="text_language" type="text" disabled>                            
                    </div> 
                </div>
                <div class="row">
                    <div class="col-md-2 col-form-label"><label class="Text_text_header">Text_text</label></div>
                    <div class="col-sm">
                        <input class="form-control" id="text_text" type="text" disabled>                            
                    </div> 
                </div>
                <div class="container" style="margin-top: 20px;">
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end" id="formButtonGroupId">
                        <button class="btn btn-danger" id="deleteAnnotationBtnId" type="button" style="display:none">Delete</button>
                        <button class="btn btn-warning me-md-2" id="editAnnotationBtnId" type="button" style="display:none">Edit</button>
                        <button class="btn btn-primary me-md-2" id="addAnnotationBtnId" type="submit" style="display:none">Add</button>
                    </div>
                </div>
            </div>            
        </form>
        <!--<div class="annotation">
            <form class="annotationform">                                
            </form>
        </div>        -->
        <div class="tablecontrols"></div>
        <div class="tablecontents">
            <table class="resulttable">
                <thead>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>
        <div class="tablecontrols"></div>

        <!-- USER window and tables -->
        <div class="usermetaform">
            <div class="usermetaform left">
                <div class="login-main-text"></div>
                    <h2>Application<br> Login Page</h2>
                    <p>Login or register from here to access.</p>
                </div>
            </div>
            <div class="usermetaform right"></div>
                <form class="row g-3 needs-validation" id = "userFormId" style="margin-top: 50px;" novalidate>
                    <!-- div class="row"> -->
                        <!--<div class="col-md-2 col-form-label"> -->
                        <div class="col-md-6">   
                            <label for="user_name" class="form-label">USER NAME</label>
                        </div>
                        <div class="col-sm">
                            <input class="form-control" id="user_name" type="text" required>
                            <div class="valid-feedback">
                                Ok!
                            </div>
                            <div class="invalid-feedback">
                                Please enter username.
                            </div>
                        </div> 
                    <!-- </div> -->
                    <!-- <div class="row"> -->
                        <!-- <div class="col-md-2 col-form-label"> -->
                        <div class="col-md-6">                        
                            <label for="user_password" class="form-label">USER PASSWORD</label>
                        </div>
                        <div class="col-sm">
                            <input class="form-control" id="user_password" type="password" required>                            
                        </div>
                    <!-- </div> -->
                    <div id="userLoginButtonContainerId" class="container" style="margin-top: 20px;">
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end" id="formButtonGroupId">
                            <button class="btn btn-danger" id="deleteUserBtnId" type="button" style="display:none">Delete user</button>
                            <button class="btn btn-warning me-md-2" id="editUserBtnId" type="button" style="display:none">Edit password</button>
                            <button class="btn btn-primary me-md-2" id="addUserBtnId" type="submit" style="display:none">Add new user</button>
                            <button class="btn btn-success me-md-2" id="loginUserBtnId" type="submit" style="display:none">Login user</button>
                        </div>
                    </div>
                </form>
            </div>
        </div> 

    </div>
    <div class="form">
        <form class="imageUploadForm" id="imageUploadFormId">
            <button class="btn btn-primary me-md-2" type="button" id="uploadFileBtnId" style="display:none">Add new image</button>
            <input type="file" id="fileElem" accept="image/*" style="display:none">
            <div class="fileList" id="fileList" style="margin-top: 10px;">
                <p id="fileInfoId" style="display: none;">No files selected!</p>
            </div>
            <div class="d-grid gap-2 d-md-block">
                <button class="btn btn-secondary" id="cancelUploadBtn" type="button" style="display:none">Cancel</button>
                <button class="btn btn-primary" id="uploadBtn" type="submit" style="display:none">Upload</button>
              </div>
        </form>
    </div>
</body>