


# ----------------------------------------------------------------------------------------------------------------
# Image and Image Collection Resources

class ImageCollection(Resource):
    """
    Resource for ImageCollection. 
    Function GET gets all the images in collection and POST adds a new image to collection.
    """

    def get(self):
        """
        GET method gets all the images from ImageCollection
        """
        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.imagecollection"))
        body.add_control_add_image()
        body["items"] = []
        
        # db query filters images and photos with is_private flag
        # request separates images and photos also with is_private flag
        # for db_photoid in Photo.query.all():
        
        for image in ImageContent.query.filter(ImageContent.is_private == False):
        
            item = HubBuilder(
                id = image.id,
                user_id = image.user_id,
                name = image.name,
                publish_date = image.publish_date,
                location = image.location,
                is_private = image.is_private,
                date = image.date
            )
            item.add_control("self", url_for("api.imageitem", id=image.id))
            item.add_control("profile", IMAGE_PROFILE)
            if image.image_annotations != []:
                item.add_control("imageannotation", url_for("api.imageannotationitem", id=image.image_annotations[0].id))
            body["items"].append(item)
        
        # definition default=str below because of datetime objects
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)


    def post(self):
        """
        POST method adds a new image to ImageCollection
        """       
        # req_content changes request form to json
        # exception if something goes wrong
        try:
            req_content = json.loads(request.form['request'])
        except Exception as e:
            print('Post exception : ' + str(e), file=sys.stderr)    
            return create_error_response(400, "Invalid JSON document", str(e))  

        # request content = req_content - includes user and private flag
        # user must be provided for photos / images
        if "user_name" in req_content:
            if req_content["user_name"] == "" or req_content["user_name"] == None:
                return create_error_response(400, "Invalid JSON document", "No user provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No user provided")
        
        # is_private must be provided for photos / images
        if "is_private" in req_content:
            if req_content["is_private"] == "" or req_content["is_private"] == None:
                return create_error_response(400, "Invalid JSON document", "No privacy flag provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No privacy provided")

        # query current user from database
        currentUser = User.query.filter_by(user_name=req_content["user_name"]).first()        
        # print('Query db currentUser : ' + str(currentUser.user_name), file=sys.stderr)
        
        # check if the post request has the file part
        if 'image' not in request.files:
            return create_error_response(400, "No file provided", "No image file found in the request")

        # check if there's a file in the request
        image = request.files['image']
        if image:            
            if image.filename == '':
                return create_error_response(400, "No file provided", "No image file found in the request")
            try:                
                imageUpload = create_image_item_from_request(req_content, image, UPLOAD_FOLDER_IMAGES)
            except Exception as e:
                create_error_response(500, "Failed to save the file", str(e) + " Failed to save file '{}'".format(image.filename))

            try:
                #print("Image publish date", imageUpload.publish_date)
                #print("Image upload date", imageUpload.date)

                currentUser.image_user.append(imageUpload)
                db.session.commit()

                # query photo item by name
                db_image = ImageContent.query.filter_by(name=imageUpload.name).first()
                #print('PRINT db_image ID :  ' + str(db_image.id), file=sys.stderr)
                return Response(status=201, headers={"Location": url_for("api.imageitem", id=db_image.id)})

            # return error response if the file exists already
            except IntegrityError:
                return create_error_response(409, "Already exists", "Image with id '{}' already exists".format(request.json["id"]))
        
            # return error response if failed to save the file
            except Exception as e:
                create_error_response(500, "Failed to save the file", str(e) + " Failed to save file '{}'".format(image.filename))
            
            # ------------------------------------------------------------
            # following two rows below return the same answer (on Postman)
            # returns api/images/<id>/ - TOIMII - vastaus on 201
            
            # http://localhost:5000/api/images/21/ 
            #return Response(status=201, headers={"Location": url_for("api.imageitem", id=db_image.id)})

            # http://localhost:5000/api/images/?id=22
            #return Response(status=201, headers={"Location": url_for("api.imagecollection", id=db_image.id)})
            # ------------------------------------------------------------
        else:
            return create_error_response(400, "No file provided", "No image file found in the request")


