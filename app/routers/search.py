from flask import Blueprint, render_template, request
import date_utils

search_bp = Blueprint("search", __name__)

@search_bp.route("/", methods=['GET'])
def search():
    from database import Tag, Day
    tags = Tag.findAll()

    query = request.args.get('q')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    tags_req = request.args.get('tags')

    print("query:", query)
    print("start_date:", start_date)
    print("end_date:", end_date)
    print("tags 1:", tags_req)

    if not query and not start_date and not end_date and not tags_req:
        return render_template("search.html", tags=tags)

    if not start_date or start_date == "None":
        start_date = date_utils.get_date_one_month_ago()
        timestamp_start = start_date.timestamp()
    else:
        year_start, month_start, day_start = map(int, start_date.split("-"))
        timestamp_start = date_utils.date_to_timestamp(year_start, month_start, day_start)


    if not end_date or end_date == "None":
        end_date = date_utils.get_today()
        timestamp_end = end_date.timestamp()
    else:
        year_end, month_end, day_end = map(int, end_date.split("-"))
        timestamp_end = date_utils.date_to_timestamp(year_end, month_end, day_end)

    print("timestamp_start:", timestamp_start)
    print("timestamp_end:", timestamp_end)

    tags_req = tags_req.split(",") if tags_req else []
    print("tags_req 2:", tags_req)

    results = []
    if timestamp_start and timestamp_end:
        results = Day.query.filter(Day.id.between(timestamp_start, timestamp_end)).all()
    else:
        results = Day.findAll()

    print("results 1:", results)

    results_tags = []
    if tags_req:
        for day in results:
            for day_tag in day.tags:
                if day_tag.name in tags_req:
                    results_tags.append(day)

        results = results_tags

    print("results 2:", results)

    results_text = []
    if query:
        for day in results:
            print(day.description)
            print(day.content)
            if (query.lower() in day.description.lower()) or (query.lower() in day.content.lower()):
                results_text.append(day)

        results = results_text

    print("results 3:", results)

    return render_template("search.html", tags=tags, results=results, query=query)