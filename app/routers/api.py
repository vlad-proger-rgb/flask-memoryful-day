import random
from flask import Blueprint, request, jsonify
from chatgpt import get_completion
from database import Day
import date_utils

api_bp = Blueprint("api", __name__)

@api_bp.get("/ask_gpt")
def ask_gpt():
    query = request.args.get("query")
    if not query:
        return "The content area is empty"

    try:
        out_query = """
        Create a short description for this text in the language that the text to short is.
        Do it with the length depending to the length of the query,
        so if short query then short and vice-versa. Here is the query:
        """ + query
        answer = get_completion(out_query)
        return answer 
    except Exception as e:
        return f"Some error asking GPT 3.5: {e}"

@api_bp.get("/get_random_day")
def get_random_day():

    random_day = random.choice(Day.findAll())
    # print("random_day dict:", random_day.to_dict())

    return jsonify(random_day.to_dict())


@api_bp.get("/search_for_days")
def search_for_days():

    query = request.args.get('q')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    tags = request.args.get('tags')

    tags = tags.split(",") if tags else []

    year_start, month_start, day_start = map(int, start_date.split("-"))
    year_end, month_end, day_end = map(int, end_date.split("-"))

    timestamp_start = date_utils.date_to_timestamp(year_start, month_start, day_start)
    timestamp_end = date_utils.date_to_timestamp(year_end, month_end, day_end)

    results = []
    if timestamp_start and timestamp_end:
        results = Day.query.filter(Day.id.between(timestamp_start, timestamp_end)).all()
    else:
        results = Day.findAll()


    results_tags = []
    if tags:
        for day in results:
            for day_tag in day.tags:
                if day_tag.name in tags:
                    results_tags.append(day)


    results_text = []
    if query:
        for day in results:
            print(day.description)
            print(day.content)
            if (query in day.description) or (query in day.content):
                results_text.append(day)

        results = results_text

    results = [{"date": result.getDate(), "description": result.description} for result in results]

    return jsonify(results)