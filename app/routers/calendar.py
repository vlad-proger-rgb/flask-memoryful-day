from flask import Blueprint, render_template, request, redirect, url_for

import sys
sys.path.append("../")

import date_utils

calendar_bp = Blueprint("calendar", __name__)


@calendar_bp.route("/<int:year>")
def calendar(year: int):

	return render_template(
		"calendar.html",
		year=year
    )


@calendar_bp.route("/<int:year>/<int:month>")
def month(year: int, month: int):
	from database import Day

	days_in_month = date_utils.get_days_in_month(year, month)

	days = []
	for i in range(days_in_month):
		timestamp = date_utils.date_to_timestamp(year, month, i + 1)
		day = Day.findById(timestamp)
		if day is not None:
			days.append(day)
		else:
			days.append(Day(timestamp))

	print("Found days: ", days)

	return render_template(
		"month.html",
		year=year,
		month=month,
		days=days
    )


@calendar_bp.route("/<int:year>/<int:month>/<int:dayNumber>", methods=["GET", "POST"])
def day(year: int, month: int, dayNumber: int):
	from database import Day, Image, City, Tag

	timestamp = date_utils.date_to_timestamp(year, month, dayNumber)
	day = Day.findById(timestamp)

	if request.method == "POST":
		if day:
			day.city_id = request.form["city_id"]
			day.description = request.form["description"]
			day.content = request.form["content"]
			day.steps = request.form["steps"]
		else:
			day = Day(
				timestamp = timestamp,
				city_id = request.form["city_id"],
				desc = request.form["description"],
				content = request.form["content"],
				steps = request.form["steps"]
			)

		if request.files["mainImage"]:
			file = request.files["mainImage"]
			file.save(f"app/static/images/calendar/vlad/{file.filename}")
			image = Image(source=file.filename, main_image=1)
			image.save()
			day.setMainImage(image)

		if request.files.getlist("otherImages[]")[0]:
			for img in request.files.getlist("otherImages[]"):
				img.save(f"app/static/images/calendar/vlad/{img.filename}")
				image = Image(source=img.filename)
				image.save()
				day.images.append(image)

		if request.form.getlist("tags"):
			day.tags.clear()
			for tag_name in request.form.getlist("tags"):
				tag = Tag.query.filter(Tag.name == tag_name).first()
				if not tag:
					tag = Tag(name=tag_name)
					tag.save()
				day.tags.append(tag)

		day.save()

		return redirect(
			url_for(
				".day",
				year=year,
				month=month,
				dayNumber=dayNumber
			)
		)

	cities = City.findAll()
	tags = Tag.findAll()

	if day is None:
		day = Day(timestamp)

	return render_template(
		"day.html",
		year=year,
		month=month,
		dayNumber=dayNumber,
		day=day,
		cities=cities,
		tags=tags,
		user="vlad"
    )