class ImageItem(Resource):
    """
    Resource for ImageItem. 
    Function GET gets one single image, PUT edits the image, and DELETE deletes the image.
    """

    def get(self, id):
        """
        GET method gets one single image
        """
        db_imageid = ImageContent.query.filter_by(id=id).first()
        if db_imageid is None:
            return create_error_response(404, "Not found", "No image was found with id {}".format(id))        

        body = HubBuilder(
                id = db_imageid.id,
                user_id = db_imageid.user_id,
                name = db_imageid.name,
                publish_date = db_imageid.publish_date,
                location = db_imageid.location,
                is_private = db_imageid.is_private,
                date = db_imageid.date
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.imageitem", id=id))
        body.add_control("profile", IMAGE_PROFILE)
        body.add_control("collection", url_for("api.imagecollection"))
        if db_imageid.image_annotations != []:            
            body.add_control("imageannotation", url_for("api.imageannotationitem", id=db_imageid.image_annotations[0].id))
        else:
            body.add_control("imageannotations", url_for("api.imageannotationcollection"))
        body.add_control_delete_image(id)
        body.add_control_edit_image(id)

        # definition default=str below because of datetime objects
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)

    def put(self, id):
        """
        PUT method edits one single image 
        """
        db_imageid = ImageContent.query.filter_by(id=id).first()

        if db_imageid is None:
            return create_error_response(404, "Not found", "No image was found with id {}".format(id))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        if "name" in request.json:
            if request.json["name"] == "" or request.json["name"] == None:
                return create_error_response(400, "Invalid JSON document", "No file name provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No file name provided")      
        
        is_db_image_name = ImageContent.query.filter_by(name=request.json["name"]).first()
        if is_db_image_name is None:
            db_imageid.name = request.json["name"]
            db.session.commit()
        else:
            return create_error_response(409, "Already exists", "Image with name '{}' already exists".format(request.json["name"]))
        
        return Response(status=204, headers={"Location": url_for("api.imageitem", id=db_imageid.id)})

    def delete(self, id):
        """
        DELETE method deletes one single image
        """
        db_imageid = ImageContent.query.filter_by(id=id).first()
        if db_imageid is None:
            return create_error_response(404, "Not found", "No image was found with id {}".format(id))
        
        db.session.delete(db_imageid)
        db.session.commit()
        return Response(status=204)


# -----------------------------------------------------------------------------------------------------------------
# Imageannotation and Imageannotation Collection Resources

class ImageannotationCollection(Resource):
    """
    Resource for ImageannotationCollection. 
    Function GET gets all the imageannotations in collection
    and POST adds a new imageannotation to collection.
    """

    def get(self):
        """
        GET method gets all imageannotations from ImageannotationCollection
        """
        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.imageannotationcollection"))
        body.add_control_add_imageannotation()
        body["items"] = []

        for db_imageanno_id in ImageAnnotation.query.all():

            item = HubBuilder(
                id = db_imageanno_id.id,
                image_id = db_imageanno_id.image_id,
                user_id = db_imageanno_id.user_id,
                meme_class = db_imageanno_id.meme_class,
                HS_class = db_imageanno_id.HS_class,
                text_class = db_imageanno_id.text_class,
                polarity_classA = db_imageanno_id.polarity_classA,
                polarity_classB = db_imageanno_id.polarity_classB,
                HS_strength = db_imageanno_id.HS_strength,
                HS_category = db_imageanno_id.HS_category,
                text_text = db_imageanno_id.text_text,
                text_language = db_imageanno_id.text_language
            )
            item.add_control("self", url_for("api.imageannotationcollection"))
            item.add_control("profile", IMAGEANNOTATION_PROFILE)
            body["items"].append(item)
        return Response(json.dumps(body), status=200, mimetype=MASON)


    def post(self):
        """
        POST method adds a new imageannotation to collection
        """        
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.imageannotation_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        
        if "image_id" in request.json:
            if request.json["image_id"] == "" or request.json["image_id"] == None:
                return create_error_response(400, "Invalid JSON document", "No image id provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No image id provided")   
       
        if "user_id" in request.json:
            if request.json["user_id"] == "" or request.json["user_id"] == None:
                return create_error_response(400, "Invalid JSON document", "No user id provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No user id provided")

        new_imageannotation = ImageAnnotation(
            image_id = request.json["image_id"],
            user_id = request.json["user_id"],
            meme_class = request.json["meme_class"],
            HS_class = request.json["HS_class"],
            text_class = request.json["text_class"],
            polarity_classA = request.json["polarity_classA"],
            polarity_classB = request.json["polarity_classB"],
            HS_strength = request.json["HS_strength"],
            HS_category = request.json["HS_category"],
            text_text = request.json["text_text"],
            text_language = request.json["text_language"]
        )

        try:
            db.session.add(new_imageannotation)
            db.session.commit()

             # query the newly added annotation             
            db_annotation = ImageAnnotation.query.filter_by(image_id=new_imageannotation.image_id).first()
            return Response(status=201, headers={"Location": url_for("api.imageannotationitem", id=db_annotation.id)})
            
        except IntegrityError:
            return create_error_response(409, "Already exists", "Imageannotation with id '{}' already exists".format(request.json["id"]))


