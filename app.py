from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        title = request.args.get('title', 'python developer')  # Default to 'python developer' if not provided
        location = request.args.get('location', 'pakistan')   # Default to 'pakistan' if not provided
        list_url = f"https://www.linkedin.com/jobs/search?keywords={title.replace(' ', '+')}&location={location.replace(' ', '+')}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&original_referer=https%3A%2F%2Fwww.linkedin.com%2Fjobs%2Fsearch%3Fkeywords%3D{title.replace(' ', '%20')}%26location%3D{location.replace(' ', '%20')}%26geoId%3D101022442%26trk%3Dpublic_jobs_jobs-search-bar_search-submit%26position%3D1%26pageNum%3D0"

        response = requests.get(list_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        list_data = response.text
        list_soup = BeautifulSoup(list_data, "html.parser")
        page_jobs = list_soup.find_all("li")

        job_ids = []
        for job in page_jobs:
            base_card_div = job.find("div", {"class": "base-card"})
            if base_card_div:
                job_urn = base_card_div.get("data-entity-urn")
                if job_urn:
                    job_id = job_urn.split(":")[3]
                    job_ids.append(job_id)

        job_list = []
        for job_id in job_ids:
            try:
                job_url = f"https://www.linkedin.com/jobs/view/{job_id}"
                job_response = requests.get(job_url)
                job_response.raise_for_status()  # Raise an HTTPError for bad responses
                job_soup = BeautifulSoup(job_response.text, "html.parser")
                job_post = {}

                job_title_tag = job_soup.find("h1", {"class": "topcard__title"})
                job_post["job_title"] = job_title_tag.text.strip() if job_title_tag else "N/A"

                company_name_tag = job_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"})
                job_post["company_name"] = company_name_tag.text.strip() if company_name_tag else "N/A"

                posted_time_tag = job_soup.find("span", {"class": "posted-time-ago__text posted-time-ago__text--new topcard__flavor--metadata"})
                job_post["posted_time"] = posted_time_tag.text.strip() if posted_time_tag else "N/A"

                job_post["job_url"] = job_url

                applicants_tag = job_soup.find("span", {"class": "num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet"})
                job_post["number_of_applicants"] = applicants_tag.text.strip() if applicants_tag else "N/A"

                job_list.append(job_post)
            except requests.RequestException as e:
                print(f"Error fetching job details for job ID {job_id}: {e}")

        return jsonify(job_list)
    except requests.RequestException as e:
        return jsonify({"error": f"Error fetching job list: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
