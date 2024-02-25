import os
import requests


def scrape_linkedin_profile(linkedin_profile_url, test_mode=True):
    """scrape information from Linkedin profiles
    Manually scrape the information from the Linkedin profile
    """
    if test_mode:
        gist_url = (
            "https://gist.githubusercontent.com/frank-xw/"
            "6f059210a1c6d9ee9649b6869e1b610a/"
            "raw/07d44364d3fd68466f1ec848a6881cb0b17a07de/andrew-ng.json"
        )
        response = requests.get(gist_url)

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        api_key = os.environ.get("PROXYCURL_API_KEY")
        headers = {"Authorization": "Bearer " + api_key}

        response = requests.get(
            api_endpoint,
            params={"linkedin_profile_url": linkedin_profile_url},
            headers=headers,
        )

    data = response.json()

    data = {
        key: value
        for key, value in data.items()
        if (
            value not in ([], "", None)
            and key not in ("people_also_viewed", "certifications")
        )
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile("test").json())