class ImageannotationItem(Resource):
    """
    Resource for ImageannotationItem. 
    Function GET gets one single imageannotation, PUT edits the imageannotation,
    and DELETE deletes the imageannotation.
    """

    def get(self, id):
        """
        GET method gets one single imageannotation
        """
        db_imageanno_id = ImageAnnotation.query.filter_by(id=id).first()
        if db_imageanno_id is None:
            return create_error_response(404, "Not found", "No imageannotation was found with id {}".format(id))

        # query annotator for annotator control
        annotator = User.query.filter_by(id=db_imageanno_id.user_id).first()

        body = HubBuilder(
            id = db_imageanno_id.id,
            image_id = db_imageanno_id.image_id,
            user_id = db_imageanno_id.user_id,
            meme_class = db_imageanno_id.meme_class,
            HS_class = db_imageanno_id.HS_class,
            text_class = db_imageanno_id.text_class,
            polarity_classA = db_imageanno_id.polarity_classA,
            polarity_classB = db_imageanno_id.polarity_classB,
            HS_strength = db_imageanno_id.HS_strength,
            HS_category = db_imageanno_id.HS_category,
            text_text = db_imageanno_id.text_text,
            text_language = db_imageanno_id.text_language
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.imageannotationitem", id=id))
        body.add_control("profile", IMAGEANNOTATION_PROFILE)
        body.add_control("collection", url_for("api.imageannotationcollection"))
        body.add_control("imageitem", url_for("api.imageitem", id=db_imageanno_id.image_id))
        body.add_control("annotator", url_for("api.useritem", user_name=annotator.user_name))
        body.add_control_delete_imageannotation(id)
        body.add_control_edit_imageannotation(id)

        return Response(json.dumps(body), status=200, mimetype=MASON)


    def put(self, id):
        """
        PUT method edits one single imageannotation
        """
        db_imageanno_id = ImageAnnotation.query.filter_by(id=id).first()

        if db_imageanno_id is None:
            return create_error_response(404, "Not found", "No imageannotation was found with id {}".format(id))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        if "image_id" in request.json:
            if request.json["image_id"] == "" or request.json["image_id"] == None:
                return create_error_response(400, "Invalid JSON document", "No image id provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No image id provided")   

        if "user_id" in request.json:
            if request.json["user_id"] == "" or request.json["user_id"] == None:
                return create_error_response(400, "Invalid JSON document", "No user id provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No user id provided")   

        try:
            validate(request.json, HubBuilder.imageannotation_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_imageanno_id.user_id=request.json["user_id"]
        db_imageanno_id.meme_class = request.json["meme_class"]
        db_imageanno_id.HS_class = request.json["HS_class"]
        db_imageanno_id.text_class = request.json["text_class"]
        db_imageanno_id.polarity_classA = request.json["polarity_classA"]
        db_imageanno_id.polarity_classB = request.json["polarity_classB"]
        db_imageanno_id.HS_strength = request.json["HS_strength"]
        db_imageanno_id.HS_category = request.json["HS_category"]
        db_imageanno_id.text_text = request.json["text_text"]
        db_imageanno_id.text_language = request.json["text_language"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Imageannotation with id '{}' already exists".format(request.json["id"]))
        return Response(status=204, headers={"Location": url_for("api.imageannotationitem", id=db_imageanno_id.id)})


    def delete(self, id):
        """
        DELETE method deletes one single imageannotation
        """
        db_imageanno_id = ImageAnnotation.query.filter_by(id=id).first()
        if db_imageanno_id is None:
            return create_error_response(404, "Not found", "No imageannotation was found with id {}".format(id))

        db.session.delete(db_imageanno_id)
        db.session.commit()
        return Response(status=204)        