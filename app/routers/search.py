from flask import Blueprint, render_template, request
import date_utils

search_bp = Blueprint("search", __name__)

@search_bp.route("/", methods=['GET'])
def search():
    from database import Tag
    tags = Tag.findAll()
    return render_template("search.html", tags=tags)


@search_bp.route('/search', methods=['GET'])
def search_perform():
    from database import Day, Tag, City
    query = request.args.get('q')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    tags = request.args.get('tags')

    print("query:", query)
    print("start_date:", start_date)
    print("end_date:", end_date)
    print("tags 1:", tags)

    tags = tags.split(",") if tags else []
    print("tags 2:", tags)

    year_start, month_start, day_start = map(int, start_date.split("-"))
    year_end, month_end, day_end = map(int, end_date.split("-"))

    print("year_start, month_start, day_start:", year_start, month_start, day_start)
    print("year_end, month_end, day_end:", year_end, month_end, day_end)

    timestamp_start = date_utils.date_to_timestamp(year_start, month_start, day_start)
    timestamp_end = date_utils.date_to_timestamp(year_end, month_end, day_end)
    print("timestamp_start, timestamp_end:", timestamp_start, timestamp_end)

    results = []
    if timestamp_start and timestamp_end:
        results = Day.query.filter(Day.id.between(timestamp_start, timestamp_end)).all()
    else:
        results = Day.findAll()

    print("results 1:", results)

    results_tags = []
    if tags:
        for day in results:
            for day_tag in day.tags:
                if day_tag.name in tags:
                    results_tags.append(day)

        results = results_tags

    print("results 2:", results)

    results_text = []
    if query:
        for day in results:
            print(day.description)
            print(day.content)
            if (query in day.description) or (query in day.content):
                results_text.append(day)

        results = results_text

    print("results 3:", results)

    return render_template("search.html", tags=tags, results=results, query=query)