from flask import Blueprint, render_template, redirect, url_for, request
from datetime import datetime
import date_utils

gallery_bp = Blueprint("gallery", __name__)

@gallery_bp.route("/")
@gallery_bp.route("/<view_mode>")
def gallery(view_mode="square"):
    from database import Album
    albums = Album.findAll()
    year_today = datetime.now().year
    return render_template(
        "gallery.html",
        year_today=year_today,
        user="vlad",
        albums=albums,
        view_mode=view_mode
    )


@gallery_bp.route("/new_album", methods=['POST'])
def new_albom():
    from database import Album, Image

    album = Album(
        name=request.form["name"]
    )
    album.save()

    if request.files.getlist("images[]"):
        print("request.files:", request.files.getlist("images[]"))
        for img in request.files.getlist("images[]"):
            img.save(f"app/static/images/calendar/vlad/{img.filename}")
            image = Image(source=img.filename)
            image.save()
            album.images.append(image)
            print("image saved:", image)

        album.save()

    if request.form.getlist("existing_images"):
        print("existing_images:", request.form.getlist("existing_images"))
        images_ids = request.form.getlist("existing_images")[0].split(",")
        print("images_ids:", images_ids)
        if images_ids[0]:
            for image_id in images_ids:
                print("image_id:", image_id)
                image = Image.findById(image_id)
                print("image:", image)
                album.images.append(image)

        album.save()

    if request.form.getlist("images_by_urls"):
        print("images_by_urls:", request.form.getlist("images_by_urls"))
        for image_url in request.form.getlist("images_by_urls")[0].split(","):
            image = Image(source=image_url)
            image.save()
            album.images.append(image)

        album.save()

    return {"success": True, "message": "Album created successfully"}

@gallery_bp.route("/album/<string:album_name>", methods=['GET', 'POST', 'DELETE'])
def album(album_name: str):
    from database import Album, Image

    album = Album.findBy(name=album_name)

    if not album:
        return redirect(url_for("gallery.gallery"))

    if request.method == 'POST':
        if not request.files.getlist("images"):
            return {"success": False, "message": "No images selected"}

        for img in request.files.getlist("images"):
            img.save(f"app/static/images/calendar/vlad/{img.filename}")
            image = Image(source=img.filename)
            image.save()
            album.images.append(image)

        print("existring image ids:", request.form.getlist("existing_images"))

        if request.form.getlist("existing_images"):
            for image_id in request.form.getlist("existing_images")[0].split(","):
                image = Image.findById(image_id)
                album.images.append(image)

        if request.form.getlist("images_by_urls"):
            for image_url in request.form.getlist("images_by_urls")[0].split(","):
                image = Image(source=image_url)
                image.save()
                album.images.append(image)

        album.save()
        return {"success": True, "message": "Images saved successfully"}

    if request.method == 'DELETE':
        if album:
            for image in album.images:
                if image.days:
                    print("This image has days:", image.days)
                    continue

                if image in album.images:
                    print(f"Removing image from album:", image)
                    album.images.remove(image)

                print("Deleting image:", image.source)
                image.delete()

            album.delete()
            return {"success": True, "message": "Album deleted successfully"}

    return render_template("album.html", album_name=album_name, album=album, user="vlad")

@gallery_bp.route("/album/<album_name>/delete_selected", methods=['POST'])
def deleteSelectedImages(album_name: str):
    from database import Album

    album = Album.findByName(album_name)
    if not album:
        return {"success": False, "message": "Album not found"}

    if not request.form.getlist("images_to_delete"):
        return {"success": False, "message": "No images selected"}

    allowToDeleteFiles = True if request.form.get("allowToDeleteFiles") == "true" else False
    print("deleteSelectedImages => allowToDeleteFiles:", allowToDeleteFiles)
    print("deleteSelectedImages => type of allowToDeleteFiles:", type(allowToDeleteFiles))

    result = album.deleteImagesByNames(
        request.form.getlist("images_to_delete")[0].split(","),
        allowToDeleteFiles
    )
    print("deleteSelectedImages => result:", result)

    if result["success"]:
        return {"success": True, "message": "Selected images deleted successfully"}
    else:
        return {"success": False, "message": result["message"]}


@gallery_bp.route("/images_by_date_range", methods=['POST'])
def imagesByDateRange():
    from database import Day, Image
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    print(f"start_date: {start_date} end_date: {end_date}")

    start_date = start_date.split("-")
    end_date = end_date.split("-")
    start_date = date_utils.date_to_timestamp(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = date_utils.date_to_timestamp(int(end_date[0]), int(end_date[1]), int(end_date[2]))

    days = Day.findAllByDateRange(start_date, end_date)
    print("days:", days)

    images = []
    for day in days:
        images.extend(day.images)

    print("images:", images)

    for image in images:
        print(image.to_dict())

    images = [image.to_dict() for image in images]

    return render_template("blocks/images_by_date_range.html", user="vlad", images=images)

@gallery_bp.route("/album/<album_name>/add_images_by_urls", methods=['POST'])
def addImagesByURLs(album_name: str):
    from database import Album, Image
    album = Album.findByName(album_name)
    if not album:
        return {"success": False, "message": "Album not found"}

    print("addImagesByURLs request:", request.form.getlist("images_by_urls"))

    if not request.form.getlist("images_by_urls"):
        return {"success": False, "message": "No image URLs provided"}

    for image_url in request.form.getlist("images_by_urls"):
        image = Image(source=image_url)
        image.save()
        album.images.append(image)

    album.save()

    return {"success": True, "message": "Images added successfully"}


@gallery_bp.route("/album/<album_name>/add_images_from_calendar", methods=['POST'])
def addImagesFromCalendar(album_name: str):
    from database import Album, Image
    album = Album.findByName(album_name)
    print("addImagesFromCalendar album_name:", album_name)

    if not album:
        return {"success": False, "message": "Album not found"}

    if not request.form.getlist("images_to_add"):
        return {"success": False, "message": "No images selected"}

    print("addImagesFromCalendar request:", request.form.getlist("images_to_add"))

    for image_id in request.form.getlist("images_to_add")[0].split(","):
        image = Image.findById(image_id)
        album.images.append(image)
        album.save()

    return {"success": True, "message": "Images added successfully"}